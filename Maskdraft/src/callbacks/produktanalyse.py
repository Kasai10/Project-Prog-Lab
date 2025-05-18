from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

def register_callbacks(app, data):
    orderitems_df = data["orderitems_df"]
    products_df = data["products_df"]
    orders_df = data["orders_df"]

    @app.callback(
        [Output("beliebteste-produkte-tabelle", "data"),
         Output("beliebteste-produkte-tabelle", "columns"),
         Output("beliebteste-produkte-plot", "figure"),
         Output("kpi-topprodukt", "children")],
        Input("page-content", "children")
    )
    def update_beliebteste_produkte(_):
        merged = pd.merge(orderitems_df, products_df, on="SKU")
        grouped = merged.groupby(["Name", "Size"])["quantity"].sum().sort_values(ascending=False).reset_index()
        grouped["Produkt"] = grouped["Name"] + " (" + grouped["Size"] + ")"
        columns = [{"name": "Produkt", "id": "Produkt"}, {"name": "Verkaufte Einheiten", "id": "quantity"}]
        fig = px.bar(
            grouped,
            x="Produkt",
            y="quantity",
            title="Top-Produkte nach Verkaufsmenge",
            labels={"Produkt": "Produkt", "quantity": "Verkaufte Einheiten"},
            height=400
        )
        fig.update_layout(plot_bgcolor="#2d2d2d", paper_bgcolor="#2d2d2d", font_color="white", xaxis_tickangle=45)
        return (grouped[["Produkt", "quantity"]].to_dict("records"), columns, fig, grouped["quantity"].iloc[0])

    @app.callback(
        [Output("umsatz-tabelle", "data"),
         Output("umsatz-tabelle", "columns"),
         Output("umsatz-plot", "figure")],
        Input("page-content", "children")
    )
    def update_umsatz_tabelle(_):
        merged = orderitems_df.merge(products_df, on="SKU")
        merged["Umsatz"] = merged["quantity"] * merged["Price"]
        umsatz_df = merged.groupby(["Name", "Size"])["Umsatz"].sum().reset_index().sort_values(by="Umsatz", ascending=False)
        umsatz_df["Produkt"] = umsatz_df["Name"] + " (" + umsatz_df["Size"] + ")"
        umsatz_df["Umsatz"] = umsatz_df["Umsatz"].round(2)
        columns = [{"name": "Produkt", "id": "Produkt"}, {"name": "Umsatz (€)", "id": "Umsatz"}]
        fig = px.bar(
            umsatz_df,
            x="Produkt",
            y="Umsatz",
            title="Umsatz pro Produkt",
            height=400
        )
        fig.update_layout(plot_bgcolor="#2d2d2d", paper_bgcolor="#2d2d2d", font_color="white", xaxis_tickangle=45)
        return (umsatz_df[["Produkt", "Umsatz"]].to_dict("records"), columns, fig)

    @app.callback(
        Output("launch-performance-graph", "figure"),
        [Input("produkt-auswahl", "value"),
         Input("zeit-einheit", "value")]
    )
    def update_launchperformance(selected_products, time_unit):
        if not selected_products:
            return px.line(title="Bitte Produkte auswählen")
        merged = orderitems_df.merge(orders_df, on="orderID").merge(products_df, on="SKU")
        merged["orderDate"] = pd.to_datetime(merged["orderDate"])
        merged = merged[merged["SKU"].isin(selected_products)]
        merged["Umsatz"] = merged["Price"] * merged["quantity"]
        merged["Produkt"] = merged["Name"] + " (" + merged["Size"] + ")"
        if time_unit == "D":
            merged["Zeit"] = merged["orderDate"].dt.date
        elif time_unit == "M":
            merged["Zeit"] = merged["orderDate"].dt.to_period("M").dt.to_timestamp()
        elif time_unit == "Y":
            merged["Zeit"] = merged["orderDate"].dt.to_period("Y").dt.to_timestamp()
        grouped = merged.groupby(["Zeit", "Produkt"]).agg({"Umsatz": "sum"}).reset_index()
        fig = px.line(
            grouped,
            x="Zeit",
            y="Umsatz",
            color="Produkt",
            markers=True,
            title="Produktumsatz über Zeit",
            height=600
        )
        fig.update_layout(plot_bgcolor="#2d2d2d", paper_bgcolor="#2d2d2d", font_color="white")
        return fig

    @app.callback(
        Output("korrelation-grafik", "figure"),
        Input("page-content", "children")
    )
    def update_korrelation(_):
        sales = orderitems_df.groupby("SKU")["quantity"].sum().reset_index()
        merged = pd.merge(sales, products_df, on="SKU")
        merged["Produkt"] = merged["Name"] + " (" + merged["Size"] + ")"
        fig = px.scatter(
            merged,
            x="Price",
            y="quantity",
            hover_name="Produkt",
            size="quantity",
            color="Category",
            title="Zusammenhang zwischen Preis und Verkaufsmenge",
            labels={"Price": "Preis (€)", "quantity": "Verkaufte Einheiten"},
            height=400
        )
        fig.update_layout(plot_bgcolor="#2d2d2d", paper_bgcolor="#2d2d2d", font_color="white")
        return fig

    @app.callback(
        Output("produkt-auswahl", "value"),
        [Input("select-all-products", "n_clicks")]
    )
    def select_all_products(n_clicks):
        if n_clicks > 0:
            return products_df["SKU"].tolist()
        return []