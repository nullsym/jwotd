from flask import render_template, request, redirect
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user, logout_user

# Import from our app
from sachiye import app, db
from sachiye.models import User, Wotd

# Rate limit password logins
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
limiter = Limiter(app, key_func=get_remote_address)






#############
#   WOTD    #
#   ADMIN   #
# Functions #
#############
@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per hour")
def login():
    if request.method == 'GET':
        if not current_user.is_anonymous:
            return 'You are already logged in'
        return render_template('login.html')
    
    elif request.method == 'POST':
        email = request.form['username']
        passwd = request.form['password']
        user = User.query.filter_by(username=email).first()

        if user is not None and user.check_password(passwd):
            login_user(user, remember=True)
            return redirect('/admin/')
    
    return 'Bad login'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user')
@login_required
def user():
    return render_template('user.html')

@app.route('/admin/', methods=['GET', 'POST'], defaults={'page': 1})
@app.route('/admin/<int:page>')
@login_required
def admin(page):
    if request.method == 'POST':
        # TODO: Add code to keep a history of the last X modified entries and by whom
        print("DB CHANGE: " + str(request.form))
        
        form_id = request.form['id']
        form_date = request.form['date']
        form_wotd = request.form['wotd']
        form_defn = request.form['def']

        if request.form.get('add'):
            print("Add entry to DB")
            db.session.add(Wotd(wotd=form_wotd, defn=form_defn, date=form_date))
        
        elif request.form.get('del'):
            print("Delete entry in DB")
            Wotd.query.filter_by(uid=form_id).delete()
        
        elif request.form.get('update'):
            print("Update entry in DB")
            tmp = db.session.query(Wotd).get(form_id)
            tmp.date = form_date
            tmp.wotd = form_wotd
            tmp.defn = form_defn

        # Save the changes to the DB
        db.session.commit()

    # Avoid error: int too large to convert to SQLite INTEGER
    if page.bit_length() > 32:
        return error("Integer too long")
    
    query = Wotd.query.order_by(Wotd.date.desc()).paginate(page, 10, True)
    next_url = url_for('admin', page=query.next_num) if query.has_next else None
    prev_url = url_for('admin', page=query.prev_num) if query.has_prev else None
    
    return render_template('admin.html', wotd = query.items,
        pagination=query, page='admin',
        next_url=next_url, prev_url=prev_url)









#############
#   WOTD    #
# Functions #
#############
@app.route('/error')
def error(msg=None):
    return render_template('error.html', error = msg)

@app.route('/rand')
def wotd_rand():
    # data = g.db.execute("SELECT * FROM WOTD ORDER BY RANDOM() LIMIT 1").fetchall()
    query = Wotd.query.first()
    return render_template('rand.html', wotd = query)

@app.route('/')
def index():
    return redirect('/page/')

@app.route('/page/', defaults={'page': 1})
@app.route('/page/<int:page>')
@limiter.limit("50 per hour", exempt_when=lambda: current_user.is_authenticated)
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


@app.route('/wotd/<int:uid>')
@login_required
def wotd_uid(uid):
    query = db.session.query(Wotd).get(uid)
    return render_template('wotd.html', wotd = query)