import json
import time
from . import ServerError
from . import REQ_INIT_VAL
from ..crypto_classes import Cryptor,AES_Cryptor
from ..db_classes import DB,Local_db

class Server:

    def __init__(self,server_dict,cryptor=None):

        if cryptor == None:
            cryptor = AES_Cryptor()
        if not isinstance(cryptor,Cryptor):
            raise TypeError("'cryptor' argument must be an instance of class extending Cryptor class ")
        self.cryptor = cryptor
        self.server = server_dict
        self.key = server_dict["key"]
        self.init_val = server_dict["init_val"]
        self.name = server_dict["uid"]
    
    @classmethod
    def make_server_from_db(server_name,cryptor=None,db=None):

        if cryptor == None:
            cryptor = AES_Cryptor()
        if db == None:
            db = Local_db()

        if not isinstance(db,Cryptor):
            raise TypeError("'cryptor' argument must be an instance of class extending Cryptor class ")
        if not isinstance(db,DB):
            raise TypeError("'db' argument must be an instance of class extending DB class ")

        server = db.get_server(server_name)
        return Server(server,cryptor)

    def verify_ticket_and_get_key(self,c_uid1,c_uid2,ticket_enc_str):

        ticket_str = self.cryptor.decrypt(self.key,ticket_enc_str,init_val=self.init_val)
        ticket = {}
        try:
            ticket = json.loads(ticket_str)
        except json.JSONDecodeError:
            raise ServerError("Invalid Ticket")
        
        crr_time = time.time()
        if ticket["uid1"] != c_uid1 or ticket["uid2"] != c_uid2:
            raise ServerError("Invalid Ticket Holder")
        if ticket["timestamp"] > crr_time:
            raise ServerError("Invalid timestamp in ticket")
        if ticket["lifetime_ms"]+ticket["timestamp"] < crr_time:
            raise ServerError("Ticket Lifetime Exceeded")
        if ticket["target"] != self.name:
            raise ServerError("Wrong Target Server")

        return ticket["key"]

    def decrypt_req(self,c_uid1,c_uid2,ticket,req_enc_str):

        key = self.verify_ticket_and_get_key(c_uid1,c_uid2,ticket)

        req_str = self.cryptor.decrypt(key,req_enc_str,init_val=REQ_INIT_VAL)

        req = {}

        try:
            req = json.loads(req_str)
        except json.JSONDecodeError:
            raise ServerError("Invalid Request Encryption")

        return req
    #! What about encrpyt Response???