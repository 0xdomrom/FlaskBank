from piggy_money.piggy_money import app, get_db

from flask import Flask, request, session, g, redirect, url_for, abort, \
                  render_template, flash


@app.route('/api/account')
def api_account():
    return json.dumps({'i':request.args.get('acc_num'),'user':session.get('user_id')})


@app.route('/api/create_account', methods=['POST'])
def api_create_account():
    if session.get('logged_in'):
        db = get_db()
        cur = db.execute("insert into accounts(account_num, balance, account_holder) values (?,?,?);",
            (request.form.get("account_num"),request.form.get("balance"),session.get("user_id")))
        db.commit()
        print("added",request.form.get("account_num"),request.form.get("balance"),session.get("user_id") )
    return redirect(url_for('accounts'))




@app.route('/api/transfer', methods=['POST'])
def api_transfer():
    if session.get('logged_in') and request.form.get('from') and request.form.get('to'):
        result = send_money(session.get("user_id"),session.get("user_id"),
            request.form.get("from_account"),request.form.get("to_account"),
            request.form.get("amount"))

        return json.dumps({"result":result})
    return json.dumps({"result":"fail"})




@app.route('/api/send', methods=['POST'])
def api_send():
    if session.get('logged_in') and request.form.get('from') and request.form.get('to'):
        result = send_money(session.get("user_id"),request.form.get("send_to_user"),
            request.form.get("from_account"),request.form.get("to_account"),
            request.form.get("amount"))
        return json.dumps({"result":result})
    return json.dumps({"result":"fail"})

        
def send_money(from_user, to_user, from_account, to_account, transfer_amt):
    db = get_db()
    cur = db.execute("select balance from accounts where account_holder=? and account_num=?",
        (from_user,from_account))
    entries = cur.fetchall()
    balance_from = entries[0]["balance"]
    
    cur = db.execute("select balance from accounts where account_holder=? and account_num=?",
        (to_user,to_account))
    entries = cur.fetchall()
    balance_to = entries[0]["balance"]

    balance_from -= int(transfer_amt)
    balance_to += int(transfer_amt)

    cur = db.execute("update accounts set balance=? where account_holder=? and account_num=?",
        balance_from, from_user, from_account)
    cur = db.execute("update accounts set balance=? where account_holder=? and account_num=?",
        balance_to, to_user, to_account)
    db.commit()
    return "success"