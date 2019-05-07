from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_login import LoginManager
from flask_admin import Admin
from flask_restful import Api

from config import Config
from admin import Controller, UserModelView, TeamModelView

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

admin = Admin(app)

from app import routes, models

@login.user_loader
def load_user(id):
	return models.User.query.get(id)

admin.add_view(UserModelView(models.User, db.session))
admin.add_view(TeamModelView(models.Team, db.session))
admin.add_view(Controller(models.Player, db.session))

# Api End Points for Teams and Team Players
api = Api(app)
api.add_resource(routes.GetTeams, '/teams', '/teams/<int:teamid>')
api.add_resource(routes.GetTeamPlayers, '/teams/<teamid>/players', '/teams/<teamid>/players/<playerid>')