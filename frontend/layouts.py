"""
Dashboard Layout - Phase 2 Homepage Redesign

Integrated with all phases:
- Phase 1: Responsive grid (dashboard_grid, collapsible_panel)
- Phase 2: Homepage with collapsible panels and presets
- Phase 3: Sidebar layout for drill-down views
- Phase 5: localStorage persistence, animations, mobile optimization

Layout structure:
1. Header: Country selector + Preset view selector
2. Row 1: Intelligence panel (1/3) + Sector Treemap (2/3)
3. Row 2: Quick stats (GDP, Unemployment, Inflation, Trade Balance)
4. Row 3+: Collapsible panels (Sentiment, Policy, Structural, Trade)
5. Drill-down area: Hidden by default, shown when navigating
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from components import build_date_controls
from components.homepage_redesign import build_redesigned_homepage


def build_layout():
    """
    Build the main dashboard layout using Phase 2 homepage redesign.

    Uses Phase 1 components for responsive grid and collapsible panels.
    Uses Phase 5 for localStorage persistence and animations.
    Uses Phase 3 sidebar layout for drill-down views.

    Returns:
        Dash layout component
    """

    homepage = build_redesigned_homepage(
        # Top-level panels (populated by callbacks)
        intelligence_container=html.Div(id="intelligence-panel-container"),
        sentiment_container=html.Div(id="sentiment-panel-container"),
        structural_container=html.Div(id="structural-panel-container"),
        policy_container=html.Div(id="policy-panel-container"),
        trade_flows_container=html.Div(id="trade-flows-container"),
        treemap_container=html.Div(
            html.Div(
                dcc.Graph(id="treemap", figure={}, config={"displayModeBar": False}),
                className="treemap-wrapper",
            ),
            id="treemap-container",
        ),

        # Header controls
        country_dropdown=dcc.Dropdown(
            id="country-dropdown",
            placeholder="Select a country",
            value=1,
            className="header-dropdown",
        ),

        # Anomaly alerts
        anomaly_container=html.Div(id="anomaly-container"),

        # Drill-down area controls and content
        breadcrumb_container=html.Div(id="breadcrumb-container"),
        date_controls=html.Div(
            id="date-controls",
            children=build_date_controls(),
            className="d-flex align-items-center justify-content-end",
        ),
        yoy_toggle=dbc.Switch(
            id="yoy-toggle",
            label="YoY %",
            value=False,
            className="d-flex align-items-center justify-content-end",
        ),

        # Drill-down tabs (hidden by default)
        drill_tabs_container=html.Div(
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

        # Drill-down content area
        drill_tab_content=html.Div(id="drill-tab-content"),

        # Main content with loading spinner
        main_content=dcc.Loading(
            id="loading",
            children=[html.Div(id="main-content")],
            type="circle",
            color="#6c8cff",
        ),

        # Storage for localStorage persistence (Phase 5)
        storage_store=dcc.Store(
            id="storage-store",
            storage_type="session",  # Use session storage for this session's prefs
            data={},
        ),
    )

    # Wrap homepage with additional stores
    return html.Div([
        homepage,
        # Store for sectors data (populated by update_treemap callback)
        dcc.Store(id="sectors-store", data={}),
        # Store for navigation state
        dcc.Store(id="nav-state", data={"level": "overview"}),
        # Store for date range preferences
        dcc.Store(id="date-range-store", data={"preset": "5Y"}),
    ])
