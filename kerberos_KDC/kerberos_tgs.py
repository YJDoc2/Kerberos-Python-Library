import json
import random
import time
from math import inf,isnan
from ..crypto_classes import Cryptor
from ..db_classes import DB,Memory_DB
from . import TGT_INIT_VAL,TICKET_LIFETIME
from . import SERVER_INIT_RAND_MIN,SERVER_INIT_RAND_MAX
from ..ServerError import ServerError

'''Class Kerberos_TGS for functionality of Genrating Authentication ticket and Ticket Granting Ticket.
    This does not actually create any server, just has all functionality required for auth and TGT generation.

'''
class Kerberos_TGS:

    #Pass check rand if want to verify random number sent in request and prevent replay attacks.
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
    
    # To generate a Server structure and save it in db passed in constructor.
    # The same structure must be used on a perticular server.
    def add_server(self,s_uid):
        name = str(s_uid)
        secrete_key = self.cryptor.get_random_key()
        server = {}
        server["uid"] = name
        server["key"] = secrete_key
        server["init_val"] = random.randint(SERVER_INIT_RAND_MIN,SERVER_INIT_RAND_MAX)
        self.db.save(name,server)

    # Generates a Ticket Granting Ticket.
    # In case this structure is changed also check Kerberos_Server/Server and Kerberos_client/Client classes as well for consistancy.
    # Also change the structure in verify_tgt_and_get_key()
    def get_tgt(self,c_uid1,c_uid2,key,lifetime_ms):
        tgt = {}
        tgt["uid1"] = str(c_uid1)
        tgt["uid2"] = str(c_uid2)
        tgt["key"] = key
        tgt["timestamp"] = int(time.time()*1000)
        tgt["lifetime"] = lifetime_ms
        tgt["target"] = "TGS"
        
        return self.cryptor.encrypt(self.key,json.dumps(tgt),init_val=TGT_INIT_VAL)


    # Helper Function to decrypt tgt, Should not be used externally
    def decrypt_tgt(self,tgt_enc_str):
        tgt_str = self.cryptor.decrypt(self.key,tgt_enc_str,init_val=TGT_INIT_VAL)
        tgt = {}
        try:
            tgt = json.loads(tgt_str)
        except json.JSONDecodeError:
            raise ServerError("Not a Ticket Granting Ticket")
        return tgt

    # Verifies an encrypted TGT and return the key from it.
    def verify_tgt_and_get_key(self,c_uid1,c_uid2,tgt_enc_str):
        tgt = self.decrypt_tgt(tgt_enc_str)
        
        crr_time = int(time.time()*1000)

        if tgt["target"] != "TGS":
            raise ServerError("Not a TGT")

        # In case there is some error of time settings on servers
        # The timestamps in ticket must alway be less than current time on any server, as ticket will be granted before any use.
        if tgt["timestamp"] > crr_time:
            raise ServerError("Invalid timestamp in ticket")

        # In case TGT is expired
        if tgt["lifetime"]+tgt["timestamp"] < crr_time:
            raise ServerError("Ticket Lifetime Eceeded")

        # in case the ticket is not meant for the user who provided it.
        if tgt["uid1"] != str(c_uid1) or tgt["uid2"] != str(c_uid2):
            raise ServerError("Invalid Ticket Holder")
        
        return tgt["key"]

    # A function to decrypt the request made to TGS
    def decrypt_req(self,enc_req_str,tgt):
        dec_tgt = self.decrypt_tgt(tgt)
        req_str = self.cryptor.decrypt(dec_tgt['key'],enc_req_str,init_val=TGT_INIT_VAL)
        return req_str

    # Function to verify the random number give by user is not already used by that user.
    # Used to prevent Replay attacks.
    # Note Must be explicitly called in order to check
    # The checkRand argument in constructor must be given true in order to use this.
    # This is not done directly in decrypt request as it may not be neccessary that the encrypted request will directly contain the
    # random as a property, thus an extra method call is required.
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
            user_data.insert(0,rand)
            self.verify_rand_db.save(user_str,user_data)

    def get_response_and_ticket(self,c_uid1,c_uid2,tgt,req_server,rand,lifetime_ms=TICKET_LIFETIME):
        """Function to generate the encrypted response and encrypted ticket.
           In case this structure is changed also check Kerberos_Server/Server and Kerberos_client/Client classes as well for consistancy.

        Arguments:
            c_uid1 {String} -- uid for gien user which must be same on all servers, eg,ip address
            c_uid2 {String} -- uid for gien user which must be same on all servers, eg,ip address
            tgt {String} -- encrypted Ticket Granting Ticket
            req_server {String} -- Server for which the ticket is to be generated
            rand {Int} -- random number given by the request

        Keyword Arguments:
            lifetime_ms {Int} -- lifetime for generated ticket (default: {TICKET_LIFETIME})

        Returns:
            Tuple -- encrypted response and encrtypted ticket
        """        

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

        # In case this structure is changed also check Kerberos_Server/Server and Kerberos_client/Client classes as well for consistancy.
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


        

