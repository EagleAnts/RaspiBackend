from uuid import uuid4
import hashlib
from datetime import datetime
from typing import TypedDict
import json


class Blockchain:
    def __init__(self):
        self.chain = []
        self.pendingTransactions = []
        self.createNewBlock(
            "000087985248cb89c29e93af0bd55ebb7b659bcea8f96ace46060b27fdc95330")

    def setChain(self, chain):
        self.chain = chain
        self.pendingTransactions = []

    def createNewBlock(self, previousBlockHash=-1):
        if(previousBlockHash == -1):
            previousBlockHash = self.getLastBlock()["hash"]
        currentBlockData = {
            "transactions": self.pendingTransactions,
            "index": len(self.chain) + 1,
        }
        nonce = self.proofOfWork(previousBlockHash, currentBlockData)
        hash = self.hashBlock(previousBlockHash, currentBlockData, nonce)
        newBlock = {
            "index": len(self.chain) + 1,
            "timestamp": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            "transactions": self.pendingTransactions,
            "nonce": nonce,
            "hash": hash,
            "previousBlockHash": previousBlockHash,
        }
        self.pendingTransactions = []
        self.chain.append(newBlock)
        return newBlock

    def getLastBlock(self):
        return self.chain[-1]

    def createNewTransaction(self, transaction):
        transaction = {**transaction,
                       "transactionId": uuid4()}
        return transaction

    def addTransactionToPendingTransaction(self, transactionObject):
        self.pendingTransactions.append(transactionObject)
        return len(self.chain) + 1

    def hashBlock(self, previousBlockHash, currentBlockData, nonce):
        dataAsString = previousBlockHash + \
            json.dumps(currentBlockData) + str(nonce)
        dataAsString = dataAsString.encode("utf-8")
        hash = hashlib.sha256(dataAsString).hexdigest()
        return hash

    def proofOfWork(self, previousBlockHash, currentBlockData):
        nonce = 0
        hash = self.hashBlock(previousBlockHash, currentBlockData, nonce)
        while hash[0:4] != "0000":
            nonce += 1
            hash = self.hashBlock(previousBlockHash, currentBlockData, nonce)
        return nonce

    def chainIsValid(self, blockchain):
        validChain = True

        for i in range(1, len(blockchain)):
            currentBlock = blockchain[i]
            prevBlock = blockchain[i - 1]
            blockHash = self.hashBlock(
                prevBlock["hash"],
                {
                    "transactions": currentBlock["transactions"],
                    "index": currentBlock["index"],
                },
                currentBlock["nonce"])
            if (currentBlock["previousBlockHash"] != prevBlock["hash"] or blockHash[0:4] != "0000" or blockHash != currentBlock["hash"]):
                # print(blockHash)
                # print(str(currentBlock["previousBlockHash"] != prevBlock["hash"]) +" "+ str(blockHash[0:4] != "0000") +" "+ str(blockHash != currentBlock["hash"]))
                validChain = False

        genesisBlock = blockchain[0]
        correctNonce = genesisBlock["nonce"] == 113552
        correctPreviousBlockHash = genesisBlock["previousBlockHash"] == "000087985248cb89c29e93af0bd55ebb7b659bcea8f96ace46060b27fdc95330"
        correctHash = genesisBlock["hash"] == "0000b931a05af802b85a18cefb05e7865bf73b12688c351bd3564ff83bdba38e"
        correctTransactions = len(genesisBlock["transactions"]) == 0

        if (not(correctNonce and correctPreviousBlockHash and correctHash and correctTransactions)):
            validChain = False
        return validChain


class Blockchains:
    def __init__(self):
        self.blockchains: dict[str, Blockchain] = {}
        self.myPiID: str = 0
        self.myNetworkID: str = 0
        self.networkNodes = []
        self.myLengthObj = {}

    def setBlockchain(self, piID, chain):
        if(self.blockchains.get(piID, -1) == -1):
            self.addEmptyBlockchain(piID)
        self.blockchains[piID].setChain(chain)

    def addEmptyBlockchain(self, piID):
        self.blockchains[piID] = Blockchain()

    def getBlockchain(self, piID):
        if(piID == ""):
            return self.blockchains.get(self.myPiID, -1)
        return self.blockchains.get(piID, -1)

    def setMyPiID(self, piID):
        if(self.blockchains.get(self.myPiID, -1) != -1):
            self.setBlockchain(piID, self.blockchains[self.myPiID].chain)
        else:
            self.addEmptyBlockchain(piID)
        self.myPiID = piID

    def initializeMyLengthObj(self):
        for i in self.blockchains.keys():
            self.myLengthObj[i] = {"length": len(
                self.blockchains[i].chain), "belongsToPi": self.getMyPiID()}

    def setMyNetworkID(self, piID):
        self.myNetworkID = piID

    def getMyPiID(self):
        return self.myPiID

    def getMyNetworkID(self):
        return self.myNetworkID


blockchainObj = Blockchains()
