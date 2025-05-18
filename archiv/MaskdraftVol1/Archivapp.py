import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import os
import logging
from math import radians, cos, sin, asin, sqrt

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mockdaten-Verzeichnis
MOCK_DATA_DIR = "mock_data"

# Funktion zum Laden von Mockdaten
def load_mock_data(file_name):
    file_path = os.path.join(MOCK_DATA_DIR, file_name)
    try:
        df = pd.read_csv(file_path)
        logger.info(f"✅ Mockdaten aus {file_name} geladen: {len(df)} Zeilen")
        return df
    except Exception as e:
        logger.error(f"❌ Fehler beim Laden von {file_name}: {str(e)}")
        raise

# Mockdaten laden
try:
    customers_df = load_mock_data("customers.csv")
    orders_df = load_mock_data("orders.csv")
    orderitems_df = load_mock_data("orderitems.csv")
    products_df = load_mock_data("products.csv")
    ingredients_df = load_mock_data("ingredients.csv")
    productingredients_df = load_mock_data("productingredients.csv")
    stores_df = load_mock_data("stores.csv")

    # Datentypen korrigieren
    orders_df['orderDate'] = pd.to_datetime(orders_df['orderDate'])
    products_df['Launch'] = pd.to_datetime(products_df['Launch'])
except Exception as e:
    app = dash.Dash(__name__)
    app.layout = html.Div([
        html.H1("Fehler beim Laden der Mockdaten", className="text-danger text-center mt-5"),
        html.P(f"Fehler: {str(e)}", className="text-center")
    ])
    logger.error("Anwendung gestoppt wegen Fehler beim Laden der Mockdaten")
    raise SystemExit

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

# Navigation mit Dropdowns für Unterseiten
navbar = dbc.NavbarSimple(
    brand="Analyse-Dashboard",
    brand_href="/",
    color="dark",
    dark=True,
    fluid=True,
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Geografische Verteilung", href="/kundenanalyse/karte"),
                dbc.DropdownMenuItem("Ø Bestellwert", href="/kundenanalyse/bestellwert"),
                dbc.DropdownMenuItem("Wiederkehrende Kunden", href="/kundenanalyse/mehrfach"),
                dbc.DropdownMenuItem("Top-Kunden", href="/kundenanalyse/topkunden"),
                dbc.DropdownMenuItem("Kundendichte", href="/kundenanalyse/dichte"),
            ],
            nav=True,
            in_navbar=True,
            label="Kundenanalyse",
            className="nav-item"
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Kundenreichweite", href="/filialanalyse/kundenreichweite"),
                dbc.DropdownMenuItem("Ø Distanz", href="/filialanalyse/distanz"),
                dbc.DropdownMenuItem("Produktverkäufe", href="/filialanalyse/produkte"),
                dbc.DropdownMenuItem("Umsatz", href="/filialanalyse/umsatz"),
                dbc.DropdownMenuItem("Umsatz Zeitverlauf", href="/filialanalyse/zeitverlauf"),
                dbc.DropdownMenuItem("Umsatz nach Staat", href="/filialanalyse/staat"),
            ],
            nav=True,
            in_navbar=True,
            label="Filialanalyse",
            className="nav-item"
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Beliebteste Produkte", href="/produktanalyse/beliebt"),
                dbc.DropdownMenuItem("Umsatz", href="/produktanalyse/umsatz"),
                dbc.DropdownMenuItem("Launch-Performance", href="/produktanalyse/launchperformance"),
                dbc.DropdownMenuItem("Ø Preis", href="/produktanalyse/preise"),
                dbc.DropdownMenuItem("Preis-Verkauf Korrelation", href="/produktanalyse/korrelation"),
            ],
            nav=True,
            in_navbar=True,
            label="Produktanalyse",
            className="nav-item"
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Umsatz Zeitverlauf", href="/bestellanalyse/zeitverlauf"),
                dbc.DropdownMenuItem("Hohe Volatilität", href="/bestellanalyse/volatil"),
                dbc.DropdownMenuItem("Ø Bestellwert", href="/bestellanalyse/durchschnitt"),
                dbc.DropdownMenuItem("Ø Artikelanzahl", href="/bestellanalyse/artikelanzahl"),
                dbc.DropdownMenuItem("Kombikauf", href="/bestellanalyse/kombikauf"),
            ],
            nav=True,
            in_navbar=True,
            label="Bestellanalyse",
            className="nav-item"
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Ø Distanz", href="/geografisch/distanz"),
                dbc.DropdownMenuItem("Neue Standorte", href="/geografisch/standorte"),
                dbc.DropdownMenuItem("Kunden-Zuordnung", href="/geografisch/zuordnung"),
                dbc.DropdownMenuItem("White-Spot-Analyse", href="/geografisch/whitespots"),
                dbc.DropdownMenuItem("Wachstumsgebiete", href="/geografisch/wachstum"),
            ],
            nav=True,
            in_navbar=True,
            label="Geografische Analysen",
            className="nav-item"
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Saisonale Trends", href="/trends/saisonal"),
                dbc.DropdownMenuItem("Wachstum", href="/trends/wachstum"),
                dbc.DropdownMenuItem("Spitzenzeiten", href="/trends/spitzenzeiten"),
                dbc.DropdownMenuItem("Frühwarnsystem", href="/trends/fruehwarnung"),
            ],
            nav=True,
            in_navbar=True,
            label="Trends & Vorhersagen",
            className="nav-item"
        ),
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

def with_back_button(content):
    return html.Div([
        html.Div([
            dcc.Link("🏠 Zur Startseite", href="/", className="btn btn-secondary mb-4")
        ], style={"textAlign": "left", "marginLeft": "20px", "marginTop": "20px"}),
        content
    ])

start_page = html.Div([
    html.H1("Willkommen beim Analyse-Dashboard", className="text-center mb-4 animate__animated animate__fadeIn"),
    html.P("Wählen Sie eine Analyseart aus der Navigation oben.", className="text-center mb-4 text-light"),
])

topkunden_page = html.Div([
    html.H2("Top 10 Kunden nach Kaufhäufigkeit", className="text-center mb-4 animate__animated animate__fadeIn"),
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
    dbc.Row([
        dbc.Col([
            html.Label("Kunde auswählen:", className="text-light"),
            dcc.Dropdown(
                id="kunde-auswahl",
                options=[{"label": cid, "value": cid} for cid in sorted(orders_df["customerID"].unique())],
                value=None,
                placeholder="Kunden-ID auswählen",
                className="mb-3",
                style={
                    "backgroundColor": "#000000",
                    "color": "#fff",
                    "border": "1px solid #444",
                    "borderRadius": "4px"
                }
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
                style={
                    "backgroundColor": "#000000",
                    "color": "#fff",
                    "border": "1px solid #444",
                    "borderRadius": "4px"
                }
            )
        ], width=4)
    ], className="mb-4"),
    dcc.Graph(id="reichweite-karte", style={"height": "600px"})
])

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
                style={
                    "backgroundColor": "#000000",
                    "color": "#fff",
                    "border": "1px solid #444",
                    "borderRadius": "4px"
                }
            )
        ], width=4)
    ], className="mb-4"),
    dcc.Graph(id="launch-performance-graph")
])

korrelation_page = html.Div([
    html.H2("Korrelation Preis-Verkauf", className="text-center mb-4 animate__animated animate__fadeIn"),
    dcc.Graph(id="korrelation-grafik")
])

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
                style={
                    "backgroundColor": "#000000",
                    "color": "#fff",
                    "border": "1px solid #444",
                    "borderRadius": "4px"
                }
            )
        ], width=4)
    ], className="mb-4"),
    dcc.Graph(id="durchschnitt-plot"),
    html.H3("Details", className="text-light mb-3"),
    dash_table.DataTable(id="durchschnitt-tabelle", style_table={"overflowX": "auto"},
                         style_cell={"backgroundColor": "#2d2d2d", "color": "white", "border": "1px solid #444"},
                         style_header={"backgroundColor": "#1f77b4", "fontWeight": "bold", "color": "white"},
                         page_size=10, sort_action="native")
])

def haversine(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return 6371 * 2 * asin(sqrt(a))

app.layout = html.Div([
    dcc.Location(id="url"),
    navbar,
    dbc.Container(id="page-content", fluid=True, className="pt-4")
])

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    layouts = {
        "/": start_page,
        "/kundenanalyse/topkunden": with_back_button(topkunden_page),
        "/kundenanalyse/bestellwert": with_back_button(bestellwert_page),
        "/kundenanalyse/karte": with_back_button(kundenkarte_page),
        "/kundenanalyse/mehrfach": with_back_button(html.Div([
            html.H2("Wiederkehrende Kunden", className="text-center mb-4"),
            html.P("Diese Seite ist noch nicht implementiert.", className="text-center text-light")
        ])),
        "/kundenanalyse/dichte": with_back_button(html.Div([
            html.H2("Kundendichte", className="text-center mb-4"),
            html.P("Diese Seite ist noch nicht implementiert.", className="text-center text-light")
        ])),
        "/filialanalyse/kundenreichweite": with_back_button(reichweite_page),
        "/filialanalyse/distanz": with_back_button(html.Div([
            html.H2("Ø Distanz", className="text-center mb-4"),
            html.P("Diese Seite ist noch nicht implementiert.", className="text-center text-light")
        ])),
        "/filialanalyse/produkte": with_back_button(html.Div([
            html.H2("Produktverkäufe", className="text-center mb-4"),
            html.P("Diese Seite ist noch nicht implementiert.", className="text-center text-light")
        ])),
        "/filialanalyse/umsatz": with_back_button(html.Div([
            html.H2("Umsatz", className="text-center mb-4"),
            html.P("Diese Seite ist noch nicht implementiert.", className="text-center text-light")
        ])),
        "/filialanalyse/zeitverlauf": with_back_button(html.Div([
            html.H2("Umsatz Zeitverlauf", className="text-center mb-4"),
            html.P("Diese Seite ist noch nicht implementiert.", className="text-center text-light")
        ])),
        "/filialanalyse/staat": with_back_button(html.Div([
            html.H2("Umsatz nach Staat", className="text-center mb-4"),
            html.P("Diese Seite ist noch nicht implementiert.", className="text-center text-light")
        ])),
        "/produktanalyse/beliebt": with_back_button(beliebte_produkte_page),
        "/produktanalyse/umsatz": with_back_button(umsatz_produkt_page),
        "/produktanalyse/launchperformance": with_back_button(launchperformance_page),
        "/produktanalyse/korrelation": with_back_button(korrelation_page),
        "/produktanalyse/preise": with_back_button(html.Div([
            html.H2("Ø Preis", className="text-center mb-4"),
            html.P("Diese Seite ist noch nicht implementiert.", className="text-center text-light")
        ])),
        "/bestellanalyse/durchschnitt": with_back_button(durchschnitt_page),
        "/bestellanalyse/zeitverlauf": with_back_button(html.Div([
            html.H2("Umsatz Zeitverlauf", className="text-center mb-4"),
            html.P("Diese Seite ist noch nicht implementiert.", className="text-center text-light")
        ])),
        "/bestellanalyse/volatil": with_back_button(html.Div([
            html.H2("Hohe Volatilität", className="text-center mb-4"),
            html.P("Diese Seite ist noch nicht implementiert.", className="text-center text-light")
        ])),
        "/bestellanalyse/artikelanzahl": with_back_button(html.Div([
            html.H2("Ø Artikelanzahl", className="text-center mb-4"),
            html.P("Diese Seite ist noch nicht implementiert.", className="text-center text-light")
        ])),
        "/bestellanalyse/kombikauf": with_back_button(html.Div([
            html.H2("Kombikauf", className="text-center mb-4"),
            html.P("Diese Seite ist noch nicht implementiert.", className="text-center text-light")
        ])),
        "/geografisch/distanz": with_back_button(html.Div([
            html.H2("Ø Distanz", className="text-center mb-4"),
            html.P("Diese Seite ist noch nicht implementiert.", className="text-center text-light")
        ])),
        "/geografisch/standorte": with_back_button(html.Div([
            html.H2("Neue Standorte", className="text-center mb-4"),
            html.P("Diese Seite ist noch nicht implementiert.", className="text-center text-light")
        ])),
        "/geografisch/zuordnung": with_back_button(html.Div([
            html.H2("Kunden-Zuordnung", className="text-center mb-4"),
            html.P("Diese Seite ist noch nicht implementiert.", className="text-center text-light")
        ])),
        "/geografisch/whitespots": with_back_button(html.Div([
            html.H2("White-Spot-Analyse", className="text-center mb-4"),
            html.P("Diese Seite ist noch nicht implementiert.", className="text-center text-light")
        ])),
        "/geografisch/wachstum": with_back_button(html.Div([
            html.H2("Wachstumsgebiete", className="text-center mb-4"),
            html.P("Diese Seite ist noch nicht implementiert.", className="text-center text-light")
        ])),
        "/trends/saisonal": with_back_button(html.Div([
            html.H2("Saisonale Trends", className="text-center mb-4"),
            html.P("Diese Seite ist noch nicht implementiert.", className="text-center text-light")
        ])),
        "/trends/wachstum": with_back_button(html.Div([
            html.H2("Wachstum", className="text-center mb-4"),
            html.P("Diese Seite ist noch nicht implementiert.", className="text-center text-light")
        ])),
        "/trends/spitzenzeiten": with_back_button(html.Div([
            html.H2("Spitzenzeiten", className="text-center mb-4"),
            html.P("Diese Seite ist noch nicht implementiert.", className="text-center text-light")
        ])),
        "/trends/fruehwarnung": with_back_button(html.Div([
            html.H2("Frühwarnsystem", className="text-center mb-4"),
            html.P("Diese Seite ist noch nicht implementiert.", className="text-center text-light")
        ])),
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

@app.callback(
    Output("produkt-auswahl", "value"),
    [Input("select-all-products", "n_clicks")]
)
def select_all_products(n_clicks):
    if n_clicks > 0:
        return products_df["SKU"].tolist()
    return []

if __name__ == "__main__":
    app.run(debug=True)