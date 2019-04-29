from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create app variable from Flask constructor
app = Flask(__name__)

# configure app
# turn debug mode on so error msgs show up in browser too
app.config['DEBUG'] = True

# set up db connection string;
# db_type+driver://db_username:db_password@server:port/db_name
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'

# turn on echo to see sql commands in cmd prompt
app.config['SQLALCHEMY_ECHO'] = True

# create db variable from SQLALchemy constructor (pass in app var)
db = SQLAlchemy(app)

# set secret key for sessions in Flask
app.secret_key = 'P0uMx81vjH'