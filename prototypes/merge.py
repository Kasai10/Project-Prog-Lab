import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import mysql.connector
import os
from dotenv import load_dotenv
from math import radians, cos, sin, asin, sqrt

# Umgebungsvariablen laden
load_dotenv()

# MySQL-Verbindung
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# Daten laden
customers_df = pd.read_sql("SELECT * FROM customers", conn)
orders_df = pd.read_sql("SELECT * FROM orders", conn)
orderitems_df = pd.read_sql("SELECT * FROM orderitems", conn)
products_df = pd.read_sql("SELECT * FROM products", conn)
ingredients_df = pd.read_sql("SELECT * FROM ingredients", conn)
productingredients_df = pd.read_sql("SELECT * FROM productingredients", conn)
stores_df = pd.read_sql("SELECT * FROM stores", conn)

# Dash-App initialisieren
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.DARKLY,
        "https://use.fontawesome.com/releases/v5.15.4/css/all.css",
        "https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap",
        "https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"
    ]
)
app.title = "Erweitertes Analyse-Dashboard"
app.config.suppress_callback_exceptions = True

# Navigation
navbar = dbc.NavbarSimple(
    brand="Analyse-Dashboard",
    brand_href="/",
    color="dark",
    dark=True,
    fluid=True,
    children=[
        dbc.NavItem(dbc.NavLink("Kundenanalyse", href="/kundenanalyse", id="nav-kunden")),
        dbc.NavItem(dbc.NavLink("Filialanalyse", href="/filialanalyse", id="nav-filialen")),
        dbc.NavItem(dbc.NavLink("Produktanalyse", href="/produktanalyse", id="nav-produkte")),
        dbc.NavItem(dbc.NavLink("Bestellanalyse", href="/bestellanalyse", id="nav-bestellungen")),
        dbc.NavItem(dbc.NavLink("Geografische Analysen", href="/geografisch", id="nav-geografisch")),
        dbc.NavItem(dbc.NavLink("Trends & Vorhersagen", href="/trends", id="nav-trends")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Profil", href="#"),
                dbc.DropdownMenuItem("Einstellungen", href="#"),
                dbc.DropdownMenuItem("Abmelden", href="#")
            ],
            nav=True,
            in_navbar=True,
            label=html.I(className="fas fa-user-cog", style={"color": "white", "fontSize": "20px"})
        )
    ],
    className="mb-4"
)

# Hilfsfunktion für Zurück-Button
def with_back_button(content):
    return html.Div([
        html.Div([
            dcc.Link("🏠 Zur Startseite", href="/", className="btn btn-secondary mb-4")
        ], style={"textAlign": "left", "marginLeft": "20px", "marginTop": "20px"}),
        content
    ])

# Startseite
start_page = html.Div([
    html.H1("Willkommen beim Analyse-Dashboard", className="text-center mb-4 animate__animated animate__fadeIn"),
    html.P("Wählen Sie einen Bereich für detaillierte Analysen.", className="text-center mb-4 text-light"),
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Link("Kundenanalyse", href="/kundenanalyse"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Filialanalyse", href="/filialanalyse"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Produktanalyse", href="/produktanalyse"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Bestellanalyse", href="/bestellanalyse"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Geografische Analysen", href="/geografisch"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Trends & Vorhersagen", href="/trends"), body=True, className="mb-3 shadow"), width=4)
    ], justify="center")
])

# Kundenanalyse-Seite
kundenanalyse_page = html.Div([
    html.H2("Kundenanalyse", className="text-center mb-4 animate__animated animate__fadeIn"),
    html.P("Wählen Sie eine Analyseart:", className="text-center mb-4 text-light"),
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Link("Geografische Verteilung", href="/kundenanalyse/karte"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Ø Bestellwert", href="/kundenanalyse/bestellwert"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Wiederkehrende Kunden", href="/kundenanalyse/mehrfach"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Top-Kunden", href="/kundenanalyse/topkunden"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Kundendichte", href="/kundenanalyse/dichte"), body=True, className="mb-3 shadow"), width=4)
    ], justify="center")
])

# Filialanalyse-Seite
filialanalyse_page = html.Div([
    html.H2("Filialanalyse", className="text-center mb-4 animate__animated animate__fadeIn"),
    html.P("Wählen Sie eine Analyseart:", className="text-center mb-4 text-light"),
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Link("Kundenreichweite", href="/filialanalyse/kundenreichweite"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Ø Distanz", href="/filialanalyse/distanz"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Produktverkäufe", href="/filialanalyse/produkte"), body=True, className="mb-3 shadow"), width=4),
        kbc.Col(dbc.Card(dcc.Link("Umsatz", href="/filialanalyse/umsatz"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Umsatz Zeitverlauf", href="/filialanalyse/zeitverlauf"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Umsatz nach Staat", href="/filialanalyse/staat"), body=True, className="mb-3 shadow"), width=4)
    ], justify="center")
])

# Produktanalyse-Seite
produktanalyse_page = html.Div([
    html.H2("Produktanalyse", className="text-center mb-4 animate__animated animate__fadeIn"),
    html.P("Wählen Sie eine Analyseart:", className="text-center mb-4 text-light"),
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Link("Beliebteste Produkte", href="/produktanalyse/beliebt"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Umsatz", href="/produktanalyse/umsatz"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Launch-Performance", href="/produktanalyse/launchperformance"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Ø Preis", href="/produktanalyse/preise"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Preis-Verkauf Korrelation", href="/produktanalyse/korrelation"), body=True, className="mb-3 shadow"), width=4)
    ], justify="center")
])

# Bestellanalyse-Seite
bestellanalyse_page = html.Div([
    html.H2("Bestellanalyse", className="text-center mb-4 animate__animated animate__fadeIn"),
    html.P("Wählen Sie eine Analyseart:", className="text-center mb-4 text-light"),
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Link("Umsatz Zeitverlauf", href="/bestellanalyse/zeitverlauf"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Hohe Volatilität", href="/bestellanalyse/volatil"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Ø Bestellwert", href="/bestellanalyse/durchschnitt"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Ø Artikelanzahl", href="/bestellanalyse/artikelanzahl"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Kombikauf", href="/bestellanalyse/kombikauf"), body=True, className="mb-3 shadow"), width=4)
    ], justify="center")
])

# Geografische Analysen-Seite
geografischanalyse_page = html.Div([
    html.H2("Geografische Analysen", className="text-center mb-4 animate__animated animate__fadeIn"),
    html.P("Wählen Sie eine Analyseart:", className="text-center mb-4 text-light"),
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Link("Ø Distanz", href="/geografisch/distanz"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Neue Standorte", href="/geografisch/standorte"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Kunden-Zuordnung", href="/geografisch/zuordnung"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("White-Spot-Analyse", href="/geografisch/whitespots"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Wachstumsgebiete", href="/geografisch/wachstum"), body=True, className="mb-3 shadow"), width=4)
    ], justify="center")
])

# Trends & Vorhersagen-Seite
trends_page = html.Div([
    html.H2("Trends & Vorhersagen", className="text-center mb-4 animate__animated animate__fadeIn"),
    html.P("Wählen Sie eine Analyseart:", className="text-center mb-4 text-light"),
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Link("Saisonale Trends", href="/trends/saisonal"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Wachstum", href="/trends/wachstum"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Spitzenzeiten", href="/trends/spitzenzeiten"), body=True, className="mb-3 shadow"), width=4),
        dbc.Col(dbc.Card(dcc.Link("Frühwarnsystem", href="/trends/fruehwarnung"), body=True, className="mb-3 shadow"), width=4)
    ], justify="center")
])

# Kundenanalyse-Unterseiten
topkunden_page = html.Div([
    html.H2("Top 10 Kunden nach Kaufhäufigkeit", className="text-center mb-4 animate__animated animate__fadeIn"),
    # KPI-Karten
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Gesamtbestellungen", className="card-title"),
                html.H2(id="kpi-gesamtbestellungen", className="card-text")
            ])
        ], color="primary", inverse=True, className="shadow"), width=3),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Top-Kunde Bestellungen", className="card-title"),
                html.H2(id="kpi-topkunden", className="card-text")
            ])
        ], color="info", inverse=True, className="shadow"), width=3)
    ], className="mb-4"),
    dcc.Graph(id="topkunden-plot"),
    html.H3("Details", className="text-light mb-3"),
    dash_table.DataTable(id="topkunden-tabelle", style_table={"overflowX": "auto"},
                         style_cell={"backgroundColor": "#2d2d2d", "color": "white", "border": "1px solid #444"},
                         style_header={"backgroundColor": "#1f77b4", "fontWeight": "bold", "color": "white"},
                         page_size=10, sort_action="native")
])

bestellwert_page = html.Div([
    html.H2("Durchschnittlicher Bestellwert pro Kunde", className="text-center mb-4 animate__animated animate__fadeIn"),
    # Filter
    dbc.Row([
        dbc.Col([
            html.Label("Kunde auswählen:", className="text-light"),
            dcc.Dropdown(
                id="kunde-auswahl",
                options=[{"label": cid, "value": cid} for cid in sorted(orders_df["customerID"].unique())],
                value=None,
                placeholder="Kunden-ID auswählen",
                className="mb-3",
                style={"backgroundColor": "#333", "color": "#fff"}
            )
        ], width=4)
    ], className="mb-4"),
    # KPI-Karten
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Gesamt Ø Bestellwert", className="card-title"),
                html.H2(id="kpi-gesamt-durchschnitt", className="card-text")
            ])
        ], color="secondary", inverse=True, className="shadow"), width=3),
        dbc.Col(dbc.DataTable([
            html.H4("Ausgewählter Kunde Ø", className="card-title"),
            html.H2(id="kpi-kunden-durchschnitt", className="card-text")
        ], color="info", inverse=True, className="shadow"), width=3)
    ], className="mb-4"),
    dcc.Graph(id="bestellwert-plot"),
    html.H3("Details", className="text-light mb-3"),
    dash_table.DataTable(id="bestellwert-tabelle", style_table={"overflowX": "auto"},
                         style_cell={"backgroundColor": "#2d2d2d", "color": "white", "border": "1px solid #444"},
                         style_header={"backgroundColor": "#1f77b4", "fontWeight": "bold", "color": "white"},
                         page_size=10, sort_action="native", filter_action="native")
])

kundenkarte_page = html.Div([
    html.H2("Geografische Verteilung der Kunden", className="text-center mb-4 animate__animated animate__fadeIn"),
    dcc.Graph(id="kundenkarte", style={"height": "600px"})
])

# Filialanalyse-Unterseiten
reichweite_page = html.Div([
    html.H2("Kundenreichweite pro Filiale", className="text-center mb-4 animate__animated animate__fadeIn"),
    dbc.Row([
        dbc.Col([
            html.Label("Filiale auswählen:", className="text-light"),
            dcc.Dropdown(
                id="filial-dropdown",
                options=[{"label": f"{row['city']} – {row['storeID']}", "value": row["storeID"]}
                         for _, row in stores_df.iterrows()],
                placeholder="Filiale auswählen",
                className="mb-3",
                style={"backgroundColor": "#333", "color": "#fff"}
            )
        ], width=4)
    ], className="mb-4"),
    dcc.Graph(id="reichweite-karte", style={"height": "600px"})
])

# Produktanalyse-Unterseiten
beliebte_produkte_page = html.Div([
    html.H2("Beliebteste Produkte", className="text-center mb-4 animate__animated animate__fadeIn"),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Top-Produkt Verkäufe", className="card-title"),
                html.H2(id="kpi-topprodukt", className="card-text")
            ])
        ], color="primary", inverse=True, className="shadow"), width=3)
    ], className="mb-4"),
    dcc.Graph(id="beliebteste-produkte-plot"),
    html.H3("Details", className="text-light mb-3"),
    dash_table.DataTable(id="beliebteste-produkte-tabelle", style_table={"overflowX": "auto"},
                         style_cell={"backgroundColor": "#2d2d2d", "color": "white", "border": "1px solid #444"},
                         style_header={"backgroundColor": "#1f77b4", "fontWeight": "bold", "color": "white"},
                         page_size=10, sort_action="native")
])

umsatz_produkt_page = html.Div([
    html.H2("Umsatz pro Produkt", className="text-center mb-4 animate__animated animate__fadeIn"),
    dcc.Graph(id="umsatz-plot"),
    html.H3("Details", className="text-light mb-3"),
    dash_table.DataTable(id="umsatz-tabelle", style_table={"overflowX": "auto"},
                         style_cell={"backgroundColor": "#2d2d2d", "color": "white", "border": "1px solid #444"},
                         style_header={"backgroundColor": "#1f77b4", "fontWeight": "bold", "color": "white"},
                         page_size=10, sort_action="native")
])

launchperformance_page = html.Div([
    html.H2("Produktleistung nach Einführungsdatum", className="text-center mb-4 animate__animated animate__fadeIn"),
    dbc.Row([
        dbc.Col([
            html.Label("Zeiteinheit auswählen:", className="text-light"),
            dcc.RadioItems(
                id="zeit-einheit",
                options=[
                    {"label": "Täglich", "value": "D"},
                    {"label": "Monatlich", "value": "M"},
                    {"label": "Jährlich", "value": "Y"}
                ],
                value="M",
                labelStyle={"display": "inline-block", "margin-right": "15px"},
                className="mb-3"
            )
        ], width=4),
        dbc.Col([
            html.Label("Produkte auswählen:", className="text-light"),
            html.Button("Alle auswählen", id="select-all-products", n_clicks=0, className="btn btn-secondary mb-2"),
            dcc.Dropdown(
                id="produkt-auswahl",
                options=[{"label": name, "value": sku} for sku, name in products_df[["SKU", "Name"]].values],
                multi=True,
                placeholder="Produkte auswählen...",
                className="mb-3",
                style={"backgroundColor": "#333", "color": "#fff"}
            )
        ], width=4)
    ], className="mb-4"),
    dcc.Graph(id="launch-performance-graph")
])

korrelation_page = html.Div([
    html.H2("Korrelation Preis-Verkauf", className="text-center mb-4 animate__animated animate__fadeIn"),
    dcc.Graph(id="korrelation-grafik")
])

# Bestellanalyse-Unterseiten
durchschnitt_page = html.Div([
    html.H2("Durchschnittlicher Bestellwert", className="text-center mb-4 animate__animated animate__fadeIn"),
    dbc.Row([
        dbc.Col([
            html.Label("Kunde auswählen:", className="text-light"),
            dcc.Dropdown(
                id="kunde-auswahl",
                options=[{"label": cid, "value": cid} for cid in sorted(orders_df["customerID"].unique())],
                placeholder="Kunden-ID auswählen",
                className="mb-3",
                style={"backgroundColor": "#333", "color": "#fff"}
            )
        ], width=4)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Gesamt Ø Bestellwert", className="card-title"),
                html.H2(id="kpi-gesamt-durchschnitt", className="card-text")
            ])
        ], color="secondary", inverse=True, className="shadow"), width=3),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Ausgewählter Kunde Ø", className="card-title"),
                html.H2(id="kpi-kunden-durchschnitt", className="card-text")
            ])
        ], color="info", inverse=True, className="shadow"), width=3)
    ], className="mb-4"),
    dcc.Graph(id="durchschnitt-plot")
])

# Haversine-Funktion
def haversine(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return 6371 * 2 * asin(sqrt(a))

# Hauptlayout
app.layout = html.Div([
    navbar,
    dbc.Container(id="page-content", fluid=True, className="pt-4")
])

# Callbacks
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    layouts = {
        "/": start_page,
        "/kundenanalyse": with_back_button(kundenanalyse_page),
        "/kundenanalyse/topkunden": with_back_button(topkunden_page),
        "/kundenanalyse/bestellwert": with_back_button(bestellwert_page),
        "/kundenanalyse/karte": with_back_button(kundenkarte_page),
        "/filialanalyse": with_back_button(filialanalyse_page),
        "/filialanalyse/kundenreichweite": with_back_button(reichweite_page),
        "/produktanalyse": with_back_button(produktanalyse_page),
        "/produktanalyse/beliebt": with_back_button(beliebte_produkte_page),
        "/produktanalyse/umsatz": with_back_button(umsatz_produkt_page),
        "/produktanalyse/launchperformance": with_back_button(launchperformance_page),
        "/produktanalyse/korrelation": with_back_button(korrelation_page),
        "/bestellanalyse": with_back_button(bestellanalyse_page),
        "/bestellanalyse/durchschnitt": with_back_button(durchschnitt_page),
        "/geografisch": with_back_button(geografischanalyse_page),
        "/trends": with_back_button(trends_page)
    }
    return layouts.get(pathname, with_back_button(html.Div([
        html.H2("Seite nicht gefunden", className="text-center mt-5"),
        html.P("Diese URL existiert nicht.", className="text-center")
    ])))

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

@app.callback(
    [Output("beliebteste-produkte-tabelle", "data"),
     Output("beliebteste-produkte-tabelle", "columns"),
     Output("beliebteste-produkte-plot", "figure"),
     Output("kpi-topprodukt", "children")],
    Input("page-content", "children")
)
def update_beliebteste_produkte(_):
    merged = pd.merge(orderitems_df, products_df, on="SKU")
    grouped = merged.groupby("Name")["quantity"].sum().sort_values(ascending=False).reset_index()
    columns = [{"name": "Produkt", "id": "Name"}, {"name": "Verkaufte Einheiten", "id": "quantity"}]
    fig = px.bar(
        grouped,
        x="Name",
        y="quantity",
        title="Top-Produkte nach Verkaufsmenge",
        labels={"Name": "Produkt", "quantity": "Verkaufte Einheiten"},
        height=400
    )
    fig.update_layout(plot_bgcolor="#2d2d2d", paper_bgcolor="#2d2d2d", font_color="white")
    return (grouped.to_dict("records"), columns, fig, grouped["quantity"].iloc[0])

@app.callback(
    [Output("umsatz-tabelle", "data"),
     Output("umsatz-tabelle", "columns"),
     Output("umsatz-plot", "figure")],
    Input("page-content", "children")
)
def update_umsatz_tabelle(_):
    merged = orderitems_df.merge(products_df, on="SKU")
    merged["Umsatz"] = merged["quantity"] * merged["Price"]
    umsatz_df = merged.groupby("Name")["Umsatz"].sum().reset_index().sort_values(by="Umsatz", ascending=False)
    columns = [{"name": "Produkt", "id": "Name"}, {"name": "Umsatz (€)", "id": "Umsatz"}]
    fig = px.bar(
        umsatz_df,
        x="Name",
        y="Umsatz",
        title="Umsatz pro Produkt",
        height=400
    )
    fig.update_layout(plot_bgcolor="#2d2d2d", paper_bgcolor="#2d2d2d", font_color="white")
    return (umsatz_df.to_dict("records"), columns, fig)

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
    if time_unit == "D":
        merged["Zeit"] = merged["orderDate"].dt.date
    elif time_unit == "M":
        merged["Zeit"] = merged["orderDate"].dt.to_period("M").dt.to_timestamp()
    elif time_unit == "Y":
        merged["Zeit"] = merged["orderDate"].dt.to_period("Y").dt.to_timestamp()
    grouped = merged.groupby(["Zeit", "Name"]).agg({"Umsatz": "sum"}).reset_index()
    fig = px.line(
        grouped,
        x="Zeit",
        y="Umsatz",
        color="Name",
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
    fig = px.scatter(
        merged,
        x="Price",
        y="quantity",
        hover_name="Name",
        size="quantity",
        color="Category",
        title="Zusammenhang zwischen Preis und Verkaufsmenge",
        labels={"Price": "Preis (€)", "quantity": "Verkaufte Einheiten"},
        height=400
    )
    fig.update_layout(plot_bgcolor="#2d2d2d", paper_bgcolor="#2d2d2d", font_color="white")
    return fig

# Server starten
if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        conn.close()