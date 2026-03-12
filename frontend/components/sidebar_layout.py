"""
Sidebar Layout Component

Provides reusable sidebar + main content layout pattern with sticky positioning
and resizable divider for detail/drill-down views.
"""

from dash import html
import dash_bootstrap_components as dbc


def build_sidebar_layout(
    sidebar_content,
    main_content,
    sidebar_width=25,
    sticky=True,
    resizable=True,
    layout_id="sidebar-layout",
):
    """
    Create a sidebar + main content layout.

    Args:
        sidebar_content: Content for left sidebar (context panel)
        main_content: Content for right main area
        sidebar_width: Sidebar width as percentage (default 25%, i.e., 1/4)
        sticky: Make sidebar sticky at top while scrolling (default True)
        resizable: Allow user to resize sidebar via drag (default True)
        layout_id: Unique ID for the layout container

    Returns:
        Div with two-column layout (sidebar + main)

    Example:
        build_sidebar_layout(
            sidebar_content=html.Div("Context Panel"),
            main_content=html.Div("Main Content"),
            sidebar_width=25,
            resizable=True
        )
    """

    # Ensure sidebar_width is an integer
    sidebar_width = int(sidebar_width) if isinstance(sidebar_width, str) else sidebar_width
    main_width = 100 - sidebar_width

    sidebar_style = {
        "display": "grid",
        "gridColumn": "1",
        "width": f"{sidebar_width}%",
        "paddingRight": "16px",
        "borderRight": "1px solid var(--border)",
        "overflowY": "auto",
        "overflowX": "hidden",
    }

    # Add sticky positioning if requested
    if sticky:
        sidebar_style.update({
            "position": "sticky",
            "top": "0",
            "maxHeight": "calc(100vh - 120px)",
            "zIndex": "10",
        })

    main_style = {
        "display": "grid",
        "gridColumn": "2",
        "width": f"{main_width}%",
        "paddingLeft": "16px",
        "overflowY": "auto",
        "overflowX": "hidden",
    }

    container_style = {
        "display": "grid",
        "gridTemplateColumns": f"{sidebar_width}fr {main_width}fr",
        "gap": "0",
        "width": "100%",
        "minHeight": "calc(100vh - 200px)",
    }

    children = [
        html.Div(
            sidebar_content,
            id=f"{layout_id}-sidebar",
            className="sidebar-column",
            style=sidebar_style,
        ),
        html.Div(
            main_content,
            id=f"{layout_id}-main",
            className="main-column",
            style=main_style,
        ),
    ]

    # Add resizable divider if requested
    if resizable:
        children.insert(
            1,
            html.Div(
                id=f"{layout_id}-divider",
                className="sidebar-divider",
                style={
                    "cursor": "col-resize",
                    "width": "4px",
                    "backgroundColor": "var(--border)",
                    "userSelect": "none",
                    "gridColumn": "1 / 2",
                    "transition": "background-color 0.2s",
                    "hover": {
                        "backgroundColor": "var(--primary)",
                    },
                },
            ),
        )

    return html.Div(
        children,
        id=layout_id,
        className="sidebar-layout",
        style=container_style,
    )


def build_sidebar_context_card(
    title,
    metrics,
    related_items=None,
    actions=None,
    metadata=None,
):
    """
    Build a context card for sidebar showing current selection info.

    Args:
        title: Title of current selection
        metrics: Dict of metric_name -> value to display
        related_items: List of related item names (chips)
        actions: List of action buttons
        metadata: Additional metadata to show (e.g., last updated, data source)

    Returns:
        Styled context card div

    Example:
        build_sidebar_context_card(
            title="Manufacturing",
            metrics={"Latest": "$245B", "YoY Change": "+3.2%", "Trend": "↑"},
            related_items=["Semiconductors", "Auto Parts"],
            actions=[dbc.Button("Save View", size="sm")]
        )
    """

    content = [
        # Title
        html.H4(title, className="sidebar-context-title"),
        # Metrics
        html.Div(
            [
                html.Div(
                    [
                        html.Span(name, className="metric-label"),
                        html.Span(value, className="metric-value"),
                    ],
                    className="sidebar-metric",
                )
                for name, value in metrics.items()
            ],
            className="sidebar-metrics",
        ),
    ]

    # Add related items if provided
    if related_items:
        content.append(
            html.Div(
                [
                    html.P("Related Items:", className="sidebar-section-label"),
                    html.Div(
                        [
                            dbc.Badge(
                                item,
                                className="related-item-badge",
                                color="secondary",
                                style={"cursor": "pointer"},
                            )
                            for item in related_items
                        ],
                        className="related-items-group",
                    ),
                ],
                className="sidebar-related-items",
            )
        )

    # Add actions if provided
    if actions:
        content.append(
            html.Div(
                actions,
                className="sidebar-actions",
                style={
                    "display": "flex",
                    "gap": "8px",
                    "marginTop": "16px",
                    "flexWrap": "wrap",
                },
            )
        )

    # Add metadata if provided
    if metadata:
        content.append(
            html.Div(
                [
                    html.Span(
                        f"{key}: {value}",
                        className="sidebar-metadata",
                    )
                    for key, value in metadata.items()
                ],
                className="sidebar-footer",
            )
        )

    return html.Div(content, className="sidebar-context-card")


def build_sticky_header(
    breadcrumb,
    controls,
    layout_id="sticky-header",
):
    """
    Build a sticky header that stays visible while scrolling.

    Args:
        breadcrumb: Breadcrumb navigation component
        controls: Control elements (date range, filters, etc.)
        layout_id: Unique ID for header

    Returns:
        Sticky header div with breadcrumb and controls

    Example:
        build_sticky_header(
            breadcrumb=html.Div("Home > US > Manufacturing"),
            controls=dbc.Row([...])
        )
    """

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(breadcrumb, width=6),
                    dbc.Col(controls, width=6, className="text-end"),
                ],
                align="center",
            ),
        ],
        id=layout_id,
        className="sticky-header",
        style={
            "position": "sticky",
            "top": "0",
            "zIndex": "100",
            "backgroundColor": "var(--surface)",
            "borderBottom": "1px solid var(--border)",
            "padding": "12px 16px",
            "marginBottom": "16px",
            "transition": "box-shadow 0.2s",
        },
    )


def build_sidebar_panel_group(
    panels,
    title=None,
    collapsible=True,
):
    """
    Group multiple sidebar panels together (e.g., Causal Factors, Anomalies).

    Args:
        panels: List of panel components to group
        title: Optional group title
        collapsible: Whether group should be collapsible

    Returns:
        Grouped panels div

    Example:
        build_sidebar_panel_group(
            panels=[causal_factors_panel, anomalies_panel],
            title="Analysis",
            collapsible=True
        )
    """

    content = panels

    if title:
        content = [
            html.H5(title, className="sidebar-panel-group-title"),
        ] + panels

    return html.Div(
        content,
        className="sidebar-panel-group",
    )


# ═════════════════════════════════════════════════════════════════════════════
# CSS for Sidebar Layouts (add to style.css)
# ═════════════════════════════════════════════════════════════════════════════

SIDEBAR_CSS = """
/* ===== Sidebar Layout ===== */

.sidebar-layout {
    display: grid;
    width: 100%;
    gap: 0;
}

.sidebar-column {
    padding-right: 16px;
    border-right: 1px solid var(--border);
    position: sticky;
    top: 0;
    max-height: calc(100vh - 120px);
    overflow-y: auto;
    overflow-x: hidden;
    z-index: 10;
}

.sidebar-column::-webkit-scrollbar {
    width: 6px;
}

.sidebar-column::-webkit-scrollbar-track {
    background: transparent;
}

.sidebar-column::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 3px;
}

.sidebar-column::-webkit-scrollbar-thumb:hover {
    background: var(--text-muted);
}

.main-column {
    padding-left: 16px;
    overflow-y: auto;
    overflow-x: hidden;
}

.sidebar-divider {
    cursor: col-resize;
    width: 4px;
    background-color: var(--border);
    user-select: none;
    transition: background-color 0.2s;
}

.sidebar-divider:hover {
    background-color: var(--primary);
}

/* Context Card */

.sidebar-context-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
}

.sidebar-context-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 12px;
    color: var(--text);
}

.sidebar-metrics {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 12px;
}

.sidebar-metric {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid var(--border);
}

.sidebar-metric:last-child {
    border-bottom: none;
}

.metric-label {
    font-size: 0.85rem;
    color: var(--text-secondary);
    font-weight: 500;
}

.metric-value {
    font-size: 1rem;
    color: var(--text);
    font-weight: 600;
}

/* Related Items */

.sidebar-related-items {
    margin: 12px 0;
}

.sidebar-section-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-muted);
    margin-bottom: 8px;
}

.related-items-group {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
}

.related-item-badge {
    font-size: 0.75rem;
    padding: 4px 8px;
    background: rgba(108, 140, 255, 0.15);
    color: var(--primary);
    border: 1px solid rgba(108, 140, 255, 0.3);
    transition: all 0.15s;
    cursor: pointer;
}

.related-item-badge:hover {
    background: rgba(108, 140, 255, 0.25);
    border-color: var(--primary);
}

/* Actions */

.sidebar-actions {
    display: flex;
    gap: 8px;
    margin-top: 16px;
    flex-wrap: wrap;
}

.sidebar-actions .btn {
    font-size: 0.8rem;
    padding: 6px 12px;
}

/* Footer */

.sidebar-footer {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid var(--border);
}

.sidebar-metadata {
    display: block;
    margin-bottom: 4px;
}

/* Panel Groups */

.sidebar-panel-group {
    margin-bottom: 16px;
}

.sidebar-panel-group-title {
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-secondary);
    margin-bottom: 12px;
    margin-top: 16px;
}

/* Sticky Header */

.sticky-header {
    position: sticky;
    top: 0;
    z-index: 100;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 12px 16px;
    margin-bottom: 16px;
    transition: box-shadow 0.2s;
}

.sticky-header.scrolled {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

/* Mobile Responsive */

@media (max-width: 1024px) {
    .sidebar-layout {
        grid-template-columns: 1fr;
    }

    .sidebar-column {
        position: relative;
        max-height: none;
        border-right: none;
        border-bottom: 1px solid var(--border);
        padding-right: 0;
        padding-bottom: 16px;
        margin-bottom: 16px;
    }

    .main-column {
        padding-left: 0;
    }

    .sidebar-divider {
        display: none;
    }
}
"""
