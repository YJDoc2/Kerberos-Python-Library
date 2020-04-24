import time
from ..db_classes import DB,Local_db,Memory_DB
from ..crypto_classes import Cryptor,AES_Cryptor
from . import Kerberos_AS,Kerberos_TGS
from ..constants import AUTH_TICKET_LIFETIME,TICKET_LIFETIME

class Kerberos_KDC:
    
    def __init__(self,cryptor=None,server_db=None,check_rand=False,verify_rand_db=None):

        if cryptor == None:
            cryptor = AES_Cryptor()
        if server_db == None:
            server_db = Local_db()
        
        if not isinstance(server_db,DB):
            raise TypeError("'server_db' argument must be an instance of class extending DB class ")
        if not isinstance(cryptor,Cryptor):
            raise TypeError("'cryptor' argument must be an instance of class extending Cryptor class ")

        if check_rand :
            if verify_rand_db == None:
                verify_rand_db = Memory_DB()
            if not isinstance(verify_rand_db,DB):
                raise TypeError("'verify_rand_db' argument must be an instance of class extending DB class ")

        self.server_db = server_db
        self.cryptor = cryptor
        self.TGS = Kerberos_TGS(cryptor,server_db,check_rand=check_rand,verify_rand_db=verify_rand_db)
        self.AS = Kerberos_AS(cryptor,self.TGS,check_rand=check_rand,verify_rand_db=verify_rand_db)
        
    def gen_auth_tickets(self,rand,c_uid1,c_uid2,user_hash,lifetime_ms=AUTH_TICKET_LIFETIME):
        if not isinstance(user_hash,str):
            raise TypeError("'user_hash' argument must be instance of a class extending str class")
        return self.AS.make_auth_tickets(rand,c_uid1,c_uid2,user_hash,lifetime_ms)

    def add_server(self,s_uid):
        return self.TGS.add_server(s_uid)

    def get_res_and_ticket(self,c_uid1,c_uid2,tgt,req_server,rand,lifetime_ms=TICKET_LIFETIME):
        return self.TGS.get_response_and_ticket(c_uid1,c_uid2,tgt,req_server,rand,lifetime_ms)

    def decrypt_req(self,enc_req_str,c_uid1,c_uid2,tgt):
        return self.TGS.decrypt_req(enc_req_str,c_uid1,c_uid2,tgt)
    
    def verify_rand(self,c_uid1,c_uid2,rand):
        return self.TGS.verify_rand(c_uid1,c_uid2,rand)