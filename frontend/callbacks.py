import dash
from dash import html, dcc, callback, Input, Output, State, ALL
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date, timedelta
import api_client
from components import (
    build_sector_treemap,
    build_breadcrumb,
    build_sparkline_table,
    build_indicator_chart,
)


def register_callbacks(app):

    @app.callback(
        Output("country-dropdown", "options"),
        Input("country-dropdown", "id"),
    )
    def load_countries(_):
        data = api_client.get_countries()
        if isinstance(data, dict) and "error" in data:
            return []
        return [{"label": c["name"], "value": c["id"]} for c in data]

    # Country selection -> update nav state
    @app.callback(
        Output("nav-state", "data", allow_duplicate=True),
        Input("country-dropdown", "value"),
        State("nav-state", "data"),
        prevent_initial_call=True,
    )
    def on_country_select(country_id, nav):
        if not country_id:
            return dash.no_update
        country = api_client.get_country(country_id)
        if isinstance(country, dict) and "error" in country:
            return dash.no_update
        return {
            "level": "sectors",
            "country_id": country_id,
            "country_name": country.get("name", ""),
            "sector_id": None,
            "sector_name": None,
            "sub_industry_id": None,
            "sub_industry_name": None,
        }

    # Treemap click -> drill into sector
    @app.callback(
        Output("nav-state", "data", allow_duplicate=True),
        Input("treemap", "clickData"),
        State("nav-state", "data"),
        prevent_initial_call=True,
    )
    def on_treemap_click(click_data, nav):
        if not click_data:
            return dash.no_update
        point = click_data["points"][0]
        sector_id = point.get("customdata")
        if not sector_id:
            return dash.no_update
        label = point.get("label", "")
        nav = {**nav, "level": "sub_industries", "sector_id": sector_id, "sector_name": label,
               "sub_industry_id": None, "sub_industry_name": None}
        return nav

    # Sub-industry row click -> drill into indicators
    @app.callback(
        Output("nav-state", "data", allow_duplicate=True),
        Input({"type": "si-row", "index": ALL}, "n_clicks"),
        State("nav-state", "data"),
        prevent_initial_call=True,
    )
    def on_sub_industry_click(n_clicks, nav):
        ctx = dash.callback_context
        if not ctx.triggered or all(n == 0 for n in n_clicks):
            return dash.no_update
        triggered_id = ctx.triggered_id
        si_id = triggered_id["index"]

        # Get sub-industry name from sector summary
        summary = api_client.get_sector_summary(nav["sector_id"])
        si_name = ""
        if not isinstance(summary, dict) or "error" not in summary:
            for si in summary.get("sub_industries", []):
                if si["id"] == si_id:
                    si_name = si["name"]
                    break

        return {**nav, "level": "indicators", "sub_industry_id": si_id, "sub_industry_name": si_name}

    # Breadcrumb click -> navigate back
    @app.callback(
        Output("nav-state", "data", allow_duplicate=True),
        Input("bc-home", "n_clicks"),
        Input("bc-country", "n_clicks"),
        Input("bc-sector", "n_clicks"),
        State("nav-state", "data"),
        prevent_initial_call=True,
    )
    def on_breadcrumb_click(home_clicks, country_clicks, sector_clicks, nav):
        ctx = dash.callback_context
        if not ctx.triggered:
            return dash.no_update
        trigger = ctx.triggered_id

        if trigger == "bc-home":
            return {**nav, "level": "overview", "country_id": None, "country_name": None,
                    "sector_id": None, "sector_name": None,
                    "sub_industry_id": None, "sub_industry_name": None}
        elif trigger == "bc-country":
            return {**nav, "level": "sectors", "sector_id": None, "sector_name": None,
                    "sub_industry_id": None, "sub_industry_name": None}
        elif trigger == "bc-sector":
            return {**nav, "level": "sub_industries",
                    "sub_industry_id": None, "sub_industry_name": None}
        return dash.no_update

    # Date preset buttons
    @app.callback(
        Output("date-range-store", "data"),
        Output("date-ytd", "active"),
        Output("date-1y", "active"),
        Output("date-2y", "active"),
        Output("date-5y", "active"),
        Input("date-ytd", "n_clicks"),
        Input("date-1y", "n_clicks"),
        Input("date-2y", "n_clicks"),
        Input("date-5y", "n_clicks"),
        prevent_initial_call=True,
    )
    def on_date_preset(ytd, y1, y2, y5):
        ctx = dash.callback_context
        if not ctx.triggered:
            return dash.no_update, False, False, False, True
        trigger = ctx.triggered_id

        presets = {"date-ytd": "YTD", "date-1y": "1Y", "date-2y": "2Y", "date-5y": "5Y"}
        preset = presets.get(trigger, "5Y")
        active = [trigger == f"date-{p.lower()}" for p in ["ytd", "1y", "2y", "5y"]]
        return {"preset": preset}, *active

    # Treemap update callback (separate from main content)
    @app.callback(
        Output("treemap", "figure"),
        Output("treemap-container", "style"),
        Input("nav-state", "data"),
    )
    def update_treemap(nav):
        level = nav.get("level", "overview")
        if level == "sectors" and nav.get("country_id"):
            summary = api_client.get_country_summary(nav["country_id"])
            if isinstance(summary, dict) and "error" not in summary:
                sectors = summary.get("sectors", [])
                fig = build_sector_treemap(sectors, nav.get("country_name", ""))
                return fig, {"display": "block"}
        return {}, {"display": "none"}

    # Master render callback
    @app.callback(
        Output("main-content", "children"),
        Output("breadcrumb-container", "children"),
        Input("nav-state", "data"),
        Input("date-range-store", "data"),
        Input("yoy-toggle", "value"),
    )
    def render_page(nav, date_store, yoy_enabled):
        level = nav.get("level", "overview")

        # Build breadcrumb
        breadcrumb = build_breadcrumb(
            country_name=nav.get("country_name"),
            sector_name=nav.get("sector_name"),
            sub_industry_name=nav.get("sub_industry_name"),
        )

        if level == "overview" or not nav.get("country_id"):
            return html.Div([
                html.P("Select a country to view sector health.", className="text-muted mt-4"),
            ]), breadcrumb

        elif level == "sectors":
            # Treemap handled by update_treemap callback
            return html.Div(), breadcrumb

        elif level == "sub_industries":
            summary = api_client.get_sector_summary(nav["sector_id"])
            if isinstance(summary, dict) and "error" in summary:
                return dbc.Alert(f"Failed to load data: {summary['error']}", color="danger"), breadcrumb

            sub_industries = summary.get("sub_industries", [])
            table = build_sparkline_table(sub_industries)
            return html.Div([
                html.H3(nav.get("sector_name", ""), className="mb-3"),
                table,
            ]), breadcrumb

        elif level == "indicators":
            si = api_client.get_sub_industry(nav["sub_industry_id"])
            if isinstance(si, dict) and "error" in si:
                return dbc.Alert(f"Failed to load data: {si['error']}", color="danger"), breadcrumb

            indicators = si.get("indicators", [])
            start_date = _compute_start_date(date_store.get("preset", "5Y"))

            charts = []
            for ind in indicators:
                series_data = api_client.get_indicator_series(ind["id"], start_date=start_date)
                if isinstance(series_data, dict) and "error" in series_data:
                    charts.append(dbc.Alert(f"Error loading {ind['name']}", color="warning"))
                    continue

                data = series_data.get("data", [])
                if data:
                    df = pd.DataFrame(data)
                    df["date"] = pd.to_datetime(df["date"])
                    df["value"] = pd.to_numeric(df["value"])

                    unit = ind.get("unit", "")
                    chart_name = ind["name"]
                    values = df["value"]

                    if yoy_enabled and len(df) > 12:
                        freq = ind.get("frequency", "monthly")
                        periods = {"weekly": 52, "daily": 252, "quarterly": 4}.get(freq, 12)
                        values = df["value"].pct_change(periods=periods) * 100
                        values = values.dropna()
                        df = df.iloc[-len(values):]
                        unit = "YoY % Change"
                        chart_name = f"{ind['name']} (YoY)"

                    fig = build_indicator_chart(chart_name, unit, df["date"], values)
                    charts.append(dcc.Graph(figure=fig))
                else:
                    charts.append(html.P(f"No data available for {ind['name']}", className="text-muted"))

            return html.Div([
                html.H3(nav.get("sub_industry_name", ""), className="mb-3"),
                html.Div(charts),
            ]), breadcrumb

        return html.P("Unknown view."), breadcrumb


def _compute_start_date(preset):
    today = date.today()
    if preset == "YTD":
        return date(today.year, 1, 1).isoformat()
    elif preset == "1Y":
        return (today - timedelta(days=365)).isoformat()
    elif preset == "2Y":
        return (today - timedelta(days=730)).isoformat()
    elif preset == "5Y":
        return (today - timedelta(days=1825)).isoformat()
    return (today - timedelta(days=1825)).isoformat()
