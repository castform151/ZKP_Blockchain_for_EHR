import prime
import random
import hashlib
import math


class ZKPUtil:
    @classmethod
    def miller_rabin(cls, num):
        s = num-1
        t = 0

        while s % 2 == 0:
            s = s//2
            t += 1

        for iter in range(5):
            a = random.randrange(2, num-1)
            v = pow(a, s, num)
            if v != 1:
                i = 0
                while v != (num-1):
                    if i == t-1:
                        return False
                    else:
                        i += 1
                        v = (pow(v, 2, num))
        return True

    @classmethod
    def generateLargePrime(cls, x):
        k = int(math.log2(x))
        print(k)
        num = random.randrange(2**k, 2**(k+1))
        while(not cls.miller_rabin(num)):
            print(num)
            num = random.randrange(k, k*2)
            # num += 1
        return num


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

#     def verify(self):
        
       
# z = ZKP("102830")

print(generateLargePrime(2**10))