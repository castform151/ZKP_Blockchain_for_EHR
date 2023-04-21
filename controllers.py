import hashlib
import json 
from time import time 
import os
import pickle
from blockchain import userList

from blockchain import Blockchain

if os.path.exists("blockchain.pickle"):
    with open("blockchain.pickle", "rb") as f:
        # unpickle the object and store it in a variable
        # b = pickle.load(f)
        pass



def find_user_transactions(user):

    pass
    


# def check_valid_user(user):
#     if user in userList:


