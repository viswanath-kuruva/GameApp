import unittest

class Common(unittest.TestCase):

    def register(self, username, email, password, confirm, isadmin):
        return self.app.post(
            '/register',
            data=dict(username=username,
                      email=email,
                      password=password,
                      password2=confirm,
                      isadmin=isadmin),
            follow_redirects=True
        )

    def login(self, username, password):
        return self.app.post(
            '/login',
            data=dict(username=username, password=password),
            follow_redirects=True
        )

    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        ) 
