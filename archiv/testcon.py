import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# .env laden
load_dotenv()

# Verbindungskette (URL) erstellen
db_url = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
engine = create_engine(db_url)

# Verbindung und Daten abrufen
try:
    with engine.connect() as conn:
        print("✅ Verbindung zur Datenbank erfolgreich!")

        # Daten aus Tabellen abrufen
        customers_df = pd.read_sql("SELECT * FROM customers", conn)
        orders_df = pd.read_sql("SELECT * FROM orders", conn)
        orderitems_df = pd.read_sql("SELECT * FROM orderitems", conn)
        products_df = pd.read_sql("SELECT * FROM products", conn)
        ingredients_df = pd.read_sql("SELECT * FROM ingredients", conn)
        productingredients_df = pd.read_sql("SELECT * FROM productingredients", conn)
        stores_df = pd.read_sql("SELECT * FROM stores", conn)

        # Ausgabe: Übersicht über geladene Daten
        def print_overview(name, df):
            print(f"\n📄 {name}:")
            print(f"  ➤ Shape: {df.shape}")
            print(f"  ➤ Spalten: {list(df.columns)}")
            print(f"  ➤ Vorschau:")
            print(df.head(3))

        print_overview("Customers", customers_df)
        print_overview("Orders", orders_df)
        print_overview("OrderItems", orderitems_df)
        print_overview("Products", products_df)
        print_overview("Ingredients", ingredients_df)
        print_overview("ProductIngredients", productingredients_df)
        print_overview("Stores", stores_df)

except Exception as e:
    print("❌ Fehler bei der Verbindung:")
    print(e)
