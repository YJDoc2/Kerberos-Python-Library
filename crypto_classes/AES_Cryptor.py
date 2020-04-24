import os
import base64
from Crypto.Cipher import AES
from Crypto.Util import Counter
from .Cryptor import Cryptor
'''Class AES_Cryptor
    This is the default class used for all cryptographers in library.

    This used AES 256 bit encryption from Crypto.Cipher module to encrypt/decrypt
'''
class AES_Cryptor(Cryptor):
    
    def encrypt(self,key,value_str,**kwargs):
        """method for encrypting the data

        Arguments:
            key {String} -- The key provided by get_random_key , must be of 256 bits or 32 bytes
            value_str {String} -- Value string to be encoded
            init_val {int} as key-word arg, required to initialize the counter

        Returns:
            String -- encrypted string encoded in base 64 , so the length is reduced
        """    
        aes = AES.new(key,mode=AES.MODE_CTR,counter=Counter.new(128,initial_value=kwargs['init_val']))
        ret_str = base64.b64encode(aes.encrypt(value_str))
        del aes
        return ret_str

    def decrypt(self,key,enc_str,**kwargs):
        """method for decrypting the data

        Arguments:
            key {String} -- The key provided by get_random_key , must be of 256 bits or 32 bytes
            enc_str {String} -- string encrypted with encrypt on client or server side encoded in base 64
            init_val {int} as key-word arg, required to initialize the counter

        Returns:
            String -- decrypted string
        """        
        aes = AES.new(key,mode=AES.MODE_CTR,counter=Counter.new(128,initial_value=kwargs['init_val']))
        ret_str = aes.decrypt(base64.b64decode(enc_str))
        del aes
        return ret_str


    def get_random_key(self):
        """Provides random key to be used by encrypt/decrypt methods

        Returns:
            String -- 32 byte long hexadecimal encoded string key 
        """        

        # As each byte = 2 hex chars, for 256 bit key we need 256/8 bytes, which are 32,
        # but as hex makes two characters for each bytes, we only request 16
        return os.urandom(16).hex()