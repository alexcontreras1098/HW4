from flask import Flask
from flask import render_template, redirect, request, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
#import secrets
import os

dbuser = os.environ.get('DBUSER')
dbpass = os.environ.get('DBPASS')
dbhost = os.environ.get('DBHOST')
dbname = os.environ.get('DBNAME')

#conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)
conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(dbuser, dbpass, dbhost, dbname)

app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class acntreras_soccerplayersapp(db.Model):
    #__tablename__ = 'results'
    soccer_playerId = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    clubteam = db.Column(db.String(255))
    nationality = db.Column(db.String(255))

    def __repr__(self):
        return "id: {0} | first name: {1} | last name: {2} | clubteam: {3} | nationality: {4} ".format(self.id, self.first_name, self.last_name, self.clubteam, self.nationality)




class PlayerForm(FlaskForm):
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    clubteam = StringField('Club team:', validators=[DataRequired()])
    nationality = StringField('Nationality:', validators=[DataRequired()])

@app.route('/')
def index():
    all_players = acntreras_soccerplayersapp.query.all()
    return render_template('index.html', players=all_players, pageTitle='Favorite Soccer Players')

@app.route('/player/new', methods=['GET', 'POST'])
def add_player():
    form = PlayerForm()
    if form.validate_on_submit():
        player = acntreras_soccerplayersapp(first_name=form.first_name.data, last_name=form.last_name.data, clubteam=form.clubteam.data, nationality=form.nationality.data)
        db.session.add(player)
        db.session.commit()
        return redirect('/')

    return render_template('add_player.html', form=form, pageTitle='Add A New Player', legend="Add A New Player")

@app.route('/player/<int:soccer_playerId>', methods=['GET','POST'])
def player(soccer_playerId):
    player = acntreras_soccerplayersapp.query.get_or_404(soccer_playerId)
    return render_template('player.html', form=player, pageTitle='Player Details')

@app.route('/friend/<int:friend_id>/update', methods=['GET','POST'])
def update_friend(soccer_playerId):
    player = acntreras_soccerplayersapp.query.get_or_404(friend_id)
    form = PlayerForm()
    if form.validate_on_submit():
        player.first_name = form.first_name.data
        player.last_name = form.last_name.data
        player.clubteam = form.clubteam.data
        player.nationality = form.nationality.data
        db.session.commit()
        flash('Your player has been updated.')
        return redirect(url_for('player', soccer_playerId=friend.soccer_playerId))
    #elif request.method == 'GET':
    form.first_name.data = friend.first_name
    form.last_name.data = friend.last_name
    player.clubteam = form.clubteam.data
    player.nationality = form.nationality.data
    return render_template('add_player.html', form=form, pageTitle='Update Post',
                            legend="Update A player")

@app.route('/player/<int:soccer_playerId>/delete', methods=['POST'])
def delete_player(soccer_playerId):
    if request.method == 'POST': #if it's a POST request, delete the friend from the database
        player = acntreras_soccerplayersapp.query.get_or_404(friend_id)
        db.session.delete(player)
        db.session.commit()
        flash('Player was successfully deleted!')
        return redirect("/")
    else: #if it's a GET request, send them to the home page
        return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
