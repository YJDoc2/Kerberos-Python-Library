import json
import random
import time
from math import inf,isnan
from ..crypto_classes import Cryptor
from ..db_classes import DB,Memory_DB
from . import TGT_INIT_VAL,TICKET_LIFETIME
from . import SERVER_INIT_RAND_MIN,SERVER_INIT_RAND_MAX
from ..ServerError import ServerError

class Kerberos_TGS:

    def __init__(self,cryptor,db,check_rand = False,verify_rand_db=None):

        if not isinstance(cryptor,Cryptor):
            raise TypeError("'cryptor' argument must be an instance of class extending class Cryptor")
        if not isinstance(db,DB):
            raise TypeError("'db' argument must be an instance of class extending class DB")
        
        if check_rand:
            if verify_rand_db == None:
                verify_rand_db = Memory_DB()
            if not isinstance(verify_rand_db,DB):
                raise TypeError("'verify_rand_db' argument must be an instance of class extending class DB")
            self.verify_rand_db = verify_rand_db
        self.check_rand = check_rand
        self.cryptor = cryptor
        self.db = db

        try:
            server = db.get('TGS_SERVER')
            self.key = server['key']
        except:
            self.key = self.cryptor.get_random_key()
            #! CHANGE THIS, maybe add IP address as uid2
            name = "TGS_SERVER"
            server = {}
            server["uid1"] = "TGS"
            server["uid2"] = "SERVER"
            server["key"] = self.key
            self.db.save(name,server)
        
    def add_server(self,s_uid):
        name = str(s_uid)
        secrete_key = self.cryptor.get_random_key()
        server = {}
        server["uid"] = name
        server["key"] = secrete_key
        server["init_val"] = random.randint(SERVER_INIT_RAND_MIN,SERVER_INIT_RAND_MAX)
        self.db.save(name,server)

    def get_tgt(self,c_uid1,c_uid2,key,lifetime_ms):
        tgt = {}
        tgt["uid1"] = str(c_uid1)
        tgt["uid2"] = str(c_uid2)
        tgt["key"] = key
        tgt["timestamp"] = int(time.time()*1000)
        tgt["lifetime"] = lifetime_ms
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

        if tgt["target"] != "TGS":
            raise ServerError("Not a TGT")
        if tgt["timestamp"] > crr_time:
            raise ServerError("Invalid timestamp in ticket")
        if tgt["lifetime"]+tgt["timestamp"] < crr_time:
            raise ServerError("Ticket Lifetime Eceeded")
        if tgt["uid1"] != str(c_uid1) or tgt["uid2"] != str(c_uid2):
            raise ServerError("Invalid Ticket Holder")
        
        return tgt["key"]

    def decrypt_req(self,enc_req_str,c_uid1,c_uid2,tgt):
        key = self.verify_tgt_and_get_key(c_uid1,c_uid2,tgt)
        req_str = self.cryptor.decrypt(key,enc_req_str,init_val=TGT_INIT_VAL)
        try:
            req = json.loads(req_str)
            return req
        except json.JSONDecodeError:
            raise ServerError('Not a valid request')


    def verify_rand(self,c_uid1,c_uid2,rand):
        if not self.check_rand:
            raise ServerError('This instance was not initialized with check_rand = true')
        if not bool(rand):
            raise ServerError("rand' is not present")

        if isnan(rand):
            raise ServerError('rand must be a number')

        user_str = f'{c_uid1}-{c_uid2}'
        user_data = self.verify_rand_db.get(user_str)

        if user_data == None:
            self.verify_rand_db.save(user_str,[rand])
        elif rand in user_data:
            raise ServerError('The random number has already been used by the user')
        else:
            self.verify_rand_db.save(user_str,user_data.insert(0,rand))

    def get_response_and_ticket(self,c_uid1,c_uid2,tgt,req_server,rand,lifetime_ms=TICKET_LIFETIME):

        key = self.verify_tgt_and_get_key(c_uid1,c_uid2,tgt)
       
        
        server = self.db.get(req_server)

        secrete_key = self.cryptor.get_random_key()
        crr_time = int(time.time()*1000)

        res = {}
        res["timestamp"] = crr_time
        res["lifetime"] = lifetime_ms
        res["target"] = req_server
        res["rand"] = rand
        res["key"] = secrete_key
        res["init_val"] = server["init_val"]

        res_enc = self.cryptor.encrypt(key,json.dumps(res),init_val=TGT_INIT_VAL)

        ticket = {}
        ticket["uid1"] = str(c_uid1)
        ticket["uid2"] = str(c_uid2)
        ticket["key"] = secrete_key
        ticket["init_val"] = server["init_val"]
        ticket["target"] = req_server
        ticket["timestamp"] = crr_time
        ticket["lifetime"] = lifetime_ms

        ticket_enc = self.cryptor.encrypt(server["key"],json.dumps(ticket),init_val=server["init_val"])

        return (res_enc,ticket_enc)


        

