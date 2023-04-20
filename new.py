import time
import hashlib
from flask import Flask, request
import requests
import json

class Transaction:
    __str__= lambda self: "Transaction: {} -> {} : {}".format(self.sender, self.recipient, self.amount)
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
        # self.transactions = transactions
        # self.merkel_root = None

    @property
    def Hash(self):
        # hashData = self.previousHash + str(self.timestamp) + str(self.transactions) + str(self.nonce)
        hashData = '{}{}{}{}'.format(
            self.previousHash, self.index, self.nonce, self.timestamp
        )
        return hashlib.sha256(hashData.encode()).hexdigest()

    
    
class Blockchain:
    def __init__(self):
        self.difficulty = 4
        self.current_Transactions = []
        self.chain = [self.createGenesisBlock()]

    def createGenesisBlock(self):
        return Block(0, time.time(), self.current_Transactions, 100, 1)

    @property
    def getLastBlock(self):
        return self.chain[-1]
   
    # def newTransaction(self, sender, recipient, amount):
    #     self.current_Transactions.append(Transaction(sender, recipient, amount))
    #     return len(self.current_Transactions)
    
    # def newTransaction(self, transaction):
    #     self.current_Transactions.append(transaction)
    #     return len(self.current_Transactions)
    def addTransaction(self):
        transaction = Transaction.takeInput()
        self.current_Transactions.append(transaction)
        return len(self.current_Transactions)
    
    def addBlock(self, block, proof):
        previous_hash = self.getLastBlock.Hash
        if previous_hash != block.previousHash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        # block.Hash = proof
        self.chain.append(block)
        return True
    
    def mineBlock(self):
        if not self.current_Transactions:
            return False
                
        last_block = self.getLastBlock
 
        new_block = Block(index=last_block.index + 1,
                          timestamp=time.time(),
                          transactions=self.current_Transactions,
                          nonce=0,
                          previousHash=last_block.Hash)
 
        proof = self.proofOfWork(new_block)
        self.addBlock(new_block, proof)
        self.unconfirmed_transactions = []
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

# app =  Flask(__name__)

# blockchain = Blockchain()

# @app.route('/chain', methods=['GET'])
# def get_chain():
#     chain_data = []
#     for block in blockchain.chain:
#         chain_data.append(block.__dict__)
#     return json.dumps({"length": len(chain_data),
#                        "chain": chain_data})
# app.run(debug=True, port=5000)