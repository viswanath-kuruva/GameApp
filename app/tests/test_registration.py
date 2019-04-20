import os

from app import app, db
from utilities import Common
 
TEST_DB = 'test.db'
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class RegistrationTests(Common):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASEDIR, TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
    # executed after each test
    def tearDown(self):
        db.drop_all()

    def test_registration(self):
        response = self.register('kk', 'kk@gmail.com', 'kk', 'kk', True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('User Registration Successful.', response.data)

    def test_username_mandatory(self):
        response = self.register('', 'kk@gmail.com', 'kk', 'kk', True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('This field is required.', response.data)

    def test_password_match(self):
        # confirm password does not match
        response = self.register('kk', 'kk@gmail.com', 'kk', 'kkk', True)
        self.assertIn('Field must be equal to password.', response.data)

    def test_username_email_same(self):
        response = self.register('kk', 'kk@gmail.com', 'kk', 'kk', True)
        self.assertEqual(response.status_code, 200)
        # check for same username registration
        response = self.register('kk', 'kk@gmail.com', 'kk', 'kk', True)
        self.assertIn('Username already exists, Kindly use different user name.', response.data)
        # check for same email registration        
        response = self.register('kkk', 'kk@gmail.com', 'kk', 'kk', True)
        self.assertIn('Email already exists, Kindly use different email id.', response.data)

if __name__ == "__main__":
    unittest.main()