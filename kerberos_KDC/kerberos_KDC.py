import time
from ..db_classes import DB,Local_DB,Memory_DB
from ..crypto_classes import Cryptor,AES_Cryptor
from . import Kerberos_AS,Kerberos_TGS
from ..constants import AUTH_TICKET_LIFETIME,TICKET_LIFETIME

'''Class Kerberos_KDC an easier interface class over Authentication Server and Ticket Granting Server
    This creates instances of KerberosAS and KerberosTGS internally and provides an interface over thier methods.
    If the Authentication Service and Ticket Granting Service is set up on single Server,
    then rather than maintaining individual objects of Kerberos_AS and Kerberos_TGS, this can be used.

'''
class Kerberos_KDC:
    
    def __init__(self,cryptor=None,server_db=None,check_rand=False,verify_rand_db=None):

        if cryptor == None:
            cryptor = AES_Cryptor()
        if server_db == None:
            server_db = Local_DB()
        
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
        """For generating initial authentication tickets
           Note this is supposed to be called after verifying that the user making request is a valid user,
           as this does not performs any auth checks,but only make the tickets.

        Arguments:
            rand {Number} -- random number sent by user, and can be verified to prevent replay attacks,if checkRand is given as true in constructor
            c_uid1 {String/Int} -- idetifiers such as username, ip from which user is requesting etc, in string form
                                    which will be saved inside Ticket Granting Tickets, 
                                    and must be same on this server, and any other perticular server where the request is to be made.
            c_uid2 {String/Int} -- idetifiers such as username, ip from which user is requesting etc, in string form
                                    which will be saved inside Ticket Granting Tickets, 
                                    and must be same on this server, and any other perticular server where the request is to be made.
            user_hash {String} -- any string that is specific to the pericular user, eg an sha256 hash of users's password.
                                    This must be exactly reproducable on client side.

        Keyword Arguments:
            lifetime_ms {Number} -- lifetime of ticket in milliseconds (default: {AUTH_TICKET_LIFETIME})

        Raises:
            TypeError: is user_hash is not of type string

        Returns:
            Tuple -- contains auth ticket and ticket granting ticket
        """        
        if not isinstance(user_hash,str):
            raise TypeError("'user_hash' argument must be instance of a class extending str class")
        return self.AS.make_auth_tickets(rand,c_uid1,c_uid2,user_hash,lifetime_ms)
    # Is used to generate a new server structure. This creates a server entry for Ticket Granting Service.
    # The created structure is saved in server_db and must be exactly same on the actual server on which Kerberos_server/Server is used.
    def add_server(self,s_uid):
        return self.TGS.add_server(s_uid)

    # This is used to generate tickets.
    # returns an encrypted response and encrypted ticket
    def get_res_and_ticket(self,c_uid1,c_uid2,tgt,req_server,rand,lifetime_ms=TICKET_LIFETIME):
        return self.TGS.get_response_and_ticket(c_uid1,c_uid2,tgt,req_server,rand,lifetime_ms)

    def decrypt_req(self,enc_req_str,c_uid1,c_uid2,tgt):
        return self.TGS.decrypt_req(enc_req_str,c_uid1,c_uid2,tgt)
    
    # To verify rand sent in the request
    # Note Must be explicitly called in order to check
    def verify_rand(self,c_uid1,c_uid2,rand):
        return self.TGS.verify_rand(c_uid1,c_uid2,rand)