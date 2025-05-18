import dash_bootstrap_components as dbc
import dash_html_components as html

def get_navbar():
    return dbc.NavbarSimple(
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