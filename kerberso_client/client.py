import json
from ..constants import REQ_INIT_VAL,TGT_INIT_VAL
from ..crypto_classes import Cryptor,AES_Cryptor
from ..interface_classes import User

class Client:

    def __init__(self,user_hash,cryptor=None):

        if cryptor == None:
            cryptor = AES_Cryptor()

        if not isinstance(cryptor,Cryptor):
            raise TypeError("'cryptor' argument must be an instance of class extending Cryptor class ")
        if not isinstance(user_hash,str):
            raise TypeError("'user_hash' argument must be an instance of str")

        self.cryptor = cryptor
        self.key = user_hash
        self.keymap = dict()
    
    def encrypt_req(self,req,key,init_val = TGT_INIT_VAL):
        return self.cryptor.encrypt(key,json.dumps(req),init_val=init_val)

    def decrypt_res(self,res_enc_str,key,init_val=TGT_INIT_VAL):

        res_str = self.cryptor.decrypt(key,res_enc_str,init_val=init_val)
        res = {}
        try:
            res = json.loads(res_str)
        except json.JSONDecodeError:
            raise TypeError("Incorrect response")

        return res

    def save_ticket(self,name,ticket):
        self.keymap[name] = ticket

    def get_ticket(self,name,ticket):
        return self.keymap.get(name,None)

    