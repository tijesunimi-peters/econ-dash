import dash
from dash import html, dcc, callback, Input, Output, State, ALL
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date, timedelta
import api_client
from styles import COLORS
from components import (
    build_sector_treemap,
    build_breadcrumb,
    build_sparkline_table,
    build_indicator_chart,
    build_percentile_gauge,
    build_anomaly_panel,
    build_intelligence_panel,
    build_momentum_scoreboard,
    build_cross_country_comparison,
    build_correlation_heatmap,
    build_policy_timeline,
    build_market_sentiment,
    _build_factors_compact,
)


def _create_popover_callback(app, trigger_id):
    """Factory function to create popover toggle callback with correct closure.

    Opens popover on trigger click, closes on outside click via autohide=True.
    """
    @app.callback(
        Output(f"{trigger_id}-popover", "is_open"),
        Input(trigger_id, "n_clicks"),
        State(f"{trigger_id}-popover", "is_open"),
        prevent_initial_call=True,
    )
    def toggle_popover(n_clicks, is_open):
        if n_clicks:
            return not is_open
        return is_open


def register_callbacks(app):

    # ── Popover Toggle Callbacks ──
    # Create callbacks for all popover triggers
    POPOVER_TRIGGERS = [
        # Metrics popovers
        "pop-latest-header", "pop-yoy-header", "pop-trend-header",
        "pop-percentile-gauge",
        # Anomaly popovers
        "pop-anomaly-zscore",
        # Cycle popovers
        "pop-cycle-phase", "pop-cycle-x", "pop-cycle-y",
        # Sector recommendations
        "pop-sector-recs",
        # Momentum popovers
        "pop-momentum-scale", "pop-momentum-roc",
        # Factor popovers
        "pop-factor-correlation", "pop-factor-status", "pop-factor-confidence",
    ]

    for trigger_id in POPOVER_TRIGGERS:
        _create_popover_callback(app, trigger_id)

    # ── Load country dropdown options ──
    @app.callback(
        Output("country-dropdown", "options"),
        Input("country-dropdown", "id"),
    )
    def load_countries(_):
        data = api_client.get_countries()
        if isinstance(data, dict) and "error" in data:
            return []
        return [{"label": c["name"], "value": c["id"]} for c in data]

    # ── Country selection -> update nav state ──
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

    # ── Treemap click -> drill into sector ──
    @app.callback(
        Output("nav-state", "data", allow_duplicate=True),
        Input("treemap", "clickData"),
        State("nav-state", "data"),
        prevent_initial_call=True,
    )
    def on_treemap_click(click_data, nav):
        if not click_data or not click_data.get("points"):
            return dash.no_update
        point = click_data["points"][0]
        sector_id = point.get("customdata")
        if not sector_id:
            return dash.no_update
        label = point.get("label", "")
        return {**nav, "level": "sub_industries", "sector_id": sector_id,
                "sector_name": label, "sub_industry_id": None, "sub_industry_name": None}

    # ── Sub-industry row click -> drill into indicators ──
    @app.callback(
        Output("nav-state", "data", allow_duplicate=True),
        Input({"type": "si-row", "index": ALL}, "n_clicks"),
        State("nav-state", "data"),
        prevent_initial_call=True,
    )
    def on_sub_industry_click(n_clicks, nav):
        ctx = dash.callback_context
        if not ctx.triggered or not n_clicks or all(n is None or n == 0 for n in n_clicks):
            return dash.no_update
        si_id = ctx.triggered_id["index"]

        summary = api_client.get_sector_summary(nav["sector_id"])
        si_name = ""
        if not isinstance(summary, dict) or "error" not in summary:
            for si in summary.get("sub_industries", []):
                if si["id"] == si_id:
                    si_name = si["name"]
                    break

        return {**nav, "level": "indicators", "sub_industry_id": si_id,
                "sub_industry_name": si_name}

    # ── Breadcrumb click -> navigate back ──
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
        triggered_value = ctx.triggered[0].get("value")
        if not triggered_value:
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

    # ── Date preset buttons ──
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

    # ── Intelligence Panel (cycle + executive summary + causal factors) ──
    # Visible at sectors and sub_industries levels; hidden at indicator level
    @app.callback(
        Output("intelligence-panel-container", "children"),
        Input("nav-state", "data"),
    )
    def update_intelligence_panel(nav):
        country_id = nav.get("country_id")
        level = nav.get("level", "overview")
        if not country_id or level == "indicators":
            return html.Div()

        cycle_data = api_client.get_country_business_cycle(country_id)
        if isinstance(cycle_data, dict) and "error" in cycle_data:
            cycle_data = None

        summary_data = api_client.get_country_executive_summary(country_id)
        if isinstance(summary_data, dict) and "error" in summary_data:
            summary_data = None

        factors_data = api_client.get_country_causal_factors(country_id)
        factors_list = None
        if not isinstance(factors_data, dict) or "error" not in factors_data:
            factors_list = factors_data.get("factors") if isinstance(factors_data, dict) else None

        return build_intelligence_panel(cycle_data, summary_data, factors_list)

    # ── Policy Timeline Panel ──
    # Visible at sectors and sub_industries levels; hidden at indicator level
    @app.callback(
        Output("policy-panel-container", "children"),
        Input("nav-state", "data"),
    )
    def update_policy_panel(nav):
        country_id = nav.get("country_id")
        level = nav.get("level", "overview")
        if not country_id or level == "indicators":
            return html.Div()

        policies_data = api_client.get_country_policies(country_id)
        if isinstance(policies_data, dict) and "error" in policies_data:
            return html.Div()
        if not isinstance(policies_data, dict):
            return html.Div()

        policies = policies_data.get("policies", [])
        if not policies:
            return html.Div()

        return build_policy_timeline(policies)

    # ── Market Sentiment Panel ──
    @app.callback(
        Output("sentiment-panel-container", "children"),
        Input("nav-state", "data"),
    )
    def update_sentiment_panel(nav):
        country_id = nav.get("country_id")
        level = nav.get("level", "overview")
        if not country_id or level == "indicators":
            return html.Div()

        sentiment_data = api_client.get_country_market_sentiment(country_id)
        if isinstance(sentiment_data, dict) and "error" in sentiment_data:
            return html.Div()
        if not isinstance(sentiment_data, dict):
            return html.Div()

        return build_market_sentiment(sentiment_data)

    # ── Structural Health Panel ──
    @app.callback(
        Output("structural-panel-container", "children"),
        Input("nav-state", "data"),
    )
    def update_structural_panel(nav):
        country_id = nav.get("country_id")
        level = nav.get("level", "overview")
        if not country_id or level == "indicators":
            return html.Div()

        structural_data = api_client.get_country_structural_trends(country_id)
        debt_data = api_client.get_country_debt_trends(country_id)

        if isinstance(structural_data, dict) and "error" in structural_data:
            return html.Div()
        if isinstance(debt_data, dict) and "error" in debt_data:
            return html.Div()
        if not isinstance(structural_data, dict) or not isinstance(debt_data, dict):
            return html.Div()

        from components import build_structural_health
        return build_structural_health(structural_data, debt_data)

    # ── Anomaly Alerts ──
    # Visible at sectors and sub_industries; hidden at indicator drill-down
    @app.callback(
        Output("anomaly-container", "children"),
        Input("nav-state", "data"),
    )
    def update_anomalies(nav):
        country_id = nav.get("country_id")
        level = nav.get("level", "overview")
        if not country_id or level == "indicators":
            return html.Div()

        anomaly_data = api_client.get_country_anomalies(country_id)
        if isinstance(anomaly_data, dict) and "error" in anomaly_data:
            return html.Div()
        if not isinstance(anomaly_data, list) or not anomaly_data:
            return html.Div()

        return build_anomaly_panel(anomaly_data)

    # ── Anomaly collapse toggle ──
    @app.callback(
        Output("anomaly-collapse", "is_open"),
        Input("anomaly-toggle", "n_clicks"),
        State("anomaly-collapse", "is_open"),
        prevent_initial_call=True,
    )
    def toggle_anomaly_panel(n_clicks, is_open):
        if n_clicks:
            return not is_open
        return is_open

    # ── Tabs visibility ──
    # Show at sector level when a country is selected
    @app.callback(
        Output("drill-tabs-container", "style"),
        Input("nav-state", "data"),
    )
    def update_tabs_visibility(nav):
        level = nav.get("level", "overview")
        if level == "sectors" and nav.get("country_id"):
            return {"display": "block", "marginBottom": "0"}
        return {"display": "none"}

    # ── Treemap (coupled with active tab) ──
    @app.callback(
        Output("treemap", "figure"),
        Output("treemap-container", "style"),
        Input("nav-state", "data"),
        Input("drill-tabs", "active_tab"),
    )
    def update_treemap(nav, active_tab):
        level = nav.get("level", "overview")
        if level == "sectors" and nav.get("country_id") and active_tab == "tab-sectors":
            summary = api_client.get_country_summary(nav["country_id"])
            if isinstance(summary, dict) and "error" not in summary:
                sectors = summary.get("sectors", [])
                fig = build_sector_treemap(sectors, nav.get("country_name", ""))
                return fig, {"display": "block"}
        return {}, {"display": "none"}

    # ── Tab content (Momentum / Compare / Correlations) ──
    @app.callback(
        Output("drill-tab-content", "children"),
        Input("drill-tabs", "active_tab"),
        Input("nav-state", "data"),
    )
    def update_tab_content(active_tab, nav):
        country_id = nav.get("country_id")
        level = nav.get("level", "overview")

        if level != "sectors" or not country_id:
            return html.Div()

        if active_tab == "tab-sectors":
            return html.Div()

        elif active_tab == "tab-momentum":
            momentum_data = api_client.get_country_momentum(country_id)
            if isinstance(momentum_data, dict) and "error" in momentum_data:
                return dbc.Alert("Failed to load momentum data", color="warning")
            if not isinstance(momentum_data, list):
                return html.Div()
            return build_momentum_scoreboard(momentum_data)

        elif active_tab == "tab-compare":
            countries = api_client.get_countries()
            if isinstance(countries, dict) and "error" in countries:
                return dbc.Alert("Failed to load countries", color="warning")

            other_options = [
                {"label": c["name"], "value": c["id"]}
                for c in countries if c["id"] != country_id
            ]
            if not other_options:
                return html.P("No other country available for comparison",
                              style={"color": COLORS["text_muted"]})

            default_other = other_options[0]["value"]

            compare_data = api_client.get_country_compare(country_id, default_other)
            initial_content = html.Div()
            if not (isinstance(compare_data, dict) and "error" in compare_data):
                initial_content = build_cross_country_comparison(compare_data)

            return html.Div([
                dbc.Row([
                    dbc.Col([
                        html.Label("Compare with:", className="text-muted me-2"),
                        dcc.Dropdown(
                            id="compare-country-dropdown",
                            options=other_options,
                            value=default_other,
                            clearable=False,
                            className="header-dropdown",
                        ),
                    ], width=4),
                ], className="mb-3"),
                html.Div(id="compare-content", children=initial_content),
            ])

        elif active_tab == "tab-correlations":
            corr_data = api_client.get_country_correlations(country_id)
            if isinstance(corr_data, dict) and "error" in corr_data:
                return dbc.Alert("Failed to load correlation data", color="warning")
            return build_correlation_heatmap(corr_data)

        return html.Div()

    # ── Compare country selection ──
    @app.callback(
        Output("compare-content", "children"),
        Input("compare-country-dropdown", "value"),
        State("nav-state", "data"),
        prevent_initial_call=True,
    )
    def on_compare_country_select(other_id, nav):
        country_id = nav.get("country_id")
        if not country_id or not other_id:
            return html.Div()

        compare_data = api_client.get_country_compare(country_id, other_id)
        if isinstance(compare_data, dict) and "error" in compare_data:
            return dbc.Alert("Failed to load comparison data", color="warning")
        return build_cross_country_comparison(compare_data)

    # ── Master render (main content + breadcrumb) ──
    @app.callback(
        Output("main-content", "children"),
        Output("breadcrumb-container", "children"),
        Input("nav-state", "data"),
        Input("date-range-store", "data"),
        Input("yoy-toggle", "value"),
    )
    def render_page(nav, date_store, yoy_enabled):
        level = nav.get("level", "overview")

        breadcrumb = build_breadcrumb(
            country_name=nav.get("country_name"),
            sector_name=nav.get("sector_name"),
            sub_industry_name=nav.get("sub_industry_name"),
        )

        if level == "overview" or not nav.get("country_id"):
            return html.Div([
                html.P("Select a country to view sector health.",
                       className="text-muted mt-4"),
            ]), breadcrumb

        elif level == "sectors":
            return html.Div(), breadcrumb

        elif level == "sub_industries":
            summary = api_client.get_sector_summary(nav["sector_id"])
            if isinstance(summary, dict) and "error" in summary:
                return dbc.Alert(f"Failed to load data: {summary['error']}",
                                 color="danger"), breadcrumb
            sub_industries = summary.get("sub_industries", [])
            table = build_sparkline_table(sub_industries)
            return html.Div([
                html.H3(nav.get("sector_name", ""), className="section-title"),
                table,
            ]), breadcrumb

        elif level == "indicators":
            si = api_client.get_sub_industry(nav["sub_industry_id"])
            if isinstance(si, dict) and "error" in si:
                return dbc.Alert(f"Failed to load data: {si['error']}",
                                 color="danger"), breadcrumb

            indicators = si.get("indicators", [])
            start_date = _compute_start_date(date_store.get("preset", "5Y"))

            country_id = nav.get("country_id")
            percentiles_data = []
            if country_id:
                pdata = api_client.get_country_percentiles(country_id)
                if isinstance(pdata, list):
                    percentiles_data = pdata

            charts = []
            for ind in indicators:
                series_data = api_client.get_indicator_series(
                    ind["id"], start_date=start_date)
                if isinstance(series_data, dict) and "error" in series_data:
                    charts.append(dbc.Alert(f"Error loading {ind['name']}",
                                            color="warning"))
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
                        periods = {"weekly": 52, "daily": 252,
                                   "quarterly": 4}.get(freq, 12)
                        values = df["value"].pct_change(periods=periods) * 100
                        values = values.dropna()
                        df = df.iloc[-len(values):]
                        unit = "YoY % Change"
                        chart_name = f"{ind['name']} (YoY)"

                    fig = build_indicator_chart(chart_name, unit,
                                                df["date"], values)

                    ind_percentile = next(
                        (p for p in percentiles_data
                         if p.get("indicator_id") == ind["id"]),
                        None,
                    )
                    gauge = (build_percentile_gauge(ind_percentile)
                             if ind_percentile else html.Div())

                    charts.append(html.Div([
                        dbc.Row([
                            dbc.Col(dcc.Graph(figure=fig), width=9),
                            dbc.Col(gauge, width=3,
                                    className="d-flex align-items-center "
                                              "justify-content-center"),
                        ]),
                    ], className="chart-card"))
                else:
                    charts.append(html.P(
                        f"No data available for {ind['name']}",
                        className="text-muted"))

            return html.Div([
                html.H3(nav.get("sub_industry_name", ""), className="section-title"),
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
