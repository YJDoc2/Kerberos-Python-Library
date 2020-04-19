import os
import json
from .DB import DB
from ..ServerError import ServerError
class Local_db(DB):

    def __init__(self,ticket_folder_path=None):
        if ticket_folder_path == None:
            ticket_folder_path = os.path.join(os.getcwd(),'Tickets')

        if not os.path.isdir(ticket_folder_path):
            os.mkdir(ticket_folder_path)

        self.ticket_path = ticket_folder_path



    def save(self,server_name,server_struct):
        path = os.path.join(self.ticket_path,server_name)

        with open(path,mode="w") as f:
            f.write(json.dumps(server_struct))

    def get(self,server_name):
        path=os.path.join(self.ticket_path,server_name)

        if not os.path.exists(path):
            raise ServerError(f"Cannot Find Requested Server with name {server_name}")
        
        ticket_string = ''
        with open(path,mode='r') as f:
            ticket_string = f.read()

        if ticket_string == '':
            raise ServerError(f"Cannot Find Requested Server with name {server_name}")
        
        try:
            return json.loads(ticket_string)
        except :
            raise ServerError("Error in decoding server information")
        

