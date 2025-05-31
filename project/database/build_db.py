import sqlite3
import pandas as pd
from pathlib import Path

# Connect and enable foreign keys
conn = sqlite3.connect("app.db")
conn.execute("PRAGMA foreign_keys = ON;")
cursor = conn.cursor()

def load_csv(table, csv_file, drop_cols=None):
    df = pd.read_csv(csv_file)
    if drop_cols:
        df.drop(columns=drop_cols, inplace=True)
    df.to_sql(table, conn, if_exists="append", index=False)

# === CREATE TABLES ===
cursor.executescript("""
DROP TABLE IF EXISTS orderItems;
DROP TABLE IF EXISTS orderItems_raw;
DROP TABLE IF EXISTS productingredients;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS ingredients;
DROP TABLE IF EXISTS stores;

CREATE TABLE customers (
    customerID TEXT PRIMARY KEY,
    latitude REAL,
    longitude REAL
);

CREATE TABLE stores (
    storeID TEXT PRIMARY KEY,
    zipcode INTEGER,
    state_abbr TEXT,
    latitude REAL,
    longitude REAL,
    city TEXT,
    state TEXT,
    distance REAL
);

CREATE TABLE products (
    SKU TEXT PRIMARY KEY,
    Name TEXT,
    Price REAL,
    Category TEXT,
    Size TEXT,
    Launch TEXT
);

CREATE TABLE ingredients (
    IngredientID INTEGER PRIMARY KEY,
    Name TEXT
);

CREATE TABLE productingredients (
    SKU TEXT,
    IngredientID INTEGER,
    PRIMARY KEY (SKU, IngredientID),
    FOREIGN KEY (SKU) REFERENCES products(SKU),
    FOREIGN KEY (IngredientID) REFERENCES ingredients(IngredientID)
);

CREATE TABLE orders (
    orderID INTEGER PRIMARY KEY,
    customerID TEXT,
    storeID TEXT,
    orderDate TEXT,
    nItems INTEGER,
    total REAL,
    FOREIGN KEY (customerID) REFERENCES customers(customerID),
    FOREIGN KEY (storeID) REFERENCES stores(storeID)
);

CREATE TABLE orderItems_raw (
    SKU TEXT,
    orderID INTEGER
);
""")

# === LOAD DATA ===
data_dir = Path(__file__).resolve().parent.parent / "data"

load_csv("customers", data_dir / "customers.csv")
load_csv("stores", data_dir / "stores.csv")
load_csv("products", data_dir / "products.csv", drop_cols=["Ingredients"])
load_csv("ingredients", data_dir / "ingredients.csv")
load_csv("orders", data_dir / "orders.csv")
load_csv("productingredients", data_dir / "productingredients.csv")
load_csv("orderItems_raw", data_dir / "orderItems.csv")

# === PROCESS orderItems_raw INTO orderItems ===
cursor.executescript("""
CREATE TABLE orderItems (
    SKU TEXT,
    orderID INTEGER,
    quantity INTEGER,
    PRIMARY KEY (SKU, orderID),
    FOREIGN KEY (SKU) REFERENCES products(SKU),
    FOREIGN KEY (orderID) REFERENCES orders(orderID)
);

INSERT INTO orderItems (SKU, orderID, quantity)
SELECT SKU, orderID, COUNT(*) AS quantity
FROM orderItems_raw
GROUP BY SKU, orderID;

DROP TABLE orderItems_raw;
""")

conn.commit()
conn.close()
print("✅ Database built successfully as app.db")
