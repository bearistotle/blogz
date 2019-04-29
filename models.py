from flask_sqlalchemy import SQLAlchemy
from app import db
from hashutils import make_pw_hash
from datetime import datetime

# create classes for tables in db (user, blog)
# TODO: add keywords table with post_id relationship (?)

class Blog(db.Model):
    blog_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    keywords = db.Column(db.String(120))
    body = db.Column(db.String(10000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    

    def __init__(self, owner_id, title, keywords, body):
        self.owner_id = owner_id
        self.title = title
        self.keywords = keywords
        self.body = body

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    pw_hash = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='user')

    def __init__(self, username, password):
        self.username = username
        self.pw_hash = make_pw_hash(password)
