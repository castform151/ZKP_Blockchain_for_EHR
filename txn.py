import hashlib
import ecdsa
from user import User


class Transaction:
    def __init__(self, sender, recipient, amount, zk_proof):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.zk_proof = zk_proof

    def calculateHash(self):
        hashData = str(self.sender) + str(self.recipient) + str(self.amount)
        return hashlib.sha256(hashData.encode()).hexdigest()

    def verifyTransaction(self, blockchain):
        senderBalance = 0
        for block in blockchain.chain:
            for transaction in block.transactions:
                if transaction.sender == self.sender:
                    senderBalance -= transaction.amount
                elif transaction.recipient == self.sender:
                    senderBalance += transaction.amount
        if senderBalance < self.amount:
            return False
        return self.verifyZkProof(senderBalance)

    def verifyZkProof(self, senderBalance):
        # Implement the zero-knowledge proof verification logic here
        # Return True if the proof is valid, and False otherwise
        pass


class Block:
    def __init__(self, timestamp, transactions, previous_hash=''):
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Calculate the hash of the block."""
        data = str(self.timestamp) + str(self.transactions) + \
            str(self.previous_hash) + str(self.nonce)
        return hashlib.sha256(data.encode()).hexdigest()

    def mine_block(self, difficulty):
        """Mine the block using proof of work."""
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

        print("Block mined: ", self.hash)
