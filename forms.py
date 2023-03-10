from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField


class SearchForm(FlaskForm):
    searched = StringField('Searched', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    # body = StringField('Body', validators=[DataRequired()], widget=TextArea())
    body = CKEditorField('Body', validators=[DataRequired()])  
    slug = StringField('Slug', validators=[DataRequired()])
    # author = StringField("Author", validators=[DataRequired()])
    submit = SubmitField('Submit')

class NameForm(FlaskForm):
    name = StringField('Your name:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class TestForm(FlaskForm):
    email = StringField('Your email:', validators=[DataRequired()])
    password = PasswordField('Your password:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UserForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    username = StringField('Username:', validators=[DataRequired()])
    email = StringField('Email:', )
    profile_pic = FileField('Profile Picture')
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords Must Much!')])
    password2 = PasswordField('Comfirm password', validators=[DataRequired()])
    submit = SubmitField('Submit')