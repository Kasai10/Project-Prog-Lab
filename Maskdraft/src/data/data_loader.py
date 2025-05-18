import pandas as pd
import os
import logging

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_mock_data(file_name, mock_data_dir="mock_data"):
    file_path = os.path.join(mock_data_dir, file_name)
    try:
        df = pd.read_csv(file_path)
        logger.info(f"✅ Mockdaten aus {file_name} geladen: {len(df)} Zeilen")
        return df
    except Exception as e:
        logger.error(f"❌ Fehler beim Laden von {file_name}: {str(e)}")
        raise

def load_all_data(mock_data_dir="mock_data"):
    try:
        customers_df = load_mock_data("customers.csv", mock_data_dir)
        orders_df = load_mock_data("orders.csv", mock_data_dir)
        orderitems_df = load_mock_data("orderitems.csv", mock_data_dir)
        products_df = load_mock_data("products.csv", mock_data_dir)
        ingredients_df = load_mock_data("ingredients.csv", mock_data_dir)
        productingredients_df = load_mock_data("productingredients.csv", mock_data_dir)
        stores_df = load_mock_data("stores.csv", mock_data_dir)

        # Datentypen korrigieren
        orders_df['orderDate'] = pd.to_datetime(orders_df['orderDate'])
        products_df['Launch'] = pd.to_datetime(products_df['Launch'])

        return {
            "customers_df": customers_df,
            "orders_df": orders_df,
            "orderitems_df": orderitems_df,
            "products_df": products_df,
            "ingredients_df": ingredients_df,
            "productingredients_df": productingredients_df,
            "stores_df": stores_df
        }
    except Exception as e:
        logger.error("Fehler beim Laden der Mockdaten")
        raise