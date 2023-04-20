import prime as primes
import random

def bobCalculation2(s, p, g, y, b, h):
    m = (pow(g, s, p))
    print(f"m = {m}")
    n = (h * pow(y, b, p))
    print(f"n = {n}")
    
    return (m == n)

def bobCalculation1(h):
    b = random.randint(0, 1) # check this
    print(f"b = {b}")
    return b

def aliceCalculation1():
    p = primes.find_prime(56)
    g = primes.find_primitive_root(p)
    print(f"p = {p}")
    print(f"g = {g}")
    
    x = 20000 # sensitive data
    y = pow(g, x, p) # Calculation of y
    print(f"y = {y}")
    
    r = random.randint(0, 100) # p-1 very large, so taking upper bound as
    print(f"r = {r}")
    
    h = pow(g, r, p)
    print(f"h = {h}")
    
    b = bobCalculation1(h)
    
    s = (r + (b*x)) % (p - 1)
    print(f"s = {s}")
    
    ans = bobCalculation2(s, p, g, y, b, h)
    return ans
    
ans = aliceCalculation1()
print(f"ans = {ans}")
    
    