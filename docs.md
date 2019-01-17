# Nginx stuff
* Could not use unix sockets and had to end up using HTTP
* You have /etc/nginx/sites-available/ and /etc/nginx/sites-enabled/ the latter has symlinks
  to the latter for the sites we want to enable.

# Certbot
pacman -Syu certbot-nginx
## Get the certs for your site
certbot certonly --webroot -w /var/lib/letsencrypt/ -d sachiye.xyz,www.sachiye.xyz

# TODO

* Write systemd unit file for gunicorn
* "      "       "     "  for the bot
* Make sure the auto renew for letsencrypt works
* Set up Failtoban
* Figure out gunicorn+prometheus
* Use Bulma
* Change www/ to blueprints
* Fix nginx so it loads static files from /opt/sachiye/git/www/static


[1]: https://www.w3schools.com/html/html5_semantic_elements.asp
