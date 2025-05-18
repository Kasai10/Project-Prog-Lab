from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from src.utils.helpers import haversine

def register_callbacks(app, data):
    stores_df = data["stores_df"]
    customers_df = data["customers_df"]

    @app.callback(
        Output("reichweite-karte", "figure"),
        Input("filial-dropdown", "value")
    )
    def update_reichweite_karte(filial_id):
        if not filial_id:
            return go.Figure()
        filiale = stores_df[stores_df["storeID"] == filial_id].iloc[0]
        radius_km = 50
        customers_df["distance"] = customers_df.apply(
            lambda row: haversine(filiale["latitude"], filiale["longitude"], row["latitude"], row["longitude"]), axis=1
        )
        customers_df["in_range"] = customers_df["distance"] <= radius_km
        fig = px.scatter_mapbox(
            customers_df,
            lat="latitude",
            lon="longitude",
            color="in_range",
            hover_name="customerID",
            zoom=6,
            center={"lat": filiale["latitude"], "lon": filiale["longitude"]},
            height=600
        )
        fig.add_trace(go.Scattermapbox(
            lat=[filiale["latitude"]],
            lon=[filiale["longitude"]],
            mode='markers',
            marker=go.scattermapbox.Marker(size=14, color='red'),
            name="Filiale"
        ))
        fig.update_layout(mapbox_style="open-street-map", plot_bgcolor="#2d2d2d", paper_bgcolor="#2d2d2d", font_color="white")
        return fig