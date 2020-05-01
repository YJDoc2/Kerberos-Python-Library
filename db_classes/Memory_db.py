from .DB import DB
from ..Server_Error import Server_Error

'''Class Memory_DB 
    used to saves data in memory using map.
    Exists only till program is running.
    Usually would be faster than LocalDB.
    Default choice for saving random numbers used by a user.
'''
class Memory_DB(DB):

    def __init__(self):
        self.data = dict()



    def save(self,name,data):
        self.data[name] = data

    def get(self,name):
        return self.data.get(name,None)
        

