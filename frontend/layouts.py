from dash import html, dcc
import dash_bootstrap_components as dbc
from components import build_date_controls


def build_layout():
    return dbc.Container([
        # Header
        dbc.Row(dbc.Col([
            html.H1("Economic Health Dashboard", className="mt-3 mb-0"),
            html.P("US & Canada — Sector Trends and Drill-Down",
                   className="text-muted mb-3"),
        ])),

        # Breadcrumb
        dbc.Row(dbc.Col(html.Div(id="breadcrumb-container"))),

        # Controls row
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id="country-dropdown",
                    placeholder="Select a country",
                    value=1,
                    className="mb-3",
                ),
                width=3,
            ),
            dbc.Col(
                html.Div(id="date-controls", children=build_date_controls()),
                width=4,
                className="d-flex align-items-center",
            ),
            dbc.Col(
                dbc.Switch(id="yoy-toggle", label="YoY % Change", value=False),
                width=2,
                className="d-flex align-items-center",
            ),
        ], className="mb-3"),

        # Treemap (persistent, visibility toggled)
        html.Div(
            dcc.Graph(id="treemap", figure={}, config={"displayModeBar": False}),
            id="treemap-container",
        ),

        # Main content with loading (sub-industries, indicators)
        dcc.Loading(
            id="loading",
            children=[html.Div(id="main-content")],
            type="circle",
            color="#4a90d9",
        ),

        # State stores
        dcc.Store(id="nav-state", data={
            "level": "sectors",
            "country_id": 1,
            "country_name": "United States",
            "sector_id": None,
            "sector_name": None,
            "sub_industry_id": None,
            "sub_industry_name": None,
        }),
        dcc.Store(id="date-range-store", data={"preset": "5Y"}),
    ], fluid=True, className="pb-5")
