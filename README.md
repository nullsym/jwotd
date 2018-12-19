# What is this
This is the source code for a website built in Flask. The website displays the Japenese word of the days that have been added by a Twitch bot in a database.

# Database Scheme
https://www.tutorialspoint.com/sqlite/sqlite_data_types.htm

```
+-------------------------------------+
| Table: WOTD                         |
|-------------------------------------|
| Date       | wotd  | definition     |
|-------------------------------------|
| text       | text  | text           |
| YYYY-MM-DD | UTF-8 | UTF-8          |
+-------------------------------------+

TODO: CHANGE ABOVE SCHEMA TO ONE BELLOW

+-------------------------------------------+---------------------+
| Table: WOTD                               |  Table: Users       |
|-------------------------------------------|---------------------|
| UID | Date       | wotd  | definition     | username | password |
|-------------------------------------------|---------------------|
| int | text       | text  | text           |  text    | text     |
|     | YYYY-MM-DD | UTF-8 | UTF-8          |          |          |
+-------------------------------------------+---------------------+
```

# Tech Used
* The flask server:   gunicorn
* The proxy:          nginx
* The cert script:    certbot-nginx


# Virtual-environment
* Install: python-virtualenv
* Activate: . venv/bin/activate
* Upgrade pip: pip install --upgrade pip
* Install things: pip install
Flask
Flask-Limiter
Flask-Login
Flask-SQLAlchemy

Flask-FontAwesome

gunicorn


django-bulma