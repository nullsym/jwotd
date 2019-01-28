# What is this
This is the source code for a website built in Flask. It shows Japanese words with their definition and a myriad of other information.

# [WARNING]
* To be able to run the website you need a to set up a secret in www/secret.txt
* To do this just run: `python3 -c 'import os; print(os.urandom(16))' > www/secret.txt`

# Tech Used
* The flask server:   gunicorn
* The proxy:          nginx
* The cert script:    certbot-nginx
* CSS framework:      Bulma

# Virtual-environment
1. Install: 	 `pacman -Syu python-virtualenv`
2. Initiate: 	 `mkdir venv && virtualenv venv`
3. Activate: 	 `source venv/bin/activate`
4. Upgrade pip:  `pip install --upgrade pip`
5. Install:      `pip install -r requirements.txt`

# Let us encrypt certificates
1. `pacman -Syu certbot-nginx`
2. `certbot certonly --webroot -w /var/lib/letsencrypt/ -d sachiye.xyz,www.sachiye.xyz`

## Misc

### Venv
* Freeze: `pip freeze > requirements.txt`

### Nginx
* Could not use unix sockets and had to end up using HTTP
* You have /etc/nginx/sites-available/ and /etc/nginx/sites-enabled/ the latter has symlinks
  to the latter for the sites we want to enable.
