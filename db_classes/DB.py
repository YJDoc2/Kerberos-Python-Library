"""DB class 
    Intended to be base interface class for all databases required in library.
    All Custom databases must extend this class and implement methods save and get
"""
class DB:    
    def save(self,name,struct):
        raise NotImplementedError("Class extending DB class must Implement save method")

    def get(self,name):
        raise NotImplementedError("Class extending DB class must Implement get method")
