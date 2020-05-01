import json
import time
from . import Server_Error
from ..crypto_classes import Cryptor,AES_Cryptor
from ..db_classes import DB,Local_DB,Memory_DB

'''Class Server which should be used on servers that are to be protected using Kerberos.
    Note this does not actually creates a Server, just has the functionality that is required on Server side.
    The optional argument checkRand in constructor allows checking of the random numbers sent in requests to prevent replay attacks

    The cUid arguments in encrypt and decrypt functions are used to verify that the ticket and request belongs to the user
    These must be same for a given user on a perticular server and the Ticket granting server. Cab be used to prevent replay attacks.
'''
class Server:


    # Direct constructor if you have a server structure ready, or doing some tests.
    # In case arguments are changed, please also check verifyRand function's comments.
    def __init__(self,server_dict,cryptor=None,check_rand = False,verify_rand_db = None):

        if cryptor == None:
            cryptor = AES_Cryptor()

        if 'key' not in server_dict or 'init_val' not in server_dict or 'uid' not in server_dict:
            raise Server_Error('Invalid Server object')

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
    

    # Static method for loading server structure from a db and make an object.
    @classmethod
    def make_server_from_db(cls,name,cryptor=None,db=None,check_rand=False,verify_rand_db=None):

        if cryptor == None:
            cryptor = AES_Cryptor()
        if db == None:
            db = Local_DB()
        if not isinstance(cryptor,Cryptor):
            raise TypeError("'cryptor' argument must be an instance of class extending Cryptor class ")
        if not isinstance(db,DB):
            raise TypeError("'db' argument must be an instance of class extending DB class ")

        server = db.get(name)
        return Server(server,cryptor,check_rand,verify_rand_db)

    # Helper Function to decrypt tgt, Should not be used externally
    def decrypt_ticket(self,ticket_enc_str):
        try:
            ticket_str = self.cryptor.decrypt(self.key,ticket_enc_str,init_val=self.init_val)
            ticket = json.loads(ticket_str)
            return ticket
        except :
            raise Server_Error("Invalid Ticket")
        
    
    # A function to decrypt the request made to TGS
    def decrypt_req(self,enc_req_str,ticket):
        dec_ticket = self.decrypt_ticket(ticket)
        req_str = self.cryptor.decrypt(dec_ticket['key'],enc_req_str,init_val=self.init_val)
        return req_str

    # Verifies the Ticket Granting Ticket and returns the key stored in it.
    # In case the structure of TGT is changed in Kerberos_KDC/Kerberos_TGS this must be updated.
    #cUid1 and cUid2 are identifies of a perticular user, and must be same on TGS and on a perticuar server
    def verify_ticket_and_get_key(self,c_uid1,c_uid2,ticket_enc_str):
        
        ticket = self.decrypt_ticket(ticket_enc_str)

        crr_time = int(time.time()*1000)
        
        # In case the requesting user is not the one ticket was granted to
        if ticket["uid1"] != c_uid1 or ticket["uid2"] != c_uid2:
            raise Server_Error("Invalid Ticket Holder")

        # In case there is some error of time settings on servers
        # The timestamps in ticket must alway be less than current time on any server, as ticket will be granted before any use.
        if ticket["timestamp"] > crr_time:
            raise Server_Error("Invalid timestamp in ticket")

        # In case ticket is expired
        if ticket["lifetime"]+ticket["timestamp"] < crr_time:
            raise Server_Error("Ticket Lifetime Exceeded")

        # In case the ticket is not intended for this server, this is set by TGS,
        # and the server creted here, and stored in TGS's DB must be same.
        if ticket["target"] != self.name:
            raise Server_Error("Wrong Target Server")

        return ticket["key"]


    
    

    # Ecrypts the encrypted response object given.
    # In case the structure of TGT is changed in Kerberos_KDC/KerberosTGS this must be updated.
    # cUid1 and cUid2 are identifies of a perticular user, and must be same on TGS and on a perticuar server
    def encrypt_res(self,c_uid1,c_uid2,response,ticket):

        key = self.verify_ticket_and_get_key(c_uid1,c_uid2,ticket)

        enc_res = self.cryptor.encrypt(key,json.dumps(response),init_val = self.init_val)

        return enc_res

    # Function to verify the random number give by user is not already used by that user.
    # Used to prevent Replay attacks.
    # The checkRand argument in constructor must be given true in order to use this.
    # This is not done directly in decrypt request as it may not be neccessary that the encrypted request will directly contain the
    # random as a property, thus an extra method call is required.
    def verify_rand(self,rand, c_uid1,c_uid2):
        if not self.check_rand:
            raise TypeError('This instance was not initialized with check_rand = True')

        if rand == None:
            raise Server_Error("'rand' is not present")
        if not isinstance(rand,int) and not isinstance(rand,float):
            raise Server_Error("rand must be a number")
        user_str = f'{c_uid1}-{c_uid2}'
        user_data = self.verify_rand_db.get(user_str)
        if user_data == None:
            self.verify_rand_db.save(user_str,[rand])
        elif rand in user_data:
            raise Server_Error('The random number has already been used by the user')
        else:
            user_data.insert(0,rand)
            self.verify_rand_db.save(user_str,user_data)