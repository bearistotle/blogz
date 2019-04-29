# import modules for templating, requests, redirects, flask, db stuff
from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from hashutils import check_pw_hash
from app import app, db
from models import Blog, User

# TODO: Add pagination

@app.route('/', methods=['GET'])
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/blog', methods=['GET', 'POST'])
def blog():

    if request.args:

        # get all blogs by user
        user_id = request.args.get('user')
        user_blogs = Blog.query.filter_by(owner_id=user_id).all()

        # sort blogs by id (lower = earlier)
        user_blogs.sort(key=lambda x: x.blog_id)
        user_blogs.reverse()

        user = [User.query.get(user_id)]

        return render_template('blogs.html', blogs=user_blogs, users=user)

# pull all blog post data from db and pass to blogs.html to display
    blogs = Blog.query.all()

    # sort blogs so they display in order of id (in lieu of a date attribute to sort by)
    blogs.sort(key=lambda x: x.blog_id)
    blogs.reverse()
    
    users = User.query.all()

    # data should be a sorted list of blog objects
    return render_template("blogs.html",  blogs=blogs, users=users)

@app.route('/newpost', methods=['GET', 'POST'])
def new_post():

    username = session['user']

    if request.method == 'GET':
        if request.args:
            title = request.args.get('title')
            body = request.args.get('body')
            keywords = request.args.get('keywords')

            return render_template('newpost.html',  
            title=title, body=body, keywords=keywords, user=username)
        
        else:
            return render_template('newpost.html',  user=username)



    elif request.method == 'POST':

        # collect form data, validate, add to db
        title = request.form['title']
        body = request.form['body']
        keywords = request.form['keywords']

        # TODO: validate and redirect to newpost page with error msgs
        if not title or not body:
            flash('Title and body fields are required.')
            return redirect('/newpost?title={0}&body={1}&keywords={2}'.format(
                title, body, keywords))

        elif len(title) > 120 or len(body) > 10000:
            flash('Title or body of post is too long. Title max is 120 char; body max is 10000 char.')
            return redirect('/newpost?title={0}&body={1}&keywords={2}'.format(
                title, body, keywords))
        
        # get user id
        username = session['user']
        user = User.query.filter_by(username=username).first()
        owner_id = user.user_id

        # create Blog object and add to db
        new_blog = Blog(owner_id, title, keywords, body)
        db.session.add(new_blog)
        db.session.commit()

        # pass form data to viewpost.html and render it
        return redirect('/viewpost?id={0}'.format(new_blog.blog_id))
    else:
        return redirect('/blog')

@app.route('/viewpost', methods=['GET'])
def view_post():       
    
    # pull blog_id from query parameter, get blog from db
    pub_blog_id = request.args.get('id')
    pub_blog = Blog.query.get(pub_blog_id)

    user = User.query.get(pub_blog.owner_id)

    return render_template('viewpost.html', blog=pub_blog, user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']
    
    user = User.query.filter_by(username=username).first()

    #validate username
    if not user:
        flash('Invalid username or password.')
        return render_template('login.html')
    
    #validate password
    if not check_pw_hash(password, user.pw_hash):
        flash('Invalid username or password.')
        return render_template('login.html')
    
    # all validation passed; add user to session
    session['user'] = username
    return redirect('/newpost')
    


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'GET':
        return render_template('signup.html')

    # get data from form and validate
    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify']

    if not username or not password:
        flash('Username and password are both required.')
        return render_template('signup.html')

    if User.query.filter_by(username=username).first():
        flash('That username is already taken. Please choose another.')
        return render_template('signup.html')

    if 3 > len(username) or 3 > len(password):
        flash('Username and password must be between 3 and 20 characters.')
        return render_template('signup.html')

    if 20 < len(username) or 20 < len(password):
        flash('Username and password must be between 3 and 20 characters.')
        return render_template('signup.html')

    if password != verify:
        flash('Passwords don\'t match.')
        return render_template('signup.html')
    
    # Note: password salted and hashed by User class constructor
    new_user = User(username, password)

    db.session.add(new_user)
    db.session.commit()

    session['user'] = username

    return redirect('/newpost')

@app.route('/logout', methods=['GET'])
def logout():
    del session['user']
    return redirect('/blog')

@app.before_request
def require_login():

    allowed_routes = ['login', 'signup', 'index']

    if request.endpoint not in allowed_routes and 'user' not in session:

        return redirect('/login')

# allow for importing without automatic execution of this file
if __name__ == "__main__":
    app.run()
