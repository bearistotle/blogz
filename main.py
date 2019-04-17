# import modules for templating, requests, redirects, flask, db stuff
from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLALchemy

# create app variable from Flask constructor
app = Flask(__name__)

# configure app
# turn debug mode on so error msgs show up in browser too
app.config['DEBUG'] = True

# set up db connection string;
# db_type+driver://db_username:db_password@server:port/db_name
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:myblog@localhost:8889/build-a-blog'

# turn on echo to see sql commands in cmd prompt
app.config['SQLALCHEMY_ECHO'] = True

# create db variable from SQLALchemy constructor (pass in app var)
db = SQLALchemy(app)

# set secret key for sessions in Flask
app.secret_key = 'P0uMx81vjH'

# create classes for tables in db (user, post)
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    keywords = db.Column(db.String(120))
    body = db.Column(db.String(10000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, keywords, body, owner_id):
        self.title = title
        self.keywords = keywords
        self.body = body
        self.owner_id = owner_id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    posts = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

# TODO: create handlers/routes for main page, blog post form page, posted blog page

@app.route('/', methods=['GET', 'POST'])
def index():

    # pull data from db on old posts, pass to index.html on render call?

    return render_template("index.html")

@app.route('/new-post', methods=['GET', 'POST'])
def new_post():
    return render_template("new_post.html")

@app.route('/view-post', methods=['GET', 'POST'])
def view_post():
    return render_template("view_post.html")

# allow for importing without automatic execution of this file
if __name__ == "__main__":
    app.run()
