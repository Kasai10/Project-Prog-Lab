from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

def register_callbacks(app, data):
    orders_df = data["orders_df"]
    customers_df = data["customers_df"]

    @app.callback(
        [Output("topkunden-tabelle", "data"),
         Output("topkunden-tabelle", "columns"),
         Output("topkunden-plot", "figure"),
         Output("kpi-gesamtbestellungen", "children"),
         Output("kpi-topkunden", "children")],
        Input("page-content", "children")
    )
    def update_topkunden(_):
        top_customers = orders_df.groupby("customerID").size().sort_values(ascending=False).head(10).reset_index()
        top_customers.columns = ["Kunde", "Anzahl Bestellungen"]
        columns = [{"name": col, "id": col} for col in top_customers.columns]
        fig = px.bar(
            top_customers,
            x="Kunde",
            y="Anzahl Bestellungen",
            title="Top 10 Kunden nach Kaufhäufigkeit",
            color="Kunde",
            height=400
        )
        fig.update_layout(plot_bgcolor="#2d2d2d", paper_bgcolor="#2d2d2d", font_color="white")
        return (top_customers.to_dict("records"), columns, fig, len(orders_df), top_customers["Anzahl Bestellungen"].iloc[0])

    @app.callback(
        [Output("bestellwert-tabelle", "data"),
         Output("bestellwert-tabelle", "columns"),
         Output("bestellwert-plot", "figure"),
         Output("kpi-gesamt-durchschnitt", "children"),
         Output("kpi-kunden-durchschnitt", "children")],
        [Input("kunde-auswahl", "value")]
    )
    def update_bestellwert(selected_customer):
        df = orders_df.groupby("customerID")["total"].mean().reset_index()
        df.columns = ["Kunde", "Ø Bestellwert"]
        df["Ø Bestellwert"] = df["Ø Bestellwert"].round(2)
        columns = [{"name": col, "id": col} for col in df.columns]
        fig = px.bar(
            df,
            x="Kunde",
            y="Ø Bestellwert",
            title="Ø Bestellwert pro Kunde",
            color="Kunde",
            height=400
        )
        fig.update_layout(plot_bgcolor="#2d2d2d", paper_bgcolor="#2d2d2d", font_color="white")
        gesamt = f"{orders_df['total'].mean():.2f} €"
        kunden_durchschnitt = "Wähle einen Kunden"
        if selected_customer:
            df_selected = orders_df[orders_df["customerID"] == selected_customer]
            kunden_durchschnitt = f"{df_selected['total'].mean():.2f} €" if not df_selected.empty else "Keine Daten"
        return (df.to_dict("records"), columns, fig, gesamt, kunden_durchschnitt)

    @app.callback(
        Output("kundenkarte", "figure"),
        Input("page-content", "children")
    )
    def update_kundenkarte(_):
        fig = px.scatter_mapbox(
            customers_df,
            lat="latitude",
            lon="longitude",
            hover_name="customerID",
            zoom=5,
            height=600
        )
        fig.update_layout(mapbox_style="open-street-map", plot_bgcolor="#2d2d2d", paper_bgcolor="#2d2d2d", font_color="white")
        return fig