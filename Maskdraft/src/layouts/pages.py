import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table

def start_page():
    return html.Div([
        html.H1("Willkommen beim Analyse-Dashboard", className="text-center mb-4 animate__animated animate__fadeIn"),
        html.P("Wählen Sie eine Analyseart aus der Navigation oben.", className="text-center mb-4 text-light"),
    ])

def topkunden_page():
    return html.Div([
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

def bestellwert_page(orders_df):
    return html.Div([
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

def kundenkarte_page():
    return html.Div([
        html.H2("Geografische Verteilung der Kunden", className="text-center mb-4 animate__animated animate__fadeIn"),
        dcc.Graph(id="kundenkarte", style={"height": "600px"})
    ])

def reichweite_page(stores_df):
    return html.Div([
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

def beliebte_produkte_page():
    return html.Div([
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

def umsatz_produkt_page():
    return html.Div([
        html.H2("Umsatz pro Produkt", className="text-center mb-4 animate__animated animate__fadeIn"),
        dcc.Graph(id="umsatz-plot"),
        html.H3("Details", className="text-light mb-3"),
        dash_table.DataTable(id="umsatz-tabelle", style_table={"overflowX": "auto"},
                             style_cell={"backgroundColor": "#2d2d2d", "color": "white", "border": "1px solid #444"},
                             style_header={"backgroundColor": "#1f77b4", "fontWeight": "bold", "color": "white"},
                             page_size=10, sort_action="native")
    ])

def launchperformance_page(products_df):
    return html.Div([
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

def korrelation_page():
    return html.Div([
        html.H2("Korrelation Preis-Verkauf", className="text-center mb-4 animate__animated animate__fadeIn"),
        dcc.Graph(id="korrelation-grafik")
    ])

def durchschnitt_page(orders_df):
    return html.Div([
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