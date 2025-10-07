import requests, json
from datetime import datetime

def write_json(data: json, path: str) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def write_txt_list(data: list, path: str) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(f"{item}\n")

def call_api(url: str, params: dict) -> json:
    try:
        return requests.get(url, params=params).json()
    except requests.exceptions.RequestException as e:
        print(f"Connetion error: {e}")

def get_countries(data: list) -> list:
    return [d['name'] for d in data if d.get('region').get('value') != 'Aggregates']

def subset_raw_data(data: list) -> list:
    return [
        (d['country']['value'], d['date'], d['value'])
        for d in data
        if filters[config["type"]](d)
        and d['country']['value'] in countries
        and d['value'] is not None
    ]

config = {
    "indicator_id": "NY.GDP.MKTP.CD",
    "type": "date", # 'country' o 'date'
    "option": "2000", # country or year
    "urls": {
        "countries": "https://api.worldbank.org/v2/country",
        "indicator": "https://api.worldbank.org/v2/country/all/indicator/{indicator_id}"
    },
    "params": {
        "countries": {"format": "json", "per_page": 500},
        "indicator": {
            "format": "json",
            "date": f"1960:{datetime.now().year}",
            "per_page": 20000
        }
    }
}
filters = {
    "country": lambda d: d["country"]["value"] == config["option"],
    "date":    lambda d: d["date"] == config["option"]
}

url_indicator = config["urls"]["indicator"].format(indicator_id=config["indicator_id"])

raw_countries = call_api(config["urls"]["countries"], config["params"]["countries"])[1]
countries = get_countries(raw_countries)
raw_data = call_api(url_indicator, config["params"]["indicator"])[1]
requested_data = subset_raw_data(raw_data)
print(requested_data)

#%% pipeline

