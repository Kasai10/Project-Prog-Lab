from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

def register_callbacks(app, data):
    orders_df = data["orders_df"]

    @app.callback(
        [Output("durchschnitt-tabelle", "data"),
         Output("durchschnitt-tabelle", "columns"),
         Output("durchschnitt-plot", "figure")],
        Input("kunde-auswahl", "value")
    )
    def update_durchschnitt(selected_customer):
        df = orders_df.groupby("customerID")["total"].mean().reset_index()
        df.columns = ["Kunde", "Ø Bestellwert"]
        df["Ø Bestellwert"] = df["Ø Bestellwert"].round(2)
        columns = [{"name": col, "id": col} for col in df.columns]
        fig_data = df
        if selected_customer:
            fig_data = df[df["Kunde"] == selected_customer]
        fig = px.bar(
            fig_data,
            x="Kunde",
            y="Ø Bestellwert",
            title="Ø Bestellwert pro Kunde",
            color="Kunde",
            height=400
        )
        fig.update_layout(plot_bgcolor="#2d2d2d", paper_bgcolor="#2d2d2d", font_color="white")
        return (df.to_dict("records"), columns, fig)