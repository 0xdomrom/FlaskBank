import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
                  render_template, flash


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



@app.route('/')
def home():
    print(session)
    if 'logged_in' in session and session['logged_in']:
        if 'dev_login' in session and session['dev_login']:
            return redirect(url_for('users'))
        return redirect(url_for('accounts'))
    return render_template('home.html')


@app.route('/login', methods=['GET','POST'])
def login():
    error = None

    if request.method == 'POST':
        if request.form.get('username') != None or request.form.get('password') != None:
            if request.form['username'] == app.config['USERNAME'] and request.form['password'] == app.config['PASSWORD']:
                session['logged_in'] = True
                session['dev_login'] = True
                flash('You were logged in')
                return redirect(url_for('users'))
            db = get_db()
            cur = db.execute('select id from users where username=? and pass_hash=? order by id desc',
                        (request.form.get('username'),request.form.get('password'))) # TODO: checking vals
            entries = cur.fetchall()
            result = [i for i in entries]
            if len(result) == 1:
                session['logged_in'] = True
                session['user_id'] = result[0]["id"]
                return redirect(url_for('accounts'))
            elif len(result) > 1:
                print('wat.')
                raise Exception
    
    if session.get('logged_in'):
        redirect(url_for('accounts'))
    else:
        return render_template('login.html',error=error)



@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    session.pop('user_id',None)
    session.pop('dev_login',None)
    flash('You were logged out')
    return redirect(url_for('home'))



@app.route('/accounts')
def accounts():
    if session.get('dev_login'):
        return redirect(url_for('users'))
    if session.get('logged_in'):
        db = get_db()
        cur = db.execute('select account_num, balance from accounts where account_holder=? order by account_num asc',
            (session['user_id'],))
        entries = cur.fetchall()
        print(entries)
        result = ""
        for item in entries:
            result += item['account_num'] + "|" + str(item['balance']) + '\n'
        return render_template('accounts.html',entries=entries)
    return redirect(url_for('home'))



@app.route('/account', methods=['GET','POST'])
def account():
    if request.method == 'GET':
        account_id = request.args.get('id')
        db = get_db()
        cur = db.execute('select account_num, balance from accounts where account_holder=? and account_num=?',
                (session['user_id'],account_id))
        entries = cur.fetchall()
        return 'show account,',entries[0]
        return render_template('account.html',account=entries[0])
    else:
        return('error')


@app.route('/users', methods=['GET','POST'])
def users():
    if request.method == 'GET':
        print(1)
        selected_user = request.args.get('id')
        print(selected_user)
        if selected_user:
            return 'show accounts of', selected_user
            pass
        else:
            print(2)
            if session.get('dev_login'):
                db = get_db()
                cur = db.execute('select username from users')
                entries = cur.fetchall()
                return render_template('users.html',entries=entries)
            else:
                return 'get out of here you hacker'
    else: #POST
        return 'ADDING USERS WOW'
