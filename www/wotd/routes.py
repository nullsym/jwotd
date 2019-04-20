from flask import render_template, request, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user, login_required

# Import from our app
from wotd import app, db
from wotd.models import User, Wotd
# To get a random WOTD
from  sqlalchemy.sql.expression import func, select
# For the search page
from sqlalchemy import or_

# Rate limit password logins
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
limiter = Limiter(app, key_func=get_remote_address)

# Forms
from wotd.forms import LoginForm, UserForm, WotdForm


#############
#   WOTD    #
#   ADMIN   #
# Functions #
#############
@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per hour")
def login():
    form = LoginForm(request.form)
    if request.method == 'GET':
        if current_user.is_anonymous:
            return render_template('login.html', form=form)
        else:
            return 'You are already logged in'

    elif request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect(url_for('index'))
    # Return template if we couldn't finish the POST successfully
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

###
# Allow a user to log out or change their password
###
@app.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    form = UserForm(request.form)

    if request.method == 'GET':
        return render_template('user.html', form=form)

    elif request.method == 'POST' and form.validate():
        print("[user()]: ** Form was validated **")
        if current_user.check_password(form.currentpwd.data):
            # Save the changes to the DB
            # current_user.set_password(form.confirm_password.data)
            # db.session.commit()
            flash('Password changed successfully', 'primary')
            return redirect(url_for('index'))
        else:
            flash('Try again. Invalid current password.', 'danger')
    return render_template('user.html', form=form)


# Delete a given WOTD (comes from wotd_uid(uid) -> wotd.html)
@app.route('/admin/del', methods=['POST'])
@login_required
def admin_del():
    print("Delete WOTD: " + str(current_user.username))
    uid = request.form.get('id')
    Wotd.query.filter_by(uid=uid).delete()
    db.session.commit()
    return "WOTD deleted"

# Edit a given WOTD
@app.route('/admin/edit', methods=['POST'])
@login_required
def admin_edit():
    form = WotdForm(request.form)

    print("Update WOTD: " + str(current_user.username))
    if request.method == 'POST' and form.validate():
        uid                 = form.uid.data
        tmp                 = db.session.query(Wotd).get(uid)
        tmp.wotd            = form.wotd.data
        tmp.romaji          = form.romaji.data
        tmp.defn            = form.defn.data
        tmp.date            = form.date.data
        tmp.example         = form.example.data
        tmp.classification  = form.classification.data
        db.session.commit()
    else:
        return("There was an error with the validation")

    return redirect('/wotd/' + uid)

# Add a given WOTD
@app.route('/admin/add', methods=['POST'])
@login_required
def admin_add():
    form = WotdForm(request.form)

    print("Add WOTD: " + str(current_user.username))
    if request.method == 'POST' and form.validate():
        db.session.add(Wotd(wotd=form.wotd.data,
            romaji  = form.romaji.data,
            defn    = form.defn.data,
            date    = form.date.data,
            example = form.example.data,
            classification  = form.classification.data))
        db.session.commit()
    else:
        return("There was an error with the validation")

    return redirect(url_for('index'))


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == "POST":
        search = request.form.get('search')
        # query = Wotd.query.filter_by(romaji=search).all()
        query = Wotd.query.filter(or_(Wotd.defn.like('%' + search + '%'), Wotd.romaji.like(search)))
    else:
        query = None
    return render_template('search.html', wotd=query)


#############
#   WOTD    #
# Functions #
#############
@app.route('/error')
def error(msg=None):
    return render_template('error.html', error=msg)

@app.route('/rand')
def wotd_rand():
    # TODO: Research if there's a more efficient way of getting a random row
    query = db.session.query(Wotd).order_by(func.random()).first()
    return render_template('rand.html', wotd=query)

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
    next_url = url_for('wotd_page', page = query.next_num) if query.has_next else None
    prev_url = url_for('wotd_page', page = query.prev_num) if query.has_prev else None

    return render_template('index.html', wotd=query.items,
        pagination=query, page='wotd_page',
        next_url=next_url, prev_url=prev_url)



# Show a specific WOTD. Shows additional info.
# Such as examples, classification, and date.
@app.route('/wotd/<int:uid>')
def wotd_uid(uid):
    form = WotdForm()

    query = db.session.query(Wotd).get(uid)
    return render_template('wotd.html', wotd=query, form=form)