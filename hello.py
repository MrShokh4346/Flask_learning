from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate


app = Flask(__name__)

app.config['SECRET_KEY'] = "this is my secter key"

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://flasker:flasker123@localhost:5432/users"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(120), nullable=True, unique=True)
    color = db.Column(db.String(50))
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Name {self.name}>"

with app.app_context():
    db.create_all()
    db.session.commit()

class NameForm(FlaskForm):
    name = StringField('Your name:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UserForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()])
    color = StringField('Color')
    submit = SubmitField('Submit')



@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    name = None
    form = UserForm()
    user_to_delete = Users.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User Deleted')
        all_users = db.session.execute(db.select(Users).order_by(Users.date_joined)).scalars()
        return render_template('add_user.html', name=name, form=form, all_users=all_users)
    except:
        flash('Something went wrong. Try again...')
        all_users = db.session.execute(db.select(Users).order_by(Users.date_joined)).scalars()
        return render_template('add_user.html', name=name, form=form, all_users=all_users)



@app.route('/update/<int:id>',  methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.username = request.form["name"]
        name_to_update.email = request.form["email"]
        name_to_update.color = request.form["color"]
        try:
            db.session.commit()
            flash('User Created Successfully')
            return render_template('update.html', name_to_update=name_to_update, form=form)

        except:
            flash('Something Went Wrong. Try again...')
            return render_template('update.html', name_to_update=name_to_update, form=form)
    else:
        return render_template('update.html', name_to_update=name_to_update, form=form)



@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        # user = Users.query.filter_by(email=form.email.data).first()
        user = db.session.execute(db.select(Users).filter_by(email=form.email.data)).scalar()
        if user is None:
            user = Users(username=form.name.data, email=form.email.data, color=form.color.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        flash("User Created Successfully")
    # all_users = Users.query.order_by(Users.date_joined)
    all_users = db.session.execute(db.select(Users).order_by(Users.date_joined)).scalars()
    return render_template('add_user.html', name=name, form=form, all_users=all_users)



@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        flash("Form Submitted Successfully")
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