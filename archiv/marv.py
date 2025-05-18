import dash
from dash import html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Expanded mock data for customer analysis
np.random.seed(42)
n_customers = 20
dates = [datetime(2024, 1, 1) + timedelta(days=x) for x in range(n_customers)]
df_kunden = pd.DataFrame({
    "Kunde": [f"K{str(i).zfill(2)}" for i in range(1, n_customers + 1)],
    "Bestellwert": np.random.randint(100, 500, n_customers),
    "Wiederkehrend": np.random.choice([True, False], n_customers, p=[0.6, 0.4]),
    "Stadt": np.random.choice(
        ["Frankfurt", "Berlin", "München", "Hamburg", "Stuttgart", "Köln", "Düsseldorf"],
        n_customers
    ),
    "Bestelldatum": dates,
    "Produktkategorie": np.random.choice(
        ["Elektronik", "Kleidung", "Haushalt", "Lebensmittel"], n_customers
    ),
    "Bewertung": np.random.randint(1, 6, n_customers)
})

# Create visualizations
# Bar chart for average order value per customer
fig_bestellwert = px.bar(
    df_kunden,
    x="Kunde",
    y="Bestellwert",
    title="Ø Bestellwert pro Kunde",
    color="Kunde",
    height=400
)
fig_bestellwert.update_layout(
    plot_bgcolor="#2d2d2d",
    paper_bgcolor="#2d2d2d",
    font_color="white",
    margin=dict(l=50, r=50, t=50, b=50)
)

# Pie chart for recurring vs non-recurring customers
fig_wiederkehrend = px.pie(
    df_kunden,
    names="Wiederkehrend",
    title="Anteil wiederkehrender Kunden",
    color_discrete_sequence=["#1f77b4", "#ff7f0e"],
    height=400
)
fig_wiederkehrend.update_layout(
    plot_bgcolor="#2d2d2d",
    paper_bgcolor="#2d2d2d",
    font_color="white",
    margin=dict(l=50, r=50, t=50, b=50)
)

# Scatter plot for order value by city
fig_stadt = px.scatter(
    df_kunden,
    x="Bestelldatum",
    y="Bestellwert",
    color="Stadt",
    size="Bewertung",
    title="Bestellwert nach Stadt und Datum",
    height=400
)
fig_stadt.update_layout(
    plot_bgcolor="#2d2d2d",
    paper_bgcolor="#2d2d2d",
    font_color="white",
    margin=dict(l=50, r=50, t=50, b=50)
)

# Initialize Dash app with Darkly theme and FontAwesome
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.DARKLY,
        "https://use.fontawesome.com/releases/v5.15.4/css/all.css",
        "https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap"
    ]
)
app.title = "Erweitertes Dashboard"

# Custom CSS for enhanced styling
app.css.append_css({
    "external_url": (
        "https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"
    )
})

# Navigation bar with additional items
navbar = dbc.NavbarSimple(
    brand="Erweitertes Dashboard",
    brand_href="#",
    color="dark",
    dark=True,
    fluid=True,
    children=[
        dbc.NavItem(dbc.NavLink("Dashboards", href="#", id="nav-dashboards")),
        dbc.NavItem(dbc.NavLink("Analysen", href="#", id="nav-analysen")),
        dbc.NavItem(dbc.NavLink("Datenfilter", href="#", id="nav-filter")),
        dbc.NavItem(dbc.NavLink("Kunden", href="#", id="nav-kunden")),
        dbc.NavItem(dbc.NavLink("Stores", href="#", id="nav-stores")),
        dbc.NavItem(dbc.NavLink("Produkte", href="#", id="nav-produkte")),
        dbc.NavItem(dbc.NavLink("Zutaten", href="#", id="nav-zutaten")),
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

# Layout for customer analysis
kunden_layout = html.Div([
    html.H2("Kundenanalyse", className="text-light mb-4 animate__animated animate__fadeIn"),
    # Filters
    dbc.Row([
        dbc.Col([
            html.Label("Stadt filtern:", className="text-light"),
            dcc.Dropdown(
                id="stadt-filter",
                options=[{"label": "Alle", "value": "Alle"}] + [
                    {"label": stadt, "value": stadt} for stadt in df_kunden["Stadt"].unique()
                ],
                value="Alle",
                className="mb-3",
                style={"backgroundColor": "#333", "color": "#fff"}
            )
        ], width=4),
        dbc.Col([
            html.Label("Wiederkehrend filtern:", className="text-light"),
            dcc.Dropdown(
                id="wiederkehrend-filter",
                options=[
                    {"label": "Alle", "value": "Alle"},
                    {"label": "Ja", "value": True},
                    {"label": "Nein", "value": False}
                ],
                value="Alle",
                className="mb-3",
                style={"backgroundColor": "#333", "color": "#fff"}
            )
        ], width=4)
    ], className="mb-4"),
    # KPI Cards
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Wiederkehrende Kunden", className="card-title"),
                html.H2(id="kpi-wiederkehrend", className="card-text")
            ])
        ], color="secondary", inverse=True, className="shadow"), width=3),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Ø Bestellwert", className="card-title"),
                html.H2(id="kpi-bestellwert", className="card-text")
            ])
        ], color="info", inverse=True, className="shadow"), width=3),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Gesamtbestellungen", className="card-title"),
                html.H2(id="kpi-gesamtbestellungen", className="card-text")
            ])
        ], color="primary", inverse=True, className="shadow"), width=3),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Höchster Bestellwert", className="card-title"),
                html.H2(id="kpi-max-bestellwert", className="card-text")
            ])
        ], color="warning", inverse=True, className="shadow"), width=3)
    ], className="mb-4"),
    # Graphs
    dbc.Row([
        dbc.Col(dcc.Graph(id="graph-bestellwert"), width=6),
        dbc.Col(dcc.Graph(id="graph-wiederkehrend"), width=6)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dcc.Graph(id="graph-stadt"), width=12)
    ], className="mb-4"),
    # Data Table
    html.H3("Kundendaten", className="text-light mb-3"),
    dash_table.DataTable(
        id="kunden-table",
        columns=[
            {"name": "Kunde", "id": "Kunde"},
            {"name": "Bestellwert (€)", "id": "Bestellwert"},
            {"name": "Wiederkehrend", "id": "Wiederkehrend"},
            {"name": "Stadt", "id": "Stadt"},
            {"name": "Bestelldatum", "id": "Bestelldatum"},
            {"name": "Produktkategorie", "id": "Produktkategorie"},
            {"name": "Bewertung", "id": "Bewertung"}
        ],
        style_table={"overflowX": "auto"},
        style_cell={
            "backgroundColor": "#2d2d2d",
            "color": "white",
            "border": "1px solid #444"
        },
        style_header={
            "backgroundColor": "#1f77b4",
            "fontWeight": "bold",
            "color": "white"
        },
        page_size=10,
        sort_action="native",
        filter_action="native"
    )
])

# Placeholder layouts for other pages
dashboards_layout = html.Div([
    html.H2("Dashboards", className="text-light"),
    html.P("Hier werden verschiedene Dashboards angezeigt.", className="text-light"),
    dbc.Button("Daten laden", color="primary", className="mt-3")
])

analysen_layout = html.Div([
    html.H2("Analysen", className="text-light"),
    html.P("Detaillierte Analysen und Berichte.", className="text-light"),
    dbc.Card([
        dbc.CardBody([
            html.H4("Analyseübersicht", className="card-title"),
            html.P("Wähle eine Analyse aus, um Details zu sehen.", className="card-text")
        ])
    ], color="secondary", inverse=True, className="mt-3")
])

filter_layout = html.Div([
    html.H2("Datenfilter", className="text-light"),
    html.P("Konfiguriere und speichere Datenfilter.", className="text-light")
])

stores_layout = html.Div([
    html.H2("Stores", className="text-light"),
    html.P("Übersicht der verfügbaren Stores.", className="text-light")
])

produkte_layout = html.Div([
    html.H2("Produkte", className="text-light"),
    html.P("Produktkatalog und Details.", className="text-light")
])

zutaten_layout = html.Div([
    html.H2("Zutaten", className="text-light"),
    html.P("Zutatenverwaltung und Analyse.", className="text-light")
])

# Main app layout
app.layout = html.Div([
    navbar,
    dbc.Container(id="page-content", fluid=True, className="pt-4")
])

# Callback for navigation
@app.callback(
    Output("page-content", "children"),
    [
        Input("nav-kunden", "n_clicks"),
        Input("nav-dashboards", "n_clicks"),
        Input("nav-analysen", "n_clicks"),
        Input("nav-filter", "n_clicks"),
        Input("nav-stores", "n_clicks"),
        Input("nav-produkte", "n_clicks"),
        Input("nav-zutaten", "n_clicks")
    ],
    prevent_initial_call=True
)
def render_page(k, d, a, f, s, p, z):
    ctx = dash.callback_context
    if not ctx.triggered:
        return html.P("Wähle einen Menüpunkt.", className="text-light")
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    layouts = {
        "nav-kunden": kunden_layout,
        "nav-dashboards": dashboards_layout,
        "nav-analysen": analysen_layout,
        "nav-filter": filter_layout,
        "nav-stores": stores_layout,
        "nav-produkte": produkte_layout,
        "nav-zutaten": zutaten_layout
    }
    return layouts.get(
        button_id,
        html.P(f"Seite '{button_id}' ist noch in Arbeit.", className="text-light")
    )

# Callback for updating customer analysis components
@app.callback(
    [
        Output("kpi-wiederkehrend", "children"),
        Output("kpi-bestellwert", "children"),
        Output("kpi-gesamtbestellungen", "children"),
        Output("kpi-max-bestellwert", "children"),
        Output("graph-bestellwert", "figure"),
        Output("graph-wiederkehrend", "figure"),
        Output("graph-stadt", "figure"),
        Output("kunden-table", "data")
    ],
    [
        Input("stadt-filter", "value"),
        Input("wiederkehrend-filter", "value")
    ]
)
def update_kunden_analyse(stadt, wiederkehrend):
    # Filter data
    filtered_df = df_kunden.copy()
    if stadt != "Alle":
        filtered_df = filtered_df[filtered_df["Stadt"] == stadt]
    if wiederkehrend != "Alle":
        filtered_df = filtered_df[filtered_df["Wiederkehrend"] == wiederkehrend]
    
    # Update KPIs
    kpi_wiederkehrend = filtered_df["Wiederkehrend"].sum()
    kpi_bestellwert = f"{filtered_df['Bestellwert'].mean():.2f} €" if len(filtered_df) > 0 else "0.00 €"
    kpi_gesamtbestellungen = len(filtered_df)
    kpi_max_bestellwert = f"{filtered_df['Bestellwert'].max():.2f} €" if len(filtered_df) > 0 else "0.00 €"
    
    # Update figures
    fig_bestellwert_new = px.bar(
        filtered_df,
        x="Kunde",
        y="Bestellwert",
        title="Ø Bestellwert pro Kunde",
        color="Kunde",
        height=400
    )
    fig_bestellwert_new.update_layout(
        plot_bgcolor="#2d2d2d",
        paper_bgcolor="#2d2d2d",
        font_color="white"
    )
    
    fig_wiederkehrend_new = px.pie(
        filtered_df,
        names="Wiederkehrend",
        title="Anteil wiederkehrender Kunden",
        color_discrete_sequence=["#1f77b4", "#ff7f0e"],
        height=400
    )
    fig_wiederkehrend_new.update_layout(
        plot_bgcolor="#2d2d2d",
        paper_bgcolor="#2d2d2d",
        font_color="white"
    )
    
    fig_stadt_new = px.scatter(
        filtered_df,
        x="Bestelldatum",
        y="Bestellwert",
        color="Stadt",
        size="Bewertung",
        title="Bestellwert nach Stadt und Datum",
        height=400
    )
    fig_stadt_new.update_layout(
        plot_bgcolor="#2d2d2d",
        paper_bgcolor="#2d2d2d",
        font_color="white"
    )
    
    # Update table data
    table_data = filtered_df.to_dict("records")
    
    return (
        kpi_wiederkehrend,
        kpi_bestellwert,
        kpi_gesamtbestellungen,
        kpi_max_bestellwert,
        fig_bestellwert_new,
        fig_wiederkehrend_new,
        fig_stadt_new,
        table_data
    )

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
