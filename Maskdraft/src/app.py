import dash
from dash import dcc, html, Output, Input
import dash_bootstrap_components as dbc
from src.config import EXTERNAL_STYLESHEETS, APP_TITLE, MOCK_DATA_DIR
from src.data.data_loader import load_all_data
from src.layouts.navbar import get_navbar
from src.layouts.pages import (
    start_page, topkunden_page, bestellwert_page, kundenkarte_page,
    reichweite_page, beliebte_produkte_page, umsatz_produkt_page,
    launchperformance_page, korrelation_page, durchschnitt_page
)
from src.layouts.components import with_back_button
from src.callbacks.kundenanalyse import register_callbacks as register_kunden_callbacks
from src.callbacks.filialanalyse import register_callbacks as register_filial_callbacks
from src.callbacks.produktanalyse import register_callbacks as register_produkt_callbacks
from src.callbacks.bestellanalyse import register_callbacks as register_bestell_callbacks

# Daten laden
data = load_all_data(MOCK_DATA_DIR)

# Dash-App initialisieren
app = dash.Dash(
    __name__,
    external_stylesheets=EXTERNAL_STYLESHEETS
)
app.title = APP_TITLE
app.config.suppress_callback_exceptions = True

# Layouts definieren
layouts = {
    "/": start_page(),
    "/kundenanalyse/topkunden": with_back_button(topkunden_page()),
    "/kundenanalyse/bestellwert": with_back_button(bestellwert_page(data["orders_df"])),
    "/kundenanalyse/karte": with_back_button(kundenkarte_page()),
    "/kundenanalyse/mehrfach": with_back_button(html.Div([
        html.H2("Wiederkehrende Kunden", className="text-center mb-4"),
        html.P("Diese Seite ist noch nicht implementiert.", className="text-center text-light")
    ])),
    "/kundenanalyse/dichte": with_back_button(html.Div([
        html.H2("Kundendichte", className="text-center mb-4"),
        html.P("Diese Seite ist noch nicht implementiert.", className="text-center text-light")
    ])),
    "/filialanalyse/kundenreichweite": with_back_button(reichweite_page(data["stores_df"])),
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
    "/produktanalyse/beliebt": with_back_button(beliebte_produkte_page()),
    "/produktanalyse/umsatz": with_back_button(umsatz_produkt_page()),
    "/produktanalyse/launchperformance": with_back_button(launchperformance_page(data["products_df"])),
    "/produktanalyse/korrelation": with_back_button(korrelation_page()),
    "/produktanalyse/preise": with_back_button(html.Div([
        html.H2("Ø Preis", className="text-center mb-4"),
        html.P("Diese Seite ist noch nicht implementiert.", className="text-center text-light")
    ])),
    "/bestellanalyse/durchschnitt": with_back_button(durchschnitt_page(data["orders_df"])),
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

app.layout = html.Div([
    dcc.Location(id="url"),
    get_navbar(),
    dbc.Container(id="page-content", fluid=True, className="pt-4")
])

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    return layouts.get(pathname, with_back_button(html.Div([
        html.H2("Seite nicht gefunden", className="text-center mt-5"),
        html.P("Diese URL existiert nicht.", className="text-center")
    ])))

# Callbacks registrieren
register_kunden_callbacks(app, data)
register_filial_callbacks(app, data)
register_produkt_callbacks(app, data)
register_bestell_callbacks(app, data)

if __name__ == "__main__":
    app.run(debug=True)