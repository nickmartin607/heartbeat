#!/usr/bin/env python3
from django.core.management import execute_from_command_line as execute
from os import environ, remove
from os.path import join, dirname, abspath, isfile
from sys import argv

FIXTURES = ['auth', 'teams', 'hosts', 'services', 'checks', 'injects']
PROJECT_PATH = dirname(abspath(__file__))
FIXTURES_PATH = join(PROJECT_PATH, 'fixtures')
DATABASE = join(PROJECT_PATH, 'heartbeat', 'db.sqlite3')

def init():
    if isfile(DATABASE):
        remove(DATABASE)
    execute(['manage.py', 'migrate'])
    for fixture in FIXTURES:
        execute(['manage.py', 'loaddata', join(FIXTURES_PATH, '{}.json'.format(fixture))])

if __name__ == "__main__":
    args = argv.copy()
    environ.setdefault("DJANGO_SETTINGS_MODULE", "heartbeat.settings")
    if len(args) > 1 and args[1] == 'init':
        init()
    else:
        execute(args)
