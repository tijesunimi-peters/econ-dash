import requests
from config import RAILS_API_URL

TIMEOUT = 15


def _get(path, params=None):
    try:
        resp = requests.get(f"{RAILS_API_URL}{path}", params=params, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        return {"error": str(e)}


def get_countries():
    return _get("/countries")


def get_country(country_id):
    return _get(f"/countries/{country_id}")


def get_country_summary(country_id):
    return _get(f"/countries/{country_id}/summary")


def get_sector(sector_id):
    return _get(f"/sectors/{sector_id}")


def get_sector_summary(sector_id):
    return _get(f"/sectors/{sector_id}/summary")


def get_sub_industry(sub_industry_id):
    return _get(f"/sub_industries/{sub_industry_id}")


def get_indicator_series(indicator_id, start_date=None, end_date=None):
    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    return _get(f"/indicators/{indicator_id}/series", params=params)


def get_indicator_acceleration(indicator_id):
    return _get(f"/indicators/{indicator_id}/acceleration")


def get_country_percentiles(country_id):
    return _get(f"/countries/{country_id}/percentiles")


def get_country_anomalies(country_id):
    return _get(f"/countries/{country_id}/anomalies")


def get_country_momentum(country_id):
    return _get(f"/countries/{country_id}/momentum")


def get_country_business_cycle(country_id):
    return _get(f"/countries/{country_id}/business_cycle")


def get_country_executive_summary(country_id):
    return _get(f"/countries/{country_id}/executive_summary")


def get_country_correlations(country_id):
    return _get(f"/countries/{country_id}/correlations")


def get_country_compare(country_id, other_id):
    return _get(f"/countries/{country_id}/compare/{other_id}")


def get_country_causal_factors(country_id):
    return _get(f"/countries/{country_id}/causal_factors")


def get_country_policies(country_id):
    """Fetch policy timeline for a country."""
    return _get(f"/countries/{country_id}/policy_timeline")


def get_country_market_sentiment(country_id):
    """Fetch market sentiment indicators for a country."""
    return _get(f"/countries/{country_id}/market_sentiment")


def get_country_structural_trends(country_id):
    """Fetch structural metrics (demographics, productivity) for a country."""
    return _get(f"/countries/{country_id}/structural_trends")


def get_country_debt_trends(country_id):
    """Fetch debt metrics (government, corporate, household) for a country."""
    return _get(f"/countries/{country_id}/debt_trends")


def get_country_structural_forecast(country_id, periods=2, method="linear"):
    """Fetch forecast projections for structural metrics."""
    return _get(f"/countries/{country_id}/structural_forecast",
                params={"periods": periods, "method": method})


def get_country_trade_flows(country_id):
    """Fetch trade flow metrics (exports, imports, FDI, supply chain) for a country."""
    return _get(f"/countries/{country_id}/trade_flows")
