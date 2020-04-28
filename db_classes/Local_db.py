import os
import json
from .DB import DB
from ..ServerError import ServerError
'''Local_DB class used as defualt DB for saving tickets and server data tickets
    This creates a folder  on given path or else creates a folder called 'Tickets',
    in directory from which the process calling was invoked.
    This saves and loads data in plain text format, using json module to convert object to string, and string to object.
    All saved object files are named as given name.
'''
class Local_DB(DB):

    def __init__(self,ticket_folder_path=None):
        
        # If no ticket path is provided, defualt to Tickets in directory from which process calling this was invoked
        if ticket_folder_path == None:
            ticket_folder_path = os.path.join(os.getcwd(),'Tickets')

        if not os.path.isdir(ticket_folder_path):
            os.makedirs(ticket_folder_path)

        self.ticket_path = ticket_folder_path



    def save(self,server_name,server_struct):
        """saves given server_struct after converting to string using json.dumps

        Arguments:
            server_name {String} -- name the structure will saved by
            server_struct {Dictionary} -- object to save

        
        For default ticketPath, Servername = 'A' will create a text file at path './Tickets/A'
     
        """        
        path = os.path.join(self.ticket_path,server_name)

        with open(path,mode="w") as f:
            f.write(json.dumps(server_struct))

    def get(self,server_name):
        """Retrives saved data

        Arguments:
            server_name {String} -- name with which the object was saved

        Raises:
            ServerError: if file with given server_name is not found
            ServerError: if the file found was empty
            ServerError: if cannot convert data stored in file to a dictionary

        Returns:
            [type] -- [description]
        """        
        path=os.path.join(self.ticket_path,server_name)

        if not os.path.exists(path):
            raise ServerError(f"Requested Server with name {server_name} not Found")
        
        ticket_string = ''
        with open(path,mode='r') as f:
            ticket_string = f.read()

        if ticket_string == '':
            raise ServerError(f"Requested Server with name {server_name} not Found")
        
        try:
            return json.loads(ticket_string)
        except :
            raise ServerError("Error in decoding server information")
        

