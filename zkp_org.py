import prime as primes
import random
import hashlib

class ZKP_Para:
    """Generates global/ pubic parameters for ZKP using discrete logarithm problem
    """
    def __init__(self) -> None:
        pt = random.randrange(0, 2**6)
        self.p = primes.find_prime(pt)
        self.g = primes.find_primitive_root(self.p)

class ZKP_Signature:
    """Generates and stores signature for ZKP using discrete logarithm problem
    """
    def __init__(self, zkp_para, secretInfo) -> None:
        """Initialises signature for secretInfo based on zkp_para

        Args:
            zkp_para (ZKP_Para): Instance of ZKP_Para agreed between prover and verifier
            secretInfo (str or int): secret information to be proved to verifier
        """
        secretInfo = int(hashlib.sha256(secretInfo.encode()).hexdigest(), 16)
        self.y = pow(zkp_para.g, secretInfo, zkp_para.p)
        
        self.r = random.randrange(0, zkp_para.p)
        self.h = pow(zkp_para.g, self.r, zkp_para.p)
        
        preHash = "{}{}{}".format(zkp_para.g, self.y, self.h)
        self.challenge = int(hashlib.sha256(preHash.encode()).hexdigest(), 16)
        
        self.sig = (self.r + (self.challenge * secretInfo)) % (zkp_para.p-1)
        
class ZKP_Verifier:
    """Class to store proof/verify procedure for ZKP using discrete logarithm problem
    """
    def __init__(self, zkp_para, zkp_sig) -> None:
        self.zkp_para = zkp_para
        self.zkp_sig = zkp_sig
        
    def verify(self):
        preHash = "{}{}{}".format(self.zkp_para.g, self.zkp_sig.y, self.zkp_sig.h)
        ver_challenge = int(hashlib.sha256(preHash.encode()).hexdigest(), 16)
        
        temp1 = pow(self.zkp_para.g, self.zkp_sig.sig, self.zkp_para.p)
        temp2 = (self.zkp_sig.h * pow(self.zkp_sig.y, ver_challenge, self.zkp_para.p)) % self.zkp_para.p
        
        return (temp1 == temp2) and (ver_challenge == self.zkp_sig.challenge)
    
    
        