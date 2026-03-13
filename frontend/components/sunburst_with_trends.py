"""
Sunburst Chart with Trend Lines for Expanded Sectors

Displays:
- Main sunburst chart for hierarchical sector/sub-industry visualization
- Detail panel with trend lines and sparklines when sector is expanded
- Historical trend data for selected sector and its sub-industries
"""

import plotly.graph_objects as go
from dash import html, dcc
import dash_bootstrap_components as dbc
from styles import COLORS, trend_arrow, trend_color


def build_sector_trend_sparkline(sparkline_data, yoy_pct, trend_direction):
    """
    Build a mini sparkline chart showing historical trend.

    Args:
        sparkline_data: List of float values (12-month historical)
        yoy_pct: YoY change percentage
        trend_direction: 'up', 'down', or 'flat'

    Returns:
        plotly.graph_objects.Figure: Compact sparkline chart
    """
    if not sparkline_data or len(sparkline_data) == 0:
        return go.Figure()

    # Calculate trend color based on YoY percentage
    color = trend_color(yoy_pct)

    # Convert hex to rgba for transparency
    # Extract hex color and convert to rgb
    if color.startswith('#'):
        hex_color = color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        fillcolor = f'rgba({r},{g},{b},0.2)'
    else:
        fillcolor = color

    fig = go.Figure(data=[
        go.Scatter(
            y=sparkline_data,
            mode='lines',
            line=dict(color=color, width=2),
            fill='tozeroy',
            fillcolor=fillcolor,  # Transparent fill
            hovertemplate='Value: %{y:.2f}<extra></extra>',
        )
    ])

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=50,
        showlegend=False,
        hovermode='x unified',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    )

    return fig


def build_sector_trend_detail(sector_name, sub_industries):
    """
    Build a detail panel showing trends for a selected sector's sub-industries.

    Args:
        sector_name: Name of the selected sector
        sub_industries: List of sub-industry dicts with indicators array

    Returns:
        Dash component with trend lines and details
    """
    if not sub_industries:
        return html.Div(
            html.P("No sub-industry data available", className="text-muted"),
            className="trend-detail-panel"
        )

    trend_rows = []
    for sub in sub_industries[:10]:  # Limit to 10 for readability
        sub_name = sub.get("name", "Unknown")
        sub_yoy = sub.get("yoy_change_pct", 0)
        trend_dir = sub.get("trend_direction", "flat")

        # Get sparkline from first indicator (or aggregate if multiple)
        indicators = sub.get("indicators", [])
        sparkline = []
        if indicators:
            # Use first indicator's sparkline, or average all if needed
            sparkline = indicators[0].get("sparkline", [])

        # Create mini sparkline
        fig = build_sector_trend_sparkline(sparkline, sub_yoy, trend_dir)

        # Format trend arrow
        arrow = trend_arrow(sub_yoy)
        color = trend_color(sub_yoy)

        trend_rows.append(
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Span(sub_name, style={"fontWeight": "500"}),
                            html.Span(
                                f"{arrow} {sub_yoy:+.1f}%",
                                style={
                                    "marginLeft": "8px",
                                    "color": color,
                                    "fontWeight": "600",
                                    "fontSize": "0.9rem"
                                }
                            ),
                        ], style={"display": "flex", "alignItems": "center"})
                    ], width=4),
                    dbc.Col([
                        dcc.Graph(
                            figure=fig,
                            config={"displayModeBar": False},
                            style={"margin": 0}
                        )
                    ], width=8),
                ], style={"paddingBottom": "12px", "borderBottom": f"1px solid {COLORS['border']}"}),
            ], className="trend-row")
        )

    return html.Div([
        html.H5(
            f"{sector_name} - Sub-Industry Trends",
            style={
                "marginBottom": "16px",
                "paddingBottom": "12px",
                "borderBottom": f"2px solid {COLORS['primary']}",
                "color": COLORS["text"]
            }
        ),
        html.Div(trend_rows),
    ], className="trend-detail-panel")


def build_sunburst_with_trends(sectors_with_subitems, country_name):
    """
    Build a complete sunburst chart with trend line support.

    Args:
        sectors_with_subitems: List of sector dicts with sub-industries and sparkline data
        country_name: Country name for the chart title

    Returns:
        dict: {
            'sunburst': Plotly figure for the sunburst chart,
            'trend_component': Dash component builder for trend details
        }
    """
    if not sectors_with_subitems:
        return {
            'sunburst': go.Figure(),
            'trend_component': lambda s: html.Div()
        }

    # Transform hierarchical data into Plotly sunburst structure
    labels = [""]  # Root label (invisible)
    parents = [""]  # Root parent
    values = [0]  # Root value (will be computed from children)
    colors = [0]  # Root color
    customdata = [""]  # Root customdata
    hover_texts = [""]  # Root hover text

    all_yoy_values = []  # Collect all YoY values for color scaling

    # First pass: collect all YoY values for proper color scaling
    for sector in sectors_with_subitems:
        all_yoy_values.append(sector["yoy_change_pct"])
        if "sub_industries" in sector:
            for sub in sector["sub_industries"]:
                all_yoy_values.append(sub.get("yoy_change_pct", 0))

    min_yoy = min(all_yoy_values) if all_yoy_values else -5
    max_yoy = max(all_yoy_values) if all_yoy_values else 5

    # Build sector and sub-industry hierarchy
    sector_values = []  # Track sector values for root computation
    for sector in sectors_with_subitems:
        sector_id = sector["id"]
        sector_name = sector["name"]
        sector_yoy = sector["yoy_change_pct"]
        sub_count = len(sector.get("sub_industries", []))

        # Add sector to hierarchy (inner ring)
        labels.append(sector_name)
        parents.append("")  # Parent is root
        values.append(sub_count if sub_count > 0 else 1)
        colors.append(sector_yoy)
        customdata.append(str(sector_id))

        # Build hover text for sector with trend indicator
        arrow = trend_arrow(sector_yoy)
        trend_icon = "📈" if sector_yoy > 0 else "📉" if sector_yoy < 0 else "→"
        sector_hover = (
            f"<b>{sector_name}</b><br>"
            f"YoY: {arrow} {sector_yoy:+.1f}%<br>"
            f"<span style='font-size:11px; color:{COLORS['text_muted']}'>"
            f"Sub-industries: {sub_count}<br>📊 Click to see trends</span>"
        )
        hover_texts.append(sector_hover)

        # Add sub-industries to hierarchy (outer ring)
        sub_industries = sector.get("sub_industries", [])
        for sub in sub_industries:
            sub_id = sub["id"]
            sub_name = sub["name"]
            sub_yoy = sub.get("yoy_change_pct", 0)
            indicator_count = sub.get("indicator_count", len(sub.get("indicators", [])))

            labels.append(sub_name)
            parents.append(sector_name)
            values.append(1)
            colors.append(sub_yoy)
            customdata.append(str(sub_id))

            # Build hover text for sub-industry
            arrow = trend_arrow(sub_yoy)
            sub_hover = (
                f"<b>{sub_name}</b><br>"
                f"YoY: {arrow} {sub_yoy:+.1f}%<br>"
                f"<span style='font-size:11px; color:{COLORS['text_muted']}'>"
                f"Indicators: {indicator_count}<br>📈 Click to view indicators</span>"
            )
            hover_texts.append(sub_hover)

        sector_values.append(sub_count if sub_count > 0 else 1)

    # Update root value to be sum of sector values
    values[0] = sum(sector_values) if sector_values else 1

    # Create sunburst figure
    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        marker=dict(
            colors=colors,
            colorscale=[
                [0, "#c0392b"],      # Deep red for -5%
                [0.3, "#e74c3c"],    # Light red for -2%
                [0.45, "#7f8c8d"],   # Gray for -0.5%
                [0.55, "#7f8c8d"],   # Gray for +0.5%
                [0.7, "#27ae60"],    # Green for +2%
                [1, "#00c896"],      # Bright green for +5%
            ],
            cmid=0,
            cmin=min_yoy,
            cmax=max_yoy,
            line=dict(width=2, color=COLORS["bg"]),
            showscale=False,
        ),
        customdata=customdata,
        text=labels,
        hovertext=hover_texts,
        hovertemplate="%{hovertext}<extra></extra>",
        textfont=dict(size=13, color=COLORS["text"]),
        maxdepth=2,
    ))

    fig.update_layout(
        title=dict(
            text=f"<b>{country_name} - Sector Performance</b><br>"
                 f"<span style='font-size:12px; color:{COLORS['text_muted']}'>"
                 f"Inner ring: Sectors | Outer ring: Sub-industries | "
                 f"Color: YoY Change | 📊 Click sector to see trend lines</span>",
            x=0.5,
            xanchor="center",
            font=dict(size=16, color=COLORS["text"]),
        ),
        margin=dict(t=120, l=0, r=0, b=0),
        height=500,
        paper_bgcolor=COLORS["surface"],
        font=dict(family="Arial, sans-serif", color=COLORS["text"]),
        clickmode="event+select",
    )

    # Create a function to build trend detail for a selected sector
    def build_trend_for_sector(sector_name):
        sector = next(
            (s for s in sectors_with_subitems if s["name"] == sector_name),
            None
        )
        if sector:
            return build_sector_trend_detail(sector_name, sector.get("sub_industries", []))
        return html.Div()

    return {
        'sunburst': fig,
        'trend_builder': build_trend_for_sector,
        'sectors_data': sectors_with_subitems
    }
