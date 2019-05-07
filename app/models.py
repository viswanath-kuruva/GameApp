from flask_login import UserMixin
from werkzeug import check_password_hash, generate_password_hash

from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), unique=True, nullable=False)
    isadmin = db.Column(db.Boolean)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def get_password_hash(self, password):
    	return generate_password_hash(password)

    def check_password(self, password):
    	return check_password_hash(self.password_hash, password)

class SerializeMixin(object):
    @property
    def serialize(self):
        return {k:v for k,v in vars(self).items() if k[:1]!='_'}

class Team(db.Model, SerializeMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)
    # https://www.gravatar.com/avatar/asasdfasdfasdoie5f35?d=identicon&s=64
    logouri = db.Column(db.String(250), nullable=False)
    players = db.relationship('Player', backref='teamname', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return 'Team : {}'.format(self.name)

class Player(db.Model, SerializeMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(25), unique=True, nullable=False)
    lastname = db.Column(db.String(25), nullable=False)
    imageuri = db.Column(db.String(250), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    # team = db.relationship

    def __repr__(self):
        return '<Player : {}>'.format(self.firstname + self.lastname)