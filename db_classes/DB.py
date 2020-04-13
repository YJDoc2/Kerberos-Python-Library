class DB:
    
    def save_server(self,ticket_name,ticket):
        raise NotImplementedError("Class extending DB class must Implement save_server method")

    def get_server(self,ticket_name):
        raise NotImplementedError("Class extending DB class must Implement get_serer method")
