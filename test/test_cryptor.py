from .. import AES_Cryptor
import json
#? AES Cryptor tests

#* should give a different random key each time
def test_random_key():
    aes_cryptor = AES_Cryptor()
    key1 = aes_cryptor.get_random_key()
    key2 = aes_cryptor.get_random_key()
    assert(isinstance(key1,str))
    assert(isinstance(key2,str))
    assert(key1 != key2)

#* should give key of length 32 bytes
def test_key_length():
    aes_cryptor = AES_Cryptor()
    key = aes_cryptor.get_random_key()
    assert(len(key) == 32)


#* should encrypt and decrypt
def test_encypt_decrypt():
    aes_cryptor = AES_Cryptor()
    data = json.dumps({'test':'test'})
    key = aes_cryptor.get_random_key()
    enc = aes_cryptor.encrypt(key,data,init_val=0)
    dec = aes_cryptor.decrypt(key,enc,init_val=0)
    assert(dec == dec)


