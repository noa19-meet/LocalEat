from flask import Flask, flash, render_template, url_for, redirect, request, session as flask_session
from database import *

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/')
def home():
    if 'username' in flask_session:
        email = flask_session['email']
        return render_template('HomePage.html',user=email)
    elif 'farmname' in flask_session:
        farmname = flask_session['farmname']
        return render_template('Farm_HomePage.html',farm=farmname,my_products=get_owner_products(farmname))
    else:
        return render_template('HomePage.html')

@app.route('/shop')
def shop():
    if 'username' or 'farmname' in flask_session:
        types = get_all_Types()
        return render_template('Shop.html',products=get_all_products(), types = types)
    else:
        return redirect(url_for('user_logIn'))

@app.route('/add-product', methods =["GET","POST"])
def add_product():
    if 'farmname' in flask_session:
        if request.method =="GET":
            types = get_all_Types()
            return render_template('Add_Product.html', types = types)
        else:
            add_Product(request.form['category'],flask_session['farmname'],
                int(request.form['productcost']))
            return redirect(url_for('shop'))
    else:
        return redirect(url_for('shop'))

@app.route('/product/<string:Type>')
def product_page(Type):
    foodlist = get_type_products(Type)
    print(foodlist)
    Type_1 = query_type_by_name(Type)
    return render_template('foodType.html', foodlist = foodlist, Type_1=Type_1)

    
@app.route('/user_sign-up', methods=['GET', 'POST'])
def user_signUp():
    if request.method == "POST":
        if query_user_by_username(request.form['email']) == None:
            add_User(request.form['email'],request.form['password'],request.form['phone'],request.form['address'],0)
            return redirect(url_for('user_logIn'))
        else:
            flash('User name already taken, please choose another one.')
            return render_template('User_signup.html')            
    else:
        return render_template('User_signup.html')

@app.route('/farm_sign-up', methods=['GET', 'POST'])  
def farm_signUp():
    if request.method == "POST":
        if query_by_farmname(request.form['farmname']) == None:
            add_Farm(request.form['farmname'],request.form['phone'],request.form['address'],request.form['password'])
            return redirect(url_for('farm_logIn'))
        else:
            flash('Farm name already taken, please choose another one.')
            return render_template('Farm_signup.html')
    else:
        return render_template('Farm_signup.html')

@app.route('/user_log-in', methods=['GET','POST'])
def user_logIn():
    if request.method == "POST":
        user = query_by_username_and_password(request.form['email'], request.form['password'])

        if user is not None and user.password == request.form['password']:
            flask_session['email'] = user.username
            return redirect(url_for('home'))
        else:
            error = 'Username & Password do not match , Please try again'
            flash(error)
            return render_template('User_login.html')
    else:       
        return render_template('User_login.html')

@app.route('/farm_log-in', methods=['GET','POST'])
def farm_logIn():
    if request.method == "POST":
        farm = query_by_farmname_and_password(request.form['farmname'], request.form['password'])

        if farm is not None and farm.password == request.form['password']:
            flask_session['farmname'] = farm.Farm_name
            return redirect(url_for('home'))
        else:
            return render_template('Farm_login.html')
    else:       
        return render_template('Farm_login.html')

@app.route('/user_log-out')
def user_logOut():
    if 'email' in flask_session:
        del flask_session['email']
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route('/farm_log-out')
def farm_logOut():
    if 'farmname' in flask_session:
        del flask_session['farmname']
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route('/add_food_type', methods=['GET','POST'])
def add_Type():
    if request.method == "GET":
            return render_template('add_type.html')
    else:
        print(request.form)
        
        add_type(request.form['name'],request.form['img'],request.form['min_price'],request.form['max_price'])       
        return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

