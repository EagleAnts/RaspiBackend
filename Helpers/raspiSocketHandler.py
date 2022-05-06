import asyncio
import socketio
import traceback
import time
import threading
import concurrent.futures
from requests import get
from socketio.exceptions import ConnectionError
from Devices.Fan import Fan
from Helpers.blockchainSocketHandler import queue
from SQLiteDB.sqlite import SQLiteDB, db
from datetime import datetime
from .socketIoClient import sio


from Devices.LED import led


class RaspberryPiNamespace(socketio.AsyncClientNamespace):

    async def on_connect(self):
        print("Connected to Raspberrypi Namespace")
        await joinRaspiRoom()
        piID = await db.getPIID()
        deviceStatus = await self.call("raspberrypi:getDevicesStatus", {"piID": piID})
        await syncDevicesStatus(deviceStatus)

    async def on_disconnect(self):
        print("Disconnected from Raspberrypi Namespace")

    async def on_connect_error(self):
        print("Connection Error")

    async def on_roomJoined(self, data):
        print("Joined room with id : ", data)

    async def on_recieve(self, data):
        print(data)

    async def on_toggleDevice(self, data):
        print("Toggle : ", data["content"]["type"])
        queue.append(data)

        if("fan" in data["content"]["type"].lower()):
            Fan.toggle()
            await self.emit("raspberrypi:recieve", {
                "toRoom": data["to"], "event": "recieve:toggleDevice", "content": {"msg": "Device Toggled", "status": True if Fan.value == 1 else False, "deviceID": data["deviceID"]}, "dbUpdateEvent": "toggleDevice", "dbUpdate": True})

        else:
            led.toggle()
            await self.emit("raspberrypi:recieve", {
                "toRoom": data["to"], "event": "recieve:toggleDevice", "content": {"msg": "Device Toggled", "status": True if led.value == 1 else False, "deviceID": data["deviceID"]}, "dbUpdateEvent": "toggleDevice", "dbUpdate": True})


sio.register_namespace(RaspberryPiNamespace("/raspberrypi"))


async def syncDevicesStatus(deviceStatus: list[dict:[str, str | bool | int]]):
    for device in deviceStatus:
        if device["gpio"] == 4:
            led.on() if device["status"] else led.off()


async def joinRaspiRoom():
    rpiDetails = await db.getRpiDetails()
    if(rpiDetails):
        print("Joining Raspi Room")
        await sio.emit("create_room", rpiDetails["piID"], namespace="/raspberrypi")


async def connectRaspberrypi(ENDPOINT, Authentication, Headers):
    print(sio.namespace_handlers)
    try:
        if not sio.connected:
            print("Connecting to Server...")
            await sio.connect(ENDPOINT, auth=Authentication, headers=Headers, namespaces=["/raspberrypi", "/blockchain"])
            await sio.emit("blockchain:setSessionID", namespace="/blockchain")

        # await getBlockchainDetails()

    except ConnectionError:
        traceback.print_exc()
        print("Error Occured While Connecting to Server...")


async def registerRaspberryPi(details):
    try:
        details["netDetails"] = get('https://api.ipify.org').text
        await sio.connect(details["serverAddress"], auth={"email": details["email"]}, namespaces="/raspberrypi")
        res = await sio.call("register", details, namespace="/raspberrypi")
        print(res)
        if res["status"] == 200:
            await db.saveToRpiDetails({**details, **res})
            res = {"status": res["status"], "msg": res["msg"]}
        elif res["status"] == 202:
            # Pi is Already Registered
            pass
        await sio.disconnect()
        await sio.sleep(2)
        return res

    except:
        # traceback.print_exc()
        print("Error While Connecting to Server")
        return {"status": 400, "msg": "Some Error Occured"}
