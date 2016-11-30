#!/usr/bin/env bash

mv heartbeat/db.sqlite3 heartbeat/db.sqlite3.bak
rm -rf heartbeat/migrations
python3 manage.py makemigrations heartbeat
python3 manage.py migrate
python3 manage.py loaddata tools/fixtures/*.json

