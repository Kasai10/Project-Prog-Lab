import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Initialize the Dash app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Generate sample sales data
np.random.seed(42)
dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="D")[:100]
regions = ["North", "South", "East", "West"]
products = ["Laptop", "Phone", "Tablet", "Desktop"]
categories = ["Electronics", "Gadgets"]

data = {
    "date": np.random.choice(dates, 100),
    "region": np.random.choice(regions, 100),
    "product": np.random.choice(products, 100),
    "category": np.random.choice(categories, 100),
    "sales": np.random.randint(100, 1000, 100),
    "profit": np.random.randint(20, 200, 100)
}
df = pd.DataFrame(data)

# Define the layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col(html.H1("Sales Dashboard", className="text-center"), width=12)
    ], className="mb-4"),

    # Filters
    dbc.Row([
        dbc.Col([
            html.Label("Select Category"),
            dcc.Dropdown(
                id="category-dropdown",
                options=[{"label": cat, "value": cat} for cat in df["category"].unique()],
                value=df["category"].unique()[0],
                multi=False
            )
        ], width=4),
        dbc.Col([
            html.Label("Sales Range"),
            dcc.Slider(
                id="sales-slider",
                min=df["sales"].min(),
                max=df["sales"].max(),
                value=df["sales"].max(),
                marks={int(i): str(int(i)) for i in np.linspace(df["sales"].min(), df["sales"].max(), 5)},
                step=10
            )
        ], width=4),
        dbc.Col([
            html.Label("Chart Type"),
            dcc.RadioItems(
                id="chart-type",
                options=[
                    {"label": "Scatter", "value": "scatter"},
                    {"label": "Bar", "value": "bar"},
                    {"label": "Line", "value": "line"}
                ],
                value="scatter",
                inline=True
            )
        ], width=4)
    ], className="mb-4"),

    # Charts
    dbc.Row([
        dbc.Col(dcc.Graph(id="sales-profit-chart"), width=6),
        dbc.Col(dcc.Graph(id="sales-region-chart"), width=6)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dcc.Graph(id="sales-trend-chart"), width=12)
    ], className="mb-4"),

    # Data Table
    dbc.Row([
        dbc.Col([
            html.H3("Filtered Data"),
            dash_table.DataTable(
                id="data-table",
                columns=[
                    {"name": col, "id": col} for col in df.columns
                ],
                page_size=10,
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "left"}
            )
        ], width=12)
    ]),

    # Store for filtered data
    dcc.Store(id="filtered-data")
], fluid=True)

# Callback to filter data and store it
@app.callback(
    Output("filtered-data", "data"),
    [
        Input("category-dropdown", "value"),
        Input("sales-slider", "value")
    ]
)
def filter_data(category, sales_max):
    filtered_df = df[df["category"] == category]
    filtered_df = filtered_df[filtered_df["sales"] <= sales_max]
    return filtered_df.to_dict("records")

# Callback to update sales vs. profit chart
@app.callback(
    Output("sales-profit-chart", "figure"),
    [
        Input("filtered-data", "data"),
        Input("chart-type", "value")
    ]
)
def update_sales_profit_chart(data, chart_type):
    filtered_df = pd.DataFrame(data)
    if chart_type == "scatter":
        fig = px.scatter(filtered_df, x="sales", y="profit", color="product",
                         title="Sales vs. Profit by Product", hover_data=["region"])
    elif chart_type == "bar":
        fig = px.bar(filtered_df, x="sales", y="profit", color="product",
                     title="Sales vs. Profit by Product")
    else:
        fig = px.line(filtered_df, x="sales", y="profit", color="product",
                      title="Sales vs. Profit by Product")
    fig.update_layout(template="plotly_dark")
    return fig

# Callback to update sales by region chart
@app.callback(
    Output("sales-region-chart", "figure"),
    Input("filtered-data", "data")
)
def update_sales_region_chart(data):
    filtered_df = pd.DataFrame(data)
    region_summary = filtered_df.groupby("region")["sales"].sum().reset_index()
    fig = px.bar(region_summary, x="region", y="sales", title="Total Sales by Region",
                 color="region")
    fig.update_layout(template="plotly_dark")
    return fig

# Callback to update sales trend chart
@app.callback(
    Output("sales-trend-chart", "figure"),
    Input("filtered-data", "data")
)
def update_sales_trend_chart(data):
    filtered_df = pd.DataFrame(data)
    trend_data = filtered_df.groupby("date")["sales"].sum().reset_index()
    fig = px.line(trend_data, x="date", y="sales", title="Sales Trend Over Time")
    fig.update_layout(template="plotly_dark")
    return fig

# Callback to update data table
@app.callback(
    Output("data-table", "data"),
    Input("filtered-data", "data")
)
def update_data_table(data):
    return data

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
