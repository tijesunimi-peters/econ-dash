"""
Phase 4: Comparison Mode Enhancement

Synchronized side-by-side comparison of countries with:
- Synchronized scrolling between two chart panels
- Divergence highlighting (when metrics move apart)
- Side-by-side metric comparison cards
- Optional 3-way comparison support

Uses Phase 1 responsive grid, Phase 3 sidebar layout, Phase 5 animations.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc


def build_comparison_view(
    country1_data,
    country2_data,
    country1_name="Country 1",
    country2_name="Country 2",
    metrics_data=None,
    comparison_type="metrics",
):
    """
    Build a comparison view with synchronized scrolling and divergence highlighting.

    Args:
        country1_data: Data for first country (charts, metrics, etc.)
        country2_data: Data for second country
        country1_name: Display name for country 1
        country2_name: Display name for country 2
        metrics_data: Optional metrics for divergence highlighting
        comparison_type: "metrics" or "full" comparison

    Returns:
        Div with synchronized comparison layout
    """

    return html.Div([
        # Comparison header with country selector
        _build_comparison_header(country1_name, country2_name),

        # Synchronized metrics comparison
        html.Div([
            dbc.Row([
                dbc.Col([
                    _build_country_metrics_panel(country1_name, country1_data),
                ], width=6, style={"borderRight": "1px solid var(--border)"}),
                dbc.Col([
                    _build_country_metrics_panel(country2_name, country2_data),
                ], width=6),
            ]),
        ], id="metrics-comparison-row", className="comparison-section"),

        # Synchronized scrolling area for charts
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div(
                        country1_data,
                        id="comparison-panel-1",
                        className="sync-scroll-panel",
                        style={"maxHeight": "600px", "overflowY": "auto"},
                    ),
                ], width=6, style={"borderRight": "1px solid var(--border)"}),
                dbc.Col([
                    html.Div(
                        country2_data,
                        id="comparison-panel-2",
                        className="sync-scroll-panel",
                        style={"maxHeight": "600px", "overflowY": "auto"},
                    ),
                ], width=6),
            ]),
        ], id="sync-scroll-container", className="comparison-section"),

        # Divergence heatmap (optional)
        html.Div(
            _build_divergence_heatmap(metrics_data) if metrics_data else html.Div(),
            className="comparison-section",
        ),

        # Store for scroll position synchronization
        dcc.Store(id="comparison-scroll-store", data={"scroll_pos": 0}),
    ], className="comparison-view")


def _build_comparison_header(country1_name, country2_name):
    """
    Build comparison header with country selectors and options.

    Args:
        country1_name: Name of first country
        country2_name: Name of second country

    Returns:
        Div with header controls
    """

    return html.Div([
        dbc.Row([
            dbc.Col([
                html.H4(country1_name, className="comparison-country-title"),
            ], width=5),
            dbc.Col([
                html.Div([
                    dbc.Button("↔ Swap", size="sm", outline=True, className="me-2",
                              id="btn-swap-countries"),
                    dbc.Button("+ Add 3rd", size="sm", outline=True,
                              id="btn-add-third-country"),
                ], style={"display": "flex", "gap": "8px"}),
            ], width=2, className="d-flex justify-content-center"),
            dbc.Col([
                html.H4(country2_name, className="comparison-country-title"),
            ], width=5, style={"textAlign": "right"}),
        ], align="center"),
    ], className="comparison-header")


def _build_country_metrics_panel(country_name, data):
    """
    Build a metric panel showing key indicators for a country.

    Args:
        country_name: Country display name
        data: Country data (dict or component)

    Returns:
        Div with metrics panel
    """

    return html.Div([
        html.H5(f"{country_name} Metrics", className="comparison-section-title"),
        html.Div(data, className="country-metrics"),
    ], className="country-panel")


def _build_divergence_heatmap(metrics_data):
    """
    Build a divergence heatmap showing where countries differ.

    Highlights metrics where countries diverge significantly (>5%, >10%, >15%).

    Args:
        metrics_data: Dict with metric comparisons

    Returns:
        Div with heatmap visualization
    """

    if not metrics_data or not isinstance(metrics_data, dict):
        return html.Div()

    # Calculate divergence for each metric
    rows = []
    for metric_name, values in metrics_data.items():
        if isinstance(values, dict) and "val1" in values and "val2" in values:
            val1 = float(values.get("val1", 0))
            val2 = float(values.get("val2", 0))

            # Calculate divergence percentage
            if val1 != 0:
                divergence = abs((val2 - val1) / val1) * 100
            else:
                divergence = 0

            # Color based on which country is ahead
            if val1 > val2:
                color = "var(--negative)"  # Country 1 ahead (red)
                winner = "Country 1 ↑"
            elif val2 > val1:
                color = "var(--positive)"  # Country 2 ahead (green)
                winner = "Country 2 ↑"
            else:
                color = "var(--neutral)"   # Tied (gray)
                winner = "Tied →"

            # Determine severity level
            if divergence > 15:
                severity_class = "divergence-critical"
                severity_label = "Large"
            elif divergence > 10:
                severity_class = "divergence-warning"
                severity_label = "Moderate"
            elif divergence > 5:
                severity_class = "divergence-info"
                severity_label = "Small"
            else:
                severity_class = "divergence-none"
                severity_label = "None"

            rows.append(html.Div([
                html.Div([
                    html.Span(metric_name, className="divergence-metric-name"),
                    html.Span(
                        f"{divergence:.1f}% {severity_label}",
                        className="divergence-value",
                        style={"color": color},
                    ),
                ], className="divergence-row"),
            ], className=f"divergence-item {severity_class}"))

    return html.Div([
        html.H5("Divergence Analysis", className="comparison-section-title"),
        html.Div(rows, className="divergence-heatmap"),
    ], className="divergence-container")


def build_sync_scroll_callback_js():
    """
    Get JavaScript for synchronized scrolling between two panels.

    Both panels scroll together when user scrolls one of them.
    """

    return """
    (function() {
        let syncScrolling = true;

        const panel1 = document.getElementById('comparison-panel-1');
        const panel2 = document.getElementById('comparison-panel-2');

        if (!panel1 || !panel2) return;

        // Sync scroll when panel 1 scrolls
        panel1.addEventListener('scroll', function() {
            if (syncScrolling) {
                syncScrolling = false;
                panel2.scrollTop = panel1.scrollTop;
                syncScrolling = true;
            }
        });

        // Sync scroll when panel 2 scrolls
        panel2.addEventListener('scroll', function() {
            if (syncScrolling) {
                syncScrolling = false;
                panel1.scrollTop = panel2.scrollTop;
                syncScrolling = true;
            }
        });
    })();
    """


# ═════════════════════════════════════════════════════════════════════════════
# CSS for Phase 4 Comparison Mode
# ═════════════════════════════════════════════════════════════════════════════

COMPARISON_CSS = """
/* ===== Phase 4: Comparison Mode ===== */

.comparison-view {
    display: flex;
    flex-direction: column;
    gap: 16px;
    width: 100%;
}

/* ===== Comparison Header ===== */

.comparison-header {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    animation: slideInTop 0.3s ease-out;
}

.comparison-country-title {
    margin: 0;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text);
}

/* ===== Comparison Section ===== */

.comparison-section {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    animation: fadeIn 0.3s ease-out;
}

.comparison-section-title {
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-secondary);
    margin-bottom: 12px;
}

/* ===== Country Panels ===== */

.country-panel {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.country-metrics {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

/* ===== Synchronized Scrolling ===== */

.sync-scroll-panel {
    max-height: 600px;
    overflow-y: auto;
    padding-right: 8px;
}

.sync-scroll-panel::-webkit-scrollbar {
    width: 6px;
}

.sync-scroll-panel::-webkit-scrollbar-track {
    background: transparent;
}

.sync-scroll-panel::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 3px;
}

.sync-scroll-panel::-webkit-scrollbar-thumb:hover {
    background: var(--text-muted);
}

/* ===== Divergence Heatmap ===== */

.divergence-container {
    margin-top: 16px;
}

.divergence-heatmap {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.divergence-item {
    background: var(--surface-hover);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 10px 12px;
    transition: all 0.15s ease;
}

.divergence-item:hover {
    border-color: var(--text-muted);
}

.divergence-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.divergence-metric-name {
    font-weight: 500;
    color: var(--text);
}

.divergence-value {
    font-weight: 600;
    font-size: 0.9rem;
}

/* Severity levels */
.divergence-critical {
    border-left: 4px solid var(--negative);
    background: rgba(255, 87, 87, 0.05);
}

.divergence-warning {
    border-left: 4px solid var(--warning);
    background: rgba(255, 179, 71, 0.05);
}

.divergence-info {
    border-left: 4px solid var(--primary);
    background: rgba(108, 140, 255, 0.05);
}

.divergence-none {
    border-left: 4px solid var(--neutral);
    background: var(--surface-hover);
}

/* ===== Responsive Comparison ===== */

@media (max-width: 1024px) {
    .comparison-header {
        flex-direction: column;
        gap: 12px;
        text-align: center;
    }

    .country-panel {
        padding-bottom: 12px;
        border-bottom: 1px solid var(--border);
    }

    .country-panel:last-child {
        border-bottom: none;
    }
}

@media (max-width: 768px) {
    .comparison-header {
        padding: 10px 12px;
    }

    .comparison-section {
        padding: 12px;
    }

    .comparison-country-title {
        font-size: 0.95rem;
    }

    .sync-scroll-panel {
        max-height: 400px;
    }
}
"""
