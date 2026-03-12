from dash import html, dcc
import dash_bootstrap_components as dbc
from components import build_date_controls


def build_layout():
    return dbc.Container([

        # ── Header with integrated country selector ──
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.H1("Economic Health Dashboard", className="mt-3 mb-0"),
                    html.P("Global Economic Sector Trends and Drill-Down"),
                ], width=True),
                dbc.Col(
                    dcc.Dropdown(
                        id="country-dropdown",
                        placeholder="Select a country",
                        value=1,
                        className="header-dropdown",
                    ),
                    width=3,
                    className="d-flex align-items-center",
                ),
            ], align="center"),
        ], className="dashboard-header"),

        # ── Intelligence Panel: cycle clock + traffic lights + narrative ──
        html.Div(id="intelligence-panel-container"),

        # ── Policy Timeline Panel ──
        html.Div(id="policy-panel-container"),

        # ── Breadcrumb + Controls bar (combined row) ──
        html.Div([
            dbc.Row([
                dbc.Col(
                    html.Div(id="breadcrumb-container"),
                    width=5,
                    className="d-flex align-items-center",
                ),
                dbc.Col(
                    html.Div(id="date-controls", children=build_date_controls()),
                    width=5,
                    className="d-flex align-items-center justify-content-end",
                ),
                dbc.Col(
                    dbc.Switch(id="yoy-toggle", label="YoY %", value=False),
                    width=2,
                    className="d-flex align-items-center justify-content-end",
                ),
            ], align="center"),
        ], className="control-bar"),

        # ── Anomaly Alerts (collapsible, sector-level only) ──
        html.Div(id="anomaly-container"),

        # ── Tabs: Sectors / Momentum / US vs Canada / Correlations ──
        html.Div(
            dbc.Tabs(
                [
                    dbc.Tab(label="Sectors", tab_id="tab-sectors"),
                    dbc.Tab(label="Momentum", tab_id="tab-momentum"),
                    dbc.Tab(label="Compare", tab_id="tab-compare"),
                    dbc.Tab(label="Correlations", tab_id="tab-correlations"),
                ],
                id="drill-tabs",
                active_tab="tab-sectors",
            ),
            id="drill-tabs-container",
            style={"display": "none"},
        ),

        # Treemap (persistent graph; visibility toggled)
        html.Div(
            html.Div(
                dcc.Graph(id="treemap", figure={}, config={"displayModeBar": False}),
                className="treemap-wrapper",
            ),
            id="treemap-container",
        ),

        # Tab content (momentum / compare / correlations)
        html.Div(id="drill-tab-content"),

        # Main content with loading (sub-industries, indicators)
        dcc.Loading(
            id="loading",
            children=[html.Div(id="main-content")],
            type="circle",
            color="#6c8cff",
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
