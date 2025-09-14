import requests, json
from datetime import datetime
from pandas import DataFrame as df

def write_json(data: df, path: str) -> None:
    # os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        # print(f"{path} printed successfully")

def call_api(url: str, params: dict) -> json:
    try:
        return requests.get(url, params=params).json()
    except requests.exceptions.RequestException as e:
        print(f"Connetion error: {e}")

def get_countries(data: list) -> list:
    return [d['name'] for d in data if d.get('region').get('value') != 'Aggregates']

def get_countries_data(data: dict, included_items) -> list:
    return [d for d in data if d.get('value') is not None and d.get('country', {}).get('value') in included_items]

def get_output_data(data) -> df:

    filters = {
        "country": lambda d: d["country"]["value"] == OPTION,
        "date":    lambda d: d["date"] == OPTION
    }
    data_requested = [
        (d['country']['value'], d['date'], d['value'])
        for d in data if filters[TYPE](d)
    ]
    return (
        df(data_requested, columns=['COUNTRY', 'YEAR', 'VALUE'])
        .sort_values(by=['COUNTRY', 'YEAR'], ascending=[True, False])
        .drop_duplicates()
        .dropna()
    )

# inputs
indicator_id = "NY.GDP.MKTP.CD"
url_countries = 'https://api.worldbank.org/v2/country'
params_countries = {'format': 'json', 'per_page': 500}
url_indicator = f'https://api.worldbank.org/v2/country/all/indicator/{indicator_id}'
params_indicator = {'format': 'json', 'date': f'1960:{datetime.now().year}', 'per_page': 20000}
TYPE, OPTION = 'country', 'Argentina' # 'date', '2021'

# orquestation
raw_countries = call_api(url_countries, params_countries)[1]
countries = get_countries(raw_countries)
raw_data = call_api(url_indicator, params_indicator)[1]
write_json(raw_data, "raw_data.json")

data_countries = get_countries_data(raw_data, countries) # pasar a spark
data_requested = get_output_data(data_countries)
print(data_requested)
