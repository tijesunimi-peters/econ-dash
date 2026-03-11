import plotly.graph_objects as go
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from styles import COLORS, CHART_TEMPLATE, RECESSIONS, trend_color, trend_arrow


def build_sector_treemap(sectors_summary, country_name):
    if not sectors_summary:
        return go.Figure()

    labels = [s["name"] for s in sectors_summary]
    parents = [""] * len(sectors_summary)
    values = [1] * len(sectors_summary)
    yoy_changes = [s["yoy_change_pct"] for s in sectors_summary]
    custom_data = [s["id"] for s in sectors_summary]

    text_labels = []
    for s in sectors_summary:
        arrow = trend_arrow(s["yoy_change_pct"])
        text_labels.append(f"<b>{s['name']}</b><br>{arrow} {s['yoy_change_pct']:+.1f}%")

    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
        marker=dict(
            colors=yoy_changes,
            colorscale="RdYlGn",
            cmid=0,
            line=dict(width=2, color="white"),
        ),
        customdata=custom_data,
        text=text_labels,
        textinfo="text",
        hovertemplate="<b>%{label}</b><br>YoY Change: %{color:+.1f}%<br>Click to drill down<extra></extra>",
        textfont=dict(size=16),
        maxdepth=1,
    ))
    fig.update_layout(
        margin=dict(t=10, l=10, r=10, b=10),
        height=450,
    )
    return fig


def build_breadcrumb(country_name=None, sector_name=None, sub_industry_name=None):
    """Build breadcrumb with always-present IDs for callback stability."""
    sep = " / "
    parts = []

    # Home - always a link
    parts.append(html.A("Home", id="bc-home", href="#", className="text-decoration-none", n_clicks=0))

    # Country
    if country_name and (sector_name or sub_industry_name):
        parts.append(html.Span(sep, className="text-muted"))
        parts.append(html.A(country_name, id="bc-country", href="#", className="text-decoration-none", n_clicks=0))
    elif country_name:
        parts.append(html.Span(sep, className="text-muted"))
        parts.append(html.Span(country_name, id="bc-country", className="fw-bold", n_clicks=0))
    else:
        parts.append(html.Span(id="bc-country", style={"display": "none"}, n_clicks=0))

    # Sector
    if sector_name and sub_industry_name:
        parts.append(html.Span(sep, className="text-muted"))
        parts.append(html.A(sector_name, id="bc-sector", href="#", className="text-decoration-none", n_clicks=0))
    elif sector_name:
        parts.append(html.Span(sep, className="text-muted"))
        parts.append(html.Span(sector_name, id="bc-sector", className="fw-bold", n_clicks=0))
    else:
        parts.append(html.Span(id="bc-sector", style={"display": "none"}, n_clicks=0))

    # Sub-industry (always terminal, never a link)
    if sub_industry_name:
        parts.append(html.Span(sep, className="text-muted"))
        parts.append(html.Span(sub_industry_name, className="fw-bold"))

    return html.Nav(parts, className="mb-2")


def build_sparkline_table(sub_industries):
    if not sub_industries:
        return html.P("No sub-industries found.")

    header = html.Thead(html.Tr([
        html.Th("Sub-Industry"),
        html.Th("Latest"),
        html.Th("YoY Change"),
        html.Th("Trend (12mo)"),
    ]))

    rows = []
    for si in sub_industries:
        yoy = si.get("yoy_change_pct", 0)
        color = trend_color(yoy)
        arrow = trend_arrow(yoy)

        # Build sparkline from first indicator's data
        sparkline_values = []
        if si.get("indicators"):
            sparkline_values = si["indicators"][0].get("sparkline", [])

        sparkline_fig = go.Figure(go.Scatter(
            y=sparkline_values,
            mode="lines",
            line=dict(width=1.5, color=COLORS["primary"]),
        ))
        sparkline_fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            height=40, width=150,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )

        row = html.Tr([
            html.Td(si["name"], style={"fontWeight": "500"}),
            html.Td(f"{si.get('latest_value_avg', 0):.1f}"),
            html.Td(
                f"{arrow} {yoy:+.1f}%",
                style={"color": color, "fontWeight": "bold"},
            ),
            html.Td(
                dcc.Graph(
                    figure=sparkline_fig,
                    config={"displayModeBar": False},
                    style={"height": "40px", "width": "150px"},
                )
            ),
        ], id={"type": "si-row", "index": si["id"]}, n_clicks=0,
           style={"cursor": "pointer"})
        rows.append(row)

    return dbc.Table(
        [header, html.Tbody(rows)],
        bordered=True, hover=True, striped=True, responsive=True,
    )


def build_indicator_chart(indicator_name, unit, dates, values):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=values,
        mode="lines",
        name=indicator_name,
        line=dict(width=2, color=COLORS["primary"]),
        hovertemplate="%{y:,.2f}<extra></extra>",
    ))

    for rec in RECESSIONS:
        fig.add_vrect(
            x0=rec["start"], x1=rec["end"],
            fillcolor="rgba(128,128,128,0.15)", line_width=0,
            annotation_text=rec["label"], annotation_position="top left",
            annotation_font_size=10, annotation_font_color="gray",
        )

    fig.update_layout(
        title=f"{indicator_name} ({unit})",
        xaxis_title="Date",
        yaxis_title=unit,
        template=CHART_TEMPLATE,
        height=350,
    )
    return fig


def build_date_controls():
    return dbc.ButtonGroup([
        dbc.Button("YTD", id="date-ytd", outline=True, color="primary", size="sm"),
        dbc.Button("1Y", id="date-1y", outline=True, color="primary", size="sm"),
        dbc.Button("2Y", id="date-2y", outline=True, color="primary", size="sm"),
        dbc.Button("5Y", id="date-5y", outline=True, color="primary", size="sm", active=True),
    ])
