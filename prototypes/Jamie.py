import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import mysql.connector
import os
from dotenv import load_dotenv
from math import radians, cos, sin, asin, sqrt
import plotly.graph_objects as go


load_dotenv()  # lädt .env-Datei
print("DB_HOST:", os.getenv("DB_HOST"))

# Verbindung mit Variablen aus .env
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

print("✅ Verbindung erfolgreich!")
conn.close()


# Daten aus MySQL laden
customers_df = pd.read_sql("SELECT * FROM customers", conn)
orders_df = pd.read_sql("SELECT * FROM orders", conn)
orderitems_df = pd.read_sql("SELECT * FROM orderitems", conn)
products_df = pd.read_sql("SELECT * FROM products", conn)
ingredients_df = pd.read_sql("SELECT * FROM ingredients", conn)
productingredients_df = pd.read_sql("SELECT * FROM productingredients", conn)
stores_df = pd.read_sql("SELECT * FROM stores", conn)





# === DASHBOARD-SEITEN ===

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.config.suppress_callback_exceptions = True

def with_back_button(content):
    return html.Div([
        html.Div([
            dcc.Link("\ud83c\udfe0 Zur Startseite", href="/", className="btn btn-secondary mb-4")
        ], style={"textAlign": "left", "marginLeft": "20px", "marginTop": "20px"}),
        content
    ])

# Startseite
start_page = html.Div([
    html.H1("Willkommen beim Dashboard-Auswertungen", className="text-center mb-4"),
    html.P("Wählen Sie einen Bereich aus, um detaillierte Analysen einzusehen.", className="text-center mb-4"),
    html.Div([
        dbc.Card(dcc.Link("Kundenanalyse", href="/kundenanalyse"), className="mb-3 text-center", body=True, style={"width": "50%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Filialanalyse", href="/filialanalyse"), className="mb-3 text-center", body=True, style={"width": "50%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Produktanalyse", href="/produktanalyse"), className="mb-3 text-center", body=True, style={"width": "50%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Bestellanalyse", href="/bestellanalyse"), className="mb-3 text-center", body=True, style={"width": "50%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Geografische Analysen", href="/geografisch"), className="mb-3 text-center", body=True, style={"width": "50%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Trends und Vorhersagen", href="/trends"), className="mb-3 text-center", body=True, style={"width": "50%", "margin": "0 auto"})
    ])
])

# Kundenanalyse Seite
kundenanalyse_page = html.Div([
    html.H2("Kundenanalyse – Optionen", className="text-center mb-4"),
    html.P("Wählen Sie eine Analyseart:", className="text-center mb-4"),
    html.Div([
        dbc.Card(dcc.Link("Geografische Verteilung der Kunden", href="/kundenanalyse/karte"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Durchschnittlicher Bestellwert pro Kunde", href="/kundenanalyse/bestellwert"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Wiederkehrende Kunden (mehr als eine Bestellung)", href="/kundenanalyse/mehrfach"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Kaufhäufigkeit pro Kunde (Top-Kunden)", href="/kundenanalyse/topkunden"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Kundendichte pro Bundesland oder Stadt", href="/kundenanalyse/dichte"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"})
    ])
])

# Filialanalyse Seite
filialanalyse_page = html.Div([
    html.H2("Filialanalyse – Optionen", className="text-center mb-4"),
    html.P("Wählen Sie eine Analyseart:", className="text-center mb-4"),
    html.Div([
        dbc.Card(dcc.Link("Kundenreichweite pro Filiale (Anzahl Kunden)", href="/filialanalyse/kundenreichweite"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Durchschnittliche Distanz zwischen Kunden und Filiale", href="/filialanalyse/distanz"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Produkt-Verkäufe pro Filiale", href="/filialanalyse/produkte"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Umsatz pro Filiale", href="/filialanalyse/umsatz"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Umsatz einzelner Filialen über Zeit", href="/filialanalyse/zeitverlauf"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Umsatz nach Staat", href="/filialanalyse/staat"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"})
    ])
])

# Produktanalyse Seite
produktanalyse_page = html.Div([
    html.H2("Produktanalyse – Optionen", className="text-center mb-4"),
    html.P("Wählen Sie eine Analyseart:", className="text-center mb-4"),
    html.Div([
        dbc.Card(dcc.Link("Beliebteste Produkte (Verkaufszahlen)", href="/produktanalyse/beliebt"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Umsatz pro Produkt oder Produktkategorie", href="/produktanalyse/umsatz"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Produktleistung nach Einführungsdatum", href="/produktanalyse/launchperformance"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Durchschnittspreis pro Produktkategorie", href="/produktanalyse/preise"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Korrelation zwischen Preis und Verkaufszahlen", href="/produktanalyse/korrelation"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"})
    ])
])

# Bestellanalyse Seite
bestellanalyse_page = html.Div([
    html.H2("Bestellanalyse – Optionen", className="text-center mb-4"),
    html.P("Wählen Sie eine Analyseart:", className="text-center mb-4"),
    html.Div([
        dbc.Card(dcc.Link("Umsatzentwicklung über die Zeit", href="/bestellanalyse/zeitverlauf"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Bestellungen mit hoher Volatilität", href="/bestellanalyse/volatil"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Durchschnittlicher Bestellwert", href="/bestellanalyse/durchschnitt"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Durchschnittliche Artikelanzahl pro Bestellung", href="/bestellanalyse/artikelanzahl"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Wird oft zusammen gekauft", href="/bestellanalyse/kombikauf"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"})
    ])
])

# Geografische Analyse Seite
geografischanalyse_page = html.Div([
    html.H2("Geografische Analysen – Optionen", className="text-center mb-4"),
    html.P("Wählen Sie eine Analyseart:", className="text-center mb-4"),
    html.Div([
        dbc.Card(dcc.Link("Durchschnittliche Distanz zwischen Kunden und Filialen", href="/geografisch/distanz"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Potenzielle Standorte für neue Filialen", href="/geografisch/standorte"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Kunden-Filial-Zuordnung basierend auf Nähe", href="/geografisch/zuordnung"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("White-Spot-Analyse", href="/geografisch/whitespots"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Gebiete mit geringem Marktanteil", href="/geografisch/wachstum"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"})
    ])
])

# Trends & Vorhersagen Seite
trends_page = html.Div([
    html.H2("Trends und Vorhersagen – Optionen", className="text-center mb-4"),
    html.P("Wählen Sie eine Analyseart:", className="text-center mb-4"),
    html.Div([
        dbc.Card(dcc.Link("Saisonale Verkaufstrends nach Produktkategorie", href="/trends/saisonal"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Wachstum der Bestellungen/Umsätze im Jahresvergleich", href="/trends/wachstum"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Identifikation von Spitzenzeiten (z. B. Feiertage)", href="/trends/spitzenzeiten"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"}),
        dbc.Card(dcc.Link("Frühwarnsystem für Umsatzrückgänge", href="/trends/fruehwarnung"), className="mb-3 text-center", body=True, style={"width": "60%", "margin": "0 auto"})
    ])
])

#UNTER SEITEN DER KUNDENANALYSE

# Top-Kunden-Seite
from dash.dependencies import Input, Output

topkunden_page = html.Div([
    html.H2("Top 10 Kunden nach Kaufhäufigkeit", className="text-center mb-4"),
    html.Div(id="topkunden-tabelle", className="text-center")
])

# Durchschnittlicher Bestellwert pro Kunde – Seite
bestellwert_page = html.Div([
    html.H2("Durchschnittlicher Bestellwert pro Kunde", className="text-center mb-4"),
    html.Div(id="bestellwert-tabelle", className="text-center"),
    html.Div(id="gesamt-bestellwert", className="text-center mt-4")
])

# Kundenkarte Seite – geografische Verteilung
kundenkarte_page = html.Div([
    html.H2("Geografische Verteilung der Kunden", className="text-center mb-4"),
    dcc.Graph(id="kundenkarte")
])

#UNTER SEITEN DER FILIALENANALYSE

# Kundenreichweite pro Filiale – Seite
reichweite_page = html.Div([
    html.H2("Kundenreichweite pro Filiale", className="text-center mb-4"),
    html.Label("Filiale auswählen:", className="text-light mb-2"),
    dcc.Dropdown(
        id="filial-dropdown",
        options=[{"label": f"{row['city']} – {row['storeID']}", "value": row["storeID"]}
                 for _, row in stores_df.iterrows()],
        placeholder="Filiale auswählen",
        className="mb-3"
    ),
    dcc.Graph(id="reichweite-karte")
])





#UNTER SEITEN DER PRODUKTANALYSE

# Beliebteste Produkte Seite
beliebte_produkte_page = html.Div([
    html.H2("Beliebteste Produkte (nach Verkaufszahlen)", className="text-center mb-4"),
    dcc.Graph(id="beliebteste-produkte-plot")
])

#Umsatz Produkt Seite
umsatz_produkt_page = html.Div([
    html.H2("Umsatz pro Produkt oder Produktkategorie", className="text-center mb-4"),
    html.Div(id="umsatz-tabelle", className="text-center")
])

# Produktleistung nach Einführungsdatum – Seite
# Produkt Launch Performance Seite
launchperformance_page = html.Div([
    html.H2("Produktleistung nach Einführungsdatum", className="text-center mb-4"),
    
    html.Div([
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
        ),

        html.Label("Produkte auswählen:", className="text-light mt-3"),
        html.Div([
            html.Button("Alle auswählen", id="select-all-products", n_clicks=0, className="btn btn-secondary mb-2"),
            dcc.Dropdown(
                id="produkt-auswahl",
                options=[{"label": name, "value": sku} for sku, name in products_df[["SKU", "Name"]].values],
                multi=True,
                placeholder="Produkte auswählen...",
                className="mb-4"
            ),
        ]),
        
        dcc.Graph(id="launch-performance-graph")
    ], className="px-4")
])


#Korrelations Seite
korrelation_page = html.Div([
    html.H2("Korrelation zwischen Preis und Verkaufszahlen", className="text-center mb-4"),
    dcc.Graph(id="korrelation-grafik")
])


#BESTELLANALYSE


#Umsatzentwicklung über die Zeit


#Durschnitt Bestellungspreis

durchschnitt_page = html.Div([
    html.H2("Durchschnittlicher Bestellwert", className="text-center mb-4"),

    html.Div([
        html.H5("Gesamtdurchschnitt aller Bestellungen:", className="mb-2"),
        html.Div(id="gesamt-durchschnitt", className="mb-4")
    ], style={"textAlign": "center"}),

    html.Div([
        html.Label("Kunde auswählen:", className="mb-2"),
        dcc.Dropdown(
            id="kunde-auswahl",
            options=[{"label": cid, "value": cid} for cid in sorted(orders_df["customerID"].unique())],
            placeholder="Kunden-ID auswählen",
            style={"width": "60%", "margin": "0 auto"}
        )
    ], className="mb-4 text-center"),

    html.Div(id="kunden-durchschnitt", className="text-center")
])





# Layout & Routing
app.layout = html.Div([
    dcc.Location(id="url"),
    html.Div(id="page-content", children=start_page)
])
@app.callback(
    Output("bestellwert-tabelle", "children"),
    Output("gesamt-bestellwert", "children"),
    Input("page-content", "children")
)
def update_bestellwert(content):
    if not content:
        return None, None
    df = orders_df.groupby("customerID")["total"].mean().reset_index()
    df.columns = ["Kunde", "Ø Bestellwert"]
    rows = [html.Tr([html.Th(col) for col in df.columns])]
    for _, row in df.iterrows():
        rows.append(html.Tr([
            html.Td(row["Kunde"]),
            html.Td(f"{row['Ø Bestellwert']:.2f} €")
        ]))
    tabelle = dbc.Table(
        [html.Thead(rows[0])] + [html.Tbody(rows[1:])],
        bordered=True, striped=True, hover=True, class_name="table-dark"
    )

    gesamt_durchschnitt = orders_df["total"].mean()
    gesamtausgabe = html.H5(f"Gesamtdurchschnitt aller Bestellungen: {gesamt_durchschnitt:.2f} €")
    return tabelle, gesamtausgabe

@app.callback(
    Output("kundenkarte", "figure"),
    Input("page-content", "children")
)
def update_kundenkarte(content):
    fig = px.scatter_mapbox(
        customers_df,
        lat="latitude",
        lon="longitude",
        hover_name="customerID",
        zoom=5,
        height=600
    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig



# Callback zur Anzeige der Topkunden
@app.callback(
    Output("topkunden-tabelle", "children"),
    Input("page-content", "children")
)
def update_topkunden(content):
    if not content:
        return None
    top_customers = orders_df.groupby("customerID").size().sort_values(ascending=False).head(10).reset_index()
    top_customers.columns = ["Kunde", "Anzahl Bestellungen"]
    # Farbliche Hervorhebung für Top 3
    row_styles = []
    for i in range(len(top_customers)):
        if i == 0:
            row_styles.append({'backgroundColor': '#FFD700'})  # Gold
        elif i == 1:
            row_styles.append({'backgroundColor': '#C0C0C0'})  # Silber
        elif i == 2:
            row_styles.append({'backgroundColor': '#CD7F32'})  # Bronze
        else:
            row_styles.append({})

    # Manuell erstellte Tabelle mit Stil pro Zeile
    header = [html.Thead(html.Tr([html.Th(col) for col in top_customers.columns]))]
    rows = [html.Tr([
    html.Td(f"🥇 {top_customers.iloc[i, 0]}" if i == 0 else \
            f"🥈 {top_customers.iloc[i, 0]}" if i == 1 else \
            f"🥉 {top_customers.iloc[i, 0]}" if i == 2 else top_customers.iloc[i, 0],
            style={"backgroundColor": "#FFD700"} if i == 0 else \
                  {"backgroundColor": "#C0C0C0"} if i == 1 else \
                  {"backgroundColor": "#CD7F32"} if i == 2 else {}),
    html.Td(top_customers.iloc[i, 1])
]) for i in range(len(top_customers))]
    table = dbc.Table(header + [html.Tbody(rows)], bordered=True, striped=True, hover=True, class_name="table-dark")
    return table

#Top Produkte

@app.callback(
    Output("beliebteste-produkte-plot", "figure"),
    Input("page-content", "children")
)
def update_beliebteste_produkte(content):
    merged = pd.merge(orderitems_df, products_df, on="SKU")
    grouped = merged.groupby("Name")["quantity"].sum().sort_values(ascending=False).reset_index()
    
    fig = px.bar(
        grouped,
        x="Name",
        y="quantity",
        title="Top-Produkte nach Verkaufsmenge",
        labels={"Name": "Produkt", "quantity": "Verkaufte Einheiten"}
    )
    fig.update_layout(template="plotly_dark")
    return fig

# Umsatz Produkte


@app.callback(
    Output("umsatz-tabelle", "children"),
    Input("page-content", "children")
)
def update_umsatz_tabelle(content):
    # Umsatz pro SKU berechnen (Summe der OrderItem-Menge × Produktpreis)
    merged = orderitems_df.merge(products_df, on="SKU")
    merged["Umsatz"] = merged["quantity"] * merged["Price"]

    # Gruppieren nach Produktname
    umsatz_df = merged.groupby("Name")["Umsatz"].sum().reset_index()
    umsatz_df = umsatz_df.sort_values(by="Umsatz", ascending=False)

    # Tabelle aufbauen
    rows = [html.Tr([html.Th(col) for col in umsatz_df.columns])]
    for _, row in umsatz_df.iterrows():
        rows.append(html.Tr([
            html.Td(row["Name"]),
            html.Td(f"{row['Umsatz']:.2f} €")
        ]))

    tabelle = dbc.Table(
        [html.Thead(rows[0])] + [html.Tbody(rows[1:])],
        bordered=True, striped=True, hover=True, class_name="table-dark"
    )

    return tabelle

#Performance after Launch
@app.callback(
    Output("launch-performance-graph", "figure"),
    Input("produkt-auswahl", "value"),
    Input("zeit-einheit", "value")
)
def update_launchperformance(selected_products, time_unit):
    if not selected_products:
        return px.line(title="Bitte Produkte auswählen")

    # Merge OrderItems mit Orders und Produkten
    merged = orderitems_df.merge(orders_df, on="orderID").merge(products_df, on="SKU")
    merged["orderDate"] = pd.to_datetime(merged["orderDate"])
    merged = merged[merged["SKU"].isin(selected_products)]

    # Umsatz berechnen
    merged["Umsatz"] = merged["Price"] * merged["quantity"]

    # Gruppierung nach Zeiteinheit
    if time_unit == "D":
        merged["Zeit"] = merged["orderDate"].dt.date  # als Date-Objekt
    elif time_unit == "M":
        merged["Zeit"] = merged["orderDate"].dt.to_period("M").dt.to_timestamp()
    elif time_unit == "Y":
        merged["Zeit"] = merged["orderDate"].dt.to_period("Y").dt.to_timestamp()

    grouped = merged.groupby(["Zeit", "Name"]).agg({"Umsatz": "sum"}).reset_index()

    # Plotly-Liniendiagramm
    fig = px.line(
        grouped,
        x="Zeit",
        y="Umsatz",
        color="Name",
        markers=True,
        title="Produktumsatz über Zeit"
    )

    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        height=600,
        xaxis_title="Zeit",
        yaxis_title="Umsatz (€)",
    )

    return fig

def haversine(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return 6371 * 2 * asin(sqrt(a))

@app.callback(
    Output("reichweite-karte", "figure"),
    Input("filial-dropdown", "value")
)
def update_reichweite_karte(filial_id):
    if not filial_id:
        return go.Figure()

    filiale = stores_df[stores_df["storeID"] == filial_id].iloc[0]
    radius_km = 50

    # Distanz zu allen Kunden berechnen
    customers_df["distance"] = customers_df.apply(
        lambda row: haversine(filiale["latitude"], filiale["longitude"], row["latitude"], row["longitude"]),
        axis=1
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
        mapbox_style="open-street-map",
        height=600
    )

    # Filiale selbst als roten Punkt anzeigen
    fig.add_trace(go.Scattermapbox(
        lat=[filiale["latitude"]],
        lon=[filiale["longitude"]],
        mode='markers',
        marker=go.scattermapbox.Marker(size=14, color='red'),
        name="Filiale"
    ))

    return fig


@app.callback(
    Output("korrelation-grafik", "figure"),
    Input("page-content", "children")
)
def update_korrelation(_):
    # Aggregierte Verkäufe pro SKU
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
        labels={"Price": "Preis (€)", "quantity": "Verkaufte Einheiten"}
    )
    fig.update_layout(template="plotly_dark")
    return fig

@app.callback(
    Output("gesamt-durchschnitt", "children"),
    Output("kunden-durchschnitt", "children"),
    Input("kunde-auswahl", "value")
)
def update_durchschnitt(selected_customer):
    gesamt = orders_df["total"].mean()
    gesamt_display = html.H4(f"{gesamt:.2f} €")

    if selected_customer:
        df = orders_df[orders_df["customerID"] == selected_customer]
        if not df.empty:
            durchschnitt = df["total"].mean()
            return gesamt_display, html.H5(f"Durchschnitt für {selected_customer}: {durchschnitt:.2f} €")
        else:
            return gesamt_display, html.P("Keine Bestellungen für diesen Kunden.")
    else:
        return gesamt_display, html.P("Bitte einen Kunden auswählen.")



@app.callback(
    dash.dependencies.Output("page-content", "children"),
    [dash.dependencies.Input("url", "pathname")]
)
def display_page(pathname):
    if pathname == "/":
        return start_page
    elif pathname == "/kundenanalyse":
        return with_back_button(kundenanalyse_page)
    elif pathname == "/kundenanalyse/topkunden":
        return with_back_button(topkunden_page)
    elif pathname == "/kundenanalyse/bestellwert":
        return with_back_button(bestellwert_page)
    elif pathname == "/kundenanalyse/karte":
        return with_back_button(kundenkarte_page)



    elif pathname == "/filialanalyse":
        return with_back_button(filialanalyse_page)
    elif pathname == "/filialanalyse/kundenreichweite":
        return with_back_button(reichweite_page)




    elif pathname == "/produktanalyse":
        return with_back_button(produktanalyse_page)
    elif pathname == "/produktanalyse/beliebt":
        return with_back_button(beliebte_produkte_page)
    elif pathname == "/produktanalyse/umsatz":
        return with_back_button(umsatz_produkt_page)
    elif pathname == "/produktanalyse/launchperformance":
        return with_back_button(launchperformance_page)
    elif pathname == "/produktanalyse/korrelation":
        return with_back_button(korrelation_page)



    elif pathname == "/bestellanalyse":
        return with_back_button(bestellanalyse_page)
    elif pathname == "/bestellanalyse/durchschnitt":
        return with_back_button(durchschnitt_page)


    elif pathname == "/geografisch":
        return with_back_button(geografischanalyse_page)
    

    elif pathname == "/trends":
        return with_back_button(trends_page)
    elif pathname == "/kundenanalyse/topkunden":
        return with_back_button(topkunden_page)
    elif pathname == "/kundenanalyse/bestellwert":
        return with_back_button(bestellwert_page)

    return with_back_button(html.Div([
        html.H2("Seite nicht gefunden", className="text-center mt-5"),
        html.P("Diese URL existiert nicht.", className="text-center")
    ]))

if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        conn.close()
