# What is this
This is the source code for a website built in Flask. The website displays the Japenese word of the days that have been added by a Twitch bot in a database.

# [WARNING]
* To be able to run the website you need a to set up a secret in www/secret.txt
* To do this just run: python3 -c 'import os; print(os.urandom(16))' > www/secret.txt

# Tech Used
* The flask server:   gunicorn
* The proxy:          nginx
* The cert script:    certbot-nginx
* CSS framework:      Bulma

# Virtual-environment
* Install: 		pacman -Syu python-virtualenv
* Initiate: 	mkdir venv && virtualenv venv
* Activate: 	. venv/bin/activate
* Upgrade pip: 	pip install --upgrade pip
* Install:      pip install -r requirements.txt

# Virtual-environment common tasks
* Freeze:       pip freeze > requirements.txt
# Nginx stuff
* Could not use unix sockets and had to end up using HTTP
* You have /etc/nginx/sites-available/ and /etc/nginx/sites-enabled/ the latter has symlinks
  to the latter for the sites we want to enable.

# Let us encrypt certificates
* pacman -Syu certbot-nginx
* certbot certonly --webroot -w /var/lib/letsencrypt/ -d sachiye.xyz,www.sachiye.xyz
