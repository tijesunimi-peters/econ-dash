import plotly.graph_objects as go
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from styles import COLORS, CHART_TEMPLATE, RECESSIONS, trend_color, trend_arrow


# ── Existing: Treemap ─────────────────────────────────────────────────

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
        text_labels.append(
            f"<b>{s['name']}</b><br>"
            f"<span style='font-size:13px'>{arrow} {s['yoy_change_pct']:+.1f}%</span>"
        )

    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
        marker=dict(
            colors=yoy_changes,
            colorscale=[
                [0, "#c0392b"],
                [0.3, "#e74c3c"],
                [0.45, "#444"],
                [0.55, "#444"],
                [0.7, "#27ae60"],
                [1, "#00c896"],
            ],
            cmid=0,
            line=dict(width=2, color=COLORS["bg"]),
        ),
        customdata=custom_data,
        text=text_labels,
        textinfo="text",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "YoY Change: %{color:+.1f}%<br>"
            "<span style='color:" + COLORS["text_muted"] + "'>Click to drill down</span>"
            "<extra></extra>"
        ),
        textfont=dict(size=15, color=COLORS["text"]),
        maxdepth=1,
    ))
    fig.update_layout(
        margin=dict(t=0, l=0, r=0, b=0),
        height=420,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


# ── Existing: Breadcrumb ──────────────────────────────────────────────

def build_breadcrumb(country_name=None, sector_name=None, sub_industry_name=None):
    sep_cls = "separator"
    parts = []

    parts.append(html.A("Home", id="bc-home", href="#", n_clicks=0))

    if country_name and (sector_name or sub_industry_name):
        parts.append(html.Span("/", className=sep_cls))
        parts.append(html.A(country_name, id="bc-country", href="#", n_clicks=0))
    elif country_name:
        parts.append(html.Span("/", className=sep_cls))
        parts.append(html.Span(country_name, id="bc-country", className="current", n_clicks=0))
    else:
        parts.append(html.Span(id="bc-country", style={"display": "none"}, n_clicks=0))

    if sector_name and sub_industry_name:
        parts.append(html.Span("/", className=sep_cls))
        parts.append(html.A(sector_name, id="bc-sector", href="#", n_clicks=0))
    elif sector_name:
        parts.append(html.Span("/", className=sep_cls))
        parts.append(html.Span(sector_name, id="bc-sector", className="current", n_clicks=0))
    else:
        parts.append(html.Span(id="bc-sector", style={"display": "none"}, n_clicks=0))

    if sub_industry_name:
        parts.append(html.Span("/", className=sep_cls))
        parts.append(html.Span(sub_industry_name, className="current"))

    return html.Nav(parts, className="breadcrumb-nav")


# ── Existing: Sparkline Table ─────────────────────────────────────────

def build_sparkline_table(sub_industries):
    if not sub_industries:
        return html.P("No sub-industries found.", style={"color": COLORS["text_muted"]})

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

        sparkline_values = []
        if si.get("indicators"):
            sparkline_values = si["indicators"][0].get("sparkline", [])

        sparkline_color = COLORS["positive"] if yoy >= 0 else COLORS["negative"]

        sparkline_fig = go.Figure(go.Scatter(
            y=sparkline_values,
            mode="lines",
            line=dict(width=1.5, color=sparkline_color),
            fill="tozeroy",
            fillcolor=sparkline_color.replace(")", ", 0.1)").replace("rgb", "rgba") if "rgb" in sparkline_color else f"rgba({int(sparkline_color[1:3], 16)}, {int(sparkline_color[3:5], 16)}, {int(sparkline_color[5:7], 16)}, 0.1)",
        ))
        sparkline_fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            height=36, width=140,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
        )

        row = html.Tr([
            html.Td(si["name"], style={"fontWeight": "500", "color": COLORS["text"]}),
            html.Td(
                f"{si.get('latest_value_avg', 0):,.1f}",
                style={"fontFamily": "monospace", "color": COLORS["text_secondary"]},
            ),
            html.Td(
                f"{arrow} {yoy:+.1f}%",
                style={"color": color, "fontWeight": "600", "fontFamily": "monospace"},
            ),
            html.Td(
                dcc.Graph(
                    figure=sparkline_fig,
                    config={"displayModeBar": False},
                    style={"height": "36px", "width": "140px"},
                )
            ),
        ], id={"type": "si-row", "index": si["id"]}, n_clicks=0)
        rows.append(row)

    return html.Div([
        dbc.Table(
            [header, html.Tbody(rows)],
            hover=True, striped=True, responsive=True,
        ),
    ], className="data-table-card")


# ── Existing: Indicator Chart ─────────────────────────────────────────

def build_indicator_chart(indicator_name, unit, dates, values):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=values,
        mode="lines",
        name=indicator_name,
        line=dict(width=2, color=COLORS["chart_line"]),
        fill="tozeroy",
        fillcolor=COLORS["chart_area"],
        hovertemplate="%{y:,.2f}<extra></extra>",
    ))

    for rec in RECESSIONS:
        fig.add_vrect(
            x0=rec["start"], x1=rec["end"],
            fillcolor=COLORS["recession"], line_width=0,
            annotation_text=rec["label"], annotation_position="top left",
            annotation_font_size=10, annotation_font_color=COLORS["text_muted"],
        )

    fig.update_layout(
        title=f"{indicator_name} ({unit})",
        xaxis_title="",
        yaxis_title=unit,
        template=CHART_TEMPLATE,
        height=340,
    )
    return fig


# ── Existing: Date Controls ───────────────────────────────────────────

def build_date_controls():
    return dbc.ButtonGroup([
        dbc.Button("YTD", id="date-ytd", outline=True, color="primary", size="sm"),
        dbc.Button("1Y", id="date-1y", outline=True, color="primary", size="sm"),
        dbc.Button("2Y", id="date-2y", outline=True, color="primary", size="sm"),
        dbc.Button("5Y", id="date-5y", outline=True, color="primary", size="sm", active=True),
    ])


# ── Percentile Gauge ──────────────────────────────────────────────────

def build_percentile_gauge(indicator_data):
    if not indicator_data:
        return html.Div()

    percentile = indicator_data.get("percentile", 50)
    classification = indicator_data.get("classification", "normal")
    name = indicator_data.get("name", "")

    color_map = {
        "extreme_low": COLORS["negative"],
        "low": COLORS["warning"],
        "normal": COLORS["primary"],
        "high": COLORS["warning"],
        "extreme_high": COLORS["negative"],
    }
    gauge_color = color_map.get(classification, COLORS["primary"])

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=percentile,
        number={"suffix": "%ile", "font": {"size": 16, "color": COLORS["text"]}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": COLORS["text_muted"],
                     "tickfont": {"size": 10, "color": COLORS["text_muted"]}},
            "bar": {"color": gauge_color, "thickness": 0.6},
            "bgcolor": COLORS["surface_hover"],
            "borderwidth": 0,
            "steps": [
                {"range": [0, 5], "color": "rgba(255,87,87,0.15)"},
                {"range": [5, 20], "color": "rgba(255,179,71,0.1)"},
                {"range": [20, 80], "color": "rgba(108,140,255,0.05)"},
                {"range": [80, 95], "color": "rgba(255,179,71,0.1)"},
                {"range": [95, 100], "color": "rgba(255,87,87,0.15)"},
            ],
        },
    ))
    fig.update_layout(
        height=140, width=180,
        margin=dict(l=15, r=15, t=25, b=5),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["text_secondary"]),
    )

    return html.Div([
        html.P(name, style={"fontSize": "0.75rem", "color": COLORS["text_secondary"],
                             "marginBottom": "2px", "textAlign": "center"}),
        dcc.Graph(figure=fig, config={"displayModeBar": False},
                  style={"height": "140px", "width": "180px"}),
    ], className="percentile-gauge")


# ── Anomaly Panel ─────────────────────────────────────────────────────

def build_anomaly_panel(anomalies):
    if not anomalies:
        return html.Div()

    badge_colors = {"critical": "danger", "warning": "warning"}

    items = []
    for a in anomalies[:10]:
        severity = a.get("severity", "warning")
        z = a.get("z_score", 0)
        direction = a.get("direction", "")

        items.append(
            html.Div([
                dbc.Badge(severity.upper(), color=badge_colors.get(severity, "secondary"),
                          className="me-2", style={"fontSize": "0.7rem"}),
                html.Span(
                    f"{a.get('indicator_name', '')} ",
                    style={"color": COLORS["text"], "fontWeight": "500"},
                ),
                html.Span(
                    f"{abs(z):.1f}\u03c3 {direction} rolling mean",
                    style={"color": COLORS["text_secondary"], "fontSize": "0.85rem"},
                ),
                html.Span(
                    f" \u2014 {a.get('sector_name', '')}",
                    style={"color": COLORS["text_muted"], "fontSize": "0.8rem"},
                ),
            ], className="anomaly-item")
        )

    count = len(anomalies)
    critical_count = sum(1 for a in anomalies if a.get("severity") == "critical")

    header_text = f"{count} Anomalies Detected"
    if critical_count:
        header_text = f"{critical_count} Critical, {count - critical_count} Warning"

    return html.Div([
        dbc.Button(
            [html.Span("\u26a0 ", style={"marginRight": "6px"}), header_text],
            id="anomaly-toggle",
            color="link",
            className="anomaly-header-btn",
            n_clicks=0,
        ),
        dbc.Collapse(
            html.Div(items, className="anomaly-list"),
            id="anomaly-collapse",
            is_open=False,
        ),
    ], className="anomaly-panel")


# ── Intelligence Panel (merged cycle + executive summary) ─────────────

PHASE_ANGLES = {
    "expansion": 45, "peak": 135, "contraction": 225, "trough": 315,
}

PHASE_COLORS = {
    "expansion": COLORS["positive"],
    "peak": COLORS["warning"],
    "contraction": COLORS["negative"],
    "trough": COLORS["primary"],
}


def build_intelligence_panel(cycle_data, summary_data):
    """Unified panel: cycle clock (left) + traffic lights, leading indicators,
    sector recs, and narrative bullets (right)."""
    if not cycle_data and not summary_data:
        return html.Div()

    # ── Left column: Cycle Clock ──
    left = _build_cycle_clock_compact(cycle_data)

    # ── Right column: traffic lights + leading + recs + narrative ──
    right_children = []

    # Traffic lights (from executive summary)
    if summary_data:
        traffic_lights = summary_data.get("traffic_lights", [])
        if traffic_lights:
            light_colors = {
                "green": COLORS["positive"],
                "yellow": COLORS["warning"],
                "red": COLORS["negative"],
            }
            dots = []
            for tl in traffic_lights:
                c = light_colors.get(tl.get("color", "yellow"), COLORS["neutral"])
                dots.append(html.Div([
                    html.Div(style={
                        "width": "10px", "height": "10px", "borderRadius": "50%",
                        "background": c, "display": "inline-block",
                        "boxShadow": f"0 0 4px {c}",
                    }),
                    html.Span(tl.get("sector_name", ""), style={
                        "fontSize": "0.7rem", "color": COLORS["text_secondary"],
                        "marginLeft": "5px",
                    }),
                ], className="traffic-light-dot"))
            right_children.append(
                html.Div(dots, className="traffic-light-grid")
            )

    # Leading indicators (from cycle data)
    if cycle_data:
        leading = cycle_data.get("leading_indicators_summary", [])
        if leading:
            right_children.append(_build_leading_compact(leading))

        # Sector recommendations
        recs = cycle_data.get("sector_recommendations", [])
        phase = cycle_data.get("current_phase", "unknown")
        if recs and phase != "insufficient_data":
            right_children.append(_build_recs_compact(recs, phase))

    # Narrative bullets (from executive summary)
    if summary_data:
        narrative = summary_data.get("narrative", [])
        if narrative:
            right_children.append(
                html.Hr(style={"borderColor": COLORS["border"], "margin": "8px 0"})
            )
            right_children.append(_build_narrative_compact(narrative))

    return html.Div([
        dbc.Row([
            dbc.Col(left, width=4, className="d-flex align-items-center justify-content-center"),
            dbc.Col(right_children, width=8),
        ]),
    ], className="intelligence-panel")


def _build_cycle_clock_compact(cycle_data):
    """Compact cycle clock for the left column of the intelligence panel."""
    if not cycle_data or cycle_data.get("current_phase") == "insufficient_data":
        return html.Div(
            html.P("Awaiting cycle data",
                   style={"color": COLORS["text_muted"], "textAlign": "center",
                          "fontSize": "0.85rem"}),
        )

    current_phase = cycle_data.get("current_phase", "unknown")
    duration = cycle_data.get("phase_duration_months", 0)
    phase_color = PHASE_COLORS.get(current_phase, COLORS["neutral"])

    fig = go.Figure()

    phases = ["Expansion", "Peak", "Contraction", "Trough"]
    angles = [45, 135, 225, 315]
    colors = [COLORS["positive"], COLORS["warning"], COLORS["negative"], COLORS["primary"]]

    for phase, angle, color in zip(phases, angles, colors):
        is_current = phase.lower() == current_phase
        fig.add_trace(go.Scatterpolar(
            r=[0, 0.85, 0.85, 0],
            theta=[angle, angle - 40, angle + 40, angle],
            fill="toself",
            fillcolor=f"rgba({int(color[1:3], 16)},{int(color[3:5], 16)},{int(color[5:7], 16)},{'0.25' if is_current else '0.06'})",
            line=dict(color="rgba(0,0,0,0)"),
            showlegend=False, hoverinfo="skip",
        ))

    current_angle = PHASE_ANGLES.get(current_phase, 0)
    fig.add_trace(go.Scatterpolar(
        r=[0.55], theta=[current_angle],
        mode="markers",
        marker=dict(size=16, color=phase_color,
                    line=dict(width=2, color=COLORS["text"]), symbol="circle"),
        showlegend=False,
        hovertemplate=f"<b>{current_phase.title()}</b><br>{duration} months<extra></extra>",
    ))

    # Trail
    composite = cycle_data.get("composite_index", [])
    if len(composite) > 6:
        recent = composite[-12:]
        trail_theta = []
        trail_r = []
        for i in range(len(recent)):
            age_frac = i / max(len(recent) - 1, 1)
            trail_theta.append(current_angle - (1 - age_frac) * 90)
            trail_r.append(0.3 + age_frac * 0.25)
        fig.add_trace(go.Scatterpolar(
            r=trail_r, theta=trail_theta,
            mode="lines",
            line=dict(width=2, color=phase_color, dash="dot"),
            opacity=0.5, showlegend=False, hoverinfo="skip",
        ))

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=False, range=[0, 1]),
            angularaxis=dict(
                tickmode="array",
                tickvals=[45, 135, 225, 315],
                ticktext=["Expansion", "Peak", "Contraction", "Trough"],
                tickfont=dict(size=10, color=COLORS["text_secondary"]),
                gridcolor=COLORS["border"],
                linecolor=COLORS["border"],
            ),
        ),
        height=220,
        margin=dict(l=30, r=30, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )

    return html.Div([
        dcc.Graph(figure=fig, config={"displayModeBar": False},
                  style={"height": "220px"}),
        html.Div([
            html.Span(current_phase.title(),
                      style={"color": phase_color, "fontSize": "1.1rem",
                             "fontWeight": "700"}),
            html.Span(f" \u00b7 {duration}mo",
                      style={"color": COLORS["text_secondary"], "fontSize": "0.8rem",
                             "marginLeft": "6px"}),
        ], style={"textAlign": "center", "marginTop": "-8px"}),
    ])


def _build_leading_compact(leading_indicators):
    """Two-column compact grid of leading indicators."""
    items = []
    for ind in leading_indicators:
        direction = ind.get("direction", "stable")
        inverted = ind.get("inverted", False)
        rate = ind.get("rate_of_change")

        if inverted:
            effective_dir = {"accelerating": "decelerating",
                             "decelerating": "accelerating"}.get(direction, direction)
        else:
            effective_dir = direction

        dir_color = {
            "accelerating": COLORS["positive"],
            "decelerating": COLORS["negative"],
            "stable": COLORS["neutral"],
        }.get(effective_dir, COLORS["neutral"])
        dir_arrow = {
            "accelerating": "\u25b2",
            "decelerating": "\u25bc",
            "stable": "\u25ac",
        }.get(effective_dir, "\u25ac")

        rate_str = f"{rate:+.1f}%" if rate is not None else "N/A"
        name_short = ind.get("name", "")[:22]

        items.append(html.Div([
            html.Span(f"{dir_arrow} ", style={"color": dir_color, "fontSize": "0.75rem"}),
            html.Span(name_short, style={
                "color": COLORS["text"], "fontSize": "0.72rem", "fontWeight": "500",
            }),
            html.Span(f" {rate_str}", style={
                "color": dir_color, "fontSize": "0.7rem", "fontFamily": "monospace",
            }),
        ], className="leading-chip"))

    return html.Div([
        html.Div("Leading Indicators", className="intel-label"),
        html.Div(items, className="leading-chips-grid"),
    ], style={"marginTop": "8px"})


def _build_recs_compact(recs, phase):
    """Inline sector recommendation chips."""
    phase_color = PHASE_COLORS.get(phase, COLORS["neutral"])
    chips = [
        html.Span(sector, className="sector-rec-chip", style={
            "background": f"rgba({int(phase_color[1:3], 16)},{int(phase_color[3:5], 16)},{int(phase_color[5:7], 16)},0.15)",
            "color": phase_color,
            "border": f"1px solid {phase_color}",
        })
        for sector in recs
    ]
    return html.Div([
        html.Div("Favored Sectors", className="intel-label"),
        html.Div(chips, className="sector-rec-chips"),
    ], style={"marginTop": "6px"})


def _build_narrative_compact(narrative):
    """Compact narrative bullets."""
    category_icons = {
        "cycle": "\u26a1", "anomaly": "\u26a0", "momentum": "\u2191",
        "percentile": "\u2195", "divergence": "\u21c4",
    }
    bullets = []
    for bullet in narrative[:5]:
        icon = category_icons.get(bullet.get("category", ""), "\u2022")
        severity = bullet.get("severity")
        text_color = COLORS["negative"] if severity == "critical" else COLORS["text_secondary"]
        bullets.append(html.Li(
            f"{icon} {bullet.get('text', '')}",
            style={"color": text_color, "fontSize": "0.78rem", "marginBottom": "3px",
                   "lineHeight": "1.3"},
        ))
    return html.Ul(bullets, style={"listStyle": "none", "padding": "0", "margin": "0"})


# ── Momentum Scoreboard (compact 2-column for tab view) ──────────────

def build_momentum_scoreboard(momentum_data):
    if not momentum_data:
        return html.Div()

    cards = []
    for sector in momentum_data:
        score = sector.get("composite_score", 0)
        rank = sector.get("rank", 0)
        yoy = sector.get("yoy_change_pct", 0)
        rate_3m = sector.get("rate_of_change_3m", 0)
        accel = sector.get("acceleration_direction", "stable")
        name = sector.get("sector_name", "")

        bar_color = COLORS["positive"] if score >= 0 else COLORS["negative"]
        bar_width = min(abs(score), 100)

        accel_arrow = {
            "accelerating": "\u25b2\u25b2", "decelerating": "\u25bc\u25bc", "stable": "\u25ac",
        }.get(accel, "\u25ac")
        accel_color = {
            "accelerating": COLORS["positive"],
            "decelerating": COLORS["negative"],
            "stable": COLORS["neutral"],
        }.get(accel, COLORS["neutral"])

        card = html.Div([
            html.Div([
                html.Span(f"#{rank}", className="momentum-rank"),
                html.Span(name, className="momentum-name"),
                html.Span(accel_arrow, style={
                    "color": accel_color, "marginLeft": "8px", "fontSize": "0.7rem",
                }),
            ], className="momentum-header"),
            html.Div([
                html.Div(style={
                    "position": "absolute", "left": "50%", "top": "0", "bottom": "0",
                    "width": "1px", "background": COLORS["text_muted"],
                }),
                html.Div(style={
                    "position": "absolute",
                    "left": f"{min(50, 50 + score / 2)}%" if score < 0 else "50%",
                    "width": f"{bar_width / 2}%",
                    "top": "2px", "bottom": "2px",
                    "background": bar_color, "borderRadius": "3px",
                }),
            ], className="momentum-bar-container"),
            html.Div([
                html.Span(f"{score:+.0f}", style={
                    "color": bar_color, "fontWeight": "600", "fontFamily": "monospace",
                    "fontSize": "0.78rem",
                }),
                html.Span(f" YoY {yoy:+.1f}%", style={
                    "color": COLORS["text_secondary"], "fontSize": "0.72rem",
                }),
                html.Span(f" 3M {rate_3m:+.1f}%", style={
                    "color": COLORS["text_secondary"], "fontSize": "0.72rem",
                }),
            ], className="momentum-metrics"),
        ], className="momentum-card")
        cards.append(card)

    # 2-column grid layout
    return html.Div([
        html.H4("Sector Momentum Rankings", className="section-title",
                 style={"fontSize": "1rem"}),
        html.Div(cards, className="momentum-grid"),
    ], className="momentum-scoreboard")


# ── Cross-Country Comparison ──────────────────────────────────────────

def build_cross_country_comparison(compare_data):
    if not compare_data or not compare_data.get("comparisons"):
        return html.Div(
            html.P("No comparison data available",
                   style={"color": COLORS["text_muted"], "textAlign": "center"}),
        )

    comparisons = compare_data["comparisons"]
    home_code = compare_data.get("home", {}).get("code", "Home")
    other_code = compare_data.get("other", {}).get("code", "Other")

    sectors = [c["sector_name"] for c in comparisons]
    home_vals = [c["home_yoy"] for c in comparisons]
    other_vals = [-c["other_yoy"] for c in comparisons]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=sectors, x=home_vals, orientation="h",
        name=home_code, marker_color=COLORS["primary"],
        hovertemplate="%{y}: %{x:+.1f}% YoY<extra>" + home_code + "</extra>",
    ))
    fig.add_trace(go.Bar(
        y=sectors, x=other_vals, orientation="h",
        name=other_code, marker_color=COLORS["warning"],
        hovertemplate="%{y}: %{customdata:+.1f}% YoY<extra>" + other_code + "</extra>",
        customdata=[c["other_yoy"] for c in comparisons],
    ))
    fig.update_layout(
        barmode="overlay", template=CHART_TEMPLATE, height=350,
        title="YoY Change Comparison",
        xaxis=dict(title="YoY %", zeroline=True, zerolinecolor=COLORS["text_muted"]),
        yaxis=dict(autorange="reversed"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    )

    return html.Div(
        dcc.Graph(figure=fig, config={"displayModeBar": False}),
        className="chart-card",
    )


# ── Correlation Heatmap ───────────────────────────────────────────────

def build_correlation_heatmap(corr_data):
    if not corr_data or not corr_data.get("matrix"):
        return html.Div(
            html.P("No correlation data available",
                   style={"color": COLORS["text_muted"], "textAlign": "center"}),
        )

    labels = corr_data["labels"]
    matrix = corr_data["matrix"]
    divergences = corr_data.get("divergences", [])

    display_matrix = []
    for row in matrix:
        display_matrix.append([v if v is not None else float("nan") for v in row])

    fig = go.Figure(go.Heatmap(
        z=display_matrix, x=labels, y=labels,
        colorscale=[
            [0, COLORS["negative"]], [0.5, COLORS["surface"]], [1, COLORS["positive"]],
        ],
        zmin=-1, zmax=1,
        text=[[f"{v:.2f}" if v is not None else "" for v in row] for row in matrix],
        texttemplate="%{text}",
        textfont=dict(size=11, color=COLORS["text"]),
        hovertemplate="%{x} vs %{y}<br>Correlation: %{z:.3f}<extra></extra>",
        colorbar=dict(
            title="Corr",
            titlefont=dict(color=COLORS["text_secondary"]),
            tickfont=dict(color=COLORS["text_secondary"]),
        ),
    ))
    fig.update_layout(
        template=CHART_TEMPLATE, height=400,
        title="Sector Correlation Matrix",
        xaxis=dict(tickangle=45),
    )

    div_items = []
    for d in divergences[:5]:
        div_items.append(html.Div([
            html.Span(f"{d['sector_a']} \u2194 {d['sector_b']}: ",
                      style={"color": COLORS["text"], "fontWeight": "500",
                             "fontSize": "0.8rem"}),
            html.Span(
                f"Full: {d['full_period_correlation']:.2f} \u2192 "
                f"Rolling: {d['rolling_correlation']:.2f} (gap: {d['gap']:.2f})",
                style={"color": COLORS["warning"], "fontSize": "0.8rem"},
            ),
        ], style={"marginBottom": "4px"}))

    content = [dcc.Graph(figure=fig, config={"displayModeBar": False})]
    if div_items:
        content.append(html.Div([
            html.H6("Correlation Divergences",
                     style={"fontSize": "0.85rem", "color": COLORS["warning"],
                            "marginTop": "12px", "marginBottom": "8px"}),
            html.Div(div_items),
        ]))

    return html.Div(content, className="chart-card")
