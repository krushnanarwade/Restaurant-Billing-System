# API Routes Documentation

Complete reference for all Flask routes, their purposes, parameters, and responses.

## Table of Contents
1. [Authentication Routes](#authentication-routes)
2. [Menu Management Routes](#menu-management-routes)
3. [Order Management Routes](#order-management-routes)
4. [Customer Management Routes](#customer-management-routes)
5. [Reports & Analytics Routes](#reports--analytics-routes)
6. [Dashboard Routes](#dashboard-routes)
7. [Utility Routes](#utility-routes)

---

## Authentication Routes

### Login Page
- **URL:** `/admin_login`
- **Method:** `GET`
- **Description:** Display admin login form
- **Response:** HTML login page
- **Authentication:** None required

### Admin Login Submit
- **URL:** `/admin_login`
- **Method:** `POST`
- **Description:** Process admin login credentials
- **Parameters:**
  ```json
  {
    "username": "admin",
    "password": "admin"
  }
  ```
- **Response:** 
  - Success: Redirects to `/admin` with session
  - Failure: Returns login form with error message
- **Status Codes:** `200` (form), `401` (invalid credentials), `500` (server error)

### Logout
- **URL:** `/logout`
- **Method:** `GET`
- **Description:** End user session and redirect to login
- **Response:** Redirects to `/admin_login`
- **Authentication:** Session required

---

## Menu Management Routes

### View Menu
- **URL:** `/menu`
- **Method:** `GET`
- **Description:** Display all menu items
- **Response:** HTML page with menu table and add item form
- **Authentication:** Login required (`@login_required`)
- **Data Returned:**
  ```python
  items = [
    {
      'id': 1,
      'item_name': 'Chicken Biryani',
      'price': 250.00
    },
    ...
  ]
  ```

### Add Menu Item
- **URL:** `/add_item`
- **Method:** `POST`
- **Description:** Create a new menu item
- **Parameters:**
  ```json
  {
    "name": "Butter Chicken",
    "price": "350.50"
  }
  ```
- **Validation:**
  - Item name: 2-50 characters
  - Price: 0 to 999,999.99
- **Response:** 
  - Success: Redirects to `/menu`
  - Failure: Returns menu page with error message
- **Status Codes:** `200`, `400` (validation error), `500` (database error)
- **Authentication:** Login required

### Delete Menu Item
- **URL:** `/delete_item/<int:item_id>`
- **Method:** `GET`
- **Description:** Remove a menu item by ID
- **Parameters:**
  - `item_id` (URL parameter): Integer item ID
- **Response:** Redirects to `/menu`
- **Authentication:** Login required
- **Example:** `/delete_item/5`

---

## Order Management Routes

### View Orders
- **URL:** `/order`
- **Method:** `GET`
- **Description:** Display all orders and available menu items
- **Response:** HTML page with order form and order history table
- **Authentication:** Login required
- **Data Returned:**
  ```python
  items = [...]  # Menu items for dropdown
  orders = [
    {
      'id': 1,
      'item_name': 'Chicken Biryani',
      'quantity': 2,
      'total': 500.00,
      'date': '2025-12-15'
    },
    ...
  ]
  ```

### Create Order
- **URL:** `/add_order`
- **Method:** `POST`
- **Description:** Create a new order
- **Parameters:**
  ```json
  {
    "item_id": "1",
    "quantity": "2"
  }
  ```
- **Validation:**
  - item_id: Valid menu item
  - quantity: 1 to 10,000
- **Calculation:** `total = item_price × quantity`
- **Response:** Redirects to `/order`
- **Authentication:** Login required
- **Stored Data:**
  ```python
  {
    'item_name': str,
    'quantity': int,
    'total': float,
    'date': 'YYYY-MM-DD'
  }
  ```

### Delete Order
- **URL:** `/delete_order/<int:order_id>`
- **Method:** `GET`
- **Description:** Remove an order by ID
- **Parameters:**
  - `order_id` (URL parameter): Integer order ID
- **Response:** Redirects to `/order`
- **Authentication:** Login required
- **Example:** `/delete_order/3`

---

## Customer Management Routes

### View Customers
- **URL:** `/customers`
- **Method:** `GET`
- **Description:** Display all customers in database
- **Response:** HTML page with add customer form and customer table
- **Authentication:** Login required
- **Data Returned:**
  ```python
  customers = [
    {
      'id': 1,
      'name': 'John Doe',
      'phone': '+91 9876543210'
    },
    ...
  ]
  ```

### Add Customer
- **URL:** `/add_customer`
- **Method:** `POST`
- **Description:** Create a new customer record
- **Parameters:**
  ```json
  {
    "name": "Jane Smith",
    "phone": "+91 9123456789"
  }
  ```
- **Validation:**
  - name: 2-100 characters
  - phone: 5-20 characters
- **Response:**
  - Success: Redirects to `/customers`
  - Failure: Returns customer page with error
- **Status Codes:** `200`, `400` (validation error), `500` (database error)
- **Authentication:** Login required

### Delete Customer
- **URL:** `/delete_customer/<int:customer_id>`
- **Method:** `GET`
- **Description:** Remove a customer by ID
- **Parameters:**
  - `customer_id` (URL parameter): Integer customer ID
- **Response:** Redirects to `/customers`
- **Authentication:** Login required
- **Example:** `/delete_customer/2`

---

## Reports & Analytics Routes

### View Reports
- **URL:** `/reports`
- **Method:** `GET`
- **Description:** Display sales analytics and order history
- **Response:** HTML page with summary cards and detailed table
- **Authentication:** Login required
- **Calculated Metrics:**
  ```python
  {
    'total_orders': int,           # Count of all orders
    'total_sales': float,          # Sum of all order totals
    'average_order_value': float   # total_sales / total_orders
  }
  ```
- **Data Returned:**
  ```python
  orders = [
    {
      'id': 1,
      'item_name': 'Chicken Biryani',
      'quantity': 2,
      'total': 500.00,
      'date': '2025-12-15'
    },
    ...
  ]
  ```

### Clear Reports
- **URL:** `/clear_reports`
- **Method:** `POST`
- **Description:** Delete all orders (resets sales data)
- **Response:** Redirects to `/reports`
- **Warning:** This action is **permanent** and requires confirmation
- **Authentication:** Login required
- **Recommendation:** Use only after month-end reporting

---

## Dashboard Routes

### Home Page (Root)
- **URL:** `/`
- **Method:** `GET`
- **Description:** Landing page with navigation
- **Response:**
  - If logged in: Redirects to admin dashboard
  - If not logged in: Displays login page
- **Authentication:** Optional (redirects if not authenticated)

### Admin Dashboard
- **URL:** `/admin`
- **Method:** `GET`
- **Description:** Main admin control panel
- **Response:** HTML dashboard with quick access to all modules
- **Authentication:** Login required (`@login_required`)
- **Features Displayed:**
  - Stats cards (menu items, performance, control)
  - Quick navigation to Menu, Orders, Customers, Reports
  - Welcome message with logged-in user
  - Logout button

---

## Utility Routes

### Database Initialization
- **Function:** `init_db()`
- **When Called:** Automatically on app startup
- **What It Does:**
  - Creates 5 database tables if they don't exist
  - Inserts default admin account (admin/admin)
  - Creates `sales` table for future use

### Cache Control Headers
- **Middleware:** Applied to all routes via `@app.after_request`
- **Headers Sent:**
  ```
  Cache-Control: no-cache, no-store, must-revalidate, public, max-age=0
  Pragma: no-cache
  Expires: 0
  ```
- **Purpose:** Prevents browser caching issues with sensitive data

---

## Input Validation Functions

All user inputs are validated using these helper functions:

### `validate_input(text, field_name, min_len=1, max_len=100)`
- **Purpose:** Validate text fields
- **Returns:** `(cleaned_text, error_message)` tuple
- **Checks:**
  - Not empty
  - Within length limits
  - Valid string type

### `validate_price(price_str)`
- **Purpose:** Validate price fields
- **Returns:** `(float, error_message)` tuple
- **Checks:**
  - Valid number
  - Not negative
  - Max 999,999.99

### `validate_quantity(qty_str)`
- **Purpose:** Validate quantity fields
- **Returns:** `(int, error_message)` tuple
- **Checks:**
  - Valid integer
  - Greater than 0
  - Max 10,000

---

## Error Handling

### HTTP Status Codes Used

| Code | Scenario |
|------|----------|
| `200` | Successful request, form display |
| `400` | Validation error (bad input) |
| `401` | Invalid login credentials |
| `500` | Server/database error |

### Common Error Responses

#### Validation Error
```
Status: 400
Message: "Item name must be between 2 and 50 characters"
Display: Form re-rendered with error message
```

#### Login Failure
```
Status: 401
Message: "Invalid username or password"
Display: Login form with error banner
```

#### Database Error
```
Status: 500
Message: "Failed to add item"
Display: Page with error message
```

---

## Rate Limiting & Security

Currently implemented:
- **Session Management:** Flask sessions with secure cookie
- **CSRF Protection:** Form submission validation
- **Input Sanitization:** All inputs validated and cleaned
- **SQL Injection Prevention:** Using parameterized queries with `?` placeholders

### Future Recommendations
- Add rate limiting for login attempts
- Implement password hashing (currently plaintext)
- Add CSRF tokens to all forms
- Implement request logging for audit trails

---

## Database Connection

### Connection Method
```python
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
```

### Example Query Usage
```python
conn = get_db_connection()
cursor = conn.cursor()

# Fetch all menu items
cursor.execute("SELECT id, item_name, price FROM menu ORDER BY id DESC")
items = cursor.fetchall()

# Create new item
cursor.execute(
    "INSERT INTO menu (item_name, price) VALUES (?, ?)",
    (item_name, price)
)
conn.commit()
conn.close()
```

---

## Testing Routes with cURL

### Login
```bash
curl -X POST http://localhost:5000/admin_login \
  -d "username=admin&password=admin"
```

### Add Menu Item
```bash
curl -X POST http://localhost:5000/add_item \
  -d "name=Biryani&price=250"
```

### View Menu
```bash
curl http://localhost:5000/menu
```

### Create Order
```bash
curl -X POST http://localhost:5000/add_order \
  -d "item_id=1&quantity=2"
```

---

## Next Steps

- Review [DATABASE_SCHEMA.md](./DATABASE_SCHEMA.md) for data structure
- Check [USER_GUIDE.md](./USER_GUIDE.md) for user workflows
- See [INSTALLATION.md](./INSTALLATION.md) for deployment info

---

**Last Updated:** December 2025 | **Version:** 1.0.0
