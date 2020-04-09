import sys
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, session
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from models import db_init, Vegetable, User, Order, OrderDetails
import maya
from shortid import ShortId


app = Flask(__name__)
db = db_init(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sfv_veggies.db'
# db = SQLAlchemy(app)
app.secret_key = 'abcd1234567890'
date = maya.now().add(days=3).slang_date()
sid = ShortId()

def mergeDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items())+ list(dict2.items))

@app.route('/')
def index():
    if "user" in session:
        
        response = [item.format() for item in Vegetable.query.all()]
        return render_template('shop.html', vegetables=response, date=date)
    else: return redirect(url_for('login_page'))
    

@app.route('/vegetables', methods=['GET'])
def get_veggies():
    response = [item.format() for item in Vegetable.query.all()]

    return jsonify(response)

@app.route('/about')
def about_page():
    return render_template('about.html', date=date)


@app.route('/cart', methods=['GET'])
def checkout():
    if 'user' in session:
        if 'cart_items' in session:
            subtotal = 0
            for product in session['cart_items']:
                subtotal += float(product['price']) * float(product['qty'])
            return render_template('checkout.html', subtotal=subtotal)
        else: return redirect(request.referrer)
    else: return redirect(url_for('login_page'))

@app.route('/cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    try:
        if 'user' in session:
            veg = Vegetable.query.get(product_id).format()
            veg['qty'] = 1
            new_item = [veg]
            if 'cart_items' in session:
                if product_id in session['cart_items']:
                    print('Item already in cart!')
                else:
                    session['cart_items'] = mergeDicts(session['cart_items'], new_item)
                    return redirect(request.referrer)
            else:
                session['cart_items'] = new_item
                return redirect(request.referrer)
    except Exception as e:
        print(f'Error ==> {e}')
    finally:
        return redirect(request.referrer)

@app.route('/cart/delete/<int:product_id>', methods=['POST'])
def delete_item_in_cart(product_id):
    if 'user' not in session and 'cart_item' not in session and len(session['cart_items'] <=0):
        return redirect(url_for('get_veggies'))
    try:
        session.modified = True
        arr = session['cart_items']
        arr[:] = [d for d in arr if d.get('id') != product_id]
        session['cart_items'] = arr
        return redirect(url_for('checkout'))

    except Exception as e:
        return redirect(url_for('checkout'))
        print(f'Error ==> {e}')


@app.route('/login', methods=['GET'])
def login_page():
    if 'user' not in session:
        return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.form.to_dict()
    try:
        user = User.query.filter_by(apt=data['apt']).first()
        if user.password == data['password']:
            # session['apt'] = data['apt']
            session['user'] = user.format()
            print(session['user'])
            return redirect(url_for('index'))
    except Exception as e:
        return render_template('login.html')

@app.route('/register', methods=['POST'])
def login_register():
    data = request.form.to_dict()
    user = User(apt=data['apt'], fname=data['name'], phone=data['phone'], password=data['password'])
    user.insert()
    if 'apt' in data:
        session['user'] = user.format()
        return redirect(url_for('about_page'))
    else: return redirect(url_for('login_page', data='Please Fill Everything'))

@app.route('/logout')
def logout_user():
    if 'user' in session:
        session.pop('apt', None)
        session.pop('user', None)
        session.pop('cart_items', None)
        return redirect(url_for('about_page'))
    else: return redirect(url_for('login_page'))
    

@app.route('/updatecart/<int:product_id>')
def update_cart(product_id):
    if 'cart_items' not in session and len(session['cart_items']) <= 0:
        return redirect(url_for('checkout'))
    else:
        qty = request.args.get('qty')
        try:
            session.modified = True
            for item in session['cart_items']:
                if item['id'] == product_id:
                    item['qty'] = qty
                    flash('Item was updated')
                    return redirect(url_for('checkout'))
        except Exception as e:
            print(f'Error ==> {e}')
            return redirect(url_for('checkout'))

@app.route('/create-order', methods=['POST'])
def create_order():
    try:
        customer = User.query.get(int(session['user']['id']))
        order = Order(customer=customer, order_number=sid.generate(), order_date=date)
        order.insert()
        subtotal = 0
        for product in session['cart_items']:
            subtotal += float(product['price']) * float(product['qty'])
        for product in session['cart_items']:
            ordered_item = Vegetable.query.get(int(product['id']))
            order_details = OrderDetails(ordered_item=ordered_item, order=order, price=product['price'], qty=product['qty'], total=subtotal)
            order_details.insert()
        session.pop('cart_items', None)
        return redirect(url_for('about_page', isOrderSuccess=True))

    except Exception as e:
        print(f'Errod ==> {e}')
        return 'Failed'

@app.route('/session')
def get_session():
    return session['user']
    


if __name__ == '__main__':
    app.run()
