import os
import json
import requests
from sqlalchemy import create_engine

from app import app,db
from app.models import User, Team, Player
from utilities import Common


TEST_DB = 'test.db'
BASEDIR = os.path.abspath(os.path.dirname(__file__))
IMAGE = 'https://www.gravatar.com/avatar/asasdfasdfasdoie5f35?d=identicon&s=64'

class DBModelsAPITests(Common):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASEDIR, TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_model(self):
        user = User(username='kk', email='kk@gmail.com', isadmin=True)
        user.password_hash = user.get_password_hash('kk')
        db.session.add(user)
        db.session.commit()
        users = db.session.query(User).all()
        self.assertEquals(len(users),1)

    def test_Team_model(self):
        team = Team(name='cricket', logouri=IMAGE)
        db.session.add(team)
        db.session.commit()
        teams = db.session.query(Team).all()
        self.assertEquals(len(teams),1)

    def test_Player_model(self):
        team = Team(name='cricket', logouri=IMAGE)
        db.session.add(team)
        team = db.session.query(Team).first()
        player = Player(firstname='dhoni', lastname='m', imageuri=IMAGE, team_id=team.id)
        db.session.add(player)
        db.session.commit()
        players = db.session.query(Player).all()
        self.assertEquals(len(players),1)

    def test_show_teams_api(self):
        team = Team(name='cricket', logouri=IMAGE)
        db.session.add(team)
        db.session.commit()
        url = 'http://localhost:5000/teams'
        teams = self.app.get(url).data
        teams = json.loads(teams)['teams']
        self.assertEquals(len(teams),1)
        self.assertEquals(teams[0]['name'], 'cricket')

    def test_show_players_api(self):
        team = Team(name='cricket', logouri=IMAGE)
        db.session.add(team)
        team = db.session.query(Team).first()
        player = Player(firstname='dhoni', lastname='m', imageuri=IMAGE, team_id=team.id)
        db.session.add(player)
        db.session.commit()
        url = 'http://localhost:5000/teams/' + str(team.id) + '/players'
        players = self.app.get(url).data
        players = json.loads(players)['players']
        self.assertEquals(len(players),1)
        self.assertEquals(players[0]['firstname'], 'dhoni')
