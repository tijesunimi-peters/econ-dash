import requests
from config import RAILS_API_URL


def get_countries():
    resp = requests.get(f"{RAILS_API_URL}/countries")
    resp.raise_for_status()
    return resp.json()


def get_country(country_id):
    resp = requests.get(f"{RAILS_API_URL}/countries/{country_id}")
    resp.raise_for_status()
    return resp.json()


def get_sector(sector_id):
    resp = requests.get(f"{RAILS_API_URL}/sectors/{sector_id}")
    resp.raise_for_status()
    return resp.json()


def get_sub_industry(sub_industry_id):
    resp = requests.get(f"{RAILS_API_URL}/sub_industries/{sub_industry_id}")
    resp.raise_for_status()
    return resp.json()


def get_indicator_series(indicator_id, start_date=None, end_date=None):
    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    resp = requests.get(f"{RAILS_API_URL}/indicators/{indicator_id}/series", params=params)
    resp.raise_for_status()
    return resp.json()
