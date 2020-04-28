import os
import shutil
import random
from .. import Server,Kerberos_TGS,Client,AES_Cryptor,Memory_DB,Local_DB,ServerError
import pytest


#! Basic Server tests

#* should throw error with incomplete details
def test_incomplete_details_error():
    with pytest.raises(ServerError) as e:
        Server({'key':'abc'})
    assert(str(e.value) == "Invalid Server object")

    with pytest.raises(ServerError) as e:
        Server({'uid':'abc'})
    assert(str(e.value) == "Invalid Server object")

    with pytest.raises(ServerError) as e:
        Server({'init_val':125})
    assert(str(e.value) == "Invalid Server object")

#! Pytest for exception not throw not found
#! hack taken from https://stackoverflow.com/questions/20274987/how-to-use-pytest-to-check-that-error-is-not-raised
#* should make server with correct object
def test_valid_server():
    try:
        Server({'uid':'abc','key':'abc','init_val':123})
    except:
        pytest.fail("Server Should Have been created")

#* should make server from db
def test_make_server_from_db():
    mdb = Memory_DB()
    mdb.save('abc',{'uid':'abc','key':'abc','init_val':123})
    try:
        Server.make_server_from_db('abc',db=mdb)
    except:
        pytest.fail("Server Should Have been created")

    ldb = Local_DB()
    ldb.save('abc',{'uid':'abc','key':'abc','init_val':123})
    try:
        Server.make_server_from_db('abc',db=ldb)
    except:
        pytest.fail("Server Should Have been created")

    shutil.rmtree('./Tickets')

#* should throw error for check rand if not enabled
def test_rand_not_enabled_error():
    mdb = Memory_DB()
    mdb.save('abc',{'uid':'abc','key':'abc','init_val':123})
    server = Server.make_server_from_db('abc',db=mdb)
    with pytest.raises(TypeError) as e:
        server.verify_rand(1,2,3)
    assert(str(e.value) == "This instance was not initialized with check_rand = True")


#* should throw error for invalid rand
def test_invalid_rand_error():
    mdb = Memory_DB()
    mdb.save('abc',{'uid':'abc','key':'abc','init_val':123})
    server = Server.make_server_from_db('abc',db=mdb,check_rand=True)
    with pytest.raises(ServerError) as e:
        server.verify_rand('t1','t2',None)
    assert(str(e.value) == "'rand' is not present")

    with pytest.raises(ServerError) as e:
        server.verify_rand('t1','t2',{})
    assert(str(e.value) == "rand must be a number")


#* should verify random
def test_verify_random():
    mdb = Memory_DB()
    mdb.save('abc',{'uid':'abc','key':'abc','init_val':123})
    server = Server.make_server_from_db('abc',db=mdb,check_rand=True)
    rand = random.randint(0,5000)

    try:
        server.verify_rand('t1','t2',rand)
    except:
        pytest.fail("rand should have been accepted")
    try:
        server.verify_rand('t1','t2',random.randint(0,5000))
    except:
        pytest.fail("rand should have been accepted")

    with pytest.raises(ServerError) as e:
        server.verify_rand('t1','t2',rand)

    assert(str(e.value) == "The random number has already been used by the user")

#! req-res tests
mdb = cryptor = tgs = server = None

def before_each():
    global mdb,cryptor,tgs,server
    mdb = Memory_DB()
    cryptor = AES_Cryptor()
    tgs = Kerberos_TGS(cryptor,mdb)
    tgs.add_server('abc')
    tgs.add_server('ccc')
    server = Server.make_server_from_db('abc',db=mdb)


#* should decrypt valid ticket
def test_decrypt_valid():
    before_each()
    global mdb,cryptor,tgs,server
    tgt = tgs.get_tgt('t1','t2',cryptor.get_random_key(),5000)
    (res,ticket) = tgs.get_response_and_ticket('t1','t2',tgt,'abc',50)
    try:
       server.verify_ticket_and_get_key('t1','t2',ticket)
    except:
        pytest.fail("Server Should Have been created")

#* should throw error for invalid ticket
def test_invalid_tickets_error():
    before_each()
    global mdb,cryptor,tgs,server
    tgt = tgs.get_tgt('t1','t2',cryptor.get_random_key(),5000)

    with pytest.raises(ServerError) as e:
        server.verify_ticket_and_get_key('t1','t2','strooo')
    assert(str(e.value) == "Invalid Ticket")
    
    ticket0 = tgs.get_response_and_ticket('t1','t2',tgt,'abc',50,-1)[1]
    with pytest.raises(ServerError) as e:
        server.verify_ticket_and_get_key('t1','t2',ticket0)
    assert(str(e.value) == "Ticket Lifetime Exceeded")
    

    ticket1 = tgs.get_response_and_ticket('t1','t2',tgt,'abc',50)[1]
    with pytest.raises(ServerError) as e:
        server.verify_ticket_and_get_key('t1','t',ticket1)
    assert(str(e.value) == "Invalid Ticket Holder")

    with pytest.raises(ServerError) as e:
        server.verify_ticket_and_get_key('t','t1',ticket1)
    assert(str(e.value) == "Invalid Ticket Holder")

    ticket2 = tgs.get_response_and_ticket('t1','t2',tgt,'ccc',50)[1]
    with pytest.raises(ServerError) as e:
        server.verify_ticket_and_get_key('t1','t',ticket2)
    assert(str(e.value) == "Invalid Ticket")