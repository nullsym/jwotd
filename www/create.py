#!/usr/bin/env python

from sachiye import db
from sachiye.models import User, Wotd


# Create the DB
db.create_all()

# Add users
admin = User(username='admin')
admin.set_password('password')
db.session.add(admin)

# Add a testing wotd
for i in range(1,200):
    t = Wotd(wotd='Wotd numba %d' % i, romaji='romaji', defn='Definition here')
    db.session.add(t)

# Commit all our changes
db.session.commit()
