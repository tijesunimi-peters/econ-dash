import plotly.graph_objects as go
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from styles import COLORS, CHART_TEMPLATE, RECESSIONS, trend_color, trend_arrow
from tooltips import get_tooltip


# ── Helper: Popover Trigger Builder ───────────────────────────────────

def _build_popover_trigger(tooltip_section, tooltip_key, trigger_id):
    """
    Build a (trigger_button, popover_component) tuple for help popovers.

    Args:
        tooltip_section (str): Section key from tooltips.py (e.g., 'metrics')
        tooltip_key (str): Tooltip key (e.g., 'yoy_change')
        trigger_id (str): Unique HTML ID for the trigger element

    Returns:
        tuple: (trigger_span, popover_component) to be added to parent
    """
    tooltip_data = get_tooltip(tooltip_section, tooltip_key)
    if not tooltip_data:
        return None, None

    trigger = html.Span(
        "?",
        id=trigger_id,
        className="popover-trigger",
        n_clicks=0,
        style={"cursor": "pointer", "marginLeft": "4px"},
    )

    popover = dbc.Popover(
        children=[
            dbc.PopoverHeader(tooltip_data["title"]),
            dbc.PopoverBody([
                dcc.Markdown(
                    tooltip_data["content"],
                    dangerously_allow_html=True,
                    style={"fontSize": "0.85rem", "lineHeight": "1.4"}
                ),
                html.Hr(style={"borderColor": COLORS["border"], "margin": "10px 0"}),
                html.Div(
                    [
                        html.Strong("💡 ", style={"marginRight": "4px"}),
                        html.Span(tooltip_data.get("action_items", ""),
                                 style={"fontSize": "0.8rem", "color": COLORS["text_secondary"]})
                    ],
                    style={"display": "flex", "alignItems": "flex-start"}
                )
            ])
        ],
        id=f"{trigger_id}-popover",
        target=trigger_id,
        is_open=False,
        placement="right",
        autohide=True,  # Auto-close when clicking outside
    )

    return trigger, popover


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

    # Build header with popovers
    trigger_latest, pop_latest = _build_popover_trigger("metrics", "percentile", "pop-latest-header")
    trigger_yoy, pop_yoy = _build_popover_trigger("metrics", "yoy_change", "pop-yoy-header")
    trigger_trend, pop_trend = _build_popover_trigger("metrics", "sparkline", "pop-trend-header")

    header = html.Thead(html.Tr([
        html.Th("Sub-Industry"),
        html.Th(["Latest", trigger_latest] if trigger_latest else "Latest"),
        html.Th(["YoY Change", trigger_yoy] if trigger_yoy else "YoY Change"),
        html.Th(["Trend (12mo)", trigger_trend] if trigger_trend else "Trend (12mo)"),
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

    # Collect all popovers
    popovers = [p for p in [pop_latest, pop_yoy, pop_trend] if p]

    return html.Div([
        dbc.Table(
            [header, html.Tbody(rows)],
            hover=True, striped=True, responsive=True,
        ),
        *popovers,  # Add all popovers to container
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

    # Build popover for percentile explanation
    trigger_perc, pop_perc = _build_popover_trigger("metrics", "percentile", "pop-percentile-gauge")

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
        html.Div([
            html.P(name, style={"fontSize": "0.75rem", "color": COLORS["text_secondary"],
                                 "marginBottom": "2px", "textAlign": "center"}),
            trigger_perc if trigger_perc else html.Div(),
        ], style={"textAlign": "center"}),
        dcc.Graph(figure=fig, config={"displayModeBar": False},
                  style={"height": "140px", "width": "180px"}),
        pop_perc if pop_perc else html.Div(),
    ], className="percentile-gauge")


# ── Anomaly Panel ─────────────────────────────────────────────────────

def build_anomaly_panel(anomalies):
    if not anomalies:
        return html.Div()

    badge_colors = {"critical": "danger", "warning": "warning"}

    # Build popovers for anomaly explanation
    trigger_zscore, pop_zscore = _build_popover_trigger("anomalies", "z_score", "pop-anomaly-zscore")
    trigger_severity, pop_severity = _build_popover_trigger("anomalies", "severity", "pop-anomaly-severity")

    items = []
    for a in anomalies[:10]:
        severity = a.get("severity", "warning")
        z = a.get("z_score", 0)
        direction = a.get("direction", "")

        items.append(
            html.Div([
                dbc.Badge(severity.upper(), color=badge_colors.get(severity, "secondary"),
                          className="me-2", style={"fontSize": "0.7rem"},
                          title="Click ? for severity explanation"),
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
        html.Div([
            dbc.Button(
                [html.Span("\u26a0 ", style={"marginRight": "6px"}), header_text],
                id="anomaly-toggle",
                color="link",
                className="anomaly-header-btn",
                n_clicks=0,
            ),
            trigger_zscore if trigger_zscore else html.Div(),
        ], style={"display": "flex", "alignItems": "center", "gap": "8px"}),
        dbc.Collapse(
            html.Div(items, className="anomaly-list"),
            id="anomaly-collapse",
            is_open=False,
        ),
        pop_zscore if pop_zscore else html.Div(),
        pop_severity if pop_severity else html.Div(),
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


def build_intelligence_panel(cycle_data, summary_data, factors_data=None):
    """Unified panel: cycle clock (left) + traffic lights, leading indicators,
    sector recs, narrative bullets, and causal factors (right)."""
    if not cycle_data and not summary_data and not factors_data:
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

    # Causal factors (if available)
    if factors_data:
        factors_panel = _build_factors_compact(factors_data)
        if factors_panel.children:  # Only add if there's content
            right_children.append(
                html.Hr(style={"borderColor": COLORS["border"], "margin": "8px 0"})
            )
            right_children.append(factors_panel)

    return html.Div([
        dbc.Row([
            dbc.Col(left, width=6),
            dbc.Col(right_children, width=6),
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

    # Build popovers for cycle explanation
    trigger_phase, pop_phase = _build_popover_trigger("business_cycle", "phase", "pop-cycle-phase")
    trigger_x, pop_x = _build_popover_trigger("business_cycle", "x_position", "pop-cycle-x")
    trigger_y, pop_y = _build_popover_trigger("business_cycle", "y_position", "pop-cycle-y")

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

    # Use cycle_position for precise 2D positioning within quadrant
    cycle_pos = cycle_data.get("cycle_position", {})
    x_pos = cycle_pos.get("x_position", 0.5)  # 0=trend low, 1=trend high
    y_pos = cycle_pos.get("y_position", 0.5)  # 0=decelerating, 1=accelerating
    momentum = cycle_pos.get("momentum", 0)

    # Map X,Y position to polar coordinates
    # X-axis determines distance from center (0=close, 1=far)
    # Y-axis determines angular offset within quadrant
    current_angle = PHASE_ANGLES.get(current_phase, 0)
    quadrant_width = 90  # degrees per quadrant

    # Distance from center (0.3-0.75 range)
    radius = 0.3 + x_pos * 0.45

    # Angular offset within quadrant based on Y position (-45 to +45 from quadrant center)
    angular_offset = (y_pos - 0.5) * quadrant_width / 2
    final_angle = current_angle + angular_offset

    # Marker size and color based on momentum
    marker_size = 20 + abs(momentum) * 2  # Larger if high momentum
    marker_color = phase_color if momentum >= 0 else COLORS["negative"]  # Red if decelerating

    fig.add_trace(go.Scatterpolar(
        r=[radius], theta=[final_angle],
        mode="markers",
        marker=dict(size=marker_size, color=marker_color,
                    line=dict(width=3, color=COLORS["text"]), symbol="circle"),
        showlegend=False,
        hovertemplate=(
            f"<b>{current_phase.title()}</b><br>"
            f"{duration} months<br>"
            f"Position: X={x_pos:.2f}, Y={y_pos:.2f}<br>"
            f"Momentum: {momentum:.2f}<extra></extra>"
        ),
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
            domain=dict(x=[0.05, 0.95], y=[0.05, 0.92]),
            radialaxis=dict(visible=False, range=[0, 1]),
            angularaxis=dict(
                tickmode="array",
                tickvals=[45, 135, 225, 315],
                ticktext=["Expansion", "Peak", "Contraction", "Trough"],
                tickfont=dict(size=14, color=COLORS["text_secondary"]),
                gridcolor=COLORS["border"],
                linecolor=COLORS["border"],
            ),
        ),
        height=420,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )

    # Build label with trigger (only include trigger if it exists)
    label_children = [
        html.Span(current_phase.title(),
                  style={"color": phase_color, "fontSize": "1.5rem",
                         "fontWeight": "700"}),
    ]
    if trigger_phase:
        label_children.append(trigger_phase)

    # Build popovers list (only include if they exist)
    popovers = [p for p in [pop_phase, pop_x, pop_y] if p]

    return html.Div([
        dcc.Graph(figure=fig, config={"displayModeBar": False},
                  style={"height": "420px", "width": "100%"}),
        html.Div([
            html.Div(
                label_children,
                style={"display": "flex", "alignItems": "center", "justifyContent": "center"}
            ),
            html.Span(f" \u00b7 {duration}mo",
                      style={"color": COLORS["text_secondary"], "fontSize": "1rem",
                             "marginLeft": "8px"}),
        ], style={"textAlign": "center", "marginTop": "-12px"}),
        *popovers,  # Unpack only non-None popovers
    ], style={"width": "100%"})


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

    # Build popover for sector recommendations
    trigger_recs, pop_recs = _build_popover_trigger("business_cycle", "sector_recommendations", "pop-sector-recs")

    chips = [
        html.Span(sector, className="sector-rec-chip", style={
            "background": f"rgba({int(phase_color[1:3], 16)},{int(phase_color[3:5], 16)},{int(phase_color[5:7], 16)},0.15)",
            "color": phase_color,
            "border": f"1px solid {phase_color}",
        })
        for sector in recs
    ]
    return html.Div([
        html.Div([
            html.Span("Favored Sectors", className="intel-label", style={"marginRight": "6px"}),
            trigger_recs if trigger_recs else html.Div(),
        ], style={"display": "flex", "alignItems": "center"}),
        html.Div(chips, className="sector-rec-chips"),
        pop_recs if pop_recs else html.Div(),
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

    # Build popovers for momentum explanation
    trigger_momentum, pop_momentum = _build_popover_trigger("momentum", "momentum_scale", "pop-momentum-scale")
    trigger_roc, pop_roc = _build_popover_trigger("momentum", "rate_of_change", "pop-momentum-roc")

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
        html.Div([
            html.H4("Sector Momentum Rankings", className="section-title",
                     style={"fontSize": "1rem", "marginBottom": "0", "borderBottom": "none"}),
            trigger_momentum if trigger_momentum else html.Div(),
        ], style={"display": "flex", "alignItems": "center", "gap": "8px", "marginBottom": "16px"}),
        html.Div(cards, className="momentum-grid"),
        pop_momentum if pop_momentum else html.Div(),
        pop_roc if pop_roc else html.Div(),
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


# ── Market Sentiment Panel ────────────────────────────────────────

def build_market_sentiment(sentiment_data):
    """Market expectations and sentiment indicators panel."""
    if not sentiment_data:
        return html.Div()

    indicators = sentiment_data.get("sentiment_indicators", [])
    if not indicators:
        return html.Div()

    cards = []
    for ind in indicators:
        metric_type = ind.get("metric_type", "")
        label = ind.get("metric_label", "")
        value = float(ind.get("value", 0))
        unit = ind.get("unit", "")
        trend = ind.get("trend", "stable")
        interpretation = ind.get("interpretation")
        change = ind.get("change_from_prior")
        source = ind.get("source", "")

        # Trend arrow and color
        trend_arrows = {"up": "\u25b2", "down": "\u25bc", "stable": "\u25ac"}
        trend_colors = {
            "up": COLORS["positive"],
            "down": COLORS["negative"],
            "stable": COLORS["neutral"]
        }
        arrow = trend_arrows.get(trend, "\u25ac")
        t_color = trend_colors.get(trend, COLORS["neutral"])

        # PMI threshold coloring: >50 = expansion (green), <50 = contraction (red)
        if metric_type in ("pmi", "services_pmi"):
            value_color = COLORS["positive"] if value > 50 else COLORS["negative"]
        elif metric_type == "cci":
            value_color = COLORS["positive"] if value > 100 else COLORS["warning"]
        elif metric_type == "vix":
            value_color = COLORS["positive"] if value < 20 else (COLORS["warning"] if value < 30 else COLORS["negative"])
        else:
            value_color = COLORS["text"]

        # Format value display
        if unit == "%":
            value_display = f"{value:.1f}%"
        elif unit == "index":
            value_display = f"{value:.1f}"
        else:
            value_display = f"{value:.2f} {unit}"

        # Change display
        change_display = ""
        if change is not None:
            change_val = float(change)
            change_sign = "+" if change_val > 0 else ""
            if unit == "%":
                change_display = f"{change_sign}{change_val:.1f}pp"
            else:
                change_display = f"{change_sign}{change_val:.1f}"

        card = html.Div([
            # Header: label
            html.Div(
                label,
                style={
                    "fontSize": "0.72rem",
                    "fontWeight": "600",
                    "color": COLORS["text_secondary"],
                    "textTransform": "uppercase",
                    "letterSpacing": "0.3px",
                    "marginBottom": "6px",
                }
            ),
            # Value row
            html.Div([
                html.Span(
                    value_display,
                    style={
                        "fontSize": "1.3rem",
                        "fontWeight": "700",
                        "color": value_color,
                        "fontFamily": "monospace",
                    }
                ),
                html.Span(
                    f" {arrow}",
                    style={
                        "color": t_color,
                        "fontSize": "0.85rem",
                        "marginLeft": "6px",
                    }
                ),
            ], style={"marginBottom": "4px"}),
            # Change from prior
            html.Div([
                html.Span(
                    change_display,
                    style={
                        "fontSize": "0.75rem",
                        "fontFamily": "monospace",
                        "color": t_color,
                        "marginRight": "8px",
                    }
                ) if change_display else html.Span(),
                html.Span(
                    interpretation or "",
                    style={
                        "fontSize": "0.7rem",
                        "color": value_color,
                        "fontWeight": "500",
                    }
                ) if interpretation else html.Span(),
            ], style={"marginBottom": "4px"}),
            # Source
            html.Div(
                source,
                style={
                    "fontSize": "0.65rem",
                    "color": COLORS["text_muted"],
                    "fontStyle": "italic",
                }
            ),
        ], className="sentiment-card")

        cards.append(card)

    last_updated = sentiment_data.get("last_updated", "")

    return html.Div([
        html.Div([
            html.H4("Market Sentiment", className="section-title",
                     style={"fontSize": "1rem", "marginBottom": "0", "borderBottom": "none"}),
            html.Span(
                f"Updated: {last_updated}" if last_updated else "",
                style={"fontSize": "0.7rem", "color": COLORS["text_muted"]}
            ),
        ], style={
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "space-between",
            "marginBottom": "14px",
        }),
        html.Div(cards, className="sentiment-grid"),
    ], className="sentiment-panel")


# ── Policy Timeline Panel ─────────────────────────────────────────

def build_policy_timeline(policies):
    """Timeline of central bank and government policy decisions."""
    if not policies:
        return html.Div()

    items = []
    for policy in policies:
        # Status color mapping
        status_colors = {
            "announced": COLORS["warning"],
            "effective": COLORS["primary"],
            "completed": COLORS["positive"],
            "reversed": COLORS["negative"]
        }
        status_color = status_colors.get(policy.get("status"), COLORS["neutral"])

        # Format dates
        announcement = policy.get("announcement_date", "")
        effective = policy.get("effective_date", "")

        # Build sector badges
        sectors = policy.get("impact_sectors", [])
        sector_badges = []
        for sector in sectors[:3]:  # Show max 3 sectors
            sector_badges.append(
                dbc.Badge(
                    sector,
                    color="secondary",
                    pill=True,
                    className="me-1 mb-1",
                    style={"fontSize": "0.65rem", "padding": "4px 8px"}
                )
            )
        if len(sectors) > 3:
            sector_badges.append(
                dbc.Badge(
                    f"+{len(sectors)-3}",
                    color="secondary",
                    pill=True,
                    className="me-1 mb-1",
                    style={"fontSize": "0.65rem", "padding": "4px 8px"}
                )
            )

        # Build policy item
        item = html.Div([
            # Top row: date, type, status
            html.Div([
                html.Span(
                    announcement,
                    style={
                        "fontFamily": "monospace",
                        "fontSize": "0.8rem",
                        "color": COLORS["text_muted"],
                        "minWidth": "90px"
                    }
                ),
                html.Span(
                    policy.get("type_label", "").upper(),
                    style={
                        "fontWeight": "600",
                        "fontSize": "0.8rem",
                        "marginLeft": "12px",
                        "color": COLORS["text"]
                    }
                ),
                dbc.Badge(
                    policy.get("status", "").upper(),
                    color=status_colors.get(policy.get("status"), "secondary"),
                    className="ms-auto",
                    style={"fontSize": "0.65rem"}
                ),
            ], style={
                "display": "flex",
                "alignItems": "center",
                "marginBottom": "6px",
                "justifyContent": "space-between"
            }),

            # Description
            html.Div(
                policy.get("description", ""),
                style={
                    "color": COLORS["text"],
                    "fontSize": "0.9rem",
                    "marginBottom": "6px",
                    "lineHeight": "1.3"
                }
            ),

            # Impact sectors
            html.Div(
                sector_badges,
                style={"marginBottom": "6px", "display": "flex", "flexWrap": "wrap"}
            ) if sector_badges else html.Div(),

            # Footer: effective date, lag, source
            html.Div([
                html.Span(
                    f"Effective: {effective}",
                    style={
                        "fontSize": "0.75rem",
                        "color": COLORS["text_muted"],
                        "marginRight": "12px"
                    }
                ),
                html.Span(
                    f"Lag: {policy.get('expected_lag_months', 0)}mo",
                    style={
                        "fontSize": "0.75rem",
                        "color": COLORS["text_muted"],
                        "marginRight": "12px"
                    }
                ),
                html.Span(
                    f"({policy.get('source', '')})",
                    style={
                        "fontSize": "0.7rem",
                        "color": COLORS["text_muted"],
                        "fontStyle": "italic"
                    }
                ),
            ], style={"display": "flex", "alignItems": "center"}),
        ], className="policy-timeline-item")

        items.append(item)

    return html.Div([
        html.H4("Policy Timeline", className="section-title", style={"fontSize": "1rem"}),
        html.Div(
            items,
            className="policy-timeline",
            style={
                "maxHeight": "400px",
                "overflowY": "auto",
                "paddingRight": "8px"
            }
        ),
    ], className="policy-panel")


# ── Causal Factors Panel ──────────────────────────────────────────

def _build_factors_compact(factors_data):
    """Build compact causal factors chips for the intelligence panel."""
    if not factors_data or not isinstance(factors_data, list) or len(factors_data) == 0:
        return html.Div()

    # Build popovers for causal factors
    trigger_corr, pop_corr = _build_popover_trigger("causal_factors", "correlation", "pop-factor-correlation")
    trigger_status, pop_status = _build_popover_trigger("causal_factors", "proxy_status", "pop-factor-status")
    trigger_confidence, pop_confidence = _build_popover_trigger("causal_factors", "confidence", "pop-factor-confidence")

    # Take top 5 factors
    top_factors = factors_data[:5]

    chips = []
    for factor in top_factors:
        correlation = factor.get("correlation_with_sector", 0)
        confidence = factor.get("confidence", 0)
        name = factor.get("name", "Unknown")
        affected_sectors = factor.get("affected_sectors", [])
        proxy_status = factor.get("proxy_status", "unknown")

        # Color coding based on confidence
        if confidence >= 0.7:
            bg_color = "rgba(39, 174, 96, 0.15)"  # Green
            border_color = COLORS["positive"]
        elif confidence >= 0.5:
            bg_color = "rgba(241, 196, 15, 0.15)"  # Yellow
            border_color = COLORS["warning"]
        else:
            bg_color = "rgba(192, 57, 43, 0.15)"  # Red
            border_color = COLORS["negative"]

        # Status indicator
        status_emoji = {"rising": "📈", "falling": "📉", "stable": "➡️", "unknown": "❓"}.get(
            proxy_status, "?"
        )

        # Build sector tags
        sector_tags = []
        for sector in affected_sectors[:2]:  # Show max 2 sectors
            sector_tags.append(
                html.Span(
                    sector,
                    style={
                        "display": "inline-block",
                        "fontSize": "0.65rem",
                        "padding": "2px 6px",
                        "backgroundColor": COLORS["surface_hover"],
                        "borderRadius": "3px",
                        "marginRight": "4px",
                        "marginTop": "4px",
                        "color": COLORS["text_secondary"],
                    },
                )
            )
        if len(affected_sectors) > 2:
            sector_tags.append(
                html.Span(
                    f"+{len(affected_sectors) - 2}",
                    style={
                        "display": "inline-block",
                        "fontSize": "0.65rem",
                        "marginTop": "4px",
                        "color": COLORS["text_muted"],
                    },
                )
            )

        # Build chip
        chip = html.Div(
            [
                html.Div(
                    [
                        html.Span(
                            f"{status_emoji} {name}",
                            style={
                                "fontSize": "0.75rem",
                                "fontWeight": "600",
                                "color": COLORS["text"],
                                "display": "block",
                                "marginBottom": "4px",
                            },
                        ),
                        html.Span(
                            f"r={correlation:.2f}",
                            style={
                                "fontSize": "0.65rem",
                                "fontFamily": "monospace",
                                "color": border_color,
                                "fontWeight": "600",
                            },
                        ),
                    ]
                ),
                html.Div(sector_tags, style={"display": "flex", "flexWrap": "wrap"}),
            ],
            style={
                "padding": "8px 10px",
                "backgroundColor": bg_color,
                "border": f"1px solid {border_color}",
                "borderRadius": "4px",
                "marginRight": "8px",
                "marginBottom": "8px",
                "minWidth": "120px",
                "flex": "0 0 auto",
            },
            title=factor.get("description", ""),
        )
        chips.append(chip)

    if not chips:
        return html.Div()

    return html.Div(
        [
            html.Div([
                html.Div(
                    "Causal Factors",
                    style={
                        "fontSize": "0.75rem",
                        "fontWeight": "600",
                        "color": COLORS["text_secondary"],
                        "textTransform": "uppercase",
                        "letterSpacing": "0.5px",
                    },
                ),
                trigger_corr if trigger_corr else html.Div(),
            ], style={"display": "flex", "alignItems": "center", "gap": "6px", "marginBottom": "8px"}),
            html.Div(chips, style={"display": "flex", "flexWrap": "wrap"}),
            pop_corr if pop_corr else html.Div(),
            pop_status if pop_status else html.Div(),
            pop_confidence if pop_confidence else html.Div(),
        ]
    )


# ── Structural Health Panel (Demographics, Debt, Productivity) ─────────────

def _build_mini_sparkline(historical_data, forecast_data=None):
    """Create tiny inline sparkline chart for metric card (30px height).

    Optionally includes forecast as dashed line if forecast_data provided.
    """
    if not historical_data or len(historical_data) < 2:
        return None

    try:
        hist_dates = [d["date"] if isinstance(d["date"], str) else d["date"].isoformat() for d in historical_data]
        hist_values = [float(d["value"]) for d in historical_data]

        # Build traces
        traces = [go.Scatter(
            x=hist_dates,
            y=hist_values,
            mode='lines',
            name='Historical',
            line=dict(color=COLORS["primary"], width=1.5),
            fill='tozeroy',
            fillcolor='rgba(59, 130, 246, 0.1)',
            hoverinfo='none'
        )]

        # Add forecast if available
        if forecast_data and len(forecast_data) > 0:
            # Combine last historical point with forecast for continuity
            last_hist_date = hist_dates[-1]
            last_hist_value = hist_values[-1]

            forecast_dates = [last_hist_date] + [f["date"] if isinstance(f["date"], str) else f["date"].isoformat()
                                                  for f in forecast_data]
            forecast_values = [last_hist_value] + [float(f["value"]) for f in forecast_data]

            traces.append(go.Scatter(
                x=forecast_dates,
                y=forecast_values,
                mode='lines',
                name='Forecast',
                line=dict(color=COLORS["warning"], width=1.5, dash='dash'),
                hoverinfo='none',
                opacity=0.7
            ))

        fig = go.Figure(data=traces)

        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            height=30,
            width=100,
            showlegend=False,
            xaxis_visible=False,
            yaxis_visible=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hovermode=False
        )

        return dcc.Graph(
            figure=fig,
            config={"displayModeBar": False, "responsive": True},
            style={"marginTop": "4px", "marginBottom": "4px", "height": "30px"}
        )
    except Exception:
        return None


def build_structural_health(structural_data, debt_data):
    """Long-term structural trends panel: demographics, debt, productivity."""
    if not structural_data or not debt_data:
        return html.Div()

    structural_metrics = structural_data.get("structural_metrics", [])
    debt_metrics = debt_data.get("debt_metrics", [])

    if not structural_metrics or not debt_metrics:
        return html.Div()

    # Group structural metrics by category
    structural_by_category = {}
    for metric in structural_metrics:
        category = metric.get("category", "other")
        if category not in structural_by_category:
            structural_by_category[category] = []
        structural_by_category[category].append(metric)

    # Group debt metrics by category
    debt_by_category = {}
    for metric in debt_metrics:
        category = metric.get("category", "other")
        if category not in debt_by_category:
            debt_by_category[category] = []
        debt_by_category[category].append(metric)

    def build_metric_card(metric):
        """Build a single metric card with alert coloring, sparkline, and enhanced metadata."""
        label = metric.get("metric_label", "")
        value = metric.get("value", 0)
        unit = metric.get("unit", "")
        alert_level = metric.get("alert_level", "none")
        source = metric.get("source", "")
        trend = metric.get("trend")
        trend_interp = metric.get("trend_interpretation")
        trend_5year = metric.get("trend_5year")
        historical = metric.get("historical", [])
        data_source = metric.get("data_source", "Seed Data")
        last_updated = metric.get("last_updated")

        # Alert color
        if alert_level == "critical":
            border_color = COLORS["negative"]
            value_color = COLORS["negative"]
        elif alert_level == "warning":
            border_color = COLORS["warning"]
            value_color = COLORS["warning"]
        else:
            border_color = COLORS["border"]
            value_color = COLORS["text"]

        # Format value display
        try:
            val_float = float(value)
            if unit in ("%", "% of GDP", "% of income"):
                value_display = f"{val_float:.1f}{unit.replace('% of GDP', '%').replace('% of income', '%')}"
            elif unit == "years":
                value_display = f"{val_float:.1f} {unit}"
            elif unit == "ratio":
                value_display = f"{val_float:.2f}x"
            else:
                value_display = f"{val_float:.1f} {unit}"
        except:
            value_display = f"{value} {unit}"

        # Trend display for debt metrics or 5-year trend
        trend_display = ""
        if trend:
            trend_arrows = {"up": "↑", "down": "↓", "stable": "→"}
            trend_display = trend_arrows.get(trend, "→")
        elif trend_5year:
            trend_arrows = {"up": "↑", "down": "↓", "stable": "→"}
            trend_display = trend_arrows.get(trend_5year, "→")

        # Build sparkline if historical data available
        sparkline = _build_mini_sparkline(historical) if historical else None

        # Format last_updated date
        last_updated_display = ""
        if last_updated:
            try:
                if isinstance(last_updated, str):
                    last_updated_display = last_updated.split("T")[0]
                else:
                    last_updated_display = last_updated.strftime("%Y-%m-%d")
            except:
                pass

        card_content = [
            # Header with label
            html.Div(
                [
                    html.Span(label, style={"flex": "1"}),
                    html.Span(trend_display, style={
                        "fontSize": "1.1rem",
                        "marginLeft": "6px",
                        "color": value_color
                    }) if trend_display else html.Span(),
                ],
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "fontSize": "0.72rem",
                    "fontWeight": "600",
                    "color": COLORS["text_secondary"],
                    "textTransform": "uppercase",
                    "letterSpacing": "0.3px",
                    "marginBottom": "8px",
                }
            ),
            # Value display
            html.Div(
                value_display,
                style={
                    "fontSize": "1.4rem",
                    "fontWeight": "700",
                    "color": value_color,
                    "fontFamily": "monospace",
                    "marginBottom": "6px",
                }
            ),
            # Sparkline (if available)
            sparkline if sparkline else html.Div(),
            # Interpretation (for debt metrics)
            html.Div(
                trend_interp or "",
                style={
                    "fontSize": "0.7rem",
                    "color": COLORS["text_secondary"],
                    "marginBottom": "6px",
                    "minHeight": "20px",
                }
            ) if trend_interp else html.Div(),
            # Metadata footer (Last updated + Data source)
            html.Div([
                html.Span(f"Updated: {last_updated_display}", style={
                    "fontSize": "0.65rem",
                    "color": COLORS["text_muted"],
                }) if last_updated_display else html.Span(),
                html.Span(f"• {data_source}", style={
                    "fontSize": "0.65rem",
                    "color": COLORS["text_muted"],
                    "marginLeft": "4px"
                })
            ], style={
                "display": "flex",
                "alignItems": "center",
                "marginTop": "4px",
                "borderTop": f"1px solid {COLORS['border']}",
                "paddingTop": "4px"
            }),
        ]

        return html.Div(
            card_content,
            className="structural-metric-card",
            style={
                "backgroundColor": "rgba(255, 255, 255, 0.02)",
                "border": f"1px solid {border_color}",
                "borderRadius": "8px",
                "padding": "12px 14px",
                "transition": "all 0.15s",
            }
        )

    sections = []

    # Demographics section
    if "demographics" in structural_by_category:
        demo_cards = [build_metric_card(m) for m in structural_by_category["demographics"]]
        sections.append(
            html.Div([
                html.Div(
                    "Demographics",
                    className="structural-section-title",
                    style={
                        "fontSize": "0.9rem",
                        "fontWeight": "600",
                        "color": COLORS["text"],
                        "marginBottom": "12px",
                        "textTransform": "uppercase",
                        "letterSpacing": "0.5px",
                    }
                ),
                html.Div(demo_cards, className="structural-grid"),
            ], className="structural-section")
        )

    # Debt & Stability section
    if debt_by_category:
        debt_cards = [build_metric_card(m) for cat_metrics in debt_by_category.values() for m in cat_metrics]
        sections.append(
            html.Div([
                html.Div(
                    "Debt & Stability",
                    className="structural-section-title",
                    style={
                        "fontSize": "0.9rem",
                        "fontWeight": "600",
                        "color": COLORS["text"],
                        "marginBottom": "12px",
                        "textTransform": "uppercase",
                        "letterSpacing": "0.5px",
                    }
                ),
                html.Div(debt_cards, className="structural-grid"),
            ], className="structural-section")
        )

    # Productivity section
    if "productivity" in structural_by_category:
        prod_cards = [build_metric_card(m) for m in structural_by_category["productivity"]]
        sections.append(
            html.Div([
                html.Div(
                    "Productivity & Innovation",
                    className="structural-section-title",
                    style={
                        "fontSize": "0.9rem",
                        "fontWeight": "600",
                        "color": COLORS["text"],
                        "marginBottom": "12px",
                        "textTransform": "uppercase",
                        "letterSpacing": "0.5px",
                    }
                ),
                html.Div(prod_cards, className="structural-grid"),
            ], className="structural-section")
        )

    last_updated = structural_data.get("last_updated", "")

    return html.Div([
        html.Div([
            html.H4("Structural Health", className="section-title",
                     style={"fontSize": "1rem", "marginBottom": "0", "borderBottom": "none"}),
            html.Span(
                f"Updated: {last_updated}" if last_updated else "",
                style={"fontSize": "0.7rem", "color": COLORS["text_muted"]}
            ),
        ], style={
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "space-between",
            "marginBottom": "14px",
        }),
        html.Div(sections, style={"display": "flex", "flexDirection": "column", "gap": "16px"}),
    ], className="structural-panel")


def build_trade_flows(trade_data):
    """Trade flows & supply chain panel: exports, imports, FDI, supply chain risk."""
    if not trade_data or "trade_flows" not in trade_data:
        return html.Div()

    trade_flows = trade_data.get("trade_flows", [])
    if not trade_flows:
        return html.Div()

    # Group by category
    by_category = {}
    for flow in trade_flows:
        cat = flow.get("category", "other")
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(flow)

    def build_flow_card(flow):
        """Build single trade flow metric card."""
        label = flow.get("metric_label", "")
        value = flow.get("value", 0)
        unit = flow.get("unit", "")
        alert = flow.get("alert_level", "none")
        trend = flow.get("trend_5year")
        historical = flow.get("historical", [])

        # Color coding
        if alert == "critical":
            border_color = COLORS["negative"]
            value_color = COLORS["negative"]
        elif alert == "warning":
            border_color = COLORS["warning"]
            value_color = COLORS["warning"]
        else:
            border_color = COLORS["border"]
            value_color = COLORS["text"]

        # Format value
        try:
            val_float = float(value)
            if unit in ("%", "% of GDP"):
                value_display = f"{val_float:.1f}%"
            elif unit == "ratio":
                value_display = f"{val_float:.2f}x"
            elif unit == "index":
                value_display = f"{val_float:.0f}"
            else:
                value_display = f"{val_float:.1f} {unit}"
        except:
            value_display = f"{value} {unit}"

        # Trend arrow
        trend_display = ""
        if trend:
            arrows = {"up": "↑", "down": "↓", "stable": "→"}
            trend_display = arrows.get(trend, "→")

        # Sparkline
        sparkline = _build_mini_sparkline(historical) if historical else None

        card_content = [
            html.Div([
                html.Span(label, style={"flex": "1"}),
                html.Span(trend_display, style={
                    "fontSize": "1.1rem", "marginLeft": "6px", "color": value_color
                }) if trend_display else html.Span()
            ], style={
                "display": "flex", "alignItems": "center",
                "fontSize": "0.72rem", "fontWeight": "600",
                "marginBottom": "8px"
            }),
            html.Div(value_display, style={
                "fontSize": "1.4rem", "fontWeight": "700", "color": value_color,
                "fontFamily": "monospace", "marginBottom": "6px"
            }),
            sparkline or html.Div(),
            html.Div([
                html.Span(f"Updated: {flow.get('date', '')}", style={
                    "fontSize": "0.65rem", "color": COLORS["text_muted"]
                }),
                html.Span(f"• {flow.get('data_source', 'Unknown')}", style={
                    "fontSize": "0.65rem", "marginLeft": "4px", "color": COLORS["text_muted"]
                })
            ], style={"marginTop": "4px", "paddingTop": "4px"})
        ]

        return html.Div(card_content, className="trade-card", style={
            "backgroundColor": "rgba(255,255,255,0.02)",
            "border": f"1px solid {border_color}",
            "borderRadius": "8px", "padding": "12px 14px",
            "transition": "all 0.15s"
        })

    sections = []

    # Trade Balance Section
    if "balance" in by_category:
        cards = [build_flow_card(f) for f in by_category["balance"]]
        sections.append(html.Div([
            html.Div("Trade Balance", className="trade-section-title", style={
                "fontSize": "0.9rem", "fontWeight": "600", "marginBottom": "12px"
            }),
            html.Div(cards, className="trade-grid", style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fill, minmax(140px, 1fr))",
                "gap": "12px"
            })
        ]))

    # Imports/Exports Section
    if "volumes" in by_category:
        cards = [build_flow_card(f) for f in by_category["volumes"]]
        sections.append(html.Div([
            html.Div("Import/Export Flows", className="trade-section-title", style={
                "fontSize": "0.9rem", "fontWeight": "600", "marginBottom": "12px"
            }),
            html.Div(cards, className="trade-grid", style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fill, minmax(140px, 1fr))",
                "gap": "12px"
            })
        ]))

    # Investment Section
    if "investment" in by_category:
        cards = [build_flow_card(f) for f in by_category["investment"]]
        sections.append(html.Div([
            html.Div("Foreign Investment", className="trade-section-title", style={
                "fontSize": "0.9rem", "fontWeight": "600", "marginBottom": "12px"
            }),
            html.Div(cards, className="trade-grid", style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fill, minmax(140px, 1fr))",
                "gap": "12px"
            })
        ]))

    # Supply Chain Risk Section
    if "risk" in by_category or "vulnerability" in by_category or "resilience" in by_category:
        risk_cards = [build_flow_card(f) for f in by_category.get("risk", [])]
        vuln_cards = [build_flow_card(f) for f in by_category.get("vulnerability", [])]
        resilience_cards = [build_flow_card(f) for f in by_category.get("resilience", [])]
        cards = risk_cards + vuln_cards + resilience_cards
        sections.append(html.Div([
            html.Div("Supply Chain", className="trade-section-title", style={
                "fontSize": "0.9rem", "fontWeight": "600", "marginBottom": "12px"
            }),
            html.Div(cards, className="trade-grid", style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fill, minmax(140px, 1fr))",
                "gap": "12px"
            })
        ]))

    last_updated = trade_data.get("last_updated", "")

    return html.Div([
        html.Div([
            html.H4("Trade Flows & Supply Chain", className="section-title",
                   style={"fontSize": "1rem", "marginBottom": "0", "borderBottom": "none"}),
            html.Span(f"Updated: {last_updated}" if last_updated else "",
                     style={"fontSize": "0.7rem", "color": COLORS["text_muted"]})
        ], style={
            "display": "flex", "alignItems": "center",
            "justifyContent": "space-between", "marginBottom": "14px"
        }),
        html.Div(sections, style={"display": "flex", "flexDirection": "column", "gap": "16px"})
    ], className="trade-panel")
