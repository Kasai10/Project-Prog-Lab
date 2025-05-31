from flask import Flask
from routes.customers import customers_bp
from routes.orders import orders_bp
from routes.stores import stores_bp

app = Flask(__name__)
app.register_blueprint(customers_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(stores_bp)


if __name__ == "__main__":
    app.run(debug=True)
