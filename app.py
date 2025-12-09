from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'foodhub123'

# Add cache control headers
@app.after_request
def set_cache_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, public, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# -------------------------------------------------
# LOGIN DECORATOR
# -------------------------------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            return redirect('/admin_login')
        return f(*args, **kwargs)
    return decorated_function

# -------------------------------------------------
# DATABASE HELPER FUNCTIONS
# -------------------------------------------------
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def validate_input(text, field_name, min_len=1, max_len=100):
    """Validate and sanitize user input"""
    if not text or not isinstance(text, str):
        return None, f"{field_name} cannot be empty"
    text = text.strip()
    if len(text) < min_len or len(text) > max_len:
        return None, f"{field_name} must be between {min_len} and {max_len} characters"
    return text, None

def validate_price(price_str):
    """Validate price input"""
    try:
        price = float(price_str)
        if price < 0:
            return None, "Price cannot be negative"
        if price > 999999.99:
            return None, "Price exceeds maximum allowed value"
        return price, None
    except (ValueError, TypeError):
        return None, "Invalid price format"

def validate_quantity(qty_str):
    """Validate quantity input"""
    try:
        qty = int(qty_str)
        if qty <= 0:
            return None, "Quantity must be greater than 0"
        if qty > 10000:
            return None, "Quantity exceeds maximum allowed value"
        return qty, None
    except (ValueError, TypeError):
        return None, "Invalid quantity format"

# -------------------------------------------------
# DATABASE INITIALIZATION
# -------------------------------------------------
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Menu Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')

    # Orders Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            total REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    # Customers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')

    # Admin Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Insert default admin if not exists
    cursor.execute("SELECT COUNT(*) FROM admin")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)", ("admin", "admin"))

    # Sales Table (reserved for later)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total REAL NOT NULL,
            tax REAL NOT NULL,
            grand_total REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# -------------------------------------------------
# HOME PAGE
# -------------------------------------------------
@app.route('/')
def home():
    if 'admin' not in session:
        return render_template('admin_login.html')
    return render_template('admin.html')

# -------------------------------------------------
# MENU MANAGEMENT
# -------------------------------------------------
@app.route('/menu')
@login_required
def menu_page():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, item_name, price FROM menu ORDER BY id DESC")
    items = cursor.fetchall()
    conn.close()
    return render_template('menu.html', items=items)

@app.route('/add_item', methods=['POST'])
@login_required
def add_item():
    name = request.form.get('name', '').strip()
    price_str = request.form.get('price', '').strip()
    
    # Validate inputs
    name, name_error = validate_input(name, 'Item name', min_len=2, max_len=50)
    if name_error:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, item_name, price FROM menu ORDER BY id DESC")
        items = cursor.fetchall()
        conn.close()
        return render_template('menu.html', items=items, error=name_error), 400
    
    price, price_error = validate_price(price_str)
    if price_error:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, item_name, price FROM menu ORDER BY id DESC")
        items = cursor.fetchall()
        conn.close()
        return render_template('menu.html', items=items, error=price_error), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO menu (item_name, price) VALUES (?, ?)", (name, price))
        conn.commit()
        conn.close()
    except Exception as e:
        return render_template('menu.html', error="Failed to add item"), 500
    
    return redirect('/menu')

@app.route('/delete_item/<int:item_id>')
@login_required
def delete_item(item_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM menu WHERE id=?", (item_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        pass
    return redirect('/menu')

# -------------------------------------------------
# ORDER MANAGEMENT
# -------------------------------------------------
@app.route('/order')
@login_required
def order_page():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, item_name, price FROM menu ORDER BY id DESC")
    items = cursor.fetchall()
    cursor.execute("SELECT id, item_name, quantity, total, date FROM orders ORDER BY id DESC")
    orders = cursor.fetchall()
    conn.close()
    return render_template('order.html', items=items, orders=orders)

@app.route('/add_order', methods=['POST'])
@login_required
def add_order():
    item_id_str = request.form.get('item_id', '').strip()
    qty_str = request.form.get('quantity', '').strip()
    
    # Validate item_id
    try:
        item_id = int(item_id_str)
    except (ValueError, TypeError):
        return redirect('/order')
    
    # Validate quantity
    qty, qty_error = validate_quantity(qty_str)
    if qty_error:
        return redirect('/order')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT item_name, price FROM menu WHERE id=?", (item_id,))
        item = cursor.fetchone()

        if item:
            item_name = item['item_name']
            price = item['price']
            total = price * qty
            date = datetime.date.today().isoformat()

            cursor.execute(
                "INSERT INTO orders (item_name, quantity, total, date) VALUES (?, ?, ?, ?)",
                (item_name, qty, total, date)
            )
            conn.commit()
        conn.close()
    except Exception as e:
        pass
    
    return redirect('/order')

@app.route('/delete_order/<int:order_id>')
@login_required
def delete_order(order_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orders WHERE id=?", (order_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        pass
    return redirect('/order')

# -------------------------------------------------
# CUSTOMER MANAGEMENT
# -------------------------------------------------
@app.route('/customers')
@login_required
def customer_page():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone FROM customers ORDER BY id DESC")
    customers = cursor.fetchall()
    conn.close()
    return render_template('customers.html', customers=customers)

@app.route('/add_customer', methods=['POST'])
@login_required
def add_customer():
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    
    # Validate inputs
    name, name_error = validate_input(name, 'Customer name', min_len=2, max_len=100)
    if name_error:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, phone FROM customers ORDER BY id DESC")
        customers = cursor.fetchall()
        conn.close()
        return render_template('customers.html', customers=customers, error=name_error), 400
    
    phone, phone_error = validate_input(phone, 'Phone number', min_len=5, max_len=20)
    if phone_error:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, phone FROM customers ORDER BY id DESC")
        customers = cursor.fetchall()
        conn.close()
        return render_template('customers.html', customers=customers, error=phone_error), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (name, phone))
        conn.commit()
        conn.close()
    except Exception as e:
        return render_template('customers.html', error="Failed to add customer"), 500
    
    return redirect('/customers')

@app.route('/delete_customer/<int:customer_id>')
@login_required
def delete_customer(customer_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customers WHERE id=?", (customer_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        pass
    return redirect('/customers')

# -------------------------------------------------
# REPORTS PAGE
# -------------------------------------------------
@app.route('/reports')
@login_required
def reports_page():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, item_name, quantity, total, date FROM orders ORDER BY date DESC")
    orders = cursor.fetchall()
    conn.close()

    total_sales = sum(order['total'] for order in orders) if orders else 0
    total_orders = len(orders)

    return render_template('reports.html', orders=orders, total_sales=total_sales, total_orders=total_orders)

@app.route('/clear_reports', methods=['POST'])
@login_required
def clear_reports():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orders")
        conn.commit()
        conn.close()
    except Exception as e:
        pass
    return redirect('/reports')

# -------------------------------------------------
# ADMIN AUTHENTICATION
# -------------------------------------------------
@app.route('/admin_login')
def admin_login_page():
    if 'admin' in session:
        return redirect('/admin')
    return render_template('admin_login.html')

@app.route('/admin_login', methods=['POST'])
def admin_login_submit():
    if 'admin' in session:
        return redirect('/admin')
    
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    
    # Validate input
    if not username or not password:
        return render_template('admin_login.html', error="Username and password are required"), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM admin WHERE username=? AND password=?", (username, password))
        admin = cursor.fetchone()
        conn.close()
        
        if admin:
            session['admin'] = username
            session.permanent = True
            return redirect('/admin')
        else:
            return render_template('admin_login.html', error="Invalid username or password"), 401
    except Exception as e:
        return render_template('admin_login.html', error="Login failed. Please try again."), 500

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/admin_login')

@app.route('/admin')
@login_required
def admin_page():
    return render_template('admin.html')
if __name__ == '__main__':
    app.run(debug=True)

# Previously added public_home route commented out per request
# @app.route('/home_page')
# def public_home():
#     return render_template('home.html')

    
