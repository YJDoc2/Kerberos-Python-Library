import json
from . import REQ_INIT_VAL
from ..crypto_classes import Cryptor,AES_Cryptor
from ..interface_classes import User

class Client:

    def __init__(self,user,cryptor=None):

        if cryptor == None:
            cryptor = AES_Cryptor()

        if not isinstance(cryptor,Cryptor):
            raise TypeError("'cryptor' argument must be an instance of class extending Cryptor class ")
        if not isinstance(user,User):
            raise TypeError("'user' argument must be an instance of class extending User")

        self.cryptor = cryptor
        self.key = user.password_to_key()
    
    def encrypt_req(self,req):
        return self.cryptor.encrypt(self.key,json.dumps(req),init_val=REQ_INIT_VAL)

    def decrypt_res(self,res_enc_str):

        res_str = self.cryptor.decrypt(self.key,res_enc_str,init_val=REQ_INIT_VAL)
        res = {}
        try:
            res = json.loads(res_str)
        except json.JSONDecodeError:
            raise TypeError("Incorrect response")

        return res

    