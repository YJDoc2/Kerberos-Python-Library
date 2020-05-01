import json
from ..db_classes import DB,Memory_DB
from ..constants import REQ_INIT_VAL,TGT_INIT_VAL
from ..crypto_classes import Cryptor,AES_Cryptor

'''Class Client for Kerberos library. This does not actually set up any kind of client,but contains methods reuired on client side.
'''
class Client:

    def __init__(self,cryptor=None,keymap_db=None):

        if cryptor == None:
            cryptor = AES_Cryptor()
        if keymap_db == None:
            keymap_db = Memory_DB()

        if not isinstance(cryptor,Cryptor):
            raise TypeError("'cryptor' argument must be an instance of class extending Cryptor class ")
        if not isinstance(keymap_db,DB):
            raise TypeError("'keymap_DB' argument must be an instance of class extending DB class ")

        self.cryptor = cryptor
        self.keymap = keymap_db

    # Encrypts a request object
    def encrypt_req(self,key,req,init_val = TGT_INIT_VAL):
        return self.cryptor.encrypt(key,json.dumps(req),init_val=init_val)

    # decrypts an encrypted response string
    def decrypt_res(self,key,res_enc_str,init_val=TGT_INIT_VAL):

        res_str = self.cryptor.decrypt(key,res_enc_str,init_val=init_val)
        res = {}
        try:
            res = json.loads(res_str)
        except :
            raise TypeError("Incorrect response")

        return res

    def save_ticket(self,name,ticket):
        self.keymap.save(name,ticket)

    def get_ticket(self,name):
        return self.keymap.get(name)

    