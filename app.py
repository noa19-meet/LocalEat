from flask import Flask, flash, render_template, url_for, redirect, request, session as flask_session
from database import *
import time

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/')
def home():
    if 'username' in flask_session:
        user_name = flask_session['username']
        return render_template('home_loggedin.html',name="Hello,  " + user_name)
    else :
        return render_template('home.html')


@app.route('/user_signup' , methods = ['GET', 'POST'])
def user_signup():
    if request.method == 'GET':
        return render_template("user_signup.html")

    else:
        username = request.form['Username']
        password = request.form['Password']
        email = request.form['Email']
        phone = request.form['Phone']
        add_user(username,password,email,phone)
        return redirect(url_for('user_login'))

@app.route('/farm_signup', methods = ['GET', 'POST'])
def farm_signup():
    if request.method == 'GET':
        return render_template('farm_signup.html')
    else:
        Farm_name = request.form['farmname']  
        email = request.form['email']
        password = request.form['password']
        print(Farm_name, email, password)
        add_farm(Farm_name,email,password)
        return redirect(url_for('farm_login'))

@app.route('/user_login', methods = ['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = query_by_name_and_password(username, password)

        if user is not None and user.password == password:
            flask_session['username'] = user.username
            return redirect(url_for('home'))
        else :
            return render_template('user_login.html')
    else:       
        return render_template('user_login.html')

@app.route('/userlog-out')
def userlog_out():

    if 'username' in flask_session:
        del flask_session['username']
        return render_template('home.html')
    else:
        return redirect(url_for('home'))
@app.route('/farm_login', methods = ['GET', 'POST'])
def farm_login():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']

        user = is_the_farm(name, password)

        if user is not None and user.password == password:
            flask_session['username'] = user.name
            return redirect(url_for('home'))
        else :
            error = 'Username & Password do not match , Please try again'
            flash(error)
        return render_template('farmer_products.html')
    else:       
        return render_template('farm_login.html')   




if __name__ == '__main__':
    app.run(debug=True)