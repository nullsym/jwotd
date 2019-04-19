Sachiye
=========

A website that shows a list of Japanese words. Has an administration panel that allows editing, adding, and deleting entries.

**Note**: Set up a secret in `www/secret.txt` by running: `python3 -c 'import os; print(os.urandom(16))' > www/secret.txt`


### Virtual-environment

1. Initiate:     `mkdir .venv && virtualenv .venv`
2. Activate:     `source .venv/bin/activate`
3. Upgrade pip:  `pip install --upgrade pip`
4. Install:      `pip install -r requirements.txt`
5. Freeze:       `pip freeze > requirements.txt`

### Let's encrypt certificates

1. Install: `pacman -Syu certbot-nginx`
2. Run: `certbot certonly --webroot -w /var/lib/letsencrypt/ -d sachiye.xyz,www.sachiye.xyz`

### Nginx notes

* `/etc/nginx/sites-available/`
* `/etc/nginx/sites-enabled/ `

The latter has symlinks to the latter for the sites we want to enable.