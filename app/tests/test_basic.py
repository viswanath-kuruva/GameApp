import os
import json

from app import app, db
from utilities import Common
 
TEST_DB = 'test.db'
BASEDIR = os.path.abspath(os.path.dirname(__file__))

ROUTES = ['/', '/index', '/login', '/logout', '/register']

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
        for url in ROUTES:
            response = self.app.get(url, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_get_teams(self):
        response = self.app.get('/teams', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.data)
        self.assertIn('teams', res)

    def test_get_team_players(self):
        response = self.app.get('/teams/111/players', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.data)
        self.assertIn('players', res)


if __name__ == "__main__":
    unittest.main()