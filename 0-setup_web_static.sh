#!/usr/bin/env bash
# sets up a web server for deployment

if ! dpkg -l | grep nginx > /dev/null; then
	apt-get update
	apt-get install -y nginx
fi

mkdir -p /data/web_static/{releases/test,shared}

echo "<!DOCTYPE html>
<html>
<head></head>
<body>
	<h1>Holberton School</h1>
</body>
</html>" | tee /data/web_static/releases/test/index.html > /dev/null

ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data

sed -i '/^server {/a \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

service nginx restart
