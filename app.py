import flask
from flask import Flask, render_template, request, redirect, url_for,flash, session
from builtins import classmethod, len, print
from data import test_posts, post1, Message1, Message2, test_messages
import sqlite3
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, IntegerField,TextAreaField 
from urllib.parse import urlparse, urljoin
from flask_socketio import SocketIO
import database

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
db = database.Database()

app.secret_key="12345"
socketio = SocketIO(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class User():

    def __init__(self, id):
        self.id = id

    def is_authenticated(self):
        return True

    def is_active():
        return True

    def is_anonymous():
        return False

    def get_id(self):
        return self.id

    @classmethod 
    def get(cls,id):
       return User(id)

class LoginForm(FlaskForm):
 username = StringField('Username')
 password = PasswordField('Password')
 submit = SubmitField('Submit')

class signUpForm(FlaskForm):
 name = StringField('Name')
 email = TextAreaField('Email')
 password = PasswordField('Password')
 submit = SubmitField('Submit')

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http','https') and \
           ref_url.netloc == test_url.netloc


@app.route("/")
def index():
     
    return render_template('login.html')



@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        user = db.get_user_data(name)[0]

        if user and check_password_hash(user['password'], password):
            user = User(user['Id'])

            login_user(user)

            return redirect("homepage")
        else:
            flash("Username and Password Mismatch","danger")
    return redirect(url_for("index"))


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        try:
            Name=request.form['Name']
            Email=request.form['Email']
            password=generate_password_hash(request.form['password'])

            db.insert_new_user(Name,Email,password)
            user_id = db.get_id_by_name(Name)[0]
            user = User(user_id['Id'])

            login_user(user)
            flash("Record Added  Successfully","success")
        except:
            flash("Error in Insert Operation","danger")
        finally:
            return redirect(url_for("homepage"))
            con.close()

    return render_template('register.html')  


@app.route("/homepage")
@login_required
def homepage():
    posts = db.get_all_posts()
    user = db.get_user_by_Id(current_user.id)[0]['Name']
    if (posts == None):
        posts = []
    return render_template('main.html', posts=posts, Id=current_user, user=user, title = "My feed")


@app.route("/createmessage", methods=['POST'])  
def createmessage():
    message_content = request.form['message-content']
    db.insert_message(current_user.id, message_content)
    return redirect(url_for('chatpage'))

@app.route("/chat")
@login_required
def chatpage():
    #messages = db.get_all_messages(current_user.id)
    return render_template('chat.html', messages = test_messages, title = "Messages")


@app.route("/Friends")
@login_required
def friendspage():
    all_users = db.get_all_users_alphabetically()
    return render_template('friends.html', title = "Friends", all_users= all_users)

#@app.route("/comments/<int:post_id>")
#def comments():
#    post = db.get_all_comments
#    return render_template('comments.html', title="Comments", post = post)

@app.route("/create", methods=['POST'])  
def create():
    post_content = request.form['post-content']
    db.insert_post(current_user.id, post_content) 
    return redirect(url_for('homepage'))


@app.route("/users/<string:user>", methods=['GET', 'POST'])
def profile(user):
    user_infor = db.get_user(user)
    if (len(user_infor) > 0):
        User = user_infor[0] 
        posts = db.get_all_posts(current_user.id)
        if (posts == None):
            posts = []
        return render_template('profile.html', title=User['Name'], User=User, posts=posts, user=current_user )


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search_users():
    search_input = request.form['search_input']
    search = db.search_results(search_input)
    user = db.get_all_users_alphabetically()
    return render_template('friends.html', title = "Friends",user = user, all_users = search)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == "__main__":
   app.run(debug=True)
   socketio.run(app)