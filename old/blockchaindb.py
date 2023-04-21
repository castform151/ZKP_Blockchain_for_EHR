import time
import hashlib
from pymongo import MongoClient


class Transaction:
    def __str__(self):
        return "Transaction: {} -> {} : {}".format(self.sender,
                                                   self.recipient, self.amount)

    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    @classmethod
    def takeInput(cls):
        sender = input("Enter sender: ")
        recipient = input("Enter recipient: ")
        amount = input("Enter amount: ")
        return cls(sender, recipient, amount)


class Block:
    def __init__(self, index, timestamp, transactions, nonce, previousHash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.previousHash = previousHash

    @property
    def Hash(self):
        hashData = '{}{}{}{}'.format(
            self.previousHash, self.index, self.nonce, self.timestamp
        )
        return hashlib.sha256(hashData.encode()).hexdigest()


class Blockchain:
    def __init__(self, db):
        self.difficulty = 4
        self.current_Transactions = []
        self.client = MongoClient('localhost', 27017)  # connect to MongoDB
        # self.db = self.client['blockchain_db']  # create a new database
        self.db = db
        self.blocks = self.db['blocks']  # create a new collection for blocks
        # index the collection by block index
        self.blocks.create_index([('index', 1)], unique=True)

    def createGenesisBlock(self):
        return Block(0, time.time(), self.current_Transactions, 100, 1)

    @property
    def getLastBlock(self):
        return self.blocks.find_one(sort=[('index', -1)])

    def addTransaction(self):
        transaction = Transaction.takeInput()
        self.current_Transactions.append(transaction)
        return len(self.current_Transactions)

    def viewTransactions(self):
        index = self.getLastBlock['index']
        for i in range(0, index):
            print(self.current_Transactions[i])

    def addBlock(self, block, proof):
        previous_block = self.getLastBlock
        if previous_block['Hash'] != block.previousHash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block_data = {
            'index': block.index,
            'timestamp': block.timestamp,
            'transactions': [str(t) for t in block.transactions],
            'nonce': block.nonce,
            'previousHash': block.previousHash,
            'Hash': proof
        }
        self.blocks.insert_one(block_data)
        return True

    def loadFromDB(self):
        for block_data in self.blocks.find():
            transactions = [Transaction(**t)
                            for t in block_data['transactions']]
            block = Block(block_data['index'], block_data['timestamp'],
                          transactions, block_data['nonce'], block_data['previousHash'])
            self.chain.append(block)

    def saveToDB(self):
        self.blocks.drop()
        for block in self.chain:
            block_data = {
                'index': block.index,
                'timestamp': block.timestamp,
                'transactions': [t.__dict__ for t in block.transactions],
                'nonce': block.nonce,
                'previousHash': block.previousHash,
                'hash': block.Hash
            }
            self.blocks.insert_one(block_data)

    def mineBlock(self):
        if not self.current_Transactions:
            return False

        last_block = self.getLastBlock

        new_block = Block(index=last_block['index'] + 1,
                          timestamp=time.time(),
                          transactions=self.current_Transactions,
                          nonce=0,
                          previousHash=last_block['Hash'])

        proof = self.proofOfWork(new_block)
        self.addBlock(new_block, proof)
        self.current_Transactions = []
        return new_block.index

    def proofOfWork(self, block):
        block.nonce = 0
        computed_hash = block.Hash
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.Hash
        return computed_hash

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * self.difficulty) and
                block_hash == block.Hash)


# The loadFromDB method fetches all the blocks from the MongoDB database and rebuilds the #blockchain, while the saveToDB method saves the current state of the blockchain to the database.
# modified the addBlock method to save the block data to the database before appending it to the chain.

client = MongoClient('mongodb://localhost:27017/')
db = client['blockchain']
blockchain = Blockchain(db)

# To load the blockchain from the database, simply call the loadFromDB method:
# blockchain.loadFromDB()

# To save the current state of the blockchain to the database, call the saveToDB method:
# blockchain.saveToDB()
