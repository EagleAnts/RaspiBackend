import json
import socketio
import asyncio
from Helpers.blockchainSocketHandler import event as MiningEvent
from .socketIoClient import sio as sioClient
from .blockchain import blockchainObj
from .raspiSocketHandler import connectRaspberrypi, registerRaspberryPi
from SQLiteDB.sqlite import SQLiteDB, db
from socketio.exceptions import ConnectionRefusedError


def on_shutdown():
    print("On Shutdown()")


def on_startup():
    print("Starting Up.....")


sio = socketio.AsyncServer(
    async_mode='asgi', cors_allowed_origins='*')
app = socketio.ASGIApp(sio, static_files={
    '/': './public/index.html',
}, on_shutdown=on_shutdown, on_startup=on_startup)

loop = asyncio.get_running_loop()


async def checkRegisteration():
    details = await db.getRpiDetails()
    if(details):
        print("Already Registered..")
        print("Raspberry Pi is Registered with Details : ")
        SQLiteDB.getAllRows(details)
        await connectRaspberrypi(
            ENDPOINT=details["serverAddress"], Authentication={"email": details["user_email"]}, Headers={
                "username": f'{details["piName"]}:{details["user_email"]}',
                "networkID": details["networkID"],
                "id": details["piID"],
                "device_type": "raspberrypi"
            })
        return "OK"

    else:
        return "Raspberry Pi Not Registered Yet"


loop.create_task(checkRegisteration()).add_done_callback(
    lambda t: print(t.result()))


@sio.event
async def connect(sid, enviro, auth):
    if not (auth['x-user-email'] and not auth['x-user-email'].isspace()):
        raise ConnectionRefusedError(
            {"msg": "User email is required", "status": "502"})

    # check Rpi Details
    details = await db.getRpiDetails()
    if(details):
        raise ConnectionRefusedError(json.dumps(
            {"status": 502, "msg": "This Raspberry Pi is Already Registered"}))

    print("Printing All Sockets")
    # for k, v in sio.manager.:
    #     print(k, v.sid)
    # await sio.disconnect(socket)

    print('user connected : ', sid, auth["x-user-email"])


@sio.event
async def disconnect(sid):
    print('user disconnected : ', sid)


@sio.event
async def register(sid, data):
    print("Registering Device....")
    # print(data)
    res = await registerRaspberryPi(data)

    if(res["status"] == 200 and (await checkRegisteration()) == "OK"):
        await sioClient.call("blockchain:broadcast", {"event": "addNewNode", "newNode": blockchainObj.getMyPiID(), "from": blockchainObj.getMyPiID(), "message": "New Node added to Your Network : "+str(blockchainObj.getMyPiID())}, namespace="/blockchain")

    return res


# 1. Set Up - form, details store in DB, Backend Register under the user store the response jwt
# 2. Bridge socket based backend
# 3. end-to-end encryption
# 4. Blockchain

# m = hashlib.sha256()
# mac = f"{':'.join(re.findall('..', '%012x' % uuid.getnode()))}"
# print(mac)
# m.update(bytes(mac, 'utf-8'))
# print(m.hexdigest())
