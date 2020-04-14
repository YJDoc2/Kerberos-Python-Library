import json
import random
import base64
import time
from math import inf
from ..crypto_classes import Cryptor
from ..db_classes import DB
from . import TGT_INIT_VAL,TICKET_LIFETIME
from . import SERVER_INIT_RAND_MIN,SERVER_INIT_RAND_MAX
from ..ServerError import ServerError

class Kerberos_TGS:

    def __init__(self,cryptor,db):

        if not isinstance(cryptor,Cryptor):
            raise TypeError("'cryptor' argument must be an instance of class extending class Cryptor")
        if not isinstance(db,DB):
            raise TypeError("'db' argument must be an instance of class extending class DB")
        self.cryptor = cryptor
        self.db = db
        self.key = base64.b64encode(random.getrandbits(256))

        #! CHANGE THIS, maybe add IP address as uid2
        name = "TGS_SERVER"
        
        server = {}
        server["uid1"] = "TGS"
        server["uid2"] = "SERVER"
        server["key"] = self.key
        self.db.save_server(name,server)
        
    def add_server(self,s_uid):
        name = str(s_uid)
        secrete_key = base64.b64encode(random.getrandbits(256))
        server = {}
        server["uid"] = name
        server["key"] = secrete_key
        server["init_val"] = random.randint(SERVER_INIT_RAND_MIN,SERVER_INIT_RAND_MAX)
        self.db.save_server(name,server)

    def get_tgt(self,c_uid1,c_uid2,key,lifetime_ms):
        tgt = {}
        tgt["uid1"] = str(c_uid1)
        tgt["uid2"] = str(c_uid2)
        tgt["key"] = key
        tgt["timestamp"] = int(time.time()*1000)
        tgt["lifetime_ms"] = lifetime_ms
        tgt["target"] = "TGS"
        return self.cryptor.encrypt(self.key,json.dumps(tgt),init_val=TGT_INIT_VAL)


    def verify_tgt_and_get_key(self,c_uid1,c_uid2,tgt_enc_str):
        tgt_str = self.cryptor.decrypt(self.key,tgt_enc_str,init_val=TGT_INIT_VAL)
        tgt = {}
        try:
            tgt = json.loads(tgt_str)
        except json.JSONDecodeError:
            raise ServerError("Not a Ticket Granting Ticket")
        
        crr_time = int(time.time()*1000)

        if tgt["target"] != "TGT":
            raise ServerError("Not a TGT")
        if tgt["timestamp"] > crr_time:
            raise ServerError("Invalid timestamp in ticket")
        if tgt["lifetime_ms"]+tgt["timestamp"] < crr_time:
            raise ServerError("Ticket Lifetime Eceeded")
        if tgt["uid1"] != str(c_uid1) or tgt["uid2"] != str(c_uid2):
            raise ServerError("Invalid Ticket Holder")
        
        return tgt["key"]

    
    def get_response_and_ticket(self,c_uid1,c_uid2,tgt,req_enc_str,lifetime_ms=TICKET_LIFETIME):

        key = self.verify_tgt_and_get_key(c_uid1,c_uid2,tgt)
        req_str = self.cryptor.decrypt(key,req_enc_str,init_val=TGT_INIT_VAL)

        req = {}
        try:
            req = json.loads(req_str)
        except json.JSONDecodeError :
            raise ServerError("Invalid request")

        if req["uid1"] != str(c_uid1) or req["uid2"] != str(c_uid2):
            raise ServerError("Invalid Ticket Holder")
        if req.get("rand",inf) == inf:
            raise ServerError("Request must contain a Random Number")

        req_server = req["target"]
        server = self.db.get_server(req_server)

        secrete_key = base64.b64encode(random.getrandbits(256))
        crr_time = int(time.time()*1000)

        res = {}
        res["timestamp"] = crr_time
        res["lifetime"] = lifetime_ms
        res["target"] = req_server
        res["rand"] = req["rand"]
        res["key"] = secrete_key

        res_enc = self.cryptor.encrypt(key,json.dumps(res),init_val=TGT_INIT_VAL)

        ticket = {}
        ticket["uid1"] = str(c_uid1)
        ticket["uid2"] = str(c_uid2)
        ticket["key"] = secrete_key
        ticket["target"] = req_server
        ticket["timestamp"] = crr_time
        ticket["lifetime"] = lifetime_ms

        ticket_enc = self.cryptor.encrypt(server["key"],json.dumps(ticket),init_val=TGT_INIT_VAL)

        return (res_enc,ticket_enc)


        

