import plotly.graph_objects as go

# Dark slate palette — designed for economic data dashboards
COLORS = {
    # Backgrounds
    "bg": "#0f1117",
    "surface": "#1a1d29",
    "surface_hover": "#222636",
    "border": "#2a2d3a",

    # Text
    "text": "#e8eaed",
    "text_secondary": "#8b8fa3",
    "text_muted": "#5a5e72",

    # Accent
    "primary": "#6c8cff",
    "primary_hover": "#8da6ff",

    # Semantic
    "positive": "#00c896",
    "negative": "#ff5757",
    "neutral": "#8b8fa3",
    "warning": "#ffb347",

    # Chart
    "chart_line": "#6c8cff",
    "chart_area": "rgba(108, 140, 255, 0.1)",
    "chart_grid": "#1e2130",
    "recession": "rgba(255, 255, 255, 0.04)",
}

CHART_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        font=dict(
            family="Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif",
            color=COLORS["text_secondary"],
            size=12,
        ),
        paper_bgcolor=COLORS["surface"],
        plot_bgcolor=COLORS["surface"],
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor=COLORS["bg"],
            font_size=13,
            font_color=COLORS["text"],
            bordercolor=COLORS["border"],
        ),
        margin=dict(l=50, r=20, t=50, b=40),
        xaxis=dict(
            gridcolor=COLORS["chart_grid"],
            zerolinecolor=COLORS["chart_grid"],
            showgrid=True,
            gridwidth=1,
        ),
        yaxis=dict(
            gridcolor=COLORS["chart_grid"],
            zerolinecolor=COLORS["chart_grid"],
            showgrid=True,
            gridwidth=1,
        ),
        title=dict(
            font=dict(color=COLORS["text"], size=14),
            x=0,
            xanchor="left",
        ),
    )
)

RECESSIONS = [
    {"start": "2020-02-01", "end": "2020-04-30", "label": "COVID-19"},
]


def trend_color(value):
    """Return high-contrast color for trend values."""
    if value > 0:
        # Brighter green for better contrast
        return "#00ff88"
    elif value < 0:
        # Brighter red for better contrast
        return "#ff6868"
    # Neutral light gray
    return "#c0c6d9"


def trend_arrow(value):
    if value > 0:
        return "\u25b2"
    elif value < 0:
        return "\u25bc"
    return "\u25ac"
