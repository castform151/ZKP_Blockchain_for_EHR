import prime
import random
import hashlib
import math

# generating large prime in range 2**(x-1) to 2**x


# def isPrime(num):
#     if num < 2:
#         return False  # as 0 and 1 are not primes
#     # lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227,
#     #              229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499]

#     # if num in lowPrimes:
#     #     return True

#     # for i in lowPrimes:
#     #     if(num % i == 0):
#     #         return False

#     return miller_rabin(num)


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


class ZKP:

    def __init__(self, secretInfo) -> None:
        self._secretInfo = secretInfo
        self.p = ZKPUtil.getLargePrime()
        self.g = prime.find_primitive_root(self.p)
        self.x = random.randint(0, self.p-2)
        self.y = pow(self.g, self.x, self.p)
        self.r = random.randint(0, self.p-2)
        self.m = int(hashlib.md5(secretInfo.encode()).hexdigest(), 16)
        self.t1 = pow(self.m, self.x, self.p)
        self.t2 = pow(self.m, self.r, self.p)
        self.t3 = pow(self.g, self.r, self.p)
        c = int(hashlib.sha256(str(self.t1).encode()).hexdigest(), 16)

        print(self.m)


# z = ZKP("102830")

print(generateLargePrime(2**10))
