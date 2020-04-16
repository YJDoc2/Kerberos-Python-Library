import time
import json
from . import AUTH_INIT_VAL,AUTH_TICKET_LIFETIME
from ..crypto_classes import Cryptor
from ..interface_classes import User
from .kerberos_tgs import Kerberos_TGS


class Kerberos_AS:

    def __init__(self,cryptor,tgs):

        if not isinstance(tgs,Kerberos_TGS):
            raise TypeError("'tgs' argument must be instance of Kerberos_TGS class")

        if not isinstance(cryptor,Cryptor):
            raise TypeError("'cryptor argument must be instance of class extending Cryptor class")
        
        self.cryptor = cryptor
        self.tgs = tgs


    def make_auth_tickets(self,rand,c_uid1,c_uid2,user_hash,lifetime_ms=AUTH_TICKET_LIFETIME):
        if not isinstance(user_hash,str):
            raise TypeError("'user_hash' argument must be an instance of class extending str")
        
        pass_hash_key = user_hash
        secrete_key = self.cryptor.get_random_key()

        ticket = {}
        ticket["uid1"] = str(c_uid1)
        ticket["uid2"] = str(c_uid2)
        ticket["timestamp"] = int(time.time()*1000) # Get timestamp in ms
        ticket["lifetime"] = lifetime_ms
        ticket["rand"] = rand
        ticket["target"] = "TGS"
        ticket["key"] = secrete_key
        
        auth_ticket = self.cryptor.encrypt(key=pass_hash_key,value_str=json.dumps(ticket),init_val=AUTH_INIT_VAL)
        tgt = self.tgs.get_tgt(c_uid1,c_uid2,key=secrete_key,lifetime_ms=lifetime_ms)
        return (auth_ticket,tgt)
        



    


        