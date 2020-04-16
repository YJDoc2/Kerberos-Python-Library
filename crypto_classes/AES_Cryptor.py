import os
import base64
from Crypto.Cipher import AES
from Crypto.Util import Counter
from .Cryptor import Cryptor

class AES_Cryptor(Cryptor):
        
    def encrypt(self,key,value_str,**kwargs):
        aes = AES.new(key,mode=AES.MODE_CTR,counter=Counter.new(128,initial_value=kwargs['init_val']))
        ret_str = base64.b64encode(aes.encrypt(value_str)).decode('ascii')
        del aes
        return ret_str

    def decrypt(self,key,enc_str,**kwargs):
        aes = AES.new(key,mode=AES.MODE_CTR,counter=Counter.new(128,initial_value=kwargs['init_val']))
        ret_str = aes.decrypt(base64.b64decode(enc_str)).decode('ascii')
        del aes
        return ret_str


    def get_random_key(self):
        # As each byte = 2 hex chars, for 256 bit key we need 256/8 bytes, which are 32,
        # but as hex makes two characters for each bytes, we only request 16
        return os.urandom(16).hex()