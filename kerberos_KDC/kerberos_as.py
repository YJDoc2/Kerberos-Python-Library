import time
import json
import random
import base64
from . import AUTH_INIT_VAL,AUTH_TICKET_LIFETIME
from ..interface_classes import User
from .kerberos_tgs import Kerberos_TGS


class Kerberos_AS:

    def __init__(self,cryptor,tgs):
        self.cryptor = cryptor
        self.tgs = tgs


    def make_auth_tickets(self,rand,c_uid1,c_uid2,user,lifetime_ms=AUTH_TICKET_LIFETIME):
        if not isinstance(user,User):
            raise TypeError("'user' argument must be an instance of class extending User")
        
        pass_hash_key = user.password_to_key()
        secrete_key = base64.b64encode(random.getrandbits(256))
        ticket = {}
        ticket["uid1"] = str(c_uid1)
        ticket["uid2"] = str(c_uid2)
        ticket["timestamp"] = int(time.time()*1000) # Get timestamp in ms
        ticket["lifetime"] = lifetime_ms
        ticket["rand"] = rand
        ticket["target"] = "TGS"
        ticket["key"] = str(secrete_key).encode('ascii')
        res_enc_str = self.cryptor.encrypt(key=pass_hash_key,value_str=json.dumps(ticket),init_val=AUTH_INIT_VAL)
        tgt = self.tgs.get_tgt(c_uid1,c_uid2,key=secrete_key,lifetime_ms=lifetime_ms)
        return (res_enc_str,tgt)



    


        