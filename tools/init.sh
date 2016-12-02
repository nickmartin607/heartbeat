#!/usr/bin/env bash

rm db.sqlite3 2>/dev/null
rm -rf heartbeat/migrations 2>/dev/null
python3 manage.py makemigrations heartbeat
python3 manage.py migrate
python3 manage.py loaddata tools/fixtures/*.json

