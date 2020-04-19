class DB:
    
    def save(self,name,struct):
        raise NotImplementedError("Class extending DB class must Implement save method")

    def get(self,name):
        raise NotImplementedError("Class extending DB class must Implement get method")
