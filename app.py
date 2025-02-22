from flask import Flask
from flask import render_template, redirect, request, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import pymysql
import os
import secrets
'''
conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)

app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
db = SQLAlchemy(app)

'''
dbuser = os.environ.get('DBUSER')
dbpass = os.environ.get('DBPASS')
dbhost = os.environ.get('DBHOST')
dbname = os.environ.get('DBNAME')
conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(dbuser, dbpass, dbhost, dbname)

app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
db = SQLAlchemy(app)

class acntreras_soccerplayersapp(db.Model):
    soccer_playerId = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    clubteam = db.Column(db.String(255))
    nationality = db.Column(db.String(255))

    def __repr__(self):
        return "id: {0} | first name: {1} | last name: {2} | clubteam: {3} | nationality: {4}".format(self.id, self.first_name, self.last_name, self.clubteam, self.nationality)

class PlayerForm(FlaskForm):
    soccer_playerId = IntegerField('Soccer Player ID:')
    first_name = StringField('first name:', validators=[DataRequired()])
    last_name = StringField('last name:', validators=[DataRequired()])
    clubteam= StringField('clubteam: ', validators=[DataRequired()])
    nationality= StringField('nationality: ', validators=[DataRequired()])

@app.route('/')
def index():
    all_players = acntreras_soccerplayersapp.query.all()
    return render_template('index.html', players=all_players, pageTitle='Alex\'s Players')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        results = acntreras_soccerplayersapp.query.filter( or_(acntreras_soccerplayersapp.first_name.like(search), acntreras_soccerplayersapp.last_name.like(search), acntreras_soccerplayersapp.clubteam.like(search), acntreras_soccerplayersapp.nationality.like(search))).all()
        return render_template('index.html', players=results, pageTitle='Alex\'s Players', legend ="Update A Player")
    else:
        return redirect('/')

@app.route('/add_player', methods=['GET', 'POST'])
def add_player():
    form = PlayerForm()
    if form.validate_on_submit():
        player = acntreras_soccerplayersapp(first_name=form.first_name.data, last_name=form.last_name.data, clubteam=form.clubteam.data, nationality=form.nationality.data )
        db.session.add(player)
        db.session.commit()
        print('Player was successully added!')
        return redirect('/')

    return render_template('add_player.html', form=form, pageTitle='Add A New Player')
'''
@app.route('/delete_player/<int:soccer_playerId>', methods=['GET','POST'])
def delete_player(soccer_playerId):
    if request.method == 'POST': #if it's a POST request, delete the friend from the database
        obj = acntreras_soccerplayersapp.query.filter_by(soccer_playerId=soccer_playerId).first()
        db.session.delete(obj)
        db.session.commit()
        flash('Player was successfully deleted!')
        return redirect("/")
    else: #if it's a GET request, send them to the home page
        return redirect("/")
'''
@app.route('/player/<int:soccer_playerId>', methods=['GET','POST'])
def get_player(soccer_playerId):
    player = acntreras_soccerplayersapp.query.get_or_404(soccer_playerId)
    return render_template('player.html', form=player, pageTitle='Player Details', legend="Player Details")

@app.route('/player/<int:soccer_playerId>/update', methods=['GET','POST'])
def update_player(soccer_playerId):
    player = acntreras_soccerplayersapp .query.get_or_404(soccer_playerId)
    form = PlayerForm()
    if form.validate_on_submit():
        player.soccer_playerId = form.soccer_playerId.data
        player.first_name = form.first_name.data
        player.last_name = form.last_name.data
        player.clubteam = form.clubteam.data
        player.nationality = form.nationality.data
        db.session.commit()
        return redirect('/')
    #elif request.method == 'GET':
    form.soccer_playerId.data = player.soccer_playerId
    form.first_name.data = player.first_name
    form.last_name.data = player.last_name
    form.clubteam.data = player.clubteam
    form.nationality.data = player.nationality
    return render_template('update_player.html', form=form, pageTitle='Update Post', legend="Update A Player")

@app.route('/player/<int:soccer_playerId>/delete', methods=['POST'])
def delete_player(soccer_playerId):
    if request.method == 'POST': #if it's a POST request, delete the friend from the database
        player = acntreras_soccerplayersapp.query.get_or_404(soccer_playerId)
        db.session.delete(player)
        db.session.commit()
        flash('Player was successfully deleted!')
        return redirect("/")
    else: #if it's a GET request, send them to the home page
        return redirect("/")




if __name__ == '__main__':
    app.run(debug=True)
