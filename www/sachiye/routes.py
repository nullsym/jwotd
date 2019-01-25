from flask import render_template, request, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user, login_required

# Import from our app
from sachiye import app, db
from sachiye.models import User, Wotd
# To get a random WOTD
from  sqlalchemy.sql.expression import func, select
# For the search page
from sqlalchemy import or_

# Rate limit password logins
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
limiter = Limiter(app, key_func=get_remote_address)

# Forms
from sachiye.forms import LoginForm, UserForm

#############
#   WOTD    #
#   ADMIN   #
# Functions #
#############
@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per hour")
def login():
    form = LoginForm()
    if request.method == 'GET':
        if current_user.is_anonymous:
            return render_template('login.html', form=form)
        else:
            return 'You are already logged in'
    
    elif request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect(url_for('index'))
    # Return template if we couldn't finish the POST successfully
    return render_template('login.html', form=form)

@app.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    form = UserForm()
    
    if request.method == 'GET':
        return render_template('user.html', form=form)

    elif request.method == 'POST' and form.validate_on_submit():
        if current_user.check_password(form.currentpwd.data):
            # Save the changes to the DB
            current_user.set_password(form.password.data)
            db.session.commit()
            flash('Password changed successfully', 'primary')
        else:
            flash('The current password you gave me was invalid. Try again.', 'warning')
    else:
        flash('Try again. Make sure that both passwords are the same.', 'warning')
    
    return render_template('user.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin', methods=['POST'])
@login_required
def admin():
    if request.method == 'POST':
        if request.form.get('add'):
            print("Add WOTD")
            db.session.add(Wotd(wotd=request.form['wotd'],
                romaji=request.form['romaji'],
                defn=request.form['def'],
                date=request.form['date'],
                example=request.form['example'],
                classification=request.form['classification']))
            # Save the changes to the DB
            db.session.commit()
            return "New WOTD added"
        
        elif request.form.get('del'):
            print("Delete WOTD")
            uid = request.form['id']
            Wotd.query.filter_by(uid=uid).delete()
            # Save the changes to the DB
            db.session.commit()
            return "WOTD deleted"
        
        elif request.form.get('update'):
            print("Update WOTD: " + str(current_user))
            uid = request.form['id']
            tmp = db.session.query(Wotd).get(uid)
            tmp.date = request.form['date']
            tmp.wotd = request.form['wotd']
            tmp.romaji = request.form['romaji']
            tmp.defn = request.form['def']
            tmp.example = request.form['example']
            tmp.classification = request.form['classification']
            # Save the changes to the DB
            db.session.commit()
            return redirect('/wotd/' + uid)

        else:
            return "Unknown Action"
    else:
        return "Method error (not a POST)"

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == "POST":
        search = request.form.get('search')
        searcht = '%' + request.form.get('search') + '%'
        # query = Wotd.query.filter_by(romaji=search).all()
        query = Wotd.query.filter(or_(Wotd.wotd.like(searcht), Wotd.romaji.like(search)))
    else:
        query = None
    return render_template('search.html', wotd = query)

#############
#   WOTD    #
# Functions #
#############
@app.route('/error')
def error(msg=None):
    return render_template('error.html', error = msg)

@app.route('/rand')
def wotd_rand():
    # TODO: Research if there's a more efficient way of getting a random row
    query = db.session.query(Wotd).order_by(func.random()).first()
    return render_template('rand.html', wotd = query)

# Main page
@app.route('/')
def index():
    return redirect('/page/')
@app.route('/page/', defaults={'page': 1})
@app.route('/page/<int:page>')
@limiter.limit("100 per hour", exempt_when=lambda: current_user.is_authenticated)
def wotd_page(page):
    # Avoid error: int too large to convert to SQLite INTEGER
    if page.bit_length() > 32:
        return error("Integer too long")
    
    query = Wotd.query.order_by(Wotd.date.desc()).paginate(page, 8, True)
    next_url = url_for('wotd_page', page=query.next_num) if query.has_next else None
    prev_url = url_for('wotd_page', page=query.prev_num) if query.has_prev else None

    return render_template('index.html', wotd = query.items,
        pagination=query, page='wotd_page',
        next_url=next_url, prev_url=prev_url)

# Show a specific word of the day. Displays additional information
# such as: examples, classification, and added date 
@app.route('/wotd/<int:uid>')
def wotd_uid(uid):
    query = db.session.query(Wotd).get(uid)
    return render_template('wotd.html', wotd = query)