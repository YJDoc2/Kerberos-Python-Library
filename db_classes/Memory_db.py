from .DB import DB
from ..ServerError import ServerError
class Memory_DB(DB):

    def __init__(self):
        self.data = dict()



    def save(self,name,struct):
        self.data[name] = struct

    def get(self,name):
        return self.data.get(name,None)
        

