from flask import Flask, render_template, request, redirect, url_for, session
import shelve

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session handling

# Import database functions from database.py
from database import create_products_db, get_all_products, get_product_by_id

@app.route('/')
def browse_products():
    products = get_all_products()
    return render_template('product_browsing.html', products=products)

@app.route('/product/<product_id>')
def product_details(product_id):
    product = get_product_by_id(product_id)
    return render_template('product_details.html', product=product, product_id=product_id)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        product = get_product_by_id(product_id)
        cart[product_id] = {'name': product['name'], 'price': product['price'], 'quantity': 1}
    session['cart'] = cart
    return redirect(url_for('browse_products'))

@app.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    return render_template('cart.html', cart=cart.values())

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = request.form.get('product_id')
    cart = session.get('cart', {})
    if product_id in cart:
        del cart[product_id]
    session['cart'] = cart
    return redirect(url_for('view_cart'))

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/process_payment', methods=['POST'])
def process_payment():
    # Process payment logic (integrate with Stripe API here)
    session['purchased_items'] = session.get('cart', {})
    session['cart'] = {}
    return redirect(url_for('success'))

@app.route('/success')
def success():
    purchased_items = session.get('purchased_items', {})
    total = sum(item['price'] * item['quantity'] for item in purchased_items.values())
    return render_template('success.html', purchased_items=purchased_items.values(), total=total)

if __name__ == '__main__':
    create_products_db()
    app.run(debug=True)
