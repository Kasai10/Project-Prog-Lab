from flask import Blueprint, jsonify
from db import query_db

customers_bp = Blueprint("customers", __name__)

# 1. GET /api/customers: Geographic distribution
@customers_bp.route("/api/customers")
def get_customers_geo_distribution():
    """
    Return all customers with their geolocation data
    """
    data = query_db("""
        SELECT customerID, latitude, longitude FROM customers
    """)
    return jsonify(data)


# 2. GET /api/customers/density: Density by state/city
@customers_bp.route("/api/customers/density")
def get_customer_density():
    """
    Return number of customers per state/city
    """
    data = query_db("""
        SELECT 
        s.state, 
        s.city, 
        COUNT(DISTINCT o.customerID) AS count
        FROM orders o
        JOIN stores s ON o.storeID = s.storeID
        GROUP BY s.state, s.city
    """)
    return jsonify(data)


# 3. GET /api/customers/top: Top customers by purchase frequency
@customers_bp.route("/api/customers/top")
def get_top_customers():
    """
    Return customers sorted by number of orders
    """
    data = query_db("""
        SELECT 
        c.customerID, 
        COUNT(*) AS order_count
        FROM customers c
        JOIN orders o ON o.customerID = c.customerID
        GROUP BY c.customerID
        ORDER BY order_count DESC
    """)
    return jsonify(data)


# 4. GET /api/customers/avg_order: Average order value per customer
@customers_bp.route("/api/customers/avg_order")
def get_avg_order_value_per_customer():
    """
    Return average order value per customer
    """
    data = query_db("""
        SELECT customerID, AVG(total) as avg_order_value
        FROM orders
        GROUP BY customerID
    """)
    return jsonify(data)


# 5. GET /api/customers/recurring: Recurring customers
@customers_bp.route("/api/customers/recurring")
def get_recurring_customers():
    """
    Return customers with more than one order
    """
    data = query_db("""
        SELECT 
        customerID, 
        COUNT(*) AS order_count
        FROM orders
        GROUP BY customerID
        HAVING COUNT(*) > 1
        ORDER BY order_count ASC
    """)
    return jsonify(data)

# 6. GET /api/customers/onetime: One-time customers
@customers_bp.route("/api/customers/onetime")
def get_onetime_customers():
    """
    Return customers who placed exactly one order
    """
    data = query_db("""
        SELECT 
            customerID, 
            COUNT(*) AS order_count
        FROM orders
        GROUP BY customerID
        HAVING COUNT(*) = 1
        ORDER BY customerID ASC
    """)
    return jsonify(data)
#idee auswertungen für one time kunden, die geografische verteilung zeigen + stores, wo das oft passiert