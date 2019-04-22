# import modules for templating, requests, redirects, flask, db stuff
from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



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
    blog_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
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
    page_title = 'Home'
# pull blog post data from db and pass to index.html to display
    blogs = Blog.query.all()

    # sort blogs so they display in order of id (in lieu of a date attribute to sort by)
    blogs.sort(key=lambda x: x.blog_id)
    blogs.reverse()

    # data should be a sorted list of blog objects
    return render_template("index.html", page_title=page_title, blogs=blogs)

@app.route('/newpost', methods=['GET', 'POST'])
def new_post():
    page_title = 'New Post'
    if request.method == 'GET':
        # TODO: pull needed data from args and pass to new post
        if request.args:
            if request.args.get('title'):
                title = request.args.get('title')
            else: 
                title = ''
            if request.args.get('body'):
                body = request.args.get('body')
            else:
                body = ''
            if request.args.get('keywords'):
                keywords = request.args.get('keywords')
            else:
                keywords = ''
            

            return render_template('newpost.html', page_title=page_title, title=title, body=body, keywords=keywords)

        else:
            return render_template('newpost.html', page_title=page_title)

    else:
        return redirect('/blog')

@app.route('/viewpost', methods=['GET', 'POST'])
def view_post():
    page_title = 'Published Post'
    # if method is POST, then pull data from form submitted by newpost
    if request.method == 'POST':

        # collect form data, validate, add to db
        title = request.form['title']
        body = request.form['body']
        keywords = request.form['keywords']

        # TODO: validate and redirect to newpost page with error msgs
        if not title or not body:
            flash('Title and body fields are required.')
            return redirect('/newpost?title={0}&body={1}&keywords={2}'.format(title, body, keywords))
        
        elif len(title) > 120 or len(body) > 10000:
            flash('Title or body of post is too long. Title max is 120 char; body max is 10000 char.')
            return redirect('/newpost?title={0}&body={1}&keywords={2}'.format(title, body, keywords))
        
        # add form data to db
        new_blog = Blog(title, keywords, body)
        db.session.add(new_blog)
        db.session.commit()

        date = new_blog.date

        # pass form data to viewpost.html and render it
        return render_template("viewpost.html", page_title=page_title, title=title, date=date, keywords=keywords, 
        body=body)
    
    # if method is GET, then pull blog_id from query parameter, get blog from db
    elif request.method == 'GET':
        old_blog_id = request.args.get('id')
        old_blog = Blog.query.get(old_blog_id)

        title = old_blog.title
        date = old_blog.date
        keywords = old_blog.keywords
        body = old_blog.body

        return render_template('viewpost.html', page_title=page_title, title=title, date=date, keywords=keywords, body=body)
    else:
        page_title = 'Home'
        return redirect('/blog', page_title=page_title)
# allow for importing without automatic execution of this file
if __name__ == "__main__":
    app.run()
