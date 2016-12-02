CONFIG_DIR='/home/heartbeat/heartbeat/config'

sudo mkdir -p /etc/uwsgi/sites

sudo ln -s ${CONFIG_DIR}/nginx.conf /etc/nginx/sites-enabled/heartbeat
sudo ln -s ${CONFIG_DIR}/uwsgi.service /etc/systemd/system/uwsgi.service
sudo ln -s ${CONFIG_DIR}/uwsgi.ini /etc/uwsgi/sites/heartbeat.ini

sudo ufw allow 'Nginx Full'

sudo systemctl uwsgi restart
sudo systemctl nginx restart

setcap cap_net_raw=eip /usr/bin/python3 2>/dev/null
setcap cap_net_raw=eip /usr/bin/python3.5 2>/dev/null
setcap cap_net_raw=eip /usr/bin/tcpdump 2>/dev/null