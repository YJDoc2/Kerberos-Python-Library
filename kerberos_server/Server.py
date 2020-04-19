import json
import time
from . import ServerError
from ..crypto_classes import Cryptor,AES_Cryptor
from ..db_classes import DB,Local_db,Memory_DB

class Server:

    def __init__(self,server_dict,cryptor=None,check_rand = False,verify_rand_db = None):

        if cryptor == None:
            cryptor = AES_Cryptor()
        
        if check_rand:
            if verify_rand_db == None:
                verify_rand_db = Memory_DB()
            if not isinstance(verify_rand_db,DB):
                raise TypeError("'verify_rand_db' argument must be an instance of class extending DB class ")
            self.verify_rand_db = verify_rand_db

        if not isinstance(cryptor,Cryptor):
            raise TypeError("'cryptor' argument must be an instance of class extending Cryptor class ")
        self.check_rand = check_rand
        self.cryptor = cryptor
        self.server = server_dict
        self.key = server_dict["key"]
        self.init_val = server_dict["init_val"]
        self.name = server_dict["uid"]
    
    @classmethod
    def make_server_from_db(cls,server_name,cryptor=None,db=None,check_rand=False,verify_rand_db=None):

        if cryptor == None:
            cryptor = AES_Cryptor()
        if db == None:
            db = Local_db()
        if not isinstance(cryptor,Cryptor):
            raise TypeError("'cryptor' argument must be an instance of class extending Cryptor class ")
        if not isinstance(db,DB):
            raise TypeError("'db' argument must be an instance of class extending DB class ")

        server = db.get(server_name)
        return Server(server,cryptor,check_rand,verify_rand_db)

    def verify_ticket_and_get_key(self,c_uid1,c_uid2,ticket_enc_str):
        ticket_str = self.cryptor.decrypt(self.key,ticket_enc_str,init_val=self.init_val)
        ticket = {}
        try:
            ticket = json.loads(ticket_str)
        except json.JSONDecodeError:
            raise ServerError("Invalid Ticket")
        crr_time = int(time.time()*1000)
        
        if ticket["uid1"] != c_uid1 or ticket["uid2"] != c_uid2:
            raise ServerError("Invalid Ticket Holder")
        if ticket["timestamp"] > crr_time:
            raise ServerError("Invalid timestamp in ticket")
        if ticket["lifetime"]+ticket["timestamp"] < crr_time:
            raise ServerError("Ticket Lifetime Exceeded")
        if ticket["target"] != self.name:
            raise ServerError("Wrong Target Server")

        return ticket["key"]

    def decrypt_req(self,c_uid1,c_uid2,ticket,req_enc_str):
        
        key = self.verify_ticket_and_get_key(c_uid1,c_uid2,ticket)

        req_str = self.cryptor.decrypt(key,req_enc_str,init_val=self.init_val)

        req = {}

        try:
            req = json.loads(req_str)
        except json.JSONDecodeError:
            raise ServerError("Invalid Request Encryption")
        
        return req
    
    def encrypt_res(self,c_uid1,c_uid2,ticket,res):

        key = self.verify_ticket_and_get_key(c_uid1,c_uid2,ticket)

        enc_res = self.cryptor.encrypt(key,json.dumps(res),init_val = self.init_val)

        return enc_res

    def verify_rand(self, c_uid1,c_uid2,rand):
        if not self.check_rand:
            return TypeError('This instance was not initialized with check_rand = True')

        if rand == None:
            raise ServerError("'rand' is not present")

        if not isinstance(rand,int) or not isinstance(rand,float):
            raise ServerError("rand must be a Number")
        
        user_str = f'{c_uid1}-{c_uid2}'
        user_data = self.verify_rand_db.get(user_str)
        if user_data == None:
            self.verify_rand_db.save(user_str,[rand])
        elif rand in user_data:
            raise ServerError('The random number has already been used by the user')
        else:
            self.verify_rand_db.save(user_str,user_data.insert(0,rand))