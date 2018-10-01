## Nginx stuff
* Could not use unix sockets and had to end up using HTTP
* You have /etc/nginx/sites-available/ and /etc/nginx/sites-enabled/ the latter has symlinks
  to the latter for the sites we want to enable.

## Certbot
pacman -Syu certbot-nginx
# Get the certs for your site
certbot certonly --webroot -w /var/lib/letsencrypt/ -d sachiye.xyz,www.sachiye.xyz

# TODO
(*) Figure out gunicorn+prometheus
(*) Set up Failtoban
(***) Finish TODO in dbdriver........................TD
(*) Write systemd unit file for gunicorn.............TD
(*) "      "       "     "  for the bot..............TD
(*) Make sure the auto renew for letsencrypt works...TD
(*) Nav bar make it disappear when screen too small..TD


[1]: https://www.w3schools.com/html/html5_semantic_elements.asp
