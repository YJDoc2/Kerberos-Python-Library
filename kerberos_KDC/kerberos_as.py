import time
import json
from . import AUTH_INIT_VAL,AUTH_TICKET_LIFETIME
from ..ServerError import ServerError
from ..db_classes import DB,Memory_DB
from ..crypto_classes import Cryptor
from .kerberos_tgs import Kerberos_TGS

'''Class Kerberos_AS for functionality of Genrating Authentication ticket and Ticket Granting Ticket.
    This does not actually create any server, just has all functionality required for auth and TGT generation.
'''
class Kerberos_AS:

    # Pass check_rand True if want to verify random number sent in request and prevent replay attacks.
    def __init__(self,cryptor,tgs,check_rand=False,verify_rand_db=None):

        if not isinstance(tgs,Kerberos_TGS):
            raise TypeError("'tgs' argument must be instance of Kerberos_TGS class")

        if not isinstance(cryptor,Cryptor):
            raise TypeError("'cryptor' argument must be instance of class extending Cryptor class")
        
        if check_rand:
            if verify_rand_db == None:
                verify_rand_db = Memory_DB()

            if not isinstance(verify_rand_db,DB):
                raise TypeError("'verify_rand_db' argument must be instance of class extending DB class")
            self.verify_rand_db = verify_rand_db
            
        self.check_rand = check_rand
        self.cryptor = cryptor
        self.tgs = tgs


    def make_auth_tickets(self,rand,c_uid1,c_uid2,user_hash,lifetime_ms=AUTH_TICKET_LIFETIME):
        """Generates authentication and Ticket Granting Ticket.Does not actually authenticate, must be called after doing authentication.

        Arguments:
            rand {int} -- random number sent in user request,can be used to detect replay attacks, if check_rand is given as True in constructor
            c_uid1 {String/Int} -- uid for gien user which must be same on all servers, eg,ip address
            c_uid2 {String/Int} -- uid for gien user which must be same on all servers, eg,ip address
            user_hash {String} -- hash generated from parameter specific to user, must be reproducible on client side,is used to encrypt auth ticket

        Keyword Arguments:
            lifetime_ms {int} -- lifetime for authentication ticket and TGT in milliseconds (default: {AUTH_TICKET_LIFETIME})

        Raises:
            TypeError: if user_hash is not of type string
            ServerError: if random number is already used by user

        Returns:
            Tuple -- contains auth-ticket and ticket granting ticket
        """        
        if not isinstance(user_hash,str):
            raise TypeError("'user_hash' argument must be an instance of class extending str")
        
        if self.check_rand:
            user_str = f'{c_uid1}-{c_uid2}'
            user_data = self.verify_rand_db.get(user_str)
            if user_data == None:
                self.verify_rand_db.save(user_str,[rand])
            elif rand in user_data:
                raise ServerError('The random number has already been used by the user')
            else:
                self.verify_rand_db.save(user_str,user_data.insert(0,rand))


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
        



    


        