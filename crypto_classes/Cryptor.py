class Cryptor:
    

    def encrypt(self,key,value_str,**kwargs):
        raise NotImplementedError("Class extending Cryptor class must Implement encrypt method")

    def decrypt(self,key,enc_str,kwargs):
        raise NotImplementedError("Class extending Cryptor class must Implement decrypt method")
