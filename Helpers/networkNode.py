from .blockchain import Blockchain
from .socketIoClient import sio
from .blockchain import blockchainObj
from socketio.exceptions import TimeoutError
import asyncio
from SQLiteDB.sqlite import db


async def checkResponseFromNodes(data):
    count = 1
    while count < 5:
        print("Checking Responses....")
        await asyncio.sleep(2)
        print("Network Nodes Pending.... : ", blockchainObj.networkNodes)
        for pi in blockchainObj.networkNodes:
            print("Retrying...")
            if(not isinstance(pi, str) and pi.get("aboutPiID", -1) != -1):
                data["aboutPiID"] = pi["aboutPiID"]
                data["to"] = pi["to"]
            else:
                data["to"] = pi
            print(await sio.call("blockchain:private_send", data, namespace="/blockchain"))
        count += 1
        if len(blockchainObj.networkNodes) == 0:
            return True
    return False


def mine():
    print("Mining Blocks.....")
    blockchain = blockchainObj.getBlockchain("")
    newBlock = blockchain.createNewBlock()


def transaction(data):
    blockchain = blockchainObj.getBlockchain("")
    index = blockchain.addTransactionToPendingTransaction(data)
    print("note : The transaction will be added on the block "+str(index))
    if len(blockchainObj.getBlockchain("").pendingTransactions) >= 2:
        mine()
    return f"Transaction {data['content']['type']} Completed..."


async def startConsensus():
    print("In Consensus Algorithm")
    blockchainObj.initializeMyLengthObj()
    data = {"event": "getLength", "msg": "Give the Blockchains Length Object",
            "from": blockchainObj.getMyPiID()}
    blockchainObj.networkNodes = (await sio.call("blockchain:getConnectedNodes", {"piID": blockchainObj.getMyPiID(), "networkID": blockchainObj.getMyNetworkID()}, namespace="/blockchain"))
    print(await sio.call("blockchain:broadcast", data, namespace="/blockchain"))
    await checkResponseFromNodes(data)

    blockchainObj.networkNodes = []
    for key, val in blockchainObj.myLengthObj.items():
        print("\n\n\n\n", val, "\n\n\n\n")
        if val["belongsToPi"] != blockchainObj.getMyPiID():
            blockchainObj.networkNodes.append(
                {"to": val["belongsToPi"], "aboutPiID": key})

    print("\n\n\n\n", blockchainObj.networkNodes, "\n\n\n\n")

    for val in blockchainObj.networkNodes:
        data = {"event": "getBlockchain", "msg": "Give the Blockchain", "from": blockchainObj.getMyPiID(
        ), "to": val["to"], "aboutPiID": val["aboutPiID"]}
        print(await sio.call("blockchain:private_send", data, namespace="/blockchain"))

    await checkResponseFromNodes(data)
    print(blockchainObj.myLengthObj)
