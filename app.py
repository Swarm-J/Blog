from flask import Flask, redirect, render_template, flash, request, url_for
from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, logout_user, LoginManager, login_required, current_user
from webforms import LoginForm, NamerForm, UserForm, PasswordForm, PostForm, PasswordForm2, SearchForm
from flask_ckeditor import CKEditor
from werkzeug.utils import secure_filename
import uuid as uuid
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret key yo"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:870113069FL4$K1987!@localhost/users'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ubecxxhtnjklgx:d2858f9e0c7a97fe3aa7d4311ad800c1e6db050f8f005e5523beeb88ae93f200@ec2-54-165-184-219.compute-1.amazonaws.com:5432/d66ttie7aqu4cc'

UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ckeditor = CKEditor(app)

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
                flash('Login Successfull!')
                return redirect(url_for('dashboard'))
            else:
                flash('Wrong Password - Try Again')
        else:
            flash('That Username does not exist!')

    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user
    flash('You Have Been Logged Out!')
    
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)

    if request.method == "POST":
        name_to_update.username = request.form['username']
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.about_author = request.form['about_author']
        name_to_update.profile_pic = request.files['profile_pic']

        pic_filename = secure_filename(name_to_update.profile_pic.filename)
        pic_name = str(uuid.uuid1()) + "_" + pic_filename
        
        saver = request.files['profile_pic']

        
        name_to_update.profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER']), pic_name)
        
        name_to_update.profile_pic = pic_name


        try:
            db.session.commit()
            saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
            flash('User Updated Successfully!')
            return render_template('dashboard.html',
                form = form,
                name_to_update = name_to_update,
                id=id)
        except:
            flash('Error! Looks like there was a problem...try again!')
            return render_template('dashboard.html',
                form = form,
                name_to_update = name_to_update,
                id=id)

    else:
        return render_template('dashboard.html', 
            form = form,
            name_to_update = name_to_update,
            id=id)


@app.route('/date')
def get_current_date():
    hunter_specs = {
        "Beast Master": "Range",
        "Marksmanship": "Range",
        "Survival": "Melee"
    }
    # return {"Date": date.today()}
    return hunter_specs

# filters #

# safe
# capitalize
# lower
# upper
# title
# trim
# striptags 


@app.route('/')
def index():
    first_name = "Swarm"
    stuff = "This is Bold Text"

    favorite_pizza= ["Pepperoni", "Cheese", "Onions", 41]
    return render_template('index.html', 
        first_name=first_name,
        stuff=stuff,
        favorite_pizza=favorite_pizza) 

@app.route('/admin')
@login_required
def admin():
    id = current_user.id
    
    if id == 20:
        return render_template('admin.html')
    else:
        flash("Sorry you don't have admin rights!")
        return redirect(url_for('dashboard'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(error):
    return render_template('500.html'), 500

@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()

    if form.validate_on_submit():
        name = form.name.data
        form.name.data= ''
        flash("Form Submitted Successfully!!!")

    return render_template('name.html', 
        name=name, 
        form=form)

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()

    if form.validate_on_submit():

        try:
            user = Users.query.filter_by(email=form.email.data).first()
            if user is None:

                hashed_pw = generate_password_hash(form.password_hash.data, "sha256")

                user = Users(username=form.username.data, name=form.name.data, email=form.email.data, about_author=form.about_author.data, password_hash=hashed_pw)
                db.session.add(user)
                db.session.commit()

                name = form.name.data
                form.username.data = ''
                form.name.data = ''
                form.email.data = ''
                form.about_author.data= ''
                form.password_hash.data = ''
                flash(f'User {name} added successfully!')

            else:
                form.email.data = ''
                flash("That email address is already in use...")
        except:
            "There was an error adding your name"

    our_users = Users.query.order_by(Users.date_created)

    return render_template("add_user.html",
        form=form,
        name=name,
        our_users=our_users)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)

    if request.method == "POST":
        name_to_update.username = request.form['username']
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.about_author = request.form['about_author']

        try:
            db.session.commit()
            flash('User Updated Successfully!')
            return redirect(url_for('dashboard'))
        except:
            flash('Error! Looks like there was a problem...try again!')
            return render_template('update.html',
                form = form,
                name_to_update = name_to_update,
                id=id)

    else:
        return render_template('update.html', 
            form = form,
            name_to_update = name_to_update,
            id = id)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    name = None
    form = UserForm()
    name_to_delete = Users.query.get_or_404(id)

    try:
        db.session.delete(name_to_delete)
        db.session.commit()
        flash('User Deleted Successfully!')

        our_users = Users.query.order_by(Users.date_created)
        return render_template('add_user.html',
            form=form,
            name=name,
            our_users=our_users)

    except:
        flash('There was a problem deleting selected user, try again!')
        render_template('add_user.html',
            form=form,
            name=name,
            our_users=our_users)

@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    password = None
    id = current_user.id
    pw_to_check = None
    passed = None
    form = PasswordForm()

    if form.validate_on_submit():
       
        password = form.current_password.data
        pw_to_check = Users.query.get_or_404(id)
        passed = check_password_hash(pw_to_check.password_hash, password)
        
        if passed:
            return render_template('test_pw.html',
                password = password, 
                pw_to_check = pw_to_check,
                passed = passed,
                form = form)            

        else:
            flash('inccorect password')
    

    return render_template('test_pw.html',
        # email = email, 
        password = password, 
        pw_to_check = pw_to_check,
        passed = passed,
        form = form)  

@app.route('/change_pw', methods=['GET', 'POST'])
@login_required
def change_pw():
    id = current_user.id
    current_password = None
    new_hashed_pw = None
    password = None
    passed = None
    form = PasswordForm2()

    if form.validate_on_submit():

        current_password = form.current_password.data
        password = Users.query.get_or_404(id)
        passed = check_password_hash(password.password_hash, current_password)
        
        if passed:
            new_hashed_pw = generate_password_hash(form.new_password.data, "sha256")
            
            try:

                password.password_hash = new_hashed_pw

                db.session.add(password)
                db.session.commit()

                form.current_password.data = ''
                form.new_password.data = ''
                form.new_password2 = ''

                flash('Password Successfully Changed')
                return redirect(url_for('dashboard'))

            except:
                flash('Error! Looks like there was a problem...try again!')
                return render_template('change_pw.html',
                    form = form)
        else:
            flash('The entered password is incorrect...try again!')

    return render_template('change_pw.html', form=form)

@app.route('/add-post', methods=['GET', 'POST'])
# @login_required
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        poster = current_user.id
        post = Posts(title=form.title.data, 
                     content=form.content.data, 
                     slug=form.slug.data,
                     poster_id=poster)

        form.title.data = ''
        form.content.data = ''
        form.slug.data = ''
        
        db.session.add(post)
        db.session.commit()

        flash("Blog Post Submitted Successfully!")

    return render_template('/add_posts.html', form = form)

@app.route('/posts')
def posts():

    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts)

@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    form = PostForm()
    post = Posts.query.get_or_404(id)

    if form.validate_on_submit():
        post.title = form.title.data
        post.slug = form.slug.data
        post.content = form.content.data

        db.session.add(post)
        db.session.commit()
        flash('Post Edited Successfully!')
        return redirect(url_for('post', id=post.id))
    
    if current_user.id == post.poster_id:
        form.title.data = post.title
        form.slug.data = post.slug
        form.content.data = post.content

        return render_template('edit_post.html', form=form, id=post.id)
    
    else:
        flash("You Aren't Authorized To Edit This Post")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)

@app.route('/posts/delete<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id
    
    if id == post_to_delete.poster.id:
    
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            flash('Post Deleted Successfully!')

            posts = Posts.query.order_by(Posts.date_posted)
            return render_template('posts.html', posts=posts)
                

        except:
            posts = Posts.query.order_by(Posts.date_posted)

            flash('There was a problem deleting your post, try again!')
            return render_template('posts.html', posts=posts)
    
    else:
        posts = Posts.query.order_by(Posts.date_posted)

        flash('You are not authorized to delete that post')
        return render_template('posts.html', posts=posts)

@app.route('/search', methods=["POST"])
def search():
    form = SearchForm()
    posts = Posts.query

    if form.validate_on_submit():
        post.searched = form.searched.data

        posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
        posts = posts.order_by(Posts.title).all()

        return render_template('search.html', 
        form=form,
        searched = post.searched,
        posts=posts)
    
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text())
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    about_author = db.Column(db.Text(), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    profile_pic = db.Column(db.String(255), nullable=True)

    password_hash = db.Column(db.String(128))

    posts = db.relationship('Posts', backref='poster')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return '<Name %r>' % self.name

if __name__ == "__main__":
    app.run(debug=True)