class User:

    def password_to_key(self):
        raise NotImplementedError("Class extending User class must Implement get_password method")