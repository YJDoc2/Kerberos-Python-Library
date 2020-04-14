class DB:
    
    def save_server(self,server_name,server_struct):
        raise NotImplementedError("Class extending DB class must Implement save_server method")

    def get_server(self,server_name):
        raise NotImplementedError("Class extending DB class must Implement get_serer method")
