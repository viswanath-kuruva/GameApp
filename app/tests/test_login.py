import os

from app import app, db
from utilities import Common
 
TEST_DB = 'test.db'
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class UserTests(Common):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASEDIR, TEST_DB)
        self.app = app.test_client()
        db.create_all()
  
    # executed after each test
    def tearDown(self):
        db.drop_all()

    # tests 
    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        response = self.register('kk', 'kk@gmail.com', 'kk', 'kk', True)
        self.assertEqual(response.status_code, 200)
        response = self.login('kk', 'kk')
        self.assertEqual(response.status_code, 200)
        self.assertIn('logout', response.data)

    def test_logout_success(self):
        response = self.register('kk', 'kk@gmail.com', 'kk', 'kk', True)
        self.assertEqual(response.status_code, 200)
        response = self.login('kk', 'kk')
        self.assertEqual(response.status_code, 200)
        self.assertIn('logout', response.data)
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn('login', response.data)

if __name__ == "__main__":
    unittest.main()