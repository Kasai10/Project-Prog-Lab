from flask import Blueprint, jsonify
from db import query_db

orders_bp = Blueprint("orders", __name__)

# 1. GET /api/orders/volatility: Products with high variance in order counts (all-time volatility)
# How...............
@orders_bp.route("/api/orders/volatility")
def get_order_volatility():
    """
    Return products with high variance in order count across all orders (all-time volatility)
    """
    data = query_db("""
        //TODO
    """)
    return jsonify(data)


# 2. GET /api/orders/avg_items: Average items per order
@orders_bp.route("/api/orders/avg_items")
def get_avg_items_per_order():
    """
    Return average number of items per order
    """
    data = query_db("""
        SELECT ROUND(AVG(total_items), 2) AS avg_items
        FROM (
            SELECT orderID, SUM(quantity) AS total_items
            FROM orderItems
            GROUP BY orderID
        )
    """)
    return jsonify(data)


# 3. GET /api/orders/avg_value: Average order value
@orders_bp.route("/api/orders/avg_value")
def get_avg_order_value():
    """
    Return average value per order
    """
    data = query_db("""
        SELECT ROUND(AVG(order_total), 2) AS avg_order_value
        FROM (
            SELECT o.orderID, SUM(p.Price * oi.quantity) AS order_total
            FROM orders o
            JOIN orderItems oi ON o.orderID = oi.orderID
            JOIN products p ON oi.SKU = p.SKU
            GROUP BY o.orderID
        )
    """)
    return jsonify(data)


# 4. GET /api/orders/basket: Frequently bought together
# Was difficult because how do i query all subsets and sum them up?
#"We want to see how often one or more products are bought together in orders, including all smaller groups, but counting all possible combinations is complex and hard to do efficiently with SQL alone."
@orders_bp.route("/api/orders/basket")
def get_frequently_bought_together():
    """
    Return most common product pairs bought together
    """
    data = query_db("""
        //TODO
    """)
    return jsonify(data)
