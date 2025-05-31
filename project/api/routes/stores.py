from flask import Blueprint, jsonify
from db import query_db

stores_bp = Blueprint("stores", __name__)

#Does this say anything? Because obviously stores that have opened longer have the advantage here!
@stores_bp.route("/api/stores/revenue")
def get_revenue_per_store():
    data = query_db("""
        SELECT s.storeID, s.city, s.state,
               ROUND(SUM(oi.quantity * p.Price), 2) AS total_revenue
        FROM stores s
        JOIN orders o ON s.storeID = o.storeID
        JOIN orderItems oi ON o.orderID = oi.orderID
        JOIN products p ON oi.SKU = p.SKU
        GROUP BY s.storeID
        ORDER BY total_revenue DESC
    """)
    return jsonify(data)

@stores_bp.route("/api/stores/revenue_trend")
def get_revenue_trend():
    data = query_db("""
        SELECT s.storeID, strftime('%Y-%m', o.orderDate) AS month,
               ROUND(SUM(oi.quantity * p.Price), 2) AS monthly_revenue
        FROM stores s
        JOIN orders o ON s.storeID = o.storeID
        JOIN orderItems oi ON o.orderID = oi.orderID
        JOIN products p ON oi.SKU = p.SKU
        GROUP BY s.storeID, month
        ORDER BY s.storeID, month
    """)
    return jsonify(data)

@stores_bp.route("/api/stores/revenue_by_state_monthly")
def get_revenue_by_state_monthly():
    data = query_db("""
        SELECT s.state,
               strftime('%Y-%m', o.orderDate) AS month,
               ROUND(SUM(oi.quantity * p.Price), 2) AS monthly_revenue
        FROM stores s
        JOIN orders o ON s.storeID = o.storeID
        JOIN orderItems oi ON o.orderID = oi.orderID
        JOIN products p ON oi.SKU = p.SKU
        GROUP BY s.state, month
        ORDER BY s.state, month
    """)
    return jsonify(data)

#Does this approach also work? Latitude and longitude probably make more sense
@stores_bp.route("/api/stores/customer_reach")
def get_customer_reach():
    data = query_db("""
        SELECT s.storeID, s.city, s.state,
               COUNT(DISTINCT o.customerID) AS customer_count
        FROM stores s
        JOIN orders o ON s.storeID = o.storeID
        GROUP BY s.storeID
        ORDER BY customer_count DESC
    """)
    return jsonify(data)

@stores_bp.route("/api/stores/product_sales")
def get_product_sales_per_store():
    data = query_db("""
        SELECT s.storeID, oi.SKU, p.Name,
               SUM(oi.quantity) AS total_quantity
        FROM stores s
        JOIN orders o ON s.storeID = o.storeID
        JOIN orderItems oi ON o.orderID = oi.orderID
        JOIN products p ON oi.SKU = p.SKU
        GROUP BY s.storeID, oi.SKU
        ORDER BY s.storeID, total_quantity DESC
    """)
    return jsonify(data)

@stores_bp.route("/api/stores/avg_distance")
def get_avg_distance():
    data = query_db("""
        SELECT s.storeID, s.city, s.state,
               ROUND(AVG(
                   6371 * 2 * 
                   ASIN(
                       SQRT(
                           POWER(SIN(RADIANS((c.latitude - s.latitude) / 2)), 2) +
                           COS(RADIANS(s.latitude)) * COS(RADIANS(c.latitude)) *
                           POWER(SIN(RADIANS((c.longitude - s.longitude) / 2)), 2)
                       )
                   )
               ), 2) AS avg_distance_km
        FROM stores s
        JOIN orders o ON s.storeID = o.storeID
        JOIN customers c ON o.customerID = c.customerID
        GROUP BY s.storeID
        ORDER BY avg_distance_km
    """)
    return jsonify(data)
#test

