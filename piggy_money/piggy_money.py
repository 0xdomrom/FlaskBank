import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
                  render_template, flash
import json

def startApp():
    app = Flask(__name__)
    app.config.from_object(__name__)

    app.config.update(dict(
        DATABASE=os.path.join(app.root_path, 'bank.db'),
        SECRET_KEY='dev',
        USERNAME='admin',
        PASSWORD='password'
    ))

    app.config.from_envvar('PIGGY_MONEY_SETTINGS', silent=True)

    return app

app = startApp()


def connect_db():
    rv=sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')

def init_db():
    db = get_db()
    with app.open_resource('schema.sql',mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.before_request
def checks():
    # could check user token here
    pass



from piggy_money.views import *
from piggy_money.api import *