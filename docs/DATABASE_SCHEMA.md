# Database Schema Documentation

Complete reference for all database tables, relationships, and data structures.

## Table of Contents
1. [Database Overview](#database-overview)
2. [Table Schemas](#table-schemas)
3. [Sample Data](#sample-data)
4. [Relationships](#relationships)
5. [Queries & Examples](#queries--examples)
6. [Backup & Restoration](#backup--restoration)

---

## Database Overview

### General Information
- **Type:** SQLite 3 (local) or PostgreSQL (production)
- **File Location:** `database.db` (root directory)
- **Auto-Created:** Yes (on first app run)
- **Size:** Starts ~4KB, grows with data
- **Backup:** Manual file copy recommended

### Database Initialization
The database is automatically created with all tables on app startup via the `init_db()` function in `app.py`.

---

## Table Schemas

### 1. Menu Table
Stores all food items available in the restaurant.

```sql
CREATE TABLE menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    price REAL NOT NULL
);
```

| Column | Type | Constraints | Description |
|--------|------|-----------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique item identifier |
| `item_name` | TEXT | NOT NULL | Name of the food item (2-50 chars) |
| `price` | REAL | NOT NULL | Price in rupees (0 to 999,999.99) |

**Example:**
```
id | item_name          | price
---|--------------------|---------
1  | Chicken Biryani    | 250.00
2  | Butter Chicken     | 350.50
3  | Paneer Tikka       | 320.00
```

### 2. Orders Table
Tracks all customer orders processed.

```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    total REAL NOT NULL,
    date TEXT NOT NULL
);
```

| Column | Type | Constraints | Description |
|--------|------|-----------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique order identifier |
| `item_name` | TEXT | NOT NULL | Name of ordered item |
| `quantity` | INTEGER | NOT NULL | Quantity ordered (1-10,000) |
| `total` | REAL | NOT NULL | Total price (quantity × item_price) |
| `date` | TEXT | NOT NULL | Order date (YYYY-MM-DD format) |

**Example:**
```
id | item_name       | quantity | total    | date
---|-----------------|----------|----------|----------
1  | Chicken Biryani | 2        | 500.00   | 2025-12-15
2  | Paneer Tikka    | 1        | 320.00   | 2025-12-15
3  | Butter Chicken  | 3        | 1051.50  | 2025-12-14
```

### 3. Customers Table
Maintains customer database with contact information.

```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL
);
```

| Column | Type | Constraints | Description |
|--------|------|-----------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique customer identifier |
| `name` | TEXT | NOT NULL | Customer full name (2-100 chars) |
| `phone` | TEXT | NOT NULL | Contact number (5-20 chars) |

**Example:**
```
id | name          | phone
---|---------------|----------------------
1  | John Doe      | +91 9876543210
2  | Jane Smith    | +91 8765432109
3  | Raj Patel     | 9123456789
```

### 4. Admin Table
Stores admin account credentials.

```sql
CREATE TABLE admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
```

| Column | Type | Constraints | Description |
|--------|------|-----------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique admin ID |
| `username` | TEXT | NOT NULL | Admin login username |
| `password` | TEXT | NOT NULL | Admin password (currently plaintext) |

**Default Entry (created automatically):**
```
id | username | password
---|----------|----------
1  | admin    | admin
```

⚠️ **Security Note:** Passwords are stored in plaintext. This is a security vulnerability. In production, use `werkzeug.security.generate_password_hash()` to hash passwords.

### 5. Sales Table
Reserved for future analytics functionality.

```sql
CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total REAL NOT NULL,
    tax REAL NOT NULL,
    grand_total REAL NOT NULL,
    date TEXT NOT NULL
);
```

| Column | Type | Constraints | Description |
|--------|------|-----------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique sale ID |
| `total` | REAL | NOT NULL | Subtotal amount |
| `tax` | REAL | NOT NULL | Tax amount (calculated) |
| `grand_total` | REAL | NOT NULL | Total with tax |
| `date` | TEXT | NOT NULL | Sale date (YYYY-MM-DD) |

**Status:** Currently not used. Available for future implementations.

---

## Sample Data

### Complete Database Example

**Menu Table (5 items):**
```
1 | Chicken Biryani    | 250.00
2 | Butter Chicken     | 350.50
3 | Paneer Tikka       | 320.00
4 | Naan (1 piece)     | 50.00
5 | Garlic Naan        | 65.00
```

**Orders Table (3 orders):**
```
1 | Chicken Biryani | 2 | 500.00   | 2025-12-15
2 | Butter Chicken  | 1 | 350.50   | 2025-12-15
3 | Naan (1 piece)  | 10| 500.00   | 2025-12-14
```

**Customers Table (3 customers):**
```
1 | John Doe      | +91 9876543210
2 | Jane Smith    | +91 8765432109
3 | Raj Patel     | 9123456789
```

**Admin Table:**
```
1 | admin | admin
```

---

## Relationships

### Data Flow Diagram

```
┌─────────────────────────────────────────────────┐
│         RESTAURANT BILLING SYSTEM               │
└─────────────────────────────────────────────────┘

┌──────────────┐    ┌─────────────┐   ┌──────────────┐
│    MENU      │    │   ORDERS    │   │  CUSTOMERS   │
├──────────────┤    ├─────────────┤   ├──────────────┤
│ id           │    │ id          │   │ id           │
│ item_name    │◄───┤ item_name   │   │ name         │
│ price        │    │ quantity    │   │ phone        │
│              │    │ total       │   │              │
│              │    │ date        │   │              │
└──────────────┘    └─────────────┘   └──────────────┘
                            │
                            │ (Order total calculated
                            │  from menu price ×
                            │  quantity)
                            │
                    ┌──────────────┐
                    │    SALES     │
                    ├──────────────┤
                    │ id           │
                    │ total        │
                    │ tax          │
                    │ grand_total  │
                    │ date         │
                    └──────────────┘
                    (Future: aggregate
                     from Orders)
```

### Primary Keys
- Each table has a unique `id` as PRIMARY KEY
- `id` auto-increments with each new record
- Used for deletion and updates

### Foreign Key Relationships
Currently **none implemented** (denormalized design):
- Orders stores `item_name` as text (not `menu.id`)
- This allows menu item name to change without affecting order history
- Trade-off: slightly more data redundancy

### Calculations
- **Order Total:** `total = menu.price × orders.quantity`
- **Report Metrics:**
  - `total_sales = SUM(orders.total)`
  - `total_orders = COUNT(orders.id)`
  - `avg_order = total_sales / total_orders`

---

## Queries & Examples

### Menu Queries

**Get all menu items:**
```sql
SELECT id, item_name, price FROM menu ORDER BY id DESC;
```

**Get item by ID:**
```sql
SELECT item_name, price FROM menu WHERE id = 1;
```

**Add new item:**
```sql
INSERT INTO menu (item_name, price) VALUES ('Chicken Biryani', 250.00);
```

**Update item price:**
```sql
UPDATE menu SET price = 275.00 WHERE id = 1;
```

**Delete item:**
```sql
DELETE FROM menu WHERE id = 1;
```

**Count menu items:**
```sql
SELECT COUNT(*) as total_items FROM menu;
```

### Order Queries

**Get all orders:**
```sql
SELECT id, item_name, quantity, total, date FROM orders ORDER BY date DESC;
```

**Get orders by date:**
```sql
SELECT * FROM orders WHERE date = '2025-12-15' ORDER BY id DESC;
```

**Calculate total sales:**
```sql
SELECT SUM(total) as total_sales FROM orders;
```

**Get average order value:**
```sql
SELECT AVG(total) as avg_order FROM orders;
```

**Count orders:**
```sql
SELECT COUNT(*) as order_count FROM orders;
```

**Get orders by item:**
```sql
SELECT * FROM orders WHERE item_name = 'Chicken Biryani' ORDER BY date DESC;
```

**Delete all orders:**
```sql
DELETE FROM orders;
```

### Customer Queries

**Get all customers:**
```sql
SELECT id, name, phone FROM customers ORDER BY id DESC;
```

**Find customer by name:**
```sql
SELECT * FROM customers WHERE name LIKE '%John%';
```

**Add customer:**
```sql
INSERT INTO customers (name, phone) VALUES ('John Doe', '+91 9876543210');
```

**Update customer phone:**
```sql
UPDATE customers SET phone = '+91 9123456789' WHERE id = 1;
```

**Delete customer:**
```sql
DELETE FROM customers WHERE id = 1;
```

**Count customers:**
```sql
SELECT COUNT(*) as total_customers FROM customers;
```

### Admin Queries

**Verify login:**
```sql
SELECT id FROM admin WHERE username = 'admin' AND password = 'admin';
```

**Update password:**
```sql
UPDATE admin SET password = 'newpassword' WHERE username = 'admin';
```

**List all admins:**
```sql
SELECT username FROM admin;
```

### Complex Queries (Analytics)

**Sales summary by date:**
```sql
SELECT date, COUNT(*) as orders, SUM(total) as daily_total
FROM orders
GROUP BY date
ORDER BY date DESC;
```

**Top selling items:**
```sql
SELECT item_name, COUNT(*) as times_ordered, SUM(total) as revenue
FROM orders
GROUP BY item_name
ORDER BY revenue DESC;
```

**Items not ordered (menu vs orders):**
```sql
SELECT m.id, m.item_name
FROM menu m
LEFT JOIN orders o ON m.item_name = o.item_name
WHERE o.id IS NULL;
```

---

## Backup & Restoration

### Manual Backup

**Windows PowerShell:**
```powershell
Copy-Item -Path database.db -Destination database_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').db
```

**macOS/Linux:**
```bash
cp database.db database_backup_$(date +%Y%m%d_%H%M%S).db
```

### Automated Backup Script

```python
# backup.py
import shutil
from datetime import datetime

def backup_database():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'database_backup_{timestamp}.db'
    shutil.copy('database.db', backup_file)
    print(f"Backup created: {backup_file}")

if __name__ == '__main__':
    backup_database()
```

Run weekly:
```bash
python backup.py
```

### Restore from Backup

```powershell
# Windows
Copy-Item -Path database_backup_20251215_120000.db -Destination database.db -Force

# macOS/Linux
cp database_backup_20251215_120000.db database.db
```

### Export Data to CSV

```python
import csv
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Export orders
cursor.execute('SELECT * FROM orders')
orders = cursor.fetchall()

with open('orders_export.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'Item', 'Quantity', 'Total', 'Date'])
    writer.writerows(orders)

conn.close()
print("Exported to orders_export.csv")
```

---

## Database Size & Performance

### Initial Size
- Empty database: ~4 KB
- With sample data: ~8 KB

### Growth Rate
- Per menu item: ~0.1 KB
- Per order: ~0.2 KB
- Per customer: ~0.15 KB

### Performance Tips
1. **Add indexes for frequently queried columns:**
   ```sql
   CREATE INDEX idx_orders_date ON orders(date);
   CREATE INDEX idx_menu_name ON menu(item_name);
   ```

2. **Archive old orders periodically** (before they accumulate too much)

3. **Use pagination** for large result sets (future feature)

---

## Future Enhancements

Recommended database improvements:

1. **Password Hashing:**
   ```python
   from werkzeug.security import generate_password_hash, check_password_hash
   password_hash = generate_password_hash('admin')
   ```

2. **Proper Foreign Keys:**
   ```sql
   ALTER TABLE orders ADD CONSTRAINT fk_menu
   FOREIGN KEY (menu_id) REFERENCES menu(id);
   ```

3. **Timestamps:**
   ```sql
   ALTER TABLE orders ADD created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
   ```

4. **Bill Table (for multi-item bills):**
   ```sql
   CREATE TABLE bills (
       id INTEGER PRIMARY KEY,
       customer_id INTEGER,
       total REAL,
       created_at TIMESTAMP,
       FOREIGN KEY(customer_id) REFERENCES customers(id)
   );
   ```

5. **Audit Logging:**
   ```sql
   CREATE TABLE audit_log (
       id INTEGER PRIMARY KEY,
       action TEXT,
       user_id INTEGER,
       timestamp TIMESTAMP
   );
   ```

---

## Viewing Database in Tools

### Using SQLite Browser (GUI)
1. Download [DB Browser for SQLite](https://sqlitebrowser.org/)
2. Open `database.db`
3. View tables, data, and structure graphically

### Using Command Line
```bash
sqlite3 database.db
```

Then run queries:
```sql
.tables              -- List all tables
.schema menu         -- View menu table structure
SELECT * FROM menu;  -- View menu data
.quit                -- Exit
```

---

## Next Steps

- Read [API_ROUTES.md](./API_ROUTES.md) for application endpoints
- Check [USER_GUIDE.md](./USER_GUIDE.md) for user workflows
- See [INSTALLATION.md](./INSTALLATION.md) for deployment

---

**Last Updated:** December 2025 | **Version:** 1.0.0
