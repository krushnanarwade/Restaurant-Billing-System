from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import datetime

app = Flask(__name__)

# -------------------------------------------------
# DATABASE INITIALIZATION
# -------------------------------------------------
def init_db():
    if not os.path.exists('database.db'):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Menu Table
        cursor.execute('''
            CREATE TABLE menu (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')

        # Orders Table
        cursor.execute('''
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                total REAL NOT NULL,
                date TEXT NOT NULL
            )
        ''')

        # Customers Table
        cursor.execute('''
            CREATE TABLE customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        ''')

        # Sales Table (reserved for later)
        cursor.execute('''
            CREATE TABLE sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total REAL NOT NULL,
                tax REAL NOT NULL,
                grand_total REAL NOT NULL,
                date TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

init_db()

# -------------------------------------------------
# HOME PAGE
# -------------------------------------------------
@app.route('/')
def home():
    return render_template('home.html')

# -------------------------------------------------
# MENU MANAGEMENT
# -------------------------------------------------
@app.route('/menu')
def menu_page():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu")
    items = cursor.fetchall()
    conn.close()
    return render_template('menu.html', items=items)

@app.route('/add_item', methods=['POST'])
def add_item():
    name = request.form['name']
    price = request.form['price']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO menu (item_name, price) VALUES (?, ?)", (name, price))
    conn.commit()
    conn.close()
    return redirect('/menu')

@app.route('/delete_item/<int:item_id>')
def delete_item(item_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM menu WHERE id=?", (item_id,))
    conn.commit()
    conn.close()
    return redirect('/menu')

# -------------------------------------------------
# ORDER MANAGEMENT
# -------------------------------------------------
@app.route('/order')
def order_page():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu")
    items = cursor.fetchall()
    cursor.execute("SELECT * FROM orders ORDER BY id DESC")
    orders = cursor.fetchall()
    conn.close()
    return render_template('order.html', items=items, orders=orders)

@app.route('/add_order', methods=['POST'])
def add_order():
    item_id = request.form['item_id']
    qty = int(request.form['quantity'])

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT item_name, price FROM menu WHERE id=?", (item_id,))
    item = cursor.fetchone()

    if item:
        item_name, price = item
        total = price * qty
        date = datetime.date.today().isoformat()

        cursor.execute(
            "INSERT INTO orders (item_name, quantity, total, date) VALUES (?, ?, ?, ?)",
            (item_name, qty, total, date)
        )
        conn.commit()

    conn.close()
    return redirect('/order')

@app.route('/delete_order/<int:order_id>')
def delete_order(order_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE id=?", (order_id,))
    conn.commit()
    conn.close()
    return redirect('/order')

# -------------------------------------------------
# CUSTOMER MANAGEMENT
# -------------------------------------------------
@app.route('/customers')
def customer_page():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    conn.close()
    return render_template('customers.html', customers=customers)

@app.route('/add_customer', methods=['POST'])
def add_customer():
    name = request.form['name']
    phone = request.form['phone']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (name, phone))
    conn.commit()
    conn.close()
    return redirect('/customers')

@app.route('/delete_customer/<int:customer_id>')
def delete_customer(customer_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id=?", (customer_id,))
    conn.commit()
    conn.close()
    return redirect('/customers')

# -------------------------------------------------
# REPORTS PAGE
# -------------------------------------------------
@app.route('/reports')
def reports_page():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders ORDER BY date DESC")
    orders = cursor.fetchall()
    conn.close()

    total_sales = sum(row[3] for row in orders) if orders else 0
    total_orders = len(orders)

    return render_template('reports.html', orders=orders, total_sales=total_sales, total_orders=total_orders)

@app.route('/clear_reports', methods=['POST'])
def clear_reports():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders")
    conn.commit()
    conn.close()
    return redirect('/reports')

# -------------------------------------------------
# RUN APP
# -------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
    