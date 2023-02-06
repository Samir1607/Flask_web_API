from flask import Flask, render_template, request, redirect, session
import mysql.connector
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)
conn = mysql.connector.connect(user='root', password='1995', host='localhost', database='sam', port='3306')
cursor = conn.cursor()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register')
def about():
    return render_template('register.html')


@app.route('/info')
def info():
    if 'id' in session:
        return render_template('info.html')
    else:
        return redirect('/')


@app.route('/login_validation', methods=['POST'])
def login_validate():
    email = request.form.get('email')
    password = request.form.get('password')

    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND password LIKE '{}'""".format(email, password))
    users1 = cursor.fetchall()
    if len(users1) > 0:
        session['id'] = users1[0][0]
        return redirect('/info')
    else:
        return redirect('/')


@app.route('/add_user', methods=['POST'])
def add_user():
    name= request.form.get('name1')
    email = request.form.get('email1')
    password = request.form.get('password1')

    cursor.execute("""INSERT INTO  `users`(`id`,`name`,`email`,`password`)  VALUES(Null,'{}','{}','{}')""".format(name, email, password))
    conn.commit()
    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
    myuser = cursor.fetchall()
    session['id'] = myuser[0][0]
    return redirect('/info')


@app.route('/logout')
def logout():
    session.pop('id')
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
