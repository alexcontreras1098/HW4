from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'


class PlayerForm(FlaskForm):
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    clubteam = StringField('Club team:', validators=[DataRequired()])
    nationality = StringField('Nationality:', validators=[DataRequired()])

@app.route('/')
def index():
    return render_template('index.html',pageTitle='Favorite Soccer Players')

@app.route('/add_player', methods=['GET', 'POST'])
def add_player():
    form = PlayerForm()
    if form.validate_on_submit():
            return "<h2> My Favorite players name is {0} {1} and they play for {2} and they are originally from {3}" .format(form.first_name.data, form.last_name.data, form.clubteam.data, form.nationality.data)

    return render_template('add_player.html', form=form, pageTitle='Add A New Player')


if __name__ == '__main__':
    app.run(debug=True)
