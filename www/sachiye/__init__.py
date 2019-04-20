from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

################
# Init the app #
################
app = Flask(__name__)
# Disable whitespace and newline weirdness
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////opt/sachiye/wotd.db'
db = SQLAlchemy(app)


# By default Flask-Login uses flask.sessions for authentication
# Meaning we must set a secret key for our application
app.secret_key = os.environ['SECRET']

# Import our routes
from sachiye import routes