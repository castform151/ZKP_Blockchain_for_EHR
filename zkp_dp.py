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

class ZKP:
    def __init__(self, secretInfo) -> None:
        self._secretInfo = secretInfo
        self.p = ZKPUtil.getLargePrime()
        self.g = prime.find_primitive_root(self.p)
        self.x = random.randint(0, self.p-1)
        self.y = pow(self.g, self.x, self.p)
        self.r = random.randint(0, self.p-1)
        self.m = int(hashlib.md5(secretInfo.encode()).hexdigest(), 16)
        self.t1 = pow(self.m, self.x, self.p)
        self.t2 = pow(self.m, self.r, self.p)
        self.t3 = pow(self.g, self.r, self.p)
        c = int(hashlib.sha256(str(self.t1).encode()).hexdigest(), 16)
        
        
        print(self.m)

    
z = ZKP("102830")