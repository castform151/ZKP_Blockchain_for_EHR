import time
import os
import pickle
import hashlib
from flask import Flask, request
import requests
import json
import zkp_org as zkp

class SimpleObject(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "__dict__"):
            return {key:value for key, value in obj.__dict__.items() if not key.startswith("_")}
        return super().default(obj)  

zkp_para = zkp.ZKP_Para()
# userList = []

class User:
    def __str__(self): return json.dumps(self.__dict__, cls = SimpleObject, indent=4)

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
        self.zkp_signature = zkp.ZKP_Signature(zkp_para, self.password)
        self.reportList = []
        
    @classmethod
    def takeInput(cls):
        return cls(input("Enter username: "), input("Enter password: "))
        
    def addReport(self, report):
        self.reportList.append(report)
        
class Transaction:
    def __str__(self): return json.dumps(self.__dict__, cls = SimpleObject, indent=4)

    def __init__(self, sender, recipient, report):
        self.sender = sender
        self.recipient = recipient
        self.report = report

    @classmethod
    def takeInput(cls):
        sender = input("Enter sender:")
        if(sender not in userList):
            print("Sender not found. Register First")
            return None
        recipient = input("Enter recipient:")
        if(recipient not in userList):
            print("Recipient not found. Invalid username")
            return None
        report = input("Enter report: ")
        return cls(sender, recipient, report)
    
    def verifyTransaction(self):
        if self.report not in self.sender.reportList:
            print("Report not found in sender's report list")
            return False
        ver1 = zkp.ZKP_Verifier(zkp_para, self.sender.zkp_signature)
        ver2 = zkp.ZKP_Verifier(zkp_para, self.recipient.zkp_signature)
        
        return ver1.verify() and ver2.verify()


class Block:
    def __str__(self): return json.dumps(self.__dict__)

    def __init__(self, index, timestamp, transactions, previousHash, nonce = 0):
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
    def __init__(self):
        self.difficulty = 4
        self.current_Transactions = []
        self.chain = [self.createGenesisBlock()]

    def createGenesisBlock(self):
        return Block(0, time.time(), [], 100)

    @property
    def getLastBlock(self):
        return self.chain[-1]
    
    def addTransaction(self, transaction=None):
        print("Adding this transaction" , transaction)
        if not transaction:
            transaction = Transaction.takeInput()
        if(transaction.verifyTransaction()):
            if transaction.report not in transaction.recipient.reportList:
                transaction.recipient.reportList.append(transaction.report)
            else:
                print("Report already present in recipient's report list")
            self.current_Transactions.append(transaction)
            if(len(self.current_Transactions) > 0):
                self.mineBlock()
            return len(self.current_Transactions)
        else:
            print("Transaction not verified")
            return -1

    def viewTransactions(self):
        index = self.getLastBlock.index
        for i in range(0, index):
            print(self.current_Transactions[i])

    def newBlock(self, block, proof):
        previous_hash = self.getLastBlock.Hash
        if previous_hash != block.previousHash:
            return False
        if not self.isValidProof(block, proof):
            return False
        # block.Hash = proof
        self.chain.append(block)
        return True

    def mineBlock(self):
        if not self.current_Transactions:
            return False

        lastBlock = self.getLastBlock

        newBlock = Block(index=lastBlock.index + 1,
                          timestamp=time.time(),
                          transactions=self.current_Transactions,
                          previousHash=lastBlock.Hash)

        proof = self.proofOfWork(newBlock)
        self.newBlock(newBlock, proof)
        self.current_Transactions = []
        return newBlock.index

    def proofOfWork(self, block):
        block.nonce = 0
        computed_hash = block.Hash
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.Hash
        return computed_hash

    def isValidProof(self, block, block_hash):
        return (block_hash.startswith('0' * self.difficulty) and
                block_hash == block.Hash)
    
    
    def isValidChain(self):
        for i in range(1, len(self.chain)):
            print(self.chain[i].previousHash, self.chain[i-1].Hash)
            if self.chain[i].previousHash != self.chain[i-1].Hash:
                return False
        return True
    
    def viewUser(self, username):
        print(userList)
        unl = [i.username for i in userList]
        if(username not in unl):
            print("Blockchain: User not found")
            return None
        tr_list = []
        for i in range(len(self.chain)):
            for j in range(0, len(self.chain[i].transactions)):
                if self.chain[i].transactions[j].sender.username == username or self.chain[i].transactions[j].recipient.username == username:
                    tr_list.append(self.chain[i].transactions[j])
        return tr_list


# u1 = User("P00san", "1234")
# u2 = User("D00Rathi", "0000")
# u3 = User("D00Amogh", "0000")
# userList = [u1,u2,u3]
# with open("userList.pickle", "wb") as f:
#     # pickle the blockchain object and write it to the file
#     pickle.dump(userList, f)

# u1.addReport("I am not feeling well")
# b = Blockchain()
# if os.path.exists("blockchain.pickle"):
#     with open("blockchain.pickle", "rb") as f:
#         # unpickle the object and store it in a variable
#         print("Hello")
#         b = pickle.load(f)
# else:
#     b.addTransaction(Transaction(u1, u2, "I am not feeling well"))
#     b.mineBlock()
#     b.addTransaction(Transaction(u2, u3, "I am not feeling well"))
#     b.mineBlock()

# # print(b.isValidChain())
# # while(int(input("Enter 1 if you want to add a transaction\n")) == 1):
# #     b.addTransaction()
# #     b.mineBlock()

# # open a file to write the pickled blockchain object
# with open("blockchain.pickle", "wb") as f:
#     # pickle the blockchain object and write it to the file
#     pickle.dump(b, f)
    # b.viewTransactions()

# print("These are transactions ")
# print(len(b.chain))
# for i in b.chain:
#     # print(i)
#     for t in i.transactions:
#         print(i, t)

u1 = User("P00san", "1234")
u2 = User("D00Rathi", "0000")
u3 = User("D00Amogh", "0000")
u1.addReport("I am not feeling well")
userList = [u1,u2,u3]
b = Blockchain()
b.addTransaction(Transaction(u1, u2, "I am not feeling well"))
b.mineBlock()
b.addTransaction(Transaction(u2, u3, "I am not feeling well"))
b.mineBlock()
