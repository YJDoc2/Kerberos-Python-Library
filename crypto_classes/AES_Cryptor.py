import base64
from Crypto.Cipher import AES
from Crypto.Util import Counter
from .Cryptor import Cryptor

class AES_Cryptor(Cryptor):
        
    def encrypt(self,key,value_str,**kwargs):
        aes = AES.new(key,mode=AES.MODE_CTR,counter=Counter.new(128,kwargs['init_val']))
        ret_str = base64.b64encode(aes.encrypt(value_str))
        del aes
        return ret_str

    def decrypt(self,key,enc_str,**kwargs):
        aes = AES.new(key,mode=AES.MODE_CTR,counter=Counter.new(128,kwargs['init_val']))
        ret_str = aes.decrypt(base64.b64decode(enc_str))
        del aes
        return ret_str
