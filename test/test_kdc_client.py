import json
import random
import time
from .. import Server,Kerberos_TGS,Client,AES_Cryptor,Memory_DB,Kerberos_KDC,ServerError
import pytest

#! Tests for KDC,CLient

kdc = mdb = server = client = key = None

def before_each():
    global kdc,mdb,server,client,key
    mdb = Memory_DB()
    cryptor = AES_Cryptor()
    kdc = Kerberos_KDC(server_db=mdb)
    kdc.add_server('abc')
    server = Server.make_server_from_db('abc',db=mdb)
    key = cryptor.get_random_key()
    client = Client(key)

#* kdc should make correct auth ticket and client dhould decrypt them
def test_auth_tickets():
    before_each()
    global kdc,mdb,server,client,key
    rand = random.randint(0,5000)
    (auth,tgt) = kdc.gen_auth_tickets(rand,'t1','test',key,8500)
    try:
        client.decrypt_res(auth,key)
    except:
        pytest.fail("Client should have decrypted auth ticket")
    dec_auth = client.decrypt_res(auth,key)
    assert(dec_auth['uid1'] == 't1')
    assert(dec_auth['uid2'] == 'test')
    assert(dec_auth['rand'] == rand)
    assert(dec_auth['key'] != None)
    assert(dec_auth['target'] == 'TGS')
    assert(dec_auth['lifetime'] == 8500)
    assert(dec_auth['timestamp'] <= int(time.time()*1000))

#* kdc should make correct ticket granting ticket
def test_TGT():
    before_each()
    global kdc,mdb,server,client,key
    rand = random.randint(0,5000)
    (auth,tgt) = kdc.gen_auth_tickets(rand,'t1','test',key,8500)
    tgs = Kerberos_TGS(AES_Cryptor(),mdb)
    try:
        tgs.decrypt_tgt(tgt)
    except:
        pytest.fail("TGS should have decrypted TGT")

    dec_tgt = tgs.decrypt_tgt(tgt)
    assert(dec_tgt['uid1'] == 't1')
    assert(dec_tgt['uid2'] == 'test')
    assert(dec_tgt['key'] != None)
    assert(dec_tgt['target'] == 'TGS')
    assert(dec_tgt['lifetime'] == 8500)
    assert(dec_tgt['timestamp'] <= int(time.time()*1000))


#* kdc should return a valid response for ticket request and client should decrypt it

def test_kdc_response():
    before_each()
    global kdc,mdb,server,client,key
    rand = random.randint(0,5000)
    (auth,tgt) = kdc.gen_auth_tickets(rand,'t1','test',key,8500)
    (res,ticket) = kdc.get_res_and_ticket('t1','test',tgt,'abc',rand,8500)
    key_in = client.decrypt_res(auth,key)['key']
    try:
        client.decrypt_res(res,key_in)
    except:
        pytest.fail("Client should have decrypted the response")
    
    dec_res = client.decrypt_res(res,key_in)
    assert(dec_res['rand'] == rand)
    assert(dec_res['key'] != None)
    assert(dec_res['target'] == 'abc')
    assert(dec_res['lifetime'] == 8500)
    assert(isinstance(dec_res['init_val'],int))
    assert(dec_res['timestamp'] <= int(time.time()*1000))

#* kdc should return a valid ticket 
def test_valid_ticket():
    before_each()
    global kdc,mdb,server,client,key
    rand = random.randint(0,5000)
    (auth,tgt) = kdc.gen_auth_tickets(rand,'t1','test',key,8500)
    (res,ticket) = kdc.get_res_and_ticket('t1','test',tgt,'abc',rand,8500)
    try:
        server.decrypt_ticket(ticket)
    except:
        pytest.fail("Server should have decrypted the ticket")

    dec_t = server.decrypt_ticket(ticket)
    assert(dec_t['uid1'] == 't1')
    assert(dec_t['uid2'] == 'test')
    assert(dec_t['key'] != None)
    assert(dec_t['target'] == 'abc')
    assert(dec_t['lifetime'] == 8500)
    assert(isinstance(dec_t['init_val'],int))
    assert(dec_t['timestamp'] <= int(time.time()*1000))

#* client should encrypt essage and server should be able to decrypt it

def test_client_encrypt_derver_decrypt():
    before_each()
    global kdc,mdb,server,client,key
    rand = random.randint(0,5000)
    (auth,tgt) = kdc.gen_auth_tickets(rand,'t1','test',key,8500)
    (res,ticket) = kdc.get_res_and_ticket('t1','test',tgt,'abc',rand,8500)

    key_in = client.decrypt_res(auth,key)['key']
    key_req = client.decrypt_res(res,key_in)['key']
    init = client.decrypt_res(res,key_in)['init_val']
    data = {'test':'test'}
    req = client.encrypt_req(data,key_req,init)

    try:
        server.decrypt_req(req,ticket)
    except:
        pytest.fail("Server Should have decrypted the request")

    dec_req = server.decrypt_req(req,ticket)
    assert(json.loads(dec_req) == data)

#* client should be able to decrypt server's response

def test_client_decrypt_server_response():
    before_each()
    global kdc,mdb,server,client,key
    rand = random.randint(0,5000)
    (auth,tgt) = kdc.gen_auth_tickets(rand,'t1','test',key,8500)
    (res,ticket) = kdc.get_res_and_ticket('t1','test',tgt,'abc',rand,8500)

    res_data = {'test':'test'}
    try:
        server.encrypt_res('t1','test',ticket,res_data)
    except:
        pytest.fail("Server Should have encrypted the response")

    s_res = server.encrypt_res('t1','test',ticket,res_data)
    key_in = client.decrypt_res(auth,key)['key']
    key_req = client.decrypt_res(res,key_in)['key']
    init = client.decrypt_res(res,key_in)['init_val']

    try:
        client.decrypt_res(s_res,key_req,init)
    except:
        pytest.fail("Server Should have encrypted the response")
    dec_res = client.decrypt_res(s_res,key_req,init)
    assert(dec_res['test'] == 'test')
    



    