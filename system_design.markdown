# Customer Analysis Dashboard: System Design

This document outlines the system architecture, file structure, and dependencies for a Dash-based customer analysis dashboard. It incorporates the provided data schema and requirements from the Anforderungsanalyse, ensuring separation of frontend and backend, support for interactive visualizations, and scalability.

---

## System Architecture

### Overview
The system follows a **client-server model** with a clear separation of frontend (Dash) and backend (Flask API). It connects to a database for data storage and supports interactive features like drill-down, filters, and export functionality.

### Architecture Diagram
```
+-------------------+       +-------------------+       +-------------------+
|    Client (Web)   | <---> |    Frontend       | <---> |    Backend        |
| - Browser         |       | - Dash App        |       | - Flask API       |
| - User Interaction|       | - Visualizations  |       | - Data Processing |
|                   |       | - Drill-down      |       | - Business Logic  |
+-------------------+       | - Filters         |       | - DB Queries      |
                            +-------------------+       +-------------------+
                                    ^                          |
                                    |                          v
                            +-------------------+       +-------------------+
                            |    Assets        |       |    Database       |
                            | - CSS, JS         |       | - Customers       |
                            | - Images          |       | - Orders          |
                            +-------------------+       | - Stores, etc.    |
                                                       +-------------------+
```

### Components
1. **Database Layer**:
   - **Technology**: SQLite (development) or PostgreSQL (production).
   - **Schema** (based on provided class diagram):
     - `Customers`: `customerID` (PK), `latitude`, `longitude`.
     - `Orders`: `orderID` (PK), `customerID` (FK), `storeID` (FK), `orderDate`, `nItems`, `total`.
     - `Stores`: `storeID` (PK), `zipcode`, `state_abbr`, `latitude`, `longitude`, `city`, `state`, `distance`.
     - `OrderItems`: `SKU` (PK, FK), `orderID` (PK, FK).
     - `Products`: `SKU` (PK), `Name`, `Price`, `Category`, `Size`, `Ingredients`, `Launch`.
   - **Access**: SQLAlchemy for ORM-based queries.

2. **Backend Layer**:
   - **Technology**: Flask with REST API.
   - **Purpose**: Data retrieval, processing, and business logic (e.g., geographic analysis, KPIs).
   - **Endpoints**: Defined in file structure (see below).

3. **Frontend Layer**:
   - **Technology**: Dash with `dash-bootstrap-components`.
   - **Features**: Maps, charts, tables, filters, drill-down, KPIs, export, and tooltips.
   - **Styling**: Bootstrap theme with custom CSS.

4. **Client Layer**:
   - **Technology**: Web browser (Firefox/Chrome on Pop!_OS).
   - **Features**: Responsive design, real-time updates.

5. **Assets**:
   - **Purpose**: Static files (CSS, JS, images).
   - **Location**: `dash_app/assets/`.

### Data Flow
1. User interacts with Dash frontend (e.g., applies filters, clicks for drill-down).
2. Dash sends requests to Flask API (e.g., `/api/customers?state=BY`).
3. Flask queries the database, processes data, and returns JSON.
4. Dash updates visualizations and tables via callbacks.
5. User exports data as CSV using `dcc.Download`.

---

## File Structure

The file structure is modular, separating frontend and backend, and supports the requirements (e.g., customer analysis, visualizations, drill-down). API endpoints are derived from the Anforderungsanalyse.

```
customer_dashboard/
├── api/                          # Backend: Flask API
│   ├── __init__.py               # Package initialization
│   ├── routes/                   # API endpoints
│   │   ├── __init__.py
│   │   ├── customers.py          # Customer endpoints
│   │   │   # GET /api/customers: Geographic distribution
│   │   │   # GET /api/customers/density: Density by state/city
│   │   │   # GET /api/customers/top: Top customers by purchase frequency
│   │   │   # GET /api/customers/avg_order: Average order value per customer
│   │   │   # GET /api/customers/recurring: Recurring customers
│   │   ├── orders.py             # Order endpoints
│   │   │   # GET /api/orders/volatility: Orders with high volatility
│   │   │   # GET /api/orders/avg_items: Average items per order
│   │   │   # GET /api/orders/avg_value: Average order value
│   │   │   # GET /api/orders/basket: Frequently bought together
│   │   ├── stores.py             # Store (branch) endpoints
│   │   │   # GET /api/stores/revenue: Revenue per store
│   │   │   # GET /api/stores/revenue_trend: Revenue trend per time
│   │   │   # GET /api/stores/revenue_by_state: Revenue by state
│   │   │   # GET /api/stores/customer_reach: Customer count per store
│   │   │   # GET /api/stores/product_sales: Product sales per store
│   │   │   # GET /api/stores/product_sales: Average distance customerToStore
│   │   ├── products.py           # Product endpoints
│   │   │   # GET /api/products/top: Top products by sales
│   │   │   # GET /api/products/revenue: Revenue by product/category
│   │   │   # GET /api/products/performance: Performance by launch date
│   │   │   # GET /api/products/avg_price: Average price by category
│   │   │   # GET /api/products/price_sales: Price-sales correlation
│   │   ├── geo.py                # Geographical endpoints
│   │   │   # GET /api/geo/distance: Average customer-store distance          
│   │   │   # GET /api/geo/assignment: Customer-store assignment by proximity
│   │   │   # GET /api/geo/potential_locations: Potential new store locations
│   │   │   # GET /api/geo/low_penetration: Low market penetration areas
│   │   │   # GET /api/geo/white_spot: White-spot analysis
│   │   ├── trends.py             # Trend endpoints
│   │   │   # GET /api/trends/seasonal: Seasonal trends by  category
│   │   │   # GET /api/trends/growth/order: Order growth
│   │   │   # GET /api/trends/growth/revenue: Revenue growth
│   │   │   # GET /api/trends/peak_times: Peak times (e.g., holidays)
│   │   └── kpis.py               # KPI endpoints
│   │       # GET /api/kpis: Total sales, avg order value, customer growth
│   ├── models/                   # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── customer.py           # Customer model
│   │   ├── order.py              # Order model
│   │   ├── store.py              # Store model
│   │   ├── order_item.py         # OrderItem model
│   │   └── product.py            # Product model
│   ├── services/                 # Business logic
│   │   ├── __init__.py
│   │   ├── analytics.py          # Analysis functions (e.g., white-spot, distance)
│   │   ├── filters.py            # Filter logic
│   │   └── utils.py              # Utilities (e.g., Haversine distance)
│   └── config.py                 # API config (e.g., DB URI)
├── dash_app/                     # Frontend: Dash application
│   ├── __init__.py               # Dash app initialization
│   ├── components/               # Reusable components
│   │   ├── __init__.py
│   │   ├── filters.py            # Filters (state, date, product category)
│   │   ├── kpis.py               # KPI displays
│   │   ├── visualizations.py     # Charts, maps, tables
│   │   └── tooltips.py           # Info tooltips
│   ├── layouts/                  # Page layouts
│   │   ├── __init__.py
│   │   ├── main.py               # Main dashboard layout
│   │   ├── customer.py           # Customer analysis layout
│   │   ├── store.py              # Store analysis layout
│   │   ├── product.py            # Product analysis layout
│   │   └── order.py              # Order analysis layout
│   ├── callbacks/                # Dash callbacks
│   │   ├── __init__.py
│   │   ├── customer_callbacks.py # Customer visualization callbacks
│   │   ├── store_callbacks.py    # Store visualization callbacks
│   │   ├── product_callbacks.py  # Product visualization callbacks
│   │   ├── order_callbacks.py    # Order visualization callbacks
│   │   └── filter_callbacks.py   # Filter update callbacks
│   └── assets/                   # Static assets
│       ├── style.css             # Custom CSS
│       ├── custom.js             # Clientside JS
│       └── images/               # Logos, icons
├── data/                         # Database files
│   ├── migrations/               # DB migrations (e.g., Alembic)
│   │   ├── __init__.py
│   │   └── initial_schema.sql    # Initial schema
│   ├── scripts/                  # Data scripts
│   │   ├── __init__.py
│   │   └── generate_sample_data.py # Sample data generation
│   └── sample_data.db            # SQLite DB (development)
├── tests/                        # Tests
│   ├── __init__.py
│   ├── test_api/                 # API tests
│   │   ├── __init__.py
│   │   ├── test_customers.py     # Customer endpoint tests
│   │   ├── test_orders.py        # Order endpoint tests
│   │   ├── test_stores.py        # Store endpoint tests
│   │   ├── test_products.py      # Product endpoint tests
│   │   └── test_kpis.py          # KPI endpoint tests
│   └── test_dash/                # Dash tests
│       ├── __init__.py
│       └── test_visualizations.py # Visualization tests
├── docs.ConcurrentHashMap        # Documentation
│   ├── requirements.md           # Anforderungsanalyse
│   ├── setup.md                 # Setup instructions
│   └── api.md                    # API documentation
├── .gitignore                    # Git ignore
├── README.md                     # Project overview
├── requirements.txt              # Dependencies
├── Procfile                      # Deployment config
├── runtime.txt                   # Python version
├── wsgi.py                       # WSGI entry point
└── app.py                        # Main app entry point
```

### Endpoints (Derived from Anforderungsanalyse)
The `api/routes/` directory includes endpoints tailored to the requirements:
- **Customer Analysis**:
  - `/api/customers`: Customer geographic distribution (map data).
  - `/api/customers/density`: Customer density by state/city.
  - `/api/customers/top`: Top customers by purchase frequency.
  - `/api/customers/avg_order`: Average order value per customer.
  - `/api/customers/recurring`: Customers with multiple orders.
- **Order Analysis**:
  - `/api/orders/trend`: Monthly/annual sales trend.
  - `/api/orders/seasonal`: Seasonal sales patterns.
  - `/api/orders/volatility`: Orders with high volatility.
  - `/api/orders/avg_items`: Average items per order.
  - `/api/orders/avg_value`: Average order value.
  - `/api/orders/basket`: Frequently bought together products.
- **Store (Branch) Analysis**:
  - `/api/stores/sales`: Sales per store.
  - `/api/stores/sales_trend`: Sales trend per store (with comparison).
  - `/api/stores/sales_by_state`: Sales by state.
  - `/api/stores/customer_reach`: Number of customers per store.
  - `/api/stores/product_sales`: Product sales per store.
- **Product Analysis**:
  - `/api/products/top`: Top products by sales volume.
  - `/api/products/sales`: Sales by product/category.
  - `/api/products/performance`: Product performance by launch date.
  - `/api/products/avg_price`: Average price by category.
  - `/api/products/price_sales`: Price-sales correlation.
- **Geographical Analysis**:
  - `/api/geo/distance`: Average customer-store distance.
  - `/api/geo/assignment`: Customer-store assignment by proximity.
  - `/api/geo/potential_locations`: Potential new store locations.
  - `/api/geo/low_penetration`: Areas with low market penetration.
  - `/api/geo/white_spot`: Regions with customers but no nearby stores.
- **Trends and Predictions**:
  - `/api/trends/seasonal`: Seasonal trends by product category.
  - `/api/trends/growth`: Order/sales growth year-over-year.
  - `/api/trends/peak_times`: Peak sales times (e.g., holidays).
  - `/api/trends/warning`: Early warning for sales drops.
- **KPIs**:
  - `/api/kpis`: Total sales, average order value, customer growth.

---

## Dependencies

The project relies on Python packages to support Dash, Flask, database interactions, and testing. These are listed in `requirements.txt`.

### requirements.txt
```text
dash==2.17.1                   # Dash framework for frontend
dash-bootstrap-components==1.6.0 # Bootstrap components for responsive UI
plotly==5.22.0                 # Interactive visualizations
pandas==2.2.2                  # Data manipulation
numpy==1.26.4                  # Numerical computations
sqlalchemy==2.0.30             # Database ORM
flask==3.0.3                   # Backend API
gunicorn==22.0.0               # WSGI server for deployment
psycopg2-binary==2.9.9         # PostgreSQL driver (optional)
pytest==8.2.2                  # Unit testing
alembic==1.13.1                # Database migrations
requests==2.32.3               # API testing
```

### Installation
```bash
pip install -r requirements.txt
```

### Environment
- **Python**: 3.8+ (compatible with Pop!_OS).
- **Database**: SQLite (development), PostgreSQL (production).
- **Tools**: VS Code with Python and Pylance extensions.

---

## Notes
- **Data Schema**: The file structure supports the provided schema (`Customers`, `Orders`, `Stores`, `OrderItems`, `Products`) via SQLAlchemy models in `api/models/`.
- **Modularity**: Endpoints and components are organized by feature (e.g., customer, order) for maintainability.
- **Scalability**: The backend can be deployed separately, and caching (e.g., Redis) can be added.
- **Deployment**: `Procfile` and `wsgi.py` support hosting on Render/Heroku.
- **User Management**: Extend `api/routes/` with authentication endpoints (e.g., `/api/auth`) for user-specific dashboards.
- **Drill-down**: Supported by `dash_app/callbacks/` and `dcc.Store` for state management.

This structure and dependencies provide a solid foundation for implementing the dashboard while meeting all requirement

---

## **Datenflussdiagramm:**

![Datenflussdiagramm.png](https://github.com/marvingoenner/Project-Prog-Lab/blob/4fd27a48f8703328016c910f4a86d5dd89a68edf/Datenflussdiagramm.png)
