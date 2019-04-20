from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError

from app.models import User
from app import db

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('email', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('ReEnter Password', validators=[DataRequired(), EqualTo('password')])
	isadmin = BooleanField('Is Admin')
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = db.session.query(User).filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username already exists, Kindly use different user name.')

	def validate_email(self, email):
		user = db.session.query(User).filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Email already exists, Kindly use different email id.')

