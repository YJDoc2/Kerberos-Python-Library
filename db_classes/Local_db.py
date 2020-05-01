import os
import json
from .DB import DB
from ..Server_Error import Server_Error
'''Local_DB class used as default DB for saving tickets and server data tickets
    This creates a folder  on given path or else creates a folder called 'Tickets',
    in directory from which the process calling was invoked.
    This saves and loads data in plain text format, using json module to convert object to string, and string to object.
    All saved object files are named as given name.
'''
class Local_DB(DB):

    def __init__(self,ticket_folder_path=None):
        
        # If no ticket path is provided, default to Tickets in directory from which process calling this was invoked
        if ticket_folder_path == None:
            ticket_folder_path = os.path.join(os.getcwd(),'Tickets')

        if not os.path.isdir(ticket_folder_path):
            os.makedirs(ticket_folder_path)

        self.ticket_path = ticket_folder_path



    def save(self,name,data):
        """saves given data after converting to string using json.dumps

        Arguments:
            name {String} -- name the structure will saved by
            data {Any} -- object to save

        
        For default ticketPath, Servername = 'A' will create a text file at path './Tickets/A'
     
        """        
        path = os.path.join(self.ticket_path,name)

        with open(path,mode="w") as f:
            f.write(json.dumps(data))

    def get(self,name):
        """Retrives saved data

        Arguments:
            name {String} -- name with which the object was saved

        Raises:
            Server_Error: if file with given server_name is not found
            Server_Error: if the file found was empty
            Server_Error: if cannot convert data stored in file to a dictionary

        Returns:
            Any -- data associated with given name if present
        """        
        path=os.path.join(self.ticket_path,name)

        if not os.path.exists(path):
            raise Server_Error(f"Requested Server with name {name} not Found")
        
        ticket_string = ''
        with open(path,mode='r') as f:
            ticket_string = f.read()

        if ticket_string == '':
            raise Server_Error(f"Requested Server with name {name} not Found")
        
        try:
            return json.loads(ticket_string)
        except :
            raise Server_Error("Error in decoding server information")
        

