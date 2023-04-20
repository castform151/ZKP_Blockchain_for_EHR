import time
import hashlib
from txn import Transaction
# from merkletools import MerkleTools


class Block:
    def __init__(self, index, previousHash, transactions, timestamp, nonce):
        self.index = index
        self.previousHash = previousHash
        self.transactions = transactions
        self.timestamp = timestamp  # or int(time.time())
        self.nonce = nonce
        # self.merkel_root = None
        self.hash = self.calculateHash()

    # def build_merkel_tree(self):
    #     """
    #     Merkel Tree used to hash all the transactions, and on mining do not recompute Txs hash everytime
    #     Which making things much faster.
    #     And tree used because we can append new Txs and rebuild root hash much faster, when just building
    #     block before mine it.
    #     """
    #     if self.merkel_root:
    #         return self.merkel_root
    #     mt = MerkleTools(hash_type="SHA256")
    #     for el in self.transactions:
    #         mt.add_leaf(el.hash)
    #     mt.make_tree()
    #     self.merkel_root = mt.get_merkle_root()
    #     return self.merkel_root

    def calculateHash(self):
        # hashData = self.previousHash + str(self.timestamp) + str(self.transactions) + str(self.nonce)
        hashData = '{}{}{}{}'.format(
            self.previousHash, self.index, self.nonce, self.timestamp
        )
        return hashlib.sha256(hashData.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.createGenesisBlock()]
        self.pendingTransactions = []
        self.newTransactions = []

    def createGenesisBlock(self):
        return Block(0, "0", [], time.time(), 0)

    def getLastBlock(self):
        return self.chain[-1]

    def addBlock(self, newBlock):
        newBlock.previousHash = self.getLastBlock().hash
        newBlock.hash = newBlock.calculateHash()
        self.chain.append(newBlock)

    def createBlock(self, transactions):
        previousBlockHash = self.getLastBlock().hash
        nonce = self.findNonce(previousBlockHash, transactions)
        timestamp = time.time()
        block = Block(self.getLastBlock().index+1,
                      previousBlockHash, transactions, timestamp, nonce)
        self.addBlock(block)

    def findNonce(self, previousHash, transactions):
        difficulty = 4
        nonce = 0
        while True:
            hashData = previousHash + \
                str(time.time()) + str(transactions) + str(nonce)
            hashResult = hashlib.sha256(hashData.encode()).hexdigest()
            if hashResult[:difficulty] == "0" * difficulty:
                return nonce
            nonce += 1

    def mineBlock(self, minerRewardAddress):
        reward = 10
        minerRewardTransaction = Transaction(
            "0", minerRewardAddress, reward, "")
        transactions = [minerRewardTransaction] + self.pendingTransactions
        self.createBlock(transactions)
        self.pendingTransactions = []

    # Move this to USer class

    def viewUser(self, userAddress):
        transactionList = []
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == userAddress or transaction.recipient == userAddress:
                    if transaction.verifySignature():
                        transactionList.append(transaction)
        return transactionList


blockchain = Blockchain()
blockchain.createGenesisBlock()
tx1 = Transaction("sender_address", "recipient_address",
                  1000, "transaction_data")
blockchain.pendingTransactions.append(tx1)
user_address = "user_address"
# blockchain.addBlock()
blockchain.createBlock(tx1)
transaction_list = blockchain.viewUser(user_address)
print(transaction_list)
