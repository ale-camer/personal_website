# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import json
import requests
from datetime import datetime
from functools import reduce

# --- Third-party ---

# --- Project ---
from .visuals import TimeSeriesPlotter, HeatmapPlotter

# =============================================================================
# CONSTANTS
# =============================================================================
url, params = "https://api.worldbank.org/v2/country", {"format": "json", "per_page": 500}

# =============================================================================
# AUXILIARY FUNCTIONS
# =============================================================================
def call_api(url: str, params: dict) -> json:
    try:
        return requests.get(url, params=params).json()
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return None

def get_countries(data: list) -> list:
    return [
        d['name'] for d in data 
        if d.get('region', {}).get('value') != 'Aggregates'
    ]
     
# =============================================================================
# CORE
# =============================================================================
raw_countries = call_api(url, params)[1]
countries = get_countries(raw_countries)

def download_data(indicator_id: str) -> list | None:
    url = f"https://api.worldbank.org/v2/country/all/indicator/{indicator_id}"
    params = {"format": "json", "date": f"1960:{datetime.now().year}", "per_page": 20000}
    raw_data = call_api(url, params)[1]
    print(f"Data for indicator '{indicator_id}' downloaded successfully.")
    return [
        entry for entry in raw_data
        if entry.get("value") is not None
        and entry.get("country", {}).get("value") in countries
    ]

def get_options(data: list, _type: str) -> list[str]:
    key_map = {
        'country': ('country', 'value'),
        'year': ('date',),
        'date': ('date',)
    }
    keys = key_map[_type]        
    options = {
        reduce(lambda v, k: v[k], keys, entry)
        for entry in data
    }
    return sorted(list(options), reverse=(_type == 'year' or _type == 'date'))

def filter_data(data: list, type_selected: str, option_selected: str) -> list:
    filter_funcs = {
        "year": lambda item, opt: item.get("date") == opt,
        "date": lambda item, opt: item.get("date") == opt,
        "country": lambda item, opt: item.get("country").get("value") == opt
    }
    filter_func = filter_funcs.get(type_selected, lambda *_: False)    
    return [
        {
            "COUNTRY": item["country"]["value"],
            "DATE": item["date"],
            "VALUE": item["value"],
            "ISO_CODE": item["countryiso3code"]
        }
        for item in data
        if filter_func(item, option_selected)
        and item.get("value") is not None
        and item.get("countryiso3code")
    ]

def plot(
        data: list, _type: str, geofile: str, title: str, 
        template: str = 'plotly'
    ) -> str:    
    try:
        match _type:
            case 'country':
                return TimeSeriesPlotter().plot(data, title=title, template=template)
            case _:
                return HeatmapPlotter(geofile).plot(data, title=title)
        print("Plot generated successfully.")
    except Exception as e:
        print(f"Error generating plot: {e}")
        return ""