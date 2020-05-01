# Kerberos Python Library API References

## Index

<ul>
    <li><a href='#constants-header'>Constants</a></li>
    <li><a href='#class-server-error'>Server_Error</a></li>
    <li><a href ="#db-header">DB Classes</a>
        <ul>
            <li><a href ="#class-db">DB</a>
                <ul>
                    <li><a href='#db-save'>save(name,data)</a></li>
                    <li><a href='#db-get'>get(name)</a></li>
                </ul>
            </li>
            <li><a href= '#class-memory-db'>Memory_DB</a>
                <ul>
                    <li><a href ='#memory-db-save'>save(name,data)</a></li>
                    <li><a href ='#memory-db-get'>get(name)</a></li>
                </ul>
            </li>
            <li><a href='#class-local-db'>Local_DB</a>
                <ul>
                    <li><a href='#local-db-constructor'>constructor(ticket_folder_path = null)</a></li>
                    <li><a href='#local-db-save'>save(name,data)</a></li>
                    <li><a href='#local-db-get'>get(name)</a></li>
                </ul>
            </li>
        </ul>
    </li>
    <li><a href='#cryptor-header'>Cryptor Classes</a>
        <ul>
            <li><a href = '#class-cryptor'>Cryptor</a>
                <ul>
                    <li><a href = '#cryptor-get-random-key'>get_random_key()</a></li>
                    <li><a href = '#cryptor-encrypt'>encrypt(key,value_str,**kwargs)</a></li>
                    <li><a href = '#cryptor-decrypt'>decrypt(key,enc_str,**kwargs)</a></li>
                </ul>
            </li>
            <li><a href = '#class-aescryptor'>AES_Cryptor</a>
                <ul>
                    <li><a href = '#aescryptor-get-random-key'>get_random_key()</a></li>
                    <li><a href = '#aescryptor-encrypt'>encrypt(key,value_str,**kwargs)</a></li>
                    <li><a href = '#aescryptor-decrypt'>decrypt(key,enc_str,**kwargs)</a></li>
                </ul>
            </li>
        </ul>
    </li>
    <li><a href ='#kdc-header'>Kerberos KDC Classes</a>
        <ul>
            <li><a href='#class-kerberos-as'>Kerberos_AS</a>
                <ul>
                    <li><a href = '#kerberos-as-constructor'>constructor(cryptor, tgs, check_rand = False, verify_rand_db = None)</a></li>
                    <li><a href = '#kerberos-as-make-auth-tickets'>make_auth_tickets(rand,c_uid1,c_uid2,user_hash,lifetime_ms = AUTH_TICKET_LIFETIME)</a></li>
                </ul>
            </li>
            <li><a href='#class-kerberos-tgs'>Kerberos_TGS</a>
                <ul>
                    <li><a href='#kerberos-tgs-constructor'>constructor(cryptor, db, check_rand = False, verify_rand_db = None)</a></li>
                    <li><a href='#kerberos-tgs-add-server'>add_server(s_uid)</a></li>
                    <li><a href='#kerberos-tgs-get-tgt'>get_tgt(c_uid1, c_uid2, key, lifetime_ms)</a></li>
                    <li><a href='#kerberos-tgs-decrypt-tgt'>decrypt_tgt(enc_tgt_str)</a></li>
                    <li><a href='#kerberos-tgs-verify-tgt-and-get-key'>verify_tgt_and_get_key(c_uid1, c_uid2, tgt_enc_str)</a></li>
                    <li><a href='#kerberos-tgs-decrypt-req'>decrypt_req(enc_req_str, tgt)</a></li>
                    <li><a href='#kerberos-tgs-verify-rand'>verify_rand(rand,c_uid1, c_uid2)</a></li>
                    <li><a href='#kerberos-tgs-get-res-and-ticket'>get_res_and_ticket(rand,req_server,c_uid1,c_uid2,tgt,lifetime_ms = TICKET_LIFETIME)</a></li>
                </ul>
            </li>
            <li><a href='#class-kerberos-kdc'>Kerberos_KDC</a>
                <ul>
                    <li><a href='#kerberos-kdc-constructor'>constructor(cryptor = None,server_db = None,check_rand = False,verify_rand_db = None)</a></li>
                    <li><a href='#kerberos-kdc-make-auth-tickets'>make_auth_tickets(rand,c_uid1,c_uid2,user_hash,lifetime_ms = AUTH_TICKET_LIFETIME)</a></li>
                    <li><a href='#kerberos-kdc-add-server'>add_server(s_uid)</a></li>
                    <li><a href='#kerberos-kdc-get-res-and-ticket'>get_res_and_ticket(rand,req_server,c_uid1,c_uid2,tgt,lifetime_ms = TICKET_LIFETIME)</a></li>
                    <li><a href='#kerberos-kdc-decrypt-req'>decrypt_req(enc_req_str, tgt)</a></li>
                    <li><a href='#kerberos-kdc-verify-rand'>verify_rand(rand,c_uid1, c_uid2)</a></li>
                </ul>
            </li>
        </ul>
    </li>
    <li><a href='#class-server'>Kerberos Server</a>
        <ul>
            <li><a href='#server-make-server-from-db'>Static make_server_from_db(name,cryptor = None,db = None,check_rand = False,verify_rand_db = None)</a></li>
            <li><a href='#server-constructor'>constructor(server_dict,cryptor=None,check_rand=False,verify_rand_db=None)</a></li>
            <li><a href='#server-decrypt-ticket'>decrypt_ticket(ticket_enc_str)</a></li>
            <li><a href='#server-verify-ticket-and-get-key'>verify_ticket_and_get_key(c_uid1,c_uid2,ticket_enc_str)</a></li>
            <li><a href='#server-decrypt-req'>decrypt_req(enc_req_str,ticket)</a></li>
            <li><a href='#server-encrypt-res'>encrypt_res(c_uid1,c_uid2,response,ticket)</a></li>
            <li><a href='#server-verify-rand'>verify_rand(rand,c_uid1,c_uid2)</a></li>
        </ul>
    </li>
    <li><a href='#class-client'>Kerberos Client
        <ul>
            <li><a href='#client-constructor'>constructor(cryptor = None, keymap_db = None)</a></li>
            <li><a href='#client-encrypt-req'>encrypt_req(key,req,init_val = TGT_INIT_VAL)</a></li>
            <li><a href='#client-decrypt-req'>decrypt_res(key,res_enc_str,init_val = TGT_INIT_VAL)</a></li>
            <li><a href='#client-save-ticket'>save_ticket(name, ticket)</a></li>
            <li><a href='#client-get-ticket'>get_ticket(name)</a></li>
        </ul>
    </li>
</ul>

## API

<h3 id='constants-header'>Constants</h3>
<p>These are constant values used as defaults in various methods.</p>
<ul>
    <li>AUTH_INIT_VAL = 5 Initialization value for Auth ticket encryption</li>
    <li> TGT_INIT_VAL = 5 Initialization value for Ticket Granting Ticket encryption</li>
    <li> AUTH_TICKET_LIFETIME = 24 * 60 * 60 * 60 * 1000 (1 Day) lifetime of Authentication Ticket and Ticket Granting Ticket</li>
    <li> TICKET_LIFETIME = 10 * 60 * 1000 (10 min) lifetime of a general server ticket</li>
    <li> SERVER_INIT_RAND_MIN = 1 Minimum limit for choosing random initialization value for a server in TGS add_server()</li>
    <li>SERVER_INIT_RAND_MAX = 2147483647 Maximum limit for choosing random initialization value for a server in TGS add_server() (Number chosen is limit of int in c++)</li>
</ul>

<h3 id='class-server-error'>Class Server_Error</h3>
<p>A class used to show errors specific to this library. This simply extends the default Error class in JS and does not specify any different methods of its own.</p>

<h3 id='db-header'>DB Classes</h3>
<p>These are classes used to store and retrieve data that is needed in the operations.The main interface is defined by Class DB, and any custom db class must extend that and implement its methods.</p>

<div>
<h4 id='class-db'>Class DB</h4>
<p>This is base class used as the interface for all DB classes in the module. This defines two methods <strong>save</strong> and <strong>get</strong> that must be implemented by any extending class.</p>

<h5 id='db-save'>save(name,data)</h5>
<p>This method is used for saving the data in db.</p>
Params :
<ul>
    <li>name {string} : The key that the data should be associated with. Same will be used for retrieving the data</li>
    <li>data {Any} : The data that is to be saved</li>
</ul>
Returns : {void}

<h5 id='db-get'>get(name)</h5>
<p>This method is used for retrieving the data from the DB</p>
Params :
<ul>
    <li>name {string} : the key that the data was saved with</li>
</ul>
Returns : {Any} The data that was saved corresponding to key.
</div>

<div>
<h4 id='class-memory-db'>Class Memory_DB</h4>
<p>This is a db class that uses python Dict internally to save data. The access speed should be usually faster than Local_DB.</p>
<p>This is used where a lightweight db just for storing temporary data is needed, like verifying random numbers or in client for saving tickets.</p>
<p>This can be replaced by a class that connects with Redis DB if one wants an option which is sharable between multiple instances.
</p>

<h5 id='memory-db-save'>save(name,data)</h5>
<p>This method is used for saving the data in db.</p>
Params :
<ul>
    <li>name {string} : The key that the data should be associated with. Same will be used for retrieving the data</li>
    <li>data {Any} : The data that is to be saved</li>
</ul>
Returns : {void}

<h5 id='memory-db-get'>get(name)</h5>
<p>This method is used for retrieving the data from the DB</p>
Params :
<ul>
    <li>name {string} : the key that the data was saved with</li>
</ul>
Returns : {Any} The data that was saved.
</div>

<div>
<h4 id='class-local-db'>Class Local_DB</h4>
<p>This class uses File System to save data in files on disk. </p>

<h5 id='local-db-constructor'>constructor(ticket_folder_path = None)</h5>
<p>This by default creates a folder named 'Tickets' in the directory from which program was invoked if no parameter is given. Otherwise The given path is constructed if not present and is used for saving the data.</p>
Params:
<ul>
    <li>ticket_folder_path {string} : the path which should be used for saving the data files.</li>
</ul>
Returns : {Object} An instance of LocalDB.

<h5 id='local-db-save'>save(name,data)</h5>
<p>This method is used for saving the data in db. Given data is stored as stringified JSON object in a file named as the parameter name.</p>
Params :
<ul>
    <li>name {string} : The key that the data should be associated with. Same will be used for retrieving the data</li>
    <li>data {Any} : The data that is to be saved</li>
</ul>
Returns : {void}

<h5 id='local-db-get'>get(name)</h5>
<p>This method is used for retrieving the data from the DB</p>
Params :
<ul>
    <li>name {string} : the key that the data was saved with</li>
</ul>
Returns : {Any} The data that was saved.
</div>

<h3 id='cryptor-header'>Cryptor Classes</h3>
<p>These are classes used for encryption and decryption of data in the module. Main interface is defined by Class cryptor, and any custom Cryptographic class must extend it and implement its methods.</p>

<div>
<h4 id='class-cryptor'>Class Cryptor</h4>
<p>This is base class used as the interface for all Cryptographic classes in the module. This defines three methods <strong>encrypt</strong>, <strong>decrypt</strong> and <strong>get_random_key</strong> that must be implemented by any extending class.</p>

<h5 id='cryptor-get-random-key'>get_random_key()</h5>
<p>This method is used to get the keys required for encryption and decryption</p>
Params : None
Returns : {String/Number} A key that can be given to encrypt and decrypt methods.

<h5 id='cryptor-encrypt'>encrypt(key,value_str,**kwargs)</h5>
<p>This method is used for encrypting the data.</p>
Params:
<ul>
    <li>key {string/Number} : The key obtained from getRandomKey Method.</li>
    <li>enc_str {String} : The data that is to be encrypted in string format</li>
    <li>**kwargs {} : init_val is the third needed keyword arg.</li>
</ul>
Returns : {String} The encrypted form of the given string.

<h5 id = 'cryptor-decrypt'>decrypt(key,enc_str,**kwargs)</h5>
<p>This method is used for decrypting the data.</p>
Params:
<ul>
    <li>key {string/Number} : The key obtained from getRandomKey Method.</li>
    <li>enc_str {String} : The encrypted string that is to be decrypted</li>
    <li>**kwargs {} : init_val is the third needed keyword arg.</li>
</ul>
Returns : {String} The decrypted form of the given string.
</div>

<div>
<h4 id='class-aescryptor'>Class AES_Cryptor</h4>
<p>This is the class that used AES 256-bit CTR mode for encryption and decryption of data.This uses PyCrypto Module's AES 256 CTR Class to perform AES encryption/decryption.This class is default for all cryptographic requirements in the module.</p>

<h5 id='aescryptor-get-random-key'>get_random_key()</h5>
<p>This method is used to get the keys required for encryption and decryption.This generates a 32 bytes (256 bit) long string that can be used for AES-CTR encryption/decryption.</p>
Params : None
Returns : {String} A key that can be given to encrypt and decrypt methods.

<h5 id='aescryptor-encrypt'>encrypt(key,value_str,**kwargs)</h5>
<p>This method is used for encrypting the data using AES-CTR mode.The Keyword argument init_val is used as initialization value for the counter required for CTR.</p>
Params:
<ul>
    <li>key {string} : The key obtained from getRandomKey Method.</li>
    <li>encStr {String} : The data that is to be encrypted in string format</li>
    <li>**kwargs {Number} : init_val is required keyword arg og type Number used as initialization value for AES CTR counter.</li>
</ul>
Returns : {String} The encrypted form of the given string.

<h5 id = 'aescryptor-decrypt'>decrypt(key,enc_str,**kwargs)</h5>
<p>This method is used for decrypting the data using AES-CTR mode.The keyword arg init_val is used as initialization value for the counter required for CTR.</p>
Params:
<ul>
    <li>key {string} : The key obtained from getRandomKey Method.</li>
    <li>encStr {String} : The encrypted string that is to be decrypted</li>
    <li>**kwargs {Number} : init_val is required keyword arg og type Number used as initialization value for AES CTR counter.</li>
</ul>
Returns : {String} The decrypted form of the given string.
</div>

<h3 id='kdc-header'>Kerberos KDC Classes</h3>
<p>These are classes that contain methods useful on Key Distribution Center.</p>

<div>
<h4 id='class-kerberos-as'>Class Kerberos_AS</h4>
<p>This Class contains methods useful for Authentication Service of Kerberos.</p>

<h5 id = 'kerberos-as-constructor'>constructor(cryptor, tgs, check_rand = False, verify_rand_db = None)</h5>
<p>Constructor for the Kerberos_AS class</p>
Params :
<ul>
    <li>cryptor {Cryptor} : An instance of a cryptographic class used for encryption and decryption. Must extend the Cryptor class</li>
    <li>tgs : {Kerberos_TGS} : An instance of Kerberos_TGS class. This is used for generating ticket granting ticket</li>
    <li>check_rand {Boolean} : Enables the verify_random Method to prevent replay attacks.The verify_rand_db is used to store user-to-used-numbers connections.Defaults to false if not provided.</li>
    <li>verify_rand_db {DB} : DB used to store mapping of user to used numbers.Defaults to Memory_DB if not provided.</li>
</ul>
Returns : {Object} An instance of Kerberos_AS class.

<h5 id ='kerberos-as-make-auth-tickets'>make_auth_tickets(rand,c_uid1,c_uid2,user_hash,lifetime_ms = AUTH_TICKET_LIFETIME)</h5>
<p>Used to generate authentication tickets <strong>after</strong> verifying user.</p>
<p><strong>Note : this does not performs any authentication of the user. This is supposed to be called after the user is verified for existence.</strong></p>
Params :
<ul>
    <li>rand {Number} : the random number sent by the user in the request</li>
    <li>c_uid1 {string/Number} : An identifier unique to the user.This is verified with the uid inside the ticket to check if user is the valid holder. Eg: username,ip address etc.</li>
    <li>c_uid2 {string/Number} : An identifier unique to the user.This is verified with the uid inside the ticket to check if user is the valid holder. Eg: username,ip address etc.</li>
    <li>user_hash {string} : A key generated by some field that is specific to a particular user such as password etc.Must be 32 bytes long (256 bit).Used for encryption of the response.Must be exactly same as that generated on client side.</li>
    <li>lifetime_ms {Number} : Lifetime of Authentication and Ticket Granting Ticket in milliseconds. defaults to AUTH_TICKET_LIFETIME if not provided.</li>
</ul>
Returns : {Tuple} 
<p>A Tuple whose 0<sup>th</sup> position is response meant for user encrypted by user_hash and 1<sup>st</sup> position is encrypted Ticket Granting Ticket for TGS in auth and tgt fields respectively.The auth object contains both UIDs,timestamp, the random number,lifetime and a key that is supposed to be used by client for encrypting the request to TGS.</p>

<h4 id='class-kerberos-tgs'>Class Kerberos_TGS</h3>
<p>This class contains method useful for Ticket Granting Service of Kerberos.</p>

<h5 id='kerberos-tgs-constructor'>constructor(cryptor, db, check_rand = False, verify_rand_db = None</h5>
<p>Constructor for class Kerberos_TGS</p>
Params:
<ul>
    <li>cryptor {Cryptor} : An instance of a cryptographic class used for encryption and decryption. Must extend the Cryptor class</li>
    <li>db {DB} : Instance of a class extending DB class.This is used for saving the Server structures generated by add_server()</li>
    <li>check_rand {Boolean} : Enables the verifyRandom Method to prevent replay attacks.The verify_rand_db is used to store user-to-used-numbers connections.Defaults to false if not provided.</li>
    <li>verify_rand_db {DB} : DB used to store mapping of user to used numbers.Defaults to MemoryDB if not provided.</li>
</ul>
Returns : {Object} An instance of class Kerberos_TGS.

<h5 id='kerberos-tgs-add-server'>add_server(s_uid)</h5>
<p>Method to generate a server structure fo specified sUid (name)</p>
Params:
<ul>
    <li>s_uid : An unique identifier for that server.This will be used as the key to save the generated structure in serverDB</li>
</ul>
Returns : {void}

<h5 id='kerberos-tgs-get-tgt'>get_tgt(c_uid1, c_uid2, key, lifetime_ms)</h5>
<p>Method for generating a new Ticket Granting Ticket.</p>
Params:
<ul>
    <li>c_uid1 {string/Number} : An identifier unique to the user.This is verified with the uid inside the ticket to check if user is the valid holder. Eg: username,ip address etc.</li>
    <li>c_uid2 {string/Number} : An identifier unique to the user.This is verified with the uid inside the ticket to check if user is the valid holder. Eg: username,ip address etc.</li>
    <li>Key : {String} A key to encrypt the TGT with.This is usually generated by a field specific to a particular user such as password etc.Must be 32 bytes long (256 bit).Used for encryption of the response.Must be exactly same as that generated on client side.</li>
    <li>lifetime_ms {Number} : Lifetime for the generated Ticket Granting Ticket in milliseconds.</li>
</ul>

<h5 id='kerberos-tgs-decrypt-tgt'>decrypt_tgt(enc_tgt_str)</h5>
<p><strong>NOTE : This is an internal method that should not be used from outside</strong></p>
<p>A method to decrypt TGT. This does not verify if the TGT is valid.</p>
Params:
<ul>
    <li>enc_tgt_str {string} : encrypted TGT string.</li>
</ul>
Returns : {dict} dict obtained from parsing JSON string of the TGT.

<h5 id='kerberos-tgs-verify-tgt-and-get-key'>verify_tgt_and_get_key(c_uid1, c_uid2, tgt_enc_str)</h4>
<p><strong>NOTE : This is an internal method that should not be used from outside</strong></p>
<p>Method to verify the TGT and get the secrete key used to decrypt the client's request.</p>
Params:
<ul>
    <li>c_uid1 {string/Number} : An identifier unique to the user.This is verified with the uid inside the ticket to check if user is the valid holder. Eg: username,ip address etc.</li>
    <li>c_uid2 {string/Number} : An identifier unique to the user.This is verified with the uid inside the ticket to check if user is the valid holder. Eg: username,ip address etc.</li>
    <li>tgt_enc_str {string} : Encrypted TGT user sent with request.</li>
</ul>
Returns : {String/Number} The secrete key inside TGT used to decrypt client's request.<br />
Throws : {Server_Error} if the TGT is not valid.

<h5 id='kerberos-tgs-decrypt-req'>decrypt_req(enc_req_str, tgt)</h5>
<p>Method used to decrypt encrypted request sent to TGS.This method does not verify if the TGT is valid or not.</p>
Params:
<ul>
    <li>enc_req_str {String} : Encrypted request string.</li>
    <li>tgt {String} : the encrypted TGT client sent with request.</li>
</ul>
Returns : {String} The decrypted request string.

<h5 id='kerberos-tgs-verify-rand'>verify_rand(rand,c_uid1, c_uid2)</h5>
<p>This method is used to verify that the random number sent by user is used for the first time and prevent replay attacks.</p>
Params:
<ul>
    <li>rand {Number} : the random number sent by the user.</li>
    <li>c_uid1 {string/Number} : An identifier unique to the user.This is verified with the uid inside the ticket to check if user is the valid holder. Eg: username,ip address etc.</li>
    <li>c_uid2 {string/Number} : An identifier unique to the user.This is verified with the uid inside the ticket to check if user is the valid holder. Eg: username,ip address etc.</li>
</ul>
Returns : {void} nothing is the random number is used for the first time by the user.<br />
Throws : {Server_Error} is the random number was already used by the user.

<h5 id='kerberos-tgs-get-res-and-ticket'>get_res_and_ticket(rand,req_server,c_uid1,c_uid2,tgt,lifetime_ms = TICKET_LIFETIME)</h5>
<p>Method to generate response and Ticket for a particular server.</p>
Params :
<ul>
    <li>rand {Number} : the random number sent by the user.</li>
    <li>req-server {string} : server for which the ticket is to be generated.This must be same as given in add_server.This fetches information of server from serverDB.</li>
    <li>c_uid1 {string/Number} : An identifier unique to the user.This is verified with the uid inside the ticket to check if user is the valid holder. Eg: username,ip address etc.</li>
    <li>c_uid2 {string/Number} : An identifier unique to the user.This is verified with the uid inside the ticket to check if user is the valid holder. Eg: username,ip address etc.</li>
    <li>tgt {string} : the Ticket Granting ticket that is sent with the request.This will be verified before generating ticket and response.</li>
    <li>lifetime_mS {Number} : Lifetime of generated ticket in milliseconds. defaults to TICKET_LIFETIME if not provided.</li>
</ul>
Returns : {Tuple} if successful
<p>A Tuple that contains response meant for user encrypted by key in tgt at 0<sup>th</sup> position and encrypted Ticket for Server at 1<sup>st</sup> position.The res object contains timestamp, the random number,lifetime and a key that is supposed to be used by client for encrypting the request to TGS and initialization vale for encryption. </p>
Throws : {Server_Error} if the tgt is not valid.

<h4 id='class-kerberos-kdc'>Class Kerberos_KDC</h4>
<p>An interface class that provides an easier interface for both Authentication ans Ticket Granting Services.This provides exactly same methods provided by Kerberos_AS and Kerberos_TGS class, but can be used instead of maintaining instances of each of them, if the AS and TGS are in the same program.</p>

<h5 id='kerberos-kdc-constructor'>constructor(cryptor = None,server_db = None,check_rand = False,verify_rand_db = None)</h5>
<p>Constructor for Kerberos_KDC class</p>
Params :
<ul>
    <li>cryptor {Cryptor} : Instance of a class extending Cryptor.Defaults to AESCryptor if not provided.</li>
    <li>serverDB {DB} : Instance of a class extending DB class.This is used for saving the Server structures generated by add_server()</li>
    <li>check_rand {Boolean} : Enables the verifyRandom Method to prevent replay attacks.The verify_rand_db is used to store user-to-used-numbers connections.Defaults to false if not provided.</li>
    <li>verify_rand_db {DB} : DB used to store mapping of user to used numbers.Defaults to Memory_DB if not provided.</li>
</ul>
Returns : {Object} An instance of Kerberos_KDC class.

<h5 id='kerberos-kdc-make-auth-tickets'>make_auth_tickets(rand,c_uid1,c_uid2,user_hash,lifetime_ms = AUTH_TICKET_LIFETIME)</h5>
<p>Method to generate initial authentication response and Ticket Granting Ticket.</p>
<ul>
    <li>rand {Number} : the random number sent by the user in the request</li>
    <li>c_uid1 {string/Number} : An identifier unique to the user.This is verified with the uid inside the ticket to check if user is the valid holder. Eg: username,ip address etc.</li>
    <li>c_uid2 {string/Number} : An identifier unique to the user.This is verified with the uid inside the ticket to check if user is the valid holder. Eg: username,ip address etc.</li>
    <li>user_hash {string} : A key generated by some field that is specific to a particular user such as password etc.Must be 32 bytes long (256 bit).Used for encryption of the response.Must be exactly same as that generated on client side.</li>
    <li>lifetime_ms {Number} : Lifetime of Authentication and Ticket Granting Ticket in milliseconds. defaults to AUTH_TICKET_LIFETIME if not provided.</li>
</ul>
Returns : {Tuple} 
<p>A Tuple whose 0<sup>th</sup> position is response meant for user encrypted by user_hash and 1<sup>st</sup> position is encrypted Ticket Granting Ticket for TGS in auth and tgt fields respectively.The auth object contains both UIDs,timestamp, the random number,lifetime and a key that is supposed to be used by client for encrypting the request to TGS.</p>

<h5 id='kerberos-kdc-add-server'>add_server(s_uid)</h5>
<p>Method to generate a server structure fo specified sUid (name)</p>
Params:
<ul>
    <li>s_uid : An unique identifier for that server.This will be used as the key to save the generated structure in serverDB</li>
</ul>
Returns : {void}

<h5 id='kerberos-kdc-get-res-and-ticket'>get_res_and_ticket(rand,req_server,c_uid1,c_uid2,tgt,lifetime_ms = TICKET_LIFETIME)</h5>
<p>Method to generate response and Ticket for a particular server.</p>
Params :
<ul>
    <li>rand {Number} : the random number sent by the user.</li>
    <li>req_server {string} : server for which the ticket is to be generated.This must be same as given in add_server.This fetches information of server from serverDB.</li>
    <li>c_uid1 {string/Number} : An identifier unique to the user.This is verified with the uid inside the ticket to check if user is the valid holder. Eg: username,ip address etc.</li>
    <li>c_uid2 {string/Number} : An identifier unique to the user.This is verified with the uid inside the ticket to check if user is the valid holder. Eg: username,ip address etc.</li>
    <li>tgt {string} : the Ticket Granting ticket that is sent with the request.This will be verified before generating ticket and response.</li>
    <li>lifetime_ms {Number} : Lifetime of generated ticket in milliseconds. defaults to TICKET_LIFETIME if not provided.</li>
</ul>
Returns : {Tuple} if successful
<p>A Tuple that contains response meant for user encrypted by key in tgt at 0<sup>th</sup> position and encrypted Ticket for Server at 1<sup>st</sup> position.The res object contains timestamp, the random number,lifetime and a key that is supposed to be used by client for encrypting the request to TGS and initialization vale for encryption. </p>
Throws : {Server_Error} if the tgt is not valid.

<h5 id='kerberos-kdc-decrypt-req'>decrypt_req(enc_req_str, tgt)</h5>
<p>Method for decrypting the request sent to KDC</p>
Params :
<ul>
    <li>enc_req_str {string} : Encrypted request string sent by client</li>
    <li>tgt {string} : the Ticket Granting ticket that is sent with the request.This will be verified before generating ticket and response.</li>
</ul>

Returns : {String} decrypted request string.

<h5 id='kerberos-kdc-verify-rand'>verify_rand(rand,c_uid1, c_uid2)</h5>
<p>This method is used to verify that the random number sent by user is used for the first time and prevent replay attacks.</p>
Params:
<ul>
    <li>rand {Number} : the random number sent by the user.</li>
    <li>c_uid1 {string/Number} : An identifier unique to the user.This is verified with the uid inside the ticket to check if user is the valid holder. Eg: username,ip address etc.</li>
    <li>c_uid2 {string/Number} : An identifier unique to the user.This is verified with the uid inside the ticket to check if user is the valid holder. Eg: username,ip address etc.</li>
</ul>
Returns : {void} nothing is the random number is used for the first time by the user.<br />
Throws : {Server_Error} is the random number was already used by the user.

</div>

<h3 id='class-server'>Kerberos Server</h3>
<div>
<h4>Class Server</h4>
<p><strong>NOTE : This does not actually creates any kind of server, just contains methods that are useful on the server.</strong></p>
<p>This defines a class that contain methods which are useful on a sever that is to be protected by Kerberos authentication methods.</p>

<h5 id='server-make-server-from-db'>Static make_server_from_db(name,cryptor = None,db = None,check_rand = False,verify_rand_db = None)</h5>
<p>This is the static method that can be used to construct an instance of the Server class from the db, where the ticket generated by TGS is stored.</p>
Params:
<ul>
    <li>name {string} : name of the server that is to be made.This is used as the key to find the server structure in DB.</li>
    <li>cryptor {Cryptor} : Instance of a class extending Cryptor.Defaults to AESCryptor if not provided.</li>
    <li>db {DB} : Instance of a class extending DB class.This must be able to retrieve the server structure generated by TGS.Defaults to LocalDB is not provided.</li>
    <li>check_rand {Boolean} : Enables the verifyRandom Method to prevent replay attacks.The verify_rand_db is used to store user-to-used-numbers connections.Defaults to false if not provided.</li>
    <li>verify_rand_db {DB} : DB used to store mapping of user to used numbers.Defaults to MemoryDB if not provided.</li>
</ul>
Returns : {Object} An instance of Server Class.

<h5 id='server-constructor'>constructor(server_dict,cryptor=None,check_rand=False,verify_rand_db=None)</h5>
<p>Constructor of the Server class</p>
Params:
<ul>
    <li>Server_dict {Dict} : A dict containing key,init_val and uid(name) of the server.Should be the structure generated by TGS.Throws TypeError if any of three is missing.</li>
    <li>cryptor {Cryptor} : Instance of a class extending Cryptor.Defaults to AESCryptor if not provided.</li>
    <li>check_rand {Boolean} : Enables the verifyRand Method to prevent replay attacks.The verify_rand_db is used to store user-to-used-numbers connections.Defaults to false if not provided.</li>
    <li>verify_rand_db {DB} : DB used to store mapping of user to used numbers.Defaults to MemoryDB if not provided.</li>
</ul>
Returns : {Object} An instance of Server Class.

<h5 id='server-decrypt-ticket'>decrypt_ticket(ticket_enc_str)</h5>
<p><strong>NOTE : This is an internal method that should not be used from outside</strong></p>
<p>A method to decrypt Ticket. This does not verify if the ticket is valid.</p>
Params :
<ul>
    <li>ticket_enc_str {String} : encrypted ticket string</li>
</ul>
Returns : {Dict} this returns the decrypted JSON object of ticket.

<h5 id ='server-verify-ticket-and-get-key'>verify_ticket_and_get_key(c_uid1,c_uid2,ticket_enc_str)</h5>
<p>Method used to verify the ticket received and get the secrete key in the ticket</p>
Params:
<ul>
    <li>c_uid1 {string/Number} : An identifier unique to the user.This is verified with the uid inside the ticket to check if user is the valid holder. Eg: username,ip address etc.</li>
    <li>c_uid2 {string/Number} : An identifier unique to the user.This is verified with the uid inside the ticket to check if user is the valid holder. Eg: username,ip address etc.</li>
    <li>ticket_enc_str {String} : The encrypted ticket that is sent with the request.</i>
</ul>
Returns : {String/Number} The secrete key inside the ticket that is used to decrypt the request of user.

<h5 id='server-decrypt-req'>decrypt_req(enc_req_str,ticket)</h5>
<p>Method used to decrypt the request of user.</p>
<p><strong>NOTE : this does not verify if the user is valid holder of ticket, or the ticket is valid or not. This just decrypts the request.</strong></p>
<p>THe reason behind keeping this method is that it is not necessary to send just an encrypted object as a request. The request itself can be another encrypted string or so,which is then again encrypted with key in ticket.Server can use this to decrypt it and obtained the string inside, which can be further decrypted if required.</p>
Params :
<ul>
    <li>enc_req_str {String} : encrypted request string</li>
    <li>ticket {String} : the encrypted ticket that was given by TGS.</li>
</ul>
Returns : {String} this returns the decrypted request.

<h5 id='server-encrypt-res'>encrypt_res(c_uid1,c_uid2,response,ticket)</h5>
<p>This method can be used to encrypt the response that is to be sent back.This verifies the ticket first and then encrypts the stringified response.</p>
Params:
<ul>
    <li>c_uid1 {string/Number} : An identifier unique to the user.This is verified with the uid inside the ticket to check if user is the valid holder. Eg: username,ip address etc.</li>
    <li>c_uid2 {string/Number} : An identifier unique to the user.This is verified with the uid inside the ticket to check if user is the valid holder. Eg: username,ip address etc.</li>
    <li>response {Any} : This is stringified using the json module and then ecrypted with the secrete key in ticket.</li>
    <li>ticket {String} : the encrypted ticket that was given by TGS.</li>
</ul>
Return : {String} Encrypted string form of the response.

<h5 id='server-verify-rand'>verify_rand(rand,c_uid1,c_uid2)</h5>
<p>This method is used to verify that the random number sent by user is used for the first time and prevent replay attacks.</p>
Params:
<ul>
    <li>rand {Number} : the random number sent by the user.</li>
    <li>c_uid1 {string/Number} : An identifier unique to the user.This is verified with the uid inside the ticket to check if user is the valid holder. Eg: username,ip address etc.</li>
    <li>c_uid2 {string/Number} : An identifier unique to the user.This is verified with the uid inside the ticket to check if user is the valid holder. Eg: username,ip address etc.</li>
</ul>
Returns : {void} nothing is the random number is used for the first time by the user.<br />
Throws : {Server_Error} is the random number was already used by the user.
</div>

<h3 id='class-client'>Kerberos Client</h3>
<div>
<h4>Class Client</h4>
<p><strong>NOTE : This does not actually creates any kind of client, just contains methods that are useful on the client.</strong></p>
<p>This defines a class that contain methods which are useful on a client that accesses the servers protected by kerberos methods.</p>

<h5 id='client-constructor'>constructor(cryptor = None, keymap_db = None)</h5>
<p>Constructor for the class</p>
Params:
<ul>
    <li>cryptor {Cryptor} : Instance of a class extending Cryptor.Defaults to AESCryptor if not provided.</li>
    <li>keymap_db {DB} : Instance of a class extending DB class.Used to save and retrieve tickets in save_ticket() and get_ticket() methods. Defaults to Memory_DB if not given</li>
</ul>
Returns : {Object} an instance of Client class.

<h5 id='client-encrypt-req'>encrypt_req(key,req,init_val = TGT_INIT_VAL)</h4>
<p>Method for encrypting the request that is to be sent to server.</p>
Params :
<ul>
    <li>key {string} : key that is to be used for encryption.This can be the user key that is generated from password or so, or the key that is returned from the TGS in its response.</li>
    <li>req {Any} : request that is to be encrypted.It it first stringified using JSON module and then that string is encrypted.</li>
    <li>init_val {Number} : initialization value for the AES CTR mode Counter.This defaults to TGT_INIT_VAL from constants if not specified. This should the one received along with the key in TGS response.</li>
</ul>
Returns : {String} encrypted string of the req.

<h5 id='client-decrypt-req'>decrypt_res(key,res_enc_str,init_val = TGT_INIT_VAL)</h5>
<p>Method used for decrypting the responses received from servers.</p> 
Params:
<ul>
    <li>key {string} : key that is to be used for encryption.This can be the user key that is generated from password or so, or the key that is returned from the TGS in its response.</li>
    <li>res_enc_str {string} : encrypted response string received from server in response.</li>
    <li>init_val {Number} : initialization value for the AES CTR mode Counter.This defaults to TGT_INIT_VAL from constants if not specified. This should the one received along with the key in TGS response.</li>
</ul>
Returns : {string} decrypted JSON parsed format of the response. if the response is simple string, it wil return string and so on as per the json module loads method.

<h5 id='client-save-ticket'>save_ticket(name, ticket)</h5>
<p>Helper method to save the ticket in the keymapDB given in constructor.Can be used to keep all tickets in one place.</p>
Params:
<ul>
    <li>name {string} : key to save the ticket with.should be used when retrieving the ticket.</li>
    <li>Ticket {Any} : ticket to be saved. This can be the encrypted string received from TGS, or the decrypted response object received from TGS.</li>
</ul>
Returns : {void}

<h5 id='client-get-ticket'>get_ticket(name)</h5>
<p>Helper method to retrieve tickets saved with save_ticket() method.</p>
Params:
<ul>
    <li>name {string} : the key with which the ticket was saved.</li>
</ul> 
Returns : {Any} the data that was given to store corresponding to the key.
</div>
