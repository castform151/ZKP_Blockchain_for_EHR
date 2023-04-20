import prime
import random
import hashlib
import math


class Prime:
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
    @classmethod
    def isPrime(cls, num):

        if (num < 2):
            return False 

        lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

        if num in lowPrimes:
            return True

        for prime in lowPrimes:
            if (num % prime == 0):
                return False

        return cls.rabinMiller(num)

class ZKP_Para:
    def __init__(self) -> None:
        self.p, self.q, self.g = self.generatepqg()
    
    def generatepqg(self):
        k = random.randrange(2**415, 2**416)
        q = Prime.generateLargePrime(160)
        p = (k*q)+1
        while not Prime.isPrime(p):
            k = random.randrange(2**415, 2**416)
            q = Prime.generateLargePrime(160)
            p = (k*q)+1
        
        t = random.randrange(1, p-1)
        g = pow(t, int((p-1)//q), p)
        return p, q, g
    
class ZKP_Signature:

    def __init__(self, zkp_para, proverID) -> None:
        a = random.randrange(0, zkp_para.q)
        self.apu = pow(zkp_para.g, a, zkp_para.p)
        
        v = random.randrange(0, zkp_para.q)
        self.vpu = pow(zkp_para.g, v, zkp_para.p)
        
        preHash = "{}{}{}{}".format(zkp_para.g, self.vpu, self.apu, proverID)
        self.challenge = int(hashlib.sha256(preHash.encode()).hexdigest(), 16)
        
        self.r = (v - a*self.challenge) % zkp_para.q
            


class ZK_Verifier:
    def __init__(self, zkp_para, zkp_signature) -> None:
        pass

    def verify(self, p, q, g, apu, vpu, challenge, r):
        temp1 = pow(apu, q, p)
        temp_vpu = (pow(g, r, p) * pow(apu, challenge, p)) % p
        if ((apu > 1 and apu < p-1) and temp1 == 1 and temp_vpu == vpu):
            return True
        return False
        
        
       
# z = ZKP("102830")

print(generateLargePrime(2**10))