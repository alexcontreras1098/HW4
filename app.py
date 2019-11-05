from flask import Flask
from flask import render_template, redirect, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
import secrets

conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)

app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)

class acntreras_soccerplayersapp(db.Model):
    soccer_playerId = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    clubteam = db.Column(db.String(255))
    nationality = db.Column(db.String(255))

    def __repr__(self):
        return "id: {0} | first name: {1} | last name: {2} | club team: {4} | nationality: {5}".format(self.id, self.first_name, self.last_name, self.clubteam, self.nationality)

class SoccerplayerForm(FlaskForm):
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    clubteam = StringField('Last Name:', validators=[DataRequired()])
    nationality = StringField('Last Name:', validators=[DataRequired()])


@app.route('/')
def index():
    all_players = acntreras_soccerplayersapp.query.all()
    return render_template('index.html', friends=all_friends, pageTitle='Best Soccer Player')

@app.route('/add_players', methods=['GET', 'POST'])
def add_player():
    form = PlayerForm()
    if form.validate_on_submit():
        player = acntreras_soccerplayersapp(first_name=form.first_name.data, last_name=form.last_name.data, clubteam = form.clubteam.data, nationality = form.nationality.data)
        db.session.add(player)
        db.session.commit()
        return redirect('/')

    return render_template('add_player.html', form=form, pageTitle='Add A New Player')

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







if __name__ == '__main__':
    app.run(debug=True)
