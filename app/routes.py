from flask import render_template, redirect, url_for, request, jsonify, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from flask_restful import Resource
import requests

from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Team

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/displayteams')
def showTeams():
    url = 'http://localhost:5000/teams'
    teams = requests.get(url).json()['teams']
    return render_template('show_teams.html', title='Teams', teams=teams)

@app.route('/teamplayers/<teamid>/<teamname>')
def displayTeamPlayers(teamid, teamname):
    url = 'http://localhost:5000/teams/' + teamid + '/players'
    players = requests.get(url).json()['players']
    return render_template('team_players.html', title='Team Players', teamname=teamname, players=players)

@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
	
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, isadmin=form.isadmin.data)
        user.password_hash = user.get_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User Registration Successful.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

class GetTeams(Resource):
    def get(self, teamid=None):
        teams = db.session.query(Team)
        if(teamid):
            teams = teams.filter_by(id=teamid)
        return jsonify({'teams': [team.serialize for team in teams]})

class GetTeamPlayers(Resource):
    def get(self, teamid, playerid=None):
        players = []
        team = db.session.query(Team).filter_by(id=teamid).first()
        if team:
            players = team.players
            if(playerid):
                players = players.filter_by(id=playerid)
        return jsonify({'players': [player.serialize for player in players]})        
