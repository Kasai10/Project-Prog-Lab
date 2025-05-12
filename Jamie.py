import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# === MOCKDATEN ERZEUGEN ===
np.random.seed(42)

# Produkte
products_df = pd.DataFrame({
    'SKU': [f'PROD{i:04d}' for i in range(1, 11)],
    'Name': [f'Product {i}' for i in range(1, 11)],
    'Price': np.random.uniform(10, 100, 10).round(2),
    'Category': np.random.choice(['Electronics', 'Clothing', 'Food'], 10),
    'Size': np.random.choice(['S', 'M', 'L', 'XL'], 10),
    'Launch_DATE': [datetime.now() - timedelta(days=np.random.randint(0, 365)) for _ in range(10)]
})

# Zutaten
ingredients_df = pd.DataFrame({
    'IngredientID': range(1, 6),
    'Name': [f'Ingredient {i}' for i in range(1, 6)]
})

# Produkt-Zutaten-Zuordnung
productingredients_df = pd.DataFrame({
    'SKU': np.random.choice(products_df['SKU'], 20),
    'IngredientID': np.random.randint(1, 6, 20)
})

# Kunden
customers_df = pd.DataFrame({
    'customerID': [f'CUST{i:04d}' for i in range(1, 21)],
    'latitude': np.random.uniform(-90, 90, 20),
    'longitude': np.random.uniform(-180, 180, 20)
})

# Filialen
stores_df = pd.DataFrame({
    'storeID': [f'STORE{i:02d}' for i in range(1, 6)],
    'zipcode': np.random.randint(10000, 99999, 5),
    'state_abbr': np.random.choice(['CA', 'NY', 'TX', 'FL'], 5),
    'latitude': np.random.uniform(-90, 90, 5),
    'longitude': np.random.uniform(-180, 180, 5),
    'city': np.random.choice(['Los Angeles', 'New York', 'Houston', 'Miami'], 5),
    'state': np.random.choice(['California', 'New York', 'Texas', 'Florida'], 5),
    'distance': np.random.uniform(0, 100, 5).round(2)
})

# Bestellungen
orders_df = pd.DataFrame({
    'orderID': range(1, 31),
    'customerID': np.random.choice(customers_df['customerID'], 30),
    'storeID': np.random.choice(stores_df['storeID'], 30),
    'orderDate': [datetime.now() - timedelta(days=np.random.randint(0, 180)) for _ in range(30)],
    'nItems': np.random.randint(1, 10, 30),
    'total': np.random.uniform(10, 500, 30).round(2)
})

# Bestellpositionen
orderitems_df = pd.DataFrame({
    'orderID': np.random.randint(1, 31, 50),
    'SKU': np.random.choice(products_df['SKU'], 50),
    'quantity': np.random.randint(1, 5, 50)
})

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



    elif pathname == "/filialanalyse":
        return with_back_button(filialanalyse_page)
    elif pathname == "/produktanalyse":
        return with_back_button(produktanalyse_page)
    elif pathname == "/bestellanalyse":
        return with_back_button(bestellanalyse_page)
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
    app.run(debug=True)
