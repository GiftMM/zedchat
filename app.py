from flask import Flask, render_template, abort, request
from data import test_posts, post1
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "GiftM": generate_password_hash("gift"),
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@app.route("/")
@auth.login_required
def homepage():
     
    return render_template('main.html', posts=test_posts, title = "My feed")


@app.route("/comments/<int:post_id>")
@auth.login_required
def comments(post_id):
    post = test_posts[post_id]
    return render_template('comments.html', title="Comments", post = post, user=auth.current_user())

@app.route("/create", methods=['POST'])
def create():
    return 'post content was: ' + request.form['post-content']

@app.route("/logout")
def logout():
    return abort(401)