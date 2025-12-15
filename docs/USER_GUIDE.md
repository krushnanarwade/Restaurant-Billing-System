# User Guide - FoodHub

Step-by-step instructions for using all features of the FoodHub restaurant billing system.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Admin Login](#admin-login)
3. [Dashboard Overview](#dashboard-overview)
4. [Menu Management](#menu-management)
5. [Order Processing](#order-processing)
6. [Customer Management](#customer-management)
7. [Sales Reports](#sales-reports)
8. [Tips & Best Practices](#tips--best-practices)
9. [Frequently Asked Questions](#frequently-asked-questions)

---

## Getting Started

### Initial Access

1. **Open the Application**
   - Start the app: `python app.py`
   - Open browser: `http://127.0.0.1:5000`

2. **You'll See One of Two Screens:**
   - If NOT logged in → Login page
   - If logged in → Admin dashboard

3. **Default Login Credentials**
   - **Username:** `admin`
   - **Password:** `admin`

⚠️ **Change these credentials immediately after first login!**

---

## Admin Login

### Step 1: Open Login Page
- You'll automatically redirect here if not logged in
- Page shows a login form with username and password fields

### Step 2: Enter Credentials
```
Username: admin
Password: admin
```

### Step 3: Click "Login"
- If correct → You're logged in and see the Admin Dashboard
- If incorrect → Error message appears: "Invalid username or password"

### Step 4: Login Features
- **Session persists** - You stay logged in until you click Logout
- **Secure cookies** - Your session is protected
- **Logout button** - Available on every page (top right)

### To Logout
- Click **"🚪 Logout"** button on any page
- You'll be redirected to the login page
- Your session ends

---

## Dashboard Overview

### What You See After Login

The Admin Dashboard displays:

#### 1. Header Section
- **FoodHub Logo** - Click to refresh page
- **Logged In As** - Shows your username
- **Logout Button** - Click to end session

#### 2. Welcome Message
```
Welcome back, admin! 👋 
Your restaurant dashboard is ready. 
Manage orders, menu, customers, and view detailed analytics.
```

#### 3. Statistics Cards (3 Cards)
```
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   🍽️ MENU ITEMS   │  │  ⚡ PERFORMANCE  │  │    🎯 CONTROL    │
│                  │  │                  │  │                  │
│    Unlimited     │  │      Live        │  │      100%        │
│ Manage offerings │  │ Real-time track  │  │ Full admin access│
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

#### 4. Management Modules (4 Cards)

Each card is clickable and links to a feature:

**🍴 Menu** - Add & manage food items
- Click to view/add menu items
- See all available dishes
- Set prices

**🧾 Orders** - Process & track orders
- Create new orders
- View order history
- Track order totals

**👥 Customers** - Manage customer info
- Add customer names
- Store phone numbers
- Maintain customer database

**📊 Reports** - View sales & analytics
- See total sales
- View all orders
- Check average order value

---

## Menu Management

### Accessing Menu Management

1. **From Dashboard:** Click **🍴 Menu** card
2. **Direct URL:** `http://127.0.0.1:5000/menu`

### Menu Page Layout

```
┌─────────────────────────────────────────┐
│  🍴 Menu Management  [Back to Dashboard] │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│         ➕ ADD NEW MENU ITEM              │
├─────────────────────────────────────────┤
│ Item Name:  [Chicken Biryani...........]  │
│ Price (₹):  [250.00......................]  │
│                    [✓ Add Item]          │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  📋 CURRENT MENU ITEMS (3 items)        │
├─────────────────────────────────────────┤
│ ID │ Item Name        │ Price  │ Action │
├────┼──────────────────┼────────┼────────┤
│ #1 │ Chicken Biryani  │ ₹250   │ Delete │
│ #2 │ Butter Chicken   │ ₹350.5 │ Delete │
│ #3 │ Paneer Tikka     │ ₹320   │ Delete │
└─────────────────────────────────────────┘
```

### How to Add a Menu Item

**Step 1:** Fill in Item Name
- Example: "Chicken Biryani"
- Requirements: 2-50 characters
- No special characters needed

**Step 2:** Fill in Price
- Example: 250.00
- Requirements: Must be a valid number
- Decimal format (e.g., 250.50) is fine

**Step 3:** Click "✓ Add Item"
- Item appears in the table immediately
- No page reload needed

**Step 4:** Verify
- Check the item appears in the menu table below
- Price displays with ₹ symbol
- You can add more items

### How to Delete a Menu Item

**Step 1:** Find the item in the table

**Step 2:** Click **"🗑 Delete"** in the Action column

**Step 3:** Confirm the action
- A popup will ask: "Delete this item?"
- Click "OK" to confirm or "Cancel" to abort

**Step 4:** Item is removed
- Table updates instantly
- Item disappears from all order forms

### Common Issues

| Problem | Solution |
|---------|----------|
| "Item name must be between 2 and 50 characters" | Enter longer name or check for typos |
| "Invalid price format" | Use numbers only (e.g., 250 or 250.50) |
| Item doesn't appear after adding | Refresh page or try again |
| Can't delete item | Make sure you clicked the Delete link and confirmed |

---

## Order Processing

### Accessing Order Management

1. **From Dashboard:** Click **🧾 Orders** card
2. **Direct URL:** `http://127.0.0.1:5000/order`

### Order Page Layout

```
┌─────────────────────────────────────────┐
│  🧾 Order Management  [Back to Dashboard] │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│         ➕ CREATE NEW ORDER               │
├─────────────────────────────────────────┤
│ Select Item:  [Chicken Biryani ▼]        │
│ Quantity:     [1..........................]  │
│                    [✓ Place Order]       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  📦 RECENT ORDERS (2 orders)            │
├─────────────────────────────────────────┤
│ ID │ Item  │ Qty │ Total │ Date   │ Act │
├────┼───────┼─────┼───────┼────────┼─────┤
│ #1 │Biryani│ 2   │ ₹500  │ 12-15  │ Del │
│ #2 │Butter │ 1   │ ₹350.5│ 12-15  │ Del │
└─────────────────────────────────────────┘
```

### How to Create an Order

**Step 1:** Select Item
- Click the dropdown under "Select Item"
- Choose an available menu item
- Shows item name and price

**Step 2:** Enter Quantity
- Type the number of items ordered
- Example: 2, 5, 10, etc.
- Requirements: 1 to 10,000

**Step 3:** Click "✓ Place Order"
- Order is created instantly
- Total = Price × Quantity (calculated automatically)
- Order appears in table below

**Step 4:** Verify Order
- Check the order in the table
- Confirm quantity and total
- Date is set to today

### Order Total Calculation

```
Order Total = Menu Item Price × Quantity

Example:
Item: Chicken Biryani (₹250)
Quantity: 2
Order Total = ₹250 × 2 = ₹500
```

### How to Delete an Order

**Step 1:** Find the order in the table

**Step 2:** Click **"🗑 Delete"** in the Action column

**Step 3:** Confirm deletion
- Popup asks: "Delete this order?"
- Click "OK" to confirm

**Step 4:** Order is removed
- Table updates instantly
- Affects total sales in Reports

### Order History Features

- **All orders listed** - Every order ever placed
- **Newest first** - Most recent orders at top
- **Shows date** - Date each order was placed
- **Sortable** - Click headers to sort (in future)

---

## Customer Management

### Accessing Customer Management

1. **From Dashboard:** Click **👥 Customers** card
2. **Direct URL:** `http://127.0.0.1:5000/customers`

### Customer Page Layout

```
┌─────────────────────────────────────────┐
│  👥 Customer Management [Back to Dashboard]│
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│         ➕ ADD NEW CUSTOMER               │
├─────────────────────────────────────────┤
│ Name:         [John Doe..................]  │
│ Phone Number: [+91 9876543210.........]  │
│                    [✓ Add Customer]    │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  📋 CUSTOMER DATABASE (2 customers)     │
├─────────────────────────────────────────┤
│ ID │ Name          │ Phone        │ Act │
├────┼───────────────┼──────────────┼─────┤
│ #1 │ John Doe      │ 9876543210   │ Del │
│ #2 │ Jane Smith    │ 8765432109   │ Del │
└─────────────────────────────────────────┘
```

### How to Add a Customer

**Step 1:** Enter Customer Name
- Example: "John Doe"
- Requirements: 2-100 characters
- Use full name when possible

**Step 2:** Enter Phone Number
- Example: "+91 9876543210" or "9876543210"
- Requirements: 5-20 characters
- Can include country code, spaces, hyphens

**Step 3:** Click "✓ Add Customer"
- Customer is added to database
- Appears in table immediately

**Step 4:** Verify Customer
- Check table for your entry
- Phone number displays correctly
- Can add more customers

### How to Delete a Customer

**Step 1:** Find customer in table

**Step 2:** Click **"🗑 Delete"** in Action column

**Step 3:** Confirm deletion
- Popup asks: "Delete this customer?"
- Click "OK" to confirm

**Step 4:** Customer is removed
- Table updates instantly
- No impact on orders

### Customer Database Uses

- Maintain customer contact list
- Quick reference for phone numbers
- Future: Link orders to customers
- Future: Loyalty programs

---

## Sales Reports

### Accessing Sales Reports

1. **From Dashboard:** Click **📊 Reports** card
2. **Direct URL:** `http://127.0.0.1:5000/reports`

### Reports Page Layout

```
┌──────────────────────────────────────────┐
│  📊 Sales Reports & Analytics            │
└──────────────────────────────────────────┘

┌────────────┐  ┌────────────┐  ┌────────────┐
│  📋 TOTAL  │  │  💰 TOTAL  │  │  📈 AVERAGE│
│   ORDERS   │  │   SALES    │  │   ORDER    │
│     5      │  │  ₹2,721.50 │  │   ₹544.30  │
└────────────┘  └────────────┘  └────────────┘

┌──────────────────────────────────────────┐
│  📦 ORDER DETAILS                        │
├──────────────────────────────────────────┤
│ ID │ Item   │ Qty │ Total    │ Date     │
├────┼────────┼─────┼──────────┼──────────┤
│ #1 │Biryani │ 2   │ ₹500     │ 2025-12-15
│ #2 │Butter  │ 1   │ ₹350.50  │ 2025-12-15
│ #3 │Paneer  │ 2   │ ₹640     │ 2025-12-14
│ #4 │Naan    │ 10  │ ₹500     │ 2025-12-14
│ #5 │Biryani │ 1   │ ₹250     │ 2025-12-14
└──────────────────────────────────────────┘

[🗑️ CLEAR ALL ORDERS] (if orders exist)
```

### Understanding the Metrics

#### 📋 Total Orders
- **What:** Number of orders placed
- **Example:** 5 orders
- **Calculation:** COUNT of all orders

#### 💰 Total Sales
- **What:** Sum of all order totals
- **Example:** ₹2,721.50
- **Calculation:** SUM of order.total
- **Currency:** Indian Rupees (₹)

#### 📈 Average Order Value
- **What:** Average amount per order
- **Example:** ₹544.30
- **Calculation:** Total Sales ÷ Total Orders
- **Use:** Track typical order size

### How to Use Reports

**Step 1:** View Summary Cards
- Check key metrics at top
- See overall sales performance
- Track order volume

**Step 2:** Review Order Details
- Scroll down to detailed table
- See all orders listed
- Check item names, quantities, totals
- View order dates

**Step 3:** Analyze Trends
- Look for popular items (ordered multiple times)
- Check which dates had most orders
- Monitor average order value

### Clear Orders (Reset Data)

⚠️ **Warning:** This is permanent!

**When to Use:**
- End of day / end of shift
- Month-end accounting
- Testing purposes

**How to Clear:**

**Step 1:** Click **"🗑️ CLEAR ALL ORDERS"** button
- Button appears only if orders exist

**Step 2:** Confirm deletion
- Popup asks: "Are you sure? This will delete all orders!"
- Click "OK" to confirm

**Step 3:** All orders deleted
- Order table becomes empty
- Metrics reset to 0
- Total Sales = ₹0
- Total Orders = 0

### Report Examples

#### Scenario 1: Morning Shift
```
Time: 11:00 AM
Total Orders: 8
Total Sales: ₹3,200
Average Order: ₹400

Top items: Biryani (3x), Naan (5x)
```

#### Scenario 2: Evening Shift
```
Time: 8:00 PM
Total Orders: 15
Total Sales: ₹6,500
Average Order: ₹433

Top items: Butter Chicken (6x), Paneer Tikka (4x)
```

---

## Tips & Best Practices

### Menu Management

✅ **DO:**
- Keep item names clear and descriptive
- Update prices regularly
- Group similar items together (soups, mains, desserts)
- Use consistent pricing strategy

❌ **DON'T:**
- Use very long item names
- Leave prices as whole numbers (add decimals: 250.00)
- Delete popular items without notifying staff
- Add duplicate items with same name

### Order Processing

✅ **DO:**
- Verify quantity before placing order
- Check total price calculation
- Delete incorrect orders immediately
- Review order history regularly

❌ **DON'T:**
- Enter quantity as 0 or negative
- Place orders for items not in menu
- Clear orders without saving data
- Ignore wrong order totals

### Customer Management

✅ **DO:**
- Add customers with full names
- Include area code in phone numbers
- Keep contact info updated
- Use consistent phone format

❌ **DON'T:**
- Add customers without phone numbers
- Use incomplete or vague names
- Add duplicate customer entries
- Delete active customers

### General Practices

✅ **DO:**
- Backup database regularly
- Check reports daily
- Keep menu current
- Change default admin password

❌ **DON'T:**
- Clear all data without backup
- Share admin credentials
- Use production for testing
- Forget to logout

---

## Frequently Asked Questions

### Q1: I forgot the admin password. What do I do?

**A:** Currently, you'll need to:
1. Stop the app (Ctrl+C)
2. Delete `database.db` file
3. Run `python app.py` again
4. Database will recreate with default: admin/admin

### Q2: Where is my data stored?

**A:** 
- Local: `database.db` file in project root
- All data (menu, orders, customers) stored in SQLite
- Always backup this file!

### Q3: Can I edit an order after placing it?

**A:** Currently no - you must:
1. Delete the order
2. Create a new order with correct details
(Edit feature planned for future)

### Q4: How do I backup my data?

**A:** 
```bash
# Windows
Copy-Item database.db database_backup.db

# Mac/Linux
cp database.db database_backup.db
```

### Q5: Can multiple admins access the system?

**A:** 
- Currently: Only one admin account (admin/admin)
- Future: Multi-admin support planned
- For now: Share same credentials

### Q6: What happens if the app crashes?

**A:**
- Data is saved in `database.db`
- Just restart: `python app.py`
- All data persists
- No data loss

### Q7: Can I delete a menu item that has orders?

**A:** Yes! Items can be deleted anytime.
- Existing orders keep the item name
- New orders can't use deleted item
- No data loss

### Q8: How do I export data?

**A:** Currently: Manual process
```python
import csv, sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM orders')

with open('orders.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(cursor.fetchall())
```

### Q9: Is my data secure?

**A:** 
- ✅ Local: Secure on your computer
- ⚠️ Production: Add password hashing
- ⚠️ Passwords currently plaintext
- ✅ Sessions: Secure cookies used

### Q10: Can I use this for multiple restaurants?

**A:** Currently: Single restaurant only
- One database per installation
- For multiple: Run separate instances
- Future: Multi-tenant support

---

## Getting Help

If you encounter issues:

1. **Check this guide** - Most answers are here
2. **Review [INSTALLATION.md](./INSTALLATION.md)** - Setup help
3. **Check [API_ROUTES.md](./API_ROUTES.md)** - Technical details
4. **Create GitHub issue** - Report bugs with details

---

**Happy billing! 🍽️**

Last Updated: December 2025 | Version: 1.0.0
