from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)

app.config['SECRET_KEY'] = 'this is my secter key'

class NameForm(FlaskForm):
    name = StringField('Your name:', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
    return render_template('name.html', name=name, form=form)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    user = name
    return render_template('profile.html', user=user)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500