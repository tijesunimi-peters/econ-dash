import plotly.graph_objects as go

COLORS = {
    "positive": "#2ecc71",
    "negative": "#e74c3c",
    "neutral": "#95a5a6",
    "primary": "#4a90d9",
    "dark": "#1a1a2e",
    "muted": "#666666",
}

CHART_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        template="plotly_white",
        font=dict(family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif"),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="white", font_size=13),
        margin=dict(l=50, r=20, t=50, b=40),
    )
)

RECESSIONS = [
    {"start": "2020-02-01", "end": "2020-04-30", "label": "COVID-19"},
]


def trend_color(value):
    if value > 0:
        return COLORS["positive"]
    elif value < 0:
        return COLORS["negative"]
    return COLORS["neutral"]


def trend_arrow(value):
    if value > 0:
        return "\u25b2"
    elif value < 0:
        return "\u25bc"
    return "\u25ac"
