from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from forms import *

app = Flask(__name__)

app.config['SECRET_KEY'] = "this is my secter key"

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://flasker:flasker123@localhost:5432/users"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash('Login Succesful')
                return redirect(url_for('dashboard'))
            else:
                flash('Wrong Password.Try again...')
        else:
            flash("This User Don't Exists!")
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    us = Users.query.all()
    if request.method == "POST":
        current_user.name = request.form["name"]
        current_user.username = request.form["username"]
        current_user.email = request.form["email"]
        current_user.color = request.form["color"]
        current_user.password = request.form["password"]
        try:
            db.session.commit()
            flash('User Updated Successfully')
            return render_template('dashboard.html', form=form)
        except:
            flash('Something Went Wrong. Try again...')
            return render_template('dashboard.html', form=form)
    else:
        return render_template('dashboard.html', form=form, us=us)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('login'))


@app.route('/delete_post/<int:id>')
@login_required
def delete_post(id):
    post = Posts.query.get_or_404(id)
    if post.user_id == current_user.id:
        try:
            post = Posts.query.get_or_404(id)
            db.session.delete(post)
            db.session.commit()
            flash('Post deleted')
            posts = Posts.query.order_by(Posts.posted_date)
            return render_template('posts.html', posts=posts)
        except:
            flash('Somethoing went wrong. Try again...')
            posts = Posts.query.order_by(Posts.posted_date)
            return render_template('posts.html', posts=posts)
    else:
        flash('You are not author')
        return redirect(url_for('posts'))

@app.route('/post/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Posts.query.get_or_404(id)
    if post.user_id == current_user.id:
        form = PostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.body = form.body.data
            post.slug = form.slug.data
            db.session.add(post)
            db.session.commit()
            flash('Post updated')
            return redirect(url_for('post', id=id))
        form.title.data = post.title
        form.body.data = post.body
        form.slug.data = post.slug
        return render_template('edit_post.html', form=form)
    else:
        flash('You are not author')
        return redirect(url_for('posts'))    
@app.route('/post/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)


@app.route('/posts')
def posts():
    posts = Posts.query.order_by(Posts.posted_date)
    return render_template('posts.html', posts=posts)

@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    
    # if form.validate_on_submit():
    #     post = Posts(
    #         title=form.title.data,
    #         body=form.body.data,
    #         slug=form.slug.data,
    #         author=form.author.data
    #     )
    #     db.session.add(post)
    #     db.session.commit()
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        slug = request.form['slug']
        poster = current_user.id
        post = Posts(
            title = title,
            body = body,
            slug = slug,
            user_id = poster
        )
        db.session.add(post)
        db.session.commit()
        flash('New post added')
        form.title.data = ''
        form.body.data = ''
        form.slug.data = ''
        return redirect(url_for('posts'))
    posts = Posts.query.all()
    return render_template('add_post.html', form=form, posts=posts)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
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
@login_required
def update(id):
    if id == current_user.id:
        form = UserForm()
        name_to_update = Users.query.get_or_404(id)
        if request.method == "POST":
            name_to_update.name = request.form["name"]
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
    else:
        return render_template('404.html')


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    # all_users = Users.query.order_by(Users.date_joined)
    if form.validate_on_submit():
        # user = Users.query.filter_by(email=form.email.data).first()
        user = db.session.execute(db.select(Users).filter_by(email=form.email.data)).scalar()
        if user is None:
            hashed_pw = generate_password_hash(form.password.data, 'sha256')
            user = Users(username=form.username.data,name=form.name.data,    email=form.email.data, color=form.color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
            name = form.name.data
            form.name.data = ''
            form.username.data = ''
            form.email.data = ''
            form.color.data = ''
            form.password.data = ''
            flash("User Created Successfully")
        else:
            flash("This Email Is Already Exists")
            all_users = db.session.execute(db.select(Users).order_by(Users.date_joined)).scalars()
            return render_template('add_user.html', name=name, form=form, all_users=all_users)
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


@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    passed = None
    user = None
    form = TestForm()
    if form.validate_on_submit():
        # user = db.session.execute(db.select(Users).filter_by(email=form.email.data).scelar())
        user = Users.query.filter_by(email=form.email.data).first()
        email = form.email.data
        password = form.password.data
        passed = check_password_hash(user.password_hash, password)
        flash("Form Submitted Successfully")
    return render_template('test_pw.html',passed=passed,
     email=email, form=form, user=user, pw=password)



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


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    # author = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    posted_date =db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"{self.title}"


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20),unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    color = db.Column(db.String(50))
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Posts', backref='poster')

    @property
    def password(self):
        raise AttributeError("Passwprd was unrreadable")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"<Name {self.name}>"

with app.app_context():
    db.create_all()
    db.session.commit()
