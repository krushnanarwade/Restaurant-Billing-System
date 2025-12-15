# 🍽️ FoodHub - Restaurant Billing System

A modern, web-based restaurant billing and order management system built with Flask. Manage menus, process orders, track customers, and generate detailed sales reports in real-time.

## ✨ Features

- **Admin Dashboard** - Centralized control panel with quick access to all features
- **Menu Management** - Add, view, and delete menu items with dynamic pricing
- **Order Processing** - Create orders, track quantities, and calculate totals
- **Customer Database** - Store and manage customer information and contact details
- **Sales Reports & Analytics** - View total sales, order counts, and average order values
- **User Authentication** - Secure admin login with session management
- **Responsive Design** - Clean, modern UI optimized for desktop and mobile devices
- **Real-time Data** - All operations update instantly without page reloads

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3.8+ with Flask 3.0.3 |
| **Database** | SQLite (local) / PostgreSQL (production) |
| **Frontend** | HTML5, CSS3, Bootstrap 5.3.3 |
| **Server** | Gunicorn (production) |
| **Deployment** | Render.com |

## 📁 Project Structure

```
restaurant-billing-system/
├── app.py                          # Main Flask application
├── database.db                     # SQLite database (local)
├── requirements.txt                # Python dependencies
├── render.yaml                     # Render deployment config
├── static/
│   ├── style.css                   # Global stylesheet
│   └── favicon.svg                 # App favicon
├── templates/
│   ├── base.html                   # Base layout template
│   ├── home.html                   # Home/dashboard page
│   ├── admin.html                  # Admin dashboard
│   ├── admin_login.html            # Admin login page
│   ├── menu.html                   # Menu management
│   ├── order.html                  # Order processing
│   ├── customers.html              # Customer management
│   ├── reports.html                # Sales reports
│   └── bill.html                   # Bill display
└── docs/
    ├── README.md                   # (This file)
    ├── INSTALLATION.md             # Setup guide
    ├── API_ROUTES.md               # Route documentation
    ├── DATABASE_SCHEMA.md          # Database structure
    └── USER_GUIDE.md               # User manual
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repo)

### Local Setup (5 minutes)

1. **Clone the repository**
   ```bash
   git clone https://github.com/krushnanarwade/Restaurant-Billing-System.git
   cd Restaurant-Billing-System
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   - Navigate to `http://127.0.0.1:5000`
   - Default login: **Username:** `admin` | **Password:** `admin`

For detailed setup instructions, see [INSTALLATION.md](./docs/INSTALLATION.md).

## 📖 Documentation

The `docs/` folder contains comprehensive guides:

- **[INSTALLATION.md](./docs/INSTALLATION.md)** - Detailed setup, database initialization, troubleshooting
- **[API_ROUTES.md](./docs/API_ROUTES.md)** - Complete list of routes, parameters, and responses
- **[DATABASE_SCHEMA.md](./docs/DATABASE_SCHEMA.md)** - Database design, tables, and relationships
- **[USER_GUIDE.md](./docs/USER_GUIDE.md)** - Step-by-step instructions for all features

## 🔐 Admin Features

### Dashboard
- Overview of total menu items, real-time performance metrics, and admin controls
- Quick access to Menu, Orders, Customers, and Reports modules

### Menu Management
- Add new food items with name and price
- View all items in a sortable table
- Delete items with confirmation

### Order Processing
- Select items from the menu
- Set quantities
- Automatic total calculation
- View order history with dates

### Customer Management
- Store customer names and phone numbers
- Maintain a customer database
- Delete customer records

### Sales Reports
- View all orders with details
- Track total sales revenue
- Calculate average order value
- Clear order history

## 🔑 Default Credentials

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `admin` |

⚠️ **Security Note:** Change default credentials immediately after first login in production environments.

## 📱 UI Features

- **Modern Gradient Design** - Purple and blue gradient backgrounds
- **Responsive Layout** - Works on desktop, tablet, and mobile
- **Emoji Icons** - Visual indicators for better UX
- **Bootstrap Components** - Professional, polished interface
- **Favicon** - Custom app icon in browser tabs
- **Smooth Transitions** - Animated buttons and interactions

## 🌐 Deployment

### Deploy to Render.com (Free)

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Select Python environment
4. Set environment variables (optional):
   - `SECRET_KEY` - Your app's secret key
5. Deploy automatically on every push to `main` branch

**Note:** SQLite data is ephemeral on Render. For persistent storage, use PostgreSQL.

See [INSTALLATION.md](./docs/INSTALLATION.md#deployment) for detailed Render deployment steps.

## 🔧 Configuration

### Environment Variables (Optional)

Create a `.env` file in the project root:

```
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
DEBUG=False
```

Then load with `python-dotenv`:
```bash
pip install python-dotenv
```

### Database Configuration

- **Local Development:** SQLite (`database.db`)
- **Production:** PostgreSQL via `DATABASE_URL` environment variable

## 📊 Usage Examples

### Add a Menu Item
1. Login as admin
2. Go to **Menu** → Fill in Item Name and Price → Click **Add Item**
3. Item appears in the table instantly

### Process an Order
1. Go to **Orders** → Select a menu item from dropdown
2. Enter quantity → Click **Place Order**
3. Order appears in the order history with total

### View Sales Reports
1. Go to **Reports**
2. See total orders, total sales, and average order value
3. View detailed order list with dates and amounts
4. Click **Clear All Orders** to reset history

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 5000 already in use | Change port in `app.py`: `app.run(debug=True, port=5001)` |
| Database not found | Run `python app.py` once to auto-initialize |
| Login fails | Check default credentials: `admin` / `admin` |
| Styles not loading | Clear browser cache or force refresh (Ctrl+Shift+R) |
| Favicon not showing | Refresh page in new private/incognito window |

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created by [Krushan Narwade](https://github.com/krushnanarwade)

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## 📞 Support

For issues, feature requests, or questions:
1. Check the [documentation](./docs/)
2. Review existing [GitHub Issues](https://github.com/krushnanarwade/Restaurant-Billing-System/issues)
3. Create a new issue with detailed information

---

**Last Updated:** December 2025 | **Version:** 1.0.0
