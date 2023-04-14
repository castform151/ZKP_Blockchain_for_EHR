import time
import hashlib
from .txn import Transaction

class Block:
    def __init__(self, previousHash, transactions, timestamp, nonce):
        self.previousHash = previousHash
        self.transactions = transactions
        self.timestamp = timestamp
        self.nonce = nonce
        self.hash = self.calculateHash()

    def calculateHash(self):
        hashData = self.previousHash + str(self.timestamp) + str(self.transactions) + str(self.nonce)
        return hashlib.sha256(hashData.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.createGenesisBlock()]
        self.pendingTransactions = []

    def createGenesisBlock(self):
        return Block("0", [], time.time(), 0)

    def getLastBlock(self):
        return self.chain[-1]

    def addBlock(self, newBlock):
        newBlock.previousHash = self.getLastBlock().hash
        newBlock.hash = newBlock.calculateHash()
        self.chain.append(newBlock)

    def createBlock(self, transactions):
        previousBlockHash = self.getLastBlock().hash
        timestamp = time.time()
        nonce = self.findNonce(previousBlockHash, transactions)
        block = Block(previousBlockHash, transactions, timestamp, nonce)
        self.addBlock(block)

    def findNonce(self, previousHash, transactions):
        difficulty = 4
        nonce = 0
        while True:
            hashData = previousHash + str(time.time()) + str(transactions) + str(nonce)
            hashResult = hashlib.sha256(hashData.encode()).hexdigest()
            if hashResult[:difficulty] == "0" * difficulty:
                return nonce
            nonce += 1

    def mineBlock(self, minerRewardAddress):
        reward = 10
        minerRewardTransaction = Transaction("0", minerRewardAddress, reward, "")
        transactions = [minerRewardTransaction] + self.pendingTransactions
        self.createBlock(transactions)
        self.pendingTransactions = []

    def viewUser(self, userAddress):
        transactionList = []
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == userAddress or transaction.recipient == userAddress:
                    if transaction.verifySignature():
                        transactionList.append(transaction)
        return transactionList
