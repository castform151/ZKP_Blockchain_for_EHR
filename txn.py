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
