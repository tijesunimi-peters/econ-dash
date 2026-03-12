"""
Phase 2: Homepage Redesign

Reorganizes the dashboard homepage with:
- Responsive 2-3 column grid layout (uses Phase 1 foundation)
- Collapsible panels for all major views (Policy, Sentiment, Structural, Trade)
- 4 preset view configurations (analyst, trader, policy, supply_chain)
- Smart panel sizing based on screen width
- localStorage persistence (Phase 5 storage)
- Smooth animations (Phase 5 animations)

Homepage Structure:
- Header: Country selector + Preset selector
- Row 1: Intelligence (1/3) + Sector Treemap (2/3)
- Row 2: Quick Stats (GDP, Unemployment, Inflation, Trade Balance)
- Row 3+: Collapsible panels (Policy, Sentiment, Structural, Trade)
- Footer: Drill-down area (visible when navigating)
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from .grid_layout import dashboard_grid, card_grid
from .collapsible_card import build_collapsible_panel

try:
    from utils.storage import get_preset_config, list_presets
except ImportError:
    # Fallback if utils not accessible from parent path
    def get_preset_config(preset_name):
        return {}
    def list_presets():
        return []


def build_redesigned_homepage(
    intelligence_container,
    sentiment_container,
    structural_container,
    policy_container,
    trade_flows_container,
    treemap_container,
    country_dropdown,
    anomaly_container,
    breadcrumb_container,
    date_controls,
    yoy_toggle,
    drill_tabs_container,
    drill_tab_content,
    main_content,
    storage_store,
):
    """
    Build the redesigned homepage with responsive grid layout and collapsible panels.

    Uses Phase 1 dashboard_grid for responsive columns:
    - 4K (3840px): 3 columns
    - 1440p: 2 columns
    - 1080p: 1-2 columns (auto-fit)
    - Mobile: 1 column

    Uses Phase 1 build_collapsible_panel for expandable panels with:
    - localStorage persistence (Phase 5)
    - Default collapse state per preset
    - Smooth animations (Phase 5)

    Args:
        intelligence_container: Intelligence panel HTML
        sentiment_container: Sentiment panel HTML
        structural_container: Structural health panel HTML
        policy_container: Policy timeline panel HTML
        trade_flows_container: Trade flows panel HTML
        treemap_container: Sector treemap graph
        country_dropdown: Country selector dropdown
        anomaly_container: Anomaly alerts
        breadcrumb_container: Breadcrumb navigation
        date_controls: Date range picker controls
        yoy_toggle: Year-over-year toggle
        drill_tabs_container: Tabs for drill-down views
        drill_tab_content: Content area for drill-down
        main_content: Main content area with loading
        storage_store: dcc.Store for localStorage persistence

    Returns:
        Div with redesigned homepage
    """

    return dbc.Container([

        # ── Header with country selector + preset selector ──
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.H1("Economic Health Dashboard", className="mt-3 mb-0"),
                    html.P("Global Economic Sector Trends and Drill-Down", className="text-muted"),
                ], width=True),
                dbc.Col([
                    dbc.Row([
                        dbc.Col(
                            country_dropdown,
                            width=6,
                            className="d-flex align-items-center",
                        ),
                        dbc.Col(
                            _build_preset_selector(),
                            width=6,
                            className="d-flex align-items-center",
                        ),
                    ], align="center"),
                ], width=4),
            ], align="center"),
        ], className="dashboard-header"),

        # ── Storage store for localStorage persistence (Phase 5) ──
        storage_store,

        # ── Row 1: Intelligence Panel (1/3) + Sector Treemap (2/3) ──
        dashboard_grid([
            intelligence_container,
            treemap_container,
        ], layout="1-2"),

        # ── Row 2: Quick Stats ──
        _build_quick_stats_row(),

        # ── Row 3+: Collapsible Panels ──
        dashboard_grid([
            build_collapsible_panel(
                title="Market Sentiment",
                children=sentiment_container,
                panel_id="sentiment-panel",
                default_open=True,
                icon="📊",
            ),
            build_collapsible_panel(
                title="Policy Timeline",
                children=policy_container,
                panel_id="policy-panel",
                default_open=False,  # Collapsed by default
                icon="📅",
            ),
        ], layout="adaptive"),

        dashboard_grid([
            build_collapsible_panel(
                title="Structural Health",
                children=structural_container,
                panel_id="structural-panel",
                default_open=True,
                icon="🏗️",
            ),
            build_collapsible_panel(
                title="Trade Flows & Supply Chain",
                children=trade_flows_container,
                panel_id="trade-panel",
                default_open=True,
                icon="🚢",
            ),
        ], layout="adaptive"),

        # ── Breadcrumb + Controls bar (shown only during drill-down) ──
        html.Div([
            dbc.Row([
                dbc.Col(breadcrumb_container, width=5, className="d-flex align-items-center"),
                dbc.Col(date_controls, width=5, className="d-flex align-items-center justify-content-end"),
                dbc.Col(yoy_toggle, width=2, className="d-flex align-items-center justify-content-end"),
            ], align="center"),
        ], className="control-bar", style={"display": "none"}, id="control-bar-container"),

        # ── Anomaly Alerts ──
        anomaly_container,

        # ── Drill-down area (hidden on homepage, shown when navigating) ──
        html.Div([
            drill_tabs_container,
            html.Div(id="drill-tab-content-wrapper", children=[main_content]),
        ], id="drill-down-area", style={"display": "none"}),

        # ── State stores ──
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


def _build_preset_selector():
    """
    Build preset view selector dropdown.

    Presets (from Phase 5 storage):
    - analyst: All panels visible, 2-column layout
    - trader: Focus on sentiment and trade flows
    - policy: Policy-focused with structural metrics
    - supply_chain: Trade flows and supply chain risk

    Returns:
        Dropdown component for preset selection
    """

    presets = list_presets()  # From Phase 5 storage.py
    preset_options = [
        {"label": p.replace("_", " ").title(), "value": p}
        for p in presets
    ]

    return dcc.Dropdown(
        id="preset-selector",
        options=preset_options,
        value="analyst",  # Default to analyst
        clearable=False,
        placeholder="Select view preset",
        className="header-dropdown",
        style={"width": "100%"},
    )


def _build_quick_stats_row():
    """
    Build quick stats row showing key economic metrics.

    Shows 4 key metrics:
    - GDP Growth (%)
    - Unemployment (%)
    - Inflation (%)
    - Trade Balance (Exports - Imports)

    Returns:
        Div with quick stats cards in a responsive grid
    """

    stat_cards = [
        _build_stat_card("📈 GDP Growth", "2.4%", "YoY", "positive"),
        _build_stat_card("👥 Unemployment", "4.2%", "Last Month", "neutral"),
        _build_stat_card("💰 Inflation", "3.1%", "YoY", "warning"),
        _build_stat_card("🌍 Trade Balance", "$125B", "Last Quarter", "positive"),
    ]

    return html.Div([
        html.H5("Quick Stats", className="section-label"),
        card_grid(stat_cards, columns=4),
    ], className="quick-stats-section", style={
        "marginTop": "16px",
        "marginBottom": "16px",
    })


def _build_stat_card(label, value, subtitle, sentiment):
    """
    Build a single quick stat card.

    Args:
        label: Stat label (e.g., "GDP Growth")
        value: Stat value (e.g., "2.4%")
        subtitle: Additional info (e.g., "YoY")
        sentiment: One of "positive", "negative", "warning", "neutral"

    Returns:
        Div with styled stat card
    """

    color_map = {
        "positive": "var(--positive)",
        "negative": "var(--negative)",
        "warning": "var(--warning)",
        "neutral": "var(--neutral)",
    }

    return html.Div([
        html.Div(label, className="stat-label"),
        html.Div(
            value,
            className="stat-value",
            style={"color": color_map.get(sentiment, "var(--text)")},
        ),
        html.Div(subtitle, className="stat-subtitle"),
    ], className="quick-stat-card", style={
        "background": "var(--surface)",
        "border": "1px solid var(--border)",
        "borderRadius": "8px",
        "padding": "12px",
        "textAlign": "center",
        "animation": "fadeIn 0.3s ease-out",
    })


def apply_preset_config(preset_name):
    """
    Apply a preset view configuration.

    From Phase 5 storage.py, presets define:
    - Which panels are visible/hidden
    - Default collapse state
    - Layout preference
    - Sidebar width

    Args:
        preset_name: One of "analyst", "trader", "policy", "supply_chain"

    Returns:
        Config dict with panel states and settings
    """

    config = get_preset_config(preset_name)
    if not config:
        return {}

    return {
        "layout": config.get("layout", "2-col"),
        "collapsed_panels": config.get("collapsed_panels", []),
        "visible_panels": config.get("visible_panels", []),
        "sidebar_width": config.get("sidebar_width", 25),
    }


# ═════════════════════════════════════════════════════════════════════════════
# CSS for Phase 2 Homepage Redesign
# ═════════════════════════════════════════════════════════════════════════════

HOMEPAGE_CSS = """
/* ===== Phase 2: Homepage Redesign ===== */

/* ===== Header with Preset Selector ===== */

.dashboard-header {
    border-bottom: 1px solid var(--border);
    padding-bottom: 14px;
    margin-bottom: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.dashboard-header h1 {
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0;
}

.dashboard-header p {
    font-size: 0.85rem;
    margin: 4px 0 0 0;
}

.header-dropdown {
    min-width: 150px;
}

/* ===== Quick Stats Section ===== */

.quick-stats-section {
    margin: 20px 0;
    padding: 0;
}

.section-label {
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-secondary);
    margin-bottom: 12px;
}

.quick-stat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px;
    text-align: center;
    transition: all 0.15s;
}

.quick-stat-card:hover {
    border-color: var(--text-muted);
    transform: translateY(-2px);
}

.stat-label {
    font-size: 0.8rem;
    color: var(--text-secondary);
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    margin-bottom: 6px;
}

.stat-value {
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 4px;
}

.stat-subtitle {
    font-size: 0.75rem;
    color: var(--text-muted);
}

/* ===== Dashboard Grid ===== */

.dashboard-grid {
    display: grid;
    gap: 16px;
    margin-bottom: 16px;
}

/* 4K: 3 columns */
@media (min-width: 2560px) {
    .dashboard-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

/* 1920p: 2 columns */
@media (min-width: 1920px) and (max-width: 2559px) {
    .dashboard-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* 1440p: 2 columns */
@media (min-width: 1440px) and (max-width: 1919px) {
    .dashboard-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* 1080p: 1-2 columns */
@media (min-width: 1025px) and (max-width: 1439px) {
    .dashboard-grid {
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    }
}

/* Tablet: 1 column */
@media (max-width: 1024px) {
    .dashboard-grid {
        grid-template-columns: 1fr;
    }
}

/* ===== Panel Spacing ===== */

.collapsible-panel {
    margin-bottom: 16px;
}

/* ===== Control Bar (Drill-down) ===== */

.control-bar {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 16px;
    display: none;  /* Hidden by default, shown during drill-down */
}

.control-bar.active {
    display: block;
    animation: slideInTop 0.3s ease-out;
}

/* ===== Drill-Down Area ===== */

#drill-down-area {
    display: none;
    animation: slideInBottom 0.3s ease-out;
}

#drill-down-area.active {
    display: block;
}

/* ===== Responsive Adjustments ===== */

@media (max-width: 768px) {
    .dashboard-header {
        flex-direction: column;
        align-items: flex-start;
        padding-bottom: 12px;
    }

    .dashboard-header h1 {
        font-size: 1.25rem;
    }

    .quick-stats-section {
        margin: 12px 0;
    }

    .quick-stat-card {
        padding: 10px;
        font-size: 0.85rem;
    }

    .stat-value {
        font-size: 1.2rem;
    }
}
"""
