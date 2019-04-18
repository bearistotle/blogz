# import modules for templating, requests, redirects, flask, db stuff
from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

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
db = SQLAlchemy(app)

# set secret key for sessions in Flask
app.secret_key = 'P0uMx81vjH'

# create classes for tables in db (user, post)
# TODO: add user_id and date to Blog class
# TODO: add keywords table with post_id relationship (?)
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    keywords = db.Column(db.String(120))
    body = db.Column(db.String(10000))

    def __init__(self, title, keywords, body):
        self.title = title
        self.keywords = keywords
        self.body = body

'''
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    posts = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password
'''

# TODO: create handlers/routes for main page, blog post form page, posted blog page

@app.route('/blog', methods=['GET', 'POST'])
def index():
# pull blog post data from db and pass to index.html to display
    blogs = Blog.query.all()

    # sort blogs so they display in order of id (in lieu of a date attribute to sort by)
    blogs.sort(key=lambda x: x.id)
    blogs.reverse()

    # data should be a sorted list of blog objects
    return render_template("index.html", blogs=blogs)

@app.route('/newpost', methods=['GET', 'POST'])
def new_post():
    return render_template("newpost.html")

@app.route('/viewpost', methods=['GET', 'POST'])
def view_post():
    # collect form data, validate, add to db
    title = request.form['title']
    body = request.form['body']
    keywords = request.form['keywords']

    # TODO: validate and redirect to newpost page with error msgs
    # add form data to db
    new_blog = Blog(title, keywords, body)
    db.session.add(new_blog)
    db.session.commit()

    # pass form data to viewpost.html and render it
    return render_template("viewpost.html", title=title, keywords=keywords, 
    body=body)

# allow for importing without automatic execution of this file
if __name__ == "__main__":
    app.run()
