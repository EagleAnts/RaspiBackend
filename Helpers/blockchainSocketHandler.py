import asyncio
from datetime import datetime
import json
import threading
from time import sleep
import socketio
from Helpers.networkNode import startConsensus
import concurrent.futures
# from Helpers.raspiSocketHandler import getBlockchainDetails
from SQLiteDB.sqlite import SQLiteDB, db
from .socketIoClient import sio
from .blockchain import blockchainObj
from socketio.exceptions import TimeoutError
import sys
from .blockchain import blockchainObj
from .networkNode import mine, transaction

# @sio.event("*", namespace="/blockchain")
# async def catch_all(event, args):
#     print(event, args)


queue = []


class DateTimeEncoder(json.JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


loop = asyncio.get_event_loop()
event = threading.Event()


def createTransaction():
    global queue
    print("Queue Status : ", queue)
    for _ in range(0, len(queue)):
        data = queue.pop(0)

        print("Creating Transaction : ", data)

        item = {
            "transactionMadeBy": data["from"],
            "content": data["content"],
            "timestamp": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        }

        transaction(item)

    # print("Blockchain  : ", blockchainObj.getBlockchain("").chain)
    print("\n\n")
    return "Mining Done....\n\n"


def mineAllBlocks():
    while True:
        # print(queue)
        print("\n\nMining All Blocks.... : ", len(queue))
        if len(queue) != 0:
            createTransaction()
            # with concurrent.futures.ThreadPoolExecutor() as pool:
            # result = pool.submit(createTransaction)
            # print(result.result())
        sleep(5)


MineblocksThread = threading.Thread(target=mineAllBlocks)
MineblocksThread.setDaemon(True)


class BlockchainNamespace(socketio.AsyncClientNamespace):

    async def on_connect(self):
        print("Connected to Blockchain Namespace")
        await joinNetworkRoom()
        await getBlockchainDetails()
        await startConsensus()
        MineblocksThread.start()

        # with concurrent.futures.ThreadPoolExecutor() as pool:
        #     pool.submit(mineAllBlocks)
        # print("Mining Started...")

    async def on_getLength(self, data):
        print(data["event"])
        chainLength: dict[str, int] = {}
        for piID in blockchainObj.blockchains.keys():
            # print(piID, " : ", len(blockchainObj.blockchains[piID].chain)) {dasdasdsa:5}
            chainLength[piID] = len(blockchainObj.blockchains[piID].chain)
        await self.call("blockchain:private_recieve", {"event": data["event"], "blockchainLengths": chainLength, "from": blockchainObj.getMyPiID(), "to": data["from"]})

    async def on_getLength_recieve(self, data):
        print(data)
        for pi in data["blockchainLengths"].keys():
            obj = blockchainObj.myLengthObj[pi]
            if(obj["length"] < data["blockchainLengths"][pi]):
                obj["length"] = data["blockchainLengths"][pi]
                obj["belongsToPi"] = pi

        if data["from"] in blockchainObj.networkNodes:
            blockchainObj.networkNodes.remove(data["from"])

        pass

    async def on_disconnect(self):
        print("Disconnected from Blockchain Namespace")

    async def on_connect_error(self):
        print("Connection Error")

    async def on_roomJoined(self, data):
        print("Joined room with id : ", data)

    async def on_getBlockchain(self, data):
        chain = blockchainObj.getBlockchain(data["aboutPiID"]).chain
        # chain = json.dumps(chain)
        await self.call("blockchain:private_recieve", {"event": data["event"], "aboutPiID": data["aboutPiID"], "blockchain": chain, "from": blockchainObj.getMyPiID(), "to": data["from"]})

    async def on_getBlockchain_recieve(self, data):
        blockchainObj.setBlockchain(data["aboutPiID"], data["blockchain"])
        for node in blockchainObj.networkNodes:
            if data["from"] == node["to"]:
                blockchainObj.networkNodes.remove(node)
        print("\n\n", data["aboutPiID"], "\n\n",
              blockchainObj.blockchains[data["aboutPiID"]].chain)

    async def on_addNewNode(self, data):
        print(data)
        blockchainObj.addEmptyBlockchain(data["newNode"])

    async def on_addNewBlock(self, data):
        print("Adding New Block...")
        userBlockchain = blockchainObj.getBlockchain(data["from"])
        newBlock = data["newBlock"]
        lastBlock = userBlockchain.getLastBlock()
        correctHash = lastBlock["hash"] == newBlock["previousBlockHash"]
        correctIndex = len(userBlockchain.chain) + 1 == newBlock["index"]
        correctCurrentHash = userBlockchain.hashBlock(lastBlock["hash"], {
            "transactions": newBlock["transactions"], "index": len(userBlockchain.chain) + 1}, newBlock["nonce"]) == newBlock["hash"]
        # print(correctHash, " ", correctIndex, " ",
        #   correctCurrentHash, " ", newBlock)
        if correctHash and correctIndex and correctCurrentHash and newBlock["hash"][0:4] == "0000":
            userBlockchain.chain.append(newBlock)
            userBlockchain.pendingTransactions = []
            print(userBlockchain.chain)
        else:
            await startConsensus()


sio.register_namespace(BlockchainNamespace("/blockchain"))


async def joinNetworkRoom():
    rpiDetails = await db.getRpiDetails()
    if(rpiDetails):
        print("Joining Network Room")
        await sio.emit("join_room", rpiDetails["networkID"], namespace="/blockchain")

        # await sio.emit("send", "Welcome to Raspi", namespace="/raspberrypi")


async def getBlockchainDetails():
    try:
        # SQLiteDB.getAllRows(await db.getBlockchainDetails())
        rpiDetails = await db.getRpiDetails()
        if(rpiDetails):
            blockchainObj.setMyPiID(rpiDetails["piID"])
            blockchainObj.setMyNetworkID(rpiDetails["networkID"])
            piID = blockchainObj.getMyPiID()
            print("Retriving Network Nodes")
            nodes = await sio.call("blockchain:getNodes", {"piID": rpiDetails["piID"], "networkID": rpiDetails["networkID"]}, namespace="/blockchain")
            print("Nodes Present in Current Network : ", nodes)
            for piID in nodes:
                if(blockchainObj.getMyPiID() != piID):
                    blockchainObj.addEmptyBlockchain(piID)

            # print(blockchainObj.blockchains)

            for piID in blockchainObj.blockchains.keys():
                print("\n", piID, ": ",
                      blockchainObj.blockchains[piID].chain, "\n")

            # if(sys.argv[-1] == "8000" or sys.argv[-1] == "8001"):
            #     blockchainObj.getBlockchain("").createNewBlock()

            blockchainObj.initializeMyLengthObj()
            return nodes

    except TimeoutError:
        print("Timeout..")
        # cbRes = await sio.call("blockchain:broadcast", {"toRoom": blockchainObj.getMyNetworkID()}, namespace="/blockchain")
        # blockchainObj.setBlockchain(data["piID"], data["chain"])
        # print(cbRes)
