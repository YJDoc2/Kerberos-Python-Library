"""Class Cryptor
    Intended to be base interface class for all cryptographers required in library.
    All Custom Cryptographers must extend this class and implement methods encrypt decrypt get_random_key

    The key returned by get_random_key will be given to encrypt and decrypt methods for encryption/decryption
"""
class Cryptor:
    
    def encrypt(self,key,value_str,**kwargs):
        raise NotImplementedError("Class extending Cryptor class must Implement encrypt method")

    def decrypt(self,key,enc_str,**kwargs):
        raise NotImplementedError("Class extending Cryptor class must Implement decrypt method")
    
    def get_random_key(self):
        raise NotImplementedError("Class extending Cryptor class must Implement get_random_key method")