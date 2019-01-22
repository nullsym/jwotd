# Imports from our app
from sachiye import db, app

# Flask-Login works via the LoginManager class: Thus, we need
# to start things off by telling LoginManager about our Flask app
from flask_login import LoginManager
login_manager = LoginManager(app)
login_manager.init_app(app)
# Password hashing
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# Get date in a specific timezone
from datetime import datetime
from pytz import timezone

def get_date():
    fmt = "%Y-%m-%d"
    naive = datetime.now(timezone('America/Los_Angeles'))
    return naive.strftime(fmt)

###############
# Our classes #
###############
class User(UserMixin, db.Model):
    username = db.Column(db.String(80), nullable=False, primary_key=True)
    password = db.Column(db.String(120))

    def __repr__(self):
        return '<user %r:%r>' % (self.username, self.password)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def get_id(self):
        return self.username


class Wotd(db.Model):
    uid = db.Column(db.Integer(), primary_key=True, unique=True)
    date = db.Column(db.String(), nullable=False, default=get_date())
    # JP word, its romanji, and its definition. All required.
    wotd = db.Column(db.String(), nullable=False, unique=True)
    romaji = db.Column(db.String(), nullable=False)
    defn = db.Column(db.String(), nullable=False)
    # Not required, but nice to have
    classification = db.Column(db.String(20))
    example = db.Column(db.Text())

    def __repr__(self):
        return '<WOTD: %r:%r:%r>' % (self.uid, self.date, self.wotd)

# Given a user ID, return the associated user object
# It should take unicode ID of a user and returns the corresponding user object
# Should return None if the ID is not valid
@login_manager.user_loader
def user_loader(email):
    # Returns true if the user does not
    # exist, otherwise it returns the user object
    return User.query.get(email)