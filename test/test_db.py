import os
import shutil
from .. import Memory_DB,Local_DB,ServerError
import pytest

#!MemoryDB Class tests

#* should retrive saved data
def test_save_and_get():
    mdb = Memory_DB()
    mdb.save('test','testData')
    data = mdb.get('test')
    assert(data == 'testData')

#* should give None for absent keys
def test_invalid_keys():
    mdb = Memory_DB()
    data = mdb.get('test')
    assert(data == None)

#! LocalDB class tests

#? Couldn't find easy way to implement before each hook for spceific funtions
def before_each():
    if os.path.isdir('./Tickets'):
        shutil.rmtree('./Tickets')
    if os.path.isdir('./testtickets'):
        shutil.rmtree('./testtickets')


#* should create Tickets folder in current dir by default
def test_create_default_folder():
    before_each()
    ldb = Local_DB()
    assert(os.path.isdir('./Tickets'))
    

#* should create given path dir for tickets
def test_given_ticket_path():
    before_each()
    ldb = Local_DB('./testtickets')
    assert(os.path.isdir('./testtickets'))
    

#* should be able to create nested folder structure
def test_nested_ticket_path():
    before_each()
    ldb = Local_DB('./testtickets/Tickets')
    assert(os.path.isdir('./testtickets/Tickets'))
    

#* should create folder inside existsing folder
def test_nested_ticket_path():
    before_each()
    os.mkdir('./testtickets')
    ldb = Local_DB('./testtickets/Tickets')
    assert(os.path.isdir('./testtickets/Tickets'))
    

#* should save data with given name
def test_save_data():
    before_each()
    ldb = Local_DB()
    ldb.save('test','test')
    assert(os.path.isfile('./Tickets/test'))
    
#* should be able to get saved data
def test_get_data():
    before_each()
    ldb = Local_DB()
    ldb.save('test','test')
    data = ldb.get('test')
    assert(isinstance(data,str))
    assert(data == 'test')

#* should save and retrive objects correctly
def test_save_objects():
    before_each()
    ldb = Local_DB()
    ldb.save('test',{'test':'test'})
    data = ldb.get('test')
    assert(isinstance(data,object))
    assert(data['test'] =='test' )

#* should throw error for non-existing keys
def test_invalid_key_error():
    before_each()
    ldb = Local_DB()
    with pytest.raises(ServerError) as e:
        ldb.get('test')
    assert str(e.value) == "Requested Server with name test not Found"
        

#* should throw error for incorrectly saved data
def test_invalid_save_error():
    before_each()
    ldb = Local_DB()
    file = open('./Tickets/test','w')
    file.write("'{test:'")
    file.close()
    with pytest.raises(ServerError) as e:
        ldb.get('test')
    assert str(e.value) == "Error in decoding server information"

    