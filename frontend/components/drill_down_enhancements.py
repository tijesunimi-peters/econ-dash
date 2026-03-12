"""
Phase 3: Drill-Down Improvements

Enhances the drill-down/detail view with:
- Sidebar layout showing context (current selection, related items)
- Sticky header with controls (date range, filters)
- Improved breadcrumb with context information
- Related items discovery (chip tags for quick navigation)
- Better organization of indicators and charts

Uses Phase 1 foundations (sidebar_layout, sticky headers, responsive grids).
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from .sidebar_layout import (
    build_sidebar_layout,
    build_sidebar_context_card,
    build_sticky_header,
)
from .grid_layout import card_grid


def build_drill_down_detail_view(
    nav_state,
    data,
    controls,
    related_items=None,
    anomalies=None,
    causal_factors=None,
):
    """
    Build a drill-down detail view with sidebar + main content layout.

    Uses Phase 1 sidebar_layout for responsive 2-column design:
    - Left sidebar (25%): Context, related items, quick actions
    - Right main (75%): Charts, tables, detailed analysis
    - Responsive: Side-by-side on desktop, stacked on mobile

    Args:
        nav_state: Navigation state dict with level, sector, sub_industry, etc.
        data: Content data (indicators, charts, tables)
        controls: Control bar with date range, filters
        related_items: List of related sector/sub-industry names (optional)
        anomalies: Anomaly data for current selection (optional)
        causal_factors: Causal factors for current selection (optional)

    Returns:
        Div containing sidebar + main content layout
    """

    # Build sidebar content
    sidebar = _build_detail_sidebar(
        nav_state=nav_state,
        related_items=related_items or [],
        anomalies=anomalies,
        causal_factors=causal_factors,
    )

    # Build main content area
    main_content = _build_detail_main_content(
        nav_state=nav_state,
        data=data,
        controls=controls,
    )

    # Use Phase 1 sidebar_layout for responsive 2-column design
    return build_sidebar_layout(
        sidebar_content=sidebar,
        main_content=main_content,
        sidebar_width="25%",
        sticky=True,
        resizable=True,
    )


def _build_detail_sidebar(nav_state, related_items, anomalies, causal_factors):
    """
    Build sidebar content showing context and quick actions.

    Shows:
    - Breadcrumb navigation
    - Current selection metrics (value, trend, alert status)
    - Related items discovery (clickable chips)
    - Anomalies summary (if any)
    - Causal factors (if available)
    - Quick action buttons
    """

    sidebar_content = []

    # Breadcrumb with context
    breadcrumb = _build_contextual_breadcrumb(nav_state)
    sidebar_content.append(breadcrumb)

    # Current selection context card
    level = nav_state.get("level", "sectors")
    if level == "sub_industries":
        selection_title = nav_state.get("sector_name", "")
    elif level == "indicators":
        selection_title = nav_state.get("sub_industry_name", "")
    else:
        selection_title = nav_state.get("sector_name", "")

    # Build context card with placeholder metrics
    # In actual implementation, would pass real data from API
    context_metrics = {
        "Current": selection_title,
        "View Level": level.replace("_", " ").title(),
    }

    context_card = build_sidebar_context_card(
        title=selection_title or "Selection",
        metrics=context_metrics,
        related_items=related_items[:5] if related_items else None,
        actions=[
            dbc.Button("Save View", size="sm", outline=True, className="me-2"),
            dbc.Button("Compare", size="sm", outline=True),
        ],
        metadata={
            "Level": level.replace("_", " ").title(),
            "Country": nav_state.get("country_name", ""),
        },
    )
    sidebar_content.append(context_card)

    # Anomalies summary
    if anomalies:
        anomalies_card = _build_anomalies_summary(anomalies)
        sidebar_content.append(anomalies_card)

    # Causal factors
    if causal_factors:
        factors_card = _build_causal_factors_summary(causal_factors)
        sidebar_content.append(factors_card)

    return html.Div(sidebar_content, className="detail-sidebar")


def _build_detail_main_content(nav_state, data, controls):
    """
    Build main content area with charts, tables, and detailed analysis.

    Shows:
    - Sticky header with breadcrumb and controls
    - Indicator charts and tables
    - Percentile gauges and comparison metrics
    - Performance metrics
    """

    # Build sticky header with controls
    sticky_header = build_sticky_header(
        breadcrumb=_build_detail_breadcrumb_compact(nav_state),
        controls=controls,
    )

    # Main content area with charts/tables
    content_area = html.Div(
        data,
        className="detail-content-area",
        style={
            "minHeight": "600px",
            "paddingTop": "12px",
        },
    )

    return html.Div([sticky_header, content_area])


def _build_contextual_breadcrumb(nav_state):
    """
    Build breadcrumb with current context information.

    Shows:
    - Hierarchy path: Country > Sector > Sub-Industry
    - Click to navigate back to previous level
    - Visual indicator of current position
    """

    level = nav_state.get("level", "sectors")
    country = nav_state.get("country_name", "")
    sector = nav_state.get("sector_name", "")
    sub_industry = nav_state.get("sub_industry_name", "")

    breadcrumb_items = [
        html.Span("🏠", className="me-2"),
        html.Span("Home", className="breadcrumb-item"),
    ]

    if country:
        breadcrumb_items.extend([
            html.Span(" › ", className="breadcrumb-sep"),
            html.Span(country, className="breadcrumb-item"),
        ])

    if sector:
        breadcrumb_items.extend([
            html.Span(" › ", className="breadcrumb-sep"),
            html.Span(sector, className="breadcrumb-item"),
        ])

    if sub_industry:
        breadcrumb_items.extend([
            html.Span(" › ", className="breadcrumb-sep"),
            html.Span(sub_industry, className="breadcrumb-item active"),
        ])

    return html.Div(
        breadcrumb_items,
        className="contextual-breadcrumb",
        style={
            "fontSize": "0.85rem",
            "marginBottom": "12px",
            "padding": "8px 0",
            "borderBottom": "1px solid var(--border)",
        },
    )


def _build_detail_breadcrumb_compact(nav_state):
    """
    Build compact breadcrumb for sticky header (less verbose).

    Shows only the essential hierarchy without full context.
    """

    country = nav_state.get("country_name", "")
    sector = nav_state.get("sector_name", "")
    sub_industry = nav_state.get("sub_industry_name", "")

    breadcrumb_text = " › ".join(filter(None, [country, sector, sub_industry]))

    return html.Div(
        breadcrumb_text or "Dashboard",
        className="sticky-breadcrumb",
        style={
            "fontSize": "0.9rem",
            "color": "var(--text-secondary)",
        },
    )


def _build_anomalies_summary(anomalies_data):
    """
    Build a summary card showing current anomalies.

    Shows:
    - Count of anomalies
    - Severity levels (critical, warning, info)
    - List of anomalous indicators
    """

    if isinstance(anomalies_data, dict) and "error" in anomalies_data:
        return html.Div()

    anomalies_list = anomalies_data.get("anomalies", [])
    if not anomalies_list:
        return html.Div()

    # Categorize by severity
    critical = [a for a in anomalies_list if a.get("severity") == "critical"]
    warning = [a for a in anomalies_list if a.get("severity") == "warning"]

    content = []

    if critical:
        content.append(
            html.Div([
                html.Span("🔴 Critical Anomalies", className="text-danger"),
                html.Ul([
                    html.Li(a.get("indicator_name", "Unknown"),
                            className="text-sm")
                    for a in critical[:3]
                ]),
            ], style={"marginBottom": "8px"})
        )

    if warning:
        content.append(
            html.Div([
                html.Span("🟠 Warning Anomalies", className="text-warning"),
                html.Ul([
                    html.Li(a.get("indicator_name", "Unknown"),
                            className="text-sm")
                    for a in warning[:3]
                ]),
            ])
        )

    return html.Div(
        [
            html.H5("Anomalies", className="text-sm"),
            html.Div(content),
        ],
        className="sidebar-anomalies",
        style={
            "background": "var(--surface)",
            "border": "1px solid var(--border)",
            "borderRadius": "8px",
            "padding": "12px",
            "marginTop": "12px",
        },
    )


def _build_causal_factors_summary(factors_data):
    """
    Build a summary card showing top causal factors.

    Shows:
    - Top 3 causal factors by confidence
    - Correlation strength (visual bar)
    - Affected sectors
    """

    if isinstance(factors_data, dict) and "error" in factors_data:
        return html.Div()

    factors_list = factors_data.get("factors", [])
    if not factors_list:
        return html.Div()

    # Get top 3 factors by confidence
    top_factors = sorted(
        factors_list,
        key=lambda f: f.get("confidence", 0),
        reverse=True
    )[:3]

    factor_items = []
    for factor in top_factors:
        confidence = factor.get("confidence", 0)
        name = factor.get("name", "Unknown")
        status = factor.get("status", "➡️")

        # Color confidence bar
        bar_color = "var(--positive)" if confidence >= 0.7 else \
                   "var(--warning)" if confidence >= 0.5 else \
                   "var(--negative)"

        factor_items.append(
            html.Div([
                html.Div([
                    html.Span(status, className="me-2"),
                    html.Span(name, className="text-sm font-weight-500"),
                ]),
                html.Div(
                    style={
                        "height": "4px",
                        "backgroundColor": bar_color,
                        "borderRadius": "2px",
                        "marginTop": "4px",
                        "width": f"{confidence * 100}%",
                    }
                ),
            ], style={"marginBottom": "8px"})
        )

    return html.Div(
        [
            html.H5("Causal Factors", className="text-sm"),
            html.Div(factor_items),
        ],
        className="sidebar-factors",
        style={
            "background": "var(--surface)",
            "border": "1px solid var(--border)",
            "borderRadius": "8px",
            "padding": "12px",
            "marginTop": "12px",
        },
    )


def build_related_items_chips(related_items, on_click_callback_id):
    """
    Build clickable chip tags for related sectors/sub-industries.

    Args:
        related_items: List of related item names
        on_click_callback_id: ID to use for click callbacks

    Returns:
        Div with chip tags
    """

    if not related_items:
        return html.Div()

    chips = [
        dbc.Badge(
            item,
            className="me-2 mb-2",
            style={
                "cursor": "pointer",
                "backgroundColor": "rgba(108, 140, 255, 0.2)",
                "color": "var(--primary)",
                "border": "1px solid rgba(108, 140, 255, 0.3)",
                "padding": "6px 12px",
                "borderRadius": "16px",
                "fontSize": "0.85rem",
                "transition": "all 0.15s",
            },
        )
        for item in related_items
    ]

    return html.Div(
        chips,
        className="related-items-group",
        style={
            "display": "flex",
            "flexWrap": "wrap",
            "gap": "6px",
        },
    )


def build_detail_view_controls(date_preset, yoy_enabled, comparison_enabled):
    """
    Build control buttons for detail view.

    Args:
        date_preset: Currently selected date preset ("5Y", "1Y", etc.)
        yoy_enabled: Whether YoY toggle is enabled
        comparison_enabled: Whether comparison mode is available

    Returns:
        Div with control buttons and toggles
    """

    return html.Div([
        dbc.ButtonGroup([
            dbc.Button(
                "📊 Save View",
                size="sm",
                outline=True,
                className="me-2",
                id="btn-save-view",
            ),
            dbc.Button(
                "🔄 Compare",
                size="sm",
                outline=True,
                className="me-2",
                id="btn-compare-view",
            ),
            dbc.Button(
                "📥 Export",
                size="sm",
                outline=True,
                id="btn-export-view",
            ),
        ]),
    ], style={"display": "flex", "gap": "8px"})


# ═════════════════════════════════════════════════════════════════════════════
# CSS for Phase 3 Drill-Down Enhancements
# ═════════════════════════════════════════════════════════════════════════════

DRILL_DOWN_CSS = """
/* ===== Detail Sidebar ===== */

.detail-sidebar {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.contextual-breadcrumb {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 4px;
    font-size: 0.85rem;
    color: var(--text-secondary);
}

.contextual-breadcrumb .breadcrumb-sep {
    color: var(--text-muted);
    margin: 0 4px;
}

.contextual-breadcrumb .breadcrumb-item {
    cursor: pointer;
    transition: color 0.15s;
    padding: 4px 0;
}

.contextual-breadcrumb .breadcrumb-item:hover:not(.active) {
    color: var(--primary);
}

.contextual-breadcrumb .breadcrumb-item.active {
    color: var(--text);
    font-weight: 600;
}

/* ===== Detail Main Content ===== */

.detail-content-area {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.sticky-breadcrumb {
    font-size: 0.9rem;
    color: var(--text-secondary);
    font-weight: 500;
}

/* ===== Anomalies & Factors ===== */

.sidebar-anomalies,
.sidebar-factors {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px;
    margin-top: 12px;
}

.sidebar-anomalies h5,
.sidebar-factors h5 {
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-secondary);
}

.sidebar-anomalies ul,
.sidebar-factors ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.sidebar-anomalies li,
.sidebar-factors li {
    font-size: 0.8rem;
    color: var(--text-secondary);
    padding: 4px 0;
}

/* ===== Related Items ===== */

.related-items-group {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 8px;
}

.related-item-badge {
    cursor: pointer;
    background: rgba(108, 140, 255, 0.15);
    color: var(--primary);
    border: 1px solid rgba(108, 140, 255, 0.3);
    padding: 6px 12px;
    border-radius: 16px;
    font-size: 0.85rem;
    transition: all 0.15s;
    white-space: nowrap;
}

.related-item-badge:hover {
    background: rgba(108, 140, 255, 0.25);
    border-color: var(--primary);
    transform: translateY(-1px);
}

/* ===== Control Buttons ===== */

.detail-controls {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.detail-controls .btn {
    font-size: 0.85rem;
    padding: 6px 12px;
}

/* ===== Responsive Detail View ===== */

@media (max-width: 1024px) {
    .detail-sidebar {
        margin-bottom: 20px;
        padding-bottom: 20px;
        border-bottom: 1px solid var(--border);
    }
}

/* ===== Chart Card in Detail View ===== */

.chart-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 16px;
    transition: all 0.2s;
}

.chart-card:hover {
    border-color: var(--text-muted);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* ===== Indicator Table in Detail View ===== */

.indicator-table {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 16px;
}

.indicator-table table {
    margin: 0;
}

.indicator-table thead {
    background: var(--surface-hover);
    border-bottom: 2px solid var(--border);
}

.indicator-table th {
    padding: 12px;
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-secondary);
}

.indicator-table td {
    padding: 12px;
    border-bottom: 1px solid var(--border);
}

.indicator-table tbody tr:hover {
    background: var(--surface-hover);
}

/* ===== Section Titles in Detail View ===== */

.section-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 16px;
    color: var(--text);
    padding-bottom: 8px;
    border-bottom: 2px solid var(--border);
}
"""
