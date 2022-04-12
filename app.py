from flask import Flask, render_template, request,session, redirect, url_for,flash
from data import test_posts, post1, Message1, Message2, test_messages
import sqlite3

app = Flask(__name__)
app.secret_key="12345"

@app.route("/")
def index():
     
    return render_template('login.html')


@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        con=sqlite3.connect("zeddata.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from Users where name=? and password=?",(name,password))
        data=cur.fetchone()

        if data:
            session["name"]=data["name"]
            session["password"]=data["password"]
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
            password=request.form['password']
            con=sqlite3.connect("zeddata.db")
            cur=con.cursor()
            cur.execute("insert into Users(Name,Email,password)values(?,?,?)",(Name,Email,password))
            con.commit()
            flash("Record Added  Successfully","success")
        except:
            flash("Error in Insert Operation","danger")
        finally:
            return redirect(url_for("homepage"))
            con.close()

    return render_template('register.html')


@app.route("/homepage")
def homepage():
     
    return render_template('main.html', posts=test_posts, title = "My feed")

@app.route("/chat")
def chatpage():
     
    return render_template('chat.html', messages = test_messages, title = "Messages")




@app.route("/Friends")
def friendspage():
     
    return render_template('friends.html', messages = test_messages, title = "Messages")

@app.route("/comments/<int:post_id>")
def comments(post_id):
    post = test_posts[post_id]
    return render_template('comments.html', title="Comments", post = post)

@app.route("/create", methods=['POST'])
def create():
    return 'post content was: ' + request.form['post-content']


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))


#@app.route("/user/<string:handle>")
#def user(handle):
#    user = get_user_by_handle(handle)
#    return render_template('users.html', user=user, #posts=get_posts_by_handle(handle), user=auth.#current_user())

if __name__ == "__main__":
   app.run(debug=True)