from piggy_money.piggy_money import app, get_db

from flask import Flask, request, session, g, redirect, url_for, abort, \
                  render_template, flash

@app.route('/')
def home():
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
        return redirect(url_for('accounts'))
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

        return render_template('accounts.html',entries=entries)
    return redirect(url_for('home'))



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



