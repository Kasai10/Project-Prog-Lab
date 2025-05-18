import dash_html_components as html
import dash_core_components as dcc

def with_back_button(content):
    return html.Div([
        html.Div([
            dcc.Link("🏠 Zur Startseite", href="/", className="btn btn-secondary mb-4")
        ], style={"textAlign": "left", "marginLeft": "20px", "marginTop": "20px"}),
        content
    ])