import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import api_client

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Economic Dashboard — US & Canada"

# ---------- Layout ----------

app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Economic Health Dashboard"),
        html.P("US & Canada — Sector Trends and Drill-Down"),
    ], className="header"),

    # Country selector
    html.Div([
        html.Label("Country"),
        dcc.Dropdown(id="country-dropdown", placeholder="Select a country"),
    ], className="controls"),

    # Sector heatmap
    html.Div(id="sector-heatmap-container"),

    # Drill-down: sub-industries
    html.Div(id="sub-industry-container", style={"display": "none"}, children=[
        html.H2(id="sector-title"),
        html.P(id="sector-description"),
        html.Div(id="sub-industry-cards"),
    ]),

    # Drill-down: indicators & time series
    html.Div(id="indicator-container", style={"display": "none"}, children=[
        html.H2(id="sub-industry-title"),
        html.Div([
            html.Label("Date Range"),
            dcc.DatePickerRange(id="date-range", start_date="2020-01-01"),
        ], className="controls"),
        html.Div(id="indicator-charts"),
    ]),

    # Navigation breadcrumb
    dcc.Store(id="nav-state", data={"level": "sectors", "country_id": None, "sector_id": None, "sub_industry_id": None}),
], className="app-container")


# ---------- Callbacks ----------

@callback(
    Output("country-dropdown", "options"),
    Input("country-dropdown", "id"),  # fires on load
)
def load_countries(_):
    countries = api_client.get_countries()
    return [{"label": c["name"], "value": c["id"]} for c in countries]


@callback(
    Output("sector-heatmap-container", "children"),
    Output("sub-industry-container", "style"),
    Output("indicator-container", "style"),
    Input("country-dropdown", "value"),
)
def show_sectors(country_id):
    if not country_id:
        return html.P("Select a country to view sectors."), {"display": "none"}, {"display": "none"}

    country = api_client.get_country(country_id)
    sectors = country.get("sectors", [])

    if not sectors:
        return html.P("No sectors found."), {"display": "none"}, {"display": "none"}

    # Build sector cards as clickable buttons
    cards = []
    for sector in sectors:
        card = html.Div([
            html.H3(sector["name"]),
            html.P(sector.get("description", "")),
        ], className="sector-card", id={"type": "sector-card", "index": sector["id"]},
           n_clicks=0)
        cards.append(card)

    return html.Div(cards, className="sector-grid"), {"display": "none"}, {"display": "none"}


@callback(
    Output("sector-title", "children"),
    Output("sector-description", "children"),
    Output("sub-industry-cards", "children"),
    Output("sub-industry-container", "style", allow_duplicate=True),
    Output("indicator-container", "style", allow_duplicate=True),
    Output("sector-heatmap-container", "style"),
    Input({"type": "sector-card", "index": dash.ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def drill_into_sector(n_clicks):
    ctx = dash.callback_context
    if not ctx.triggered or all(n == 0 for n in n_clicks):
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    triggered_id = ctx.triggered_id
    sector_id = triggered_id["index"]

    sector = api_client.get_sector(sector_id)
    sub_industries = sector.get("sub_industries", [])

    cards = []
    for si in sub_industries:
        card = html.Div([
            html.H4(si["name"]),
            html.P(si.get("description", "")),
        ], className="sub-industry-card", id={"type": "si-card", "index": si["id"]},
           n_clicks=0)
        cards.append(card)

    return (
        sector["name"],
        sector.get("description", ""),
        html.Div(cards, className="sector-grid"),
        {"display": "block"},
        {"display": "none"},
        {"display": "none"},
    )


@callback(
    Output("sub-industry-title", "children"),
    Output("indicator-charts", "children"),
    Output("indicator-container", "style", allow_duplicate=True),
    Output("sub-industry-container", "style", allow_duplicate=True),
    Input({"type": "si-card", "index": dash.ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def drill_into_sub_industry(n_clicks):
    ctx = dash.callback_context
    if not ctx.triggered or all(n == 0 for n in n_clicks):
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    triggered_id = ctx.triggered_id
    si_id = triggered_id["index"]

    si = api_client.get_sub_industry(si_id)
    indicators = si.get("indicators", [])

    charts = []
    for ind in indicators:
        series_data = api_client.get_indicator_series(ind["id"])
        data = series_data.get("data", [])

        if data:
            df = pd.DataFrame(data)
            df["date"] = pd.to_datetime(df["date"])
            df["value"] = pd.to_numeric(df["value"])

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df["date"], y=df["value"],
                mode="lines",
                name=ind["name"],
                line=dict(width=2),
            ))
            fig.update_layout(
                title=f"{ind['name']} ({ind.get('unit', '')})",
                xaxis_title="Date",
                yaxis_title=ind.get("unit", ""),
                template="plotly_white",
                height=350,
                margin=dict(l=50, r=20, t=50, b=40),
            )
            charts.append(dcc.Graph(figure=fig))
        else:
            charts.append(html.P(f"No data available for {ind['name']}"))

    return (
        si["name"],
        html.Div(charts),
        {"display": "block"},
        {"display": "none"},
    )


# ---------- CSS ----------

app.index_string = '''
<!DOCTYPE html>
<html>
<head>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 0; background: #f5f7fa; }
        .app-container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { margin-bottom: 20px; }
        .header h1 { margin: 0; color: #1a1a2e; }
        .header p { color: #666; margin: 5px 0 0; }
        .controls { margin-bottom: 20px; max-width: 300px; }
        .sector-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; margin-top: 16px; }
        .sector-card, .sub-industry-card {
            background: white; border-radius: 8px; padding: 20px; cursor: pointer;
            border: 1px solid #e0e0e0; transition: box-shadow 0.2s, border-color 0.2s;
        }
        .sector-card:hover, .sub-industry-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-color: #4a90d9; }
        .sector-card h3, .sub-industry-card h4 { margin: 0 0 8px; color: #1a1a2e; }
        .sector-card p, .sub-industry-card p { margin: 0; color: #666; font-size: 14px; }
    </style>
</head>
<body>
    {%app_entry%}
    <footer>{%config%}{%scripts%}{%renderer%}</footer>
</body>
</html>
'''

if __name__ == "__main__":
    from config import DASH_HOST, DASH_PORT, DASH_DEBUG
    app.run(debug=DASH_DEBUG, host=DASH_HOST, port=DASH_PORT)
