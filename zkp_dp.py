import prime
import random
import hashlib

def getLargePrime():
    b = random.randint(2**8, 2**10) 

# #Large PRime
# p = getLargePrime()
# #generator
# g = prime.find_primitive_root(p)
# #Private Key
# x = random.randint(1, p-1)
# #Public Key
# y = pow(g, x, p)

class ZKPUtil:
    @classmethod
    def getLargePrime(cls):
        # return random.randint(2**8, 2**10)
        return 23

class ZKP_Signature:
    def __init__(self, secretInfo) -> None:
        self._secretInfo = secretInfo
        p = ZKPUtil.getLargePrime()
        g = prime.find_primitive_root(p)
        x = random.randint(0, p-2)
        y = pow(g, x, p)
        r = random.randint(0, p-2)
        m = int(hashlib.md5(secretInfo.encode()).hexdigest(), 16)
        self.t1 = pow(m, x, p)
        self.t2 = pow(m, r, p)
        self.t3 = pow(g, r, p)
        preHash = "{}{}{}".format(self.t1, self.t2, self.t3)
        c = int(hashlib.sha256(preHash.encode()).hexdigest(), 16)
        self.s = c*x + r
    
    def generatepqg(self):
        k = random.randrange(2**8, 2**10)
        
        print(self.m)

class ZK_Verifier:
    def __init__(self) -> None:
        pass
    
    def verify(self):
        
       
# z = ZKP("102830")