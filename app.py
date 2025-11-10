from flask import Flask, render_template, request, redirect
import sqlite3
import os
import datetime

# -------------------------------------------------
# Flask App Setup
# -------------------------------------------------
app = Flask(__name__)

# -------------------------------------------------
# Database Initialization
# -------------------------------------------------
def init_db():
    if not os.path.exists('database.db'):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Menu table
        cursor.execute('''
            CREATE TABLE menu (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')

        # Customers table
        cursor.execute('''
            CREATE TABLE customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        ''')

        # Sales table
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
# ROUTE 1 : Home Page
# -------------------------------------------------
@app.route('/')
def home():
    return render_template('home.html')

# -------------------------------------------------
# ROUTE 2 : Menu Management
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
# ROUTE 3 : Order & Billing
# -------------------------------------------------
@app.route('/order')
def order_page():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu")
    items = cursor.fetchall()
    conn.close()
    return render_template('order.html', items=items)

@app.route('/generate_bill', methods=['POST'])
def generate_bill():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu")
    menu_items = cursor.fetchall()
    conn.close()

    ordered_items = []
    total = 0

    for item in menu_items:
        qty = int(request.form.get(str(item[0]), 0))
        if qty > 0:
            amount = qty * item[2]
            total += amount
            ordered_items.append({
                'name': item[1],
                'price': item[2],
                'qty': qty,
                'amount': amount
            })

    tax = total * 0.05   # 5% tax
    grand_total = total + tax

    # Save sale record
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sales (total, tax, grand_total, date) VALUES (?, ?, ?, ?)",
        (total, tax, grand_total, datetime.date.today().isoformat())
    )
    conn.commit()
    conn.close()

    return render_template('bill.html', items=ordered_items, total=total, tax=tax, grand_total=grand_total)

# -------------------------------------------------
# ROUTE 4 : Customer Management
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
# ROUTE 5 : Reports (Improved Design)
# -------------------------------------------------
@app.route('/reports')
def reports_page():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sales ORDER BY date DESC")
    sales = cursor.fetchall()
    conn.close()

    total_sales = sum(row[3] for row in sales)
    total_tax = sum(row[2] for row in sales)

    return render_template(
        'reports.html',
        sales=sales,
        total_sales=total_sales,
        total_tax=total_tax
    )

# -------------------------------------------------
# Run the App
# -------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
