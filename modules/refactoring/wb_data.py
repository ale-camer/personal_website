import requests, json, subprocess
from datetime import datetime

def read_csv(filename, encoding: str = "utf-8"):
    with open(filename, encoding=encoding) as f:
        return f.readlines()

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

def main(config: dict):

    url_indicator = config["urls"]["indicator"].format(indicator_id=config["indicator_id"])

    raw_countries = call_api(config["urls"]["countries"], config["params"]["countries"])[1]
    countries = get_countries(raw_countries)
    raw_data = call_api(url_indicator, config["params"]["indicator"])[1]

    write_json(raw_data, config["paths"]["input_json"])
    write_txt_list(countries, config["paths"]["country_list"])

    command = [
        'java', '-jar', config["paths"]["scala_jar"],
        config["paths"]["input_json"],
        config["paths"]["country_list"],
        config["paths"]["output_csv"],
        config["type"],
        config["option"]
    ]

    subprocess.run(command, check=True, capture_output=True, text=True)
    data_requested = read_csv(config["paths"]["output_csv"])
    return [d.split(",") for d in data_requested]

CONFIG = {
    "indicator_id": "NY.GDP.MKTP.CD",
    "type": "date", # 'country' o 'date'
    "option": "2021", # country or year
    "paths": {
        "input_json": "temp_data_for_scala.json",
        "country_list": "temp_country_list.txt",
        "output_csv": "wb_results.csv",
        "scala_jar": "DataProcessor.jar"
    },
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

if __name__ == "__main__":
    df = main(CONFIG)
    # print(df)

#%% otros

# def get_countries_data(data: dict, included_items) -> list:
#     return [d for d in data if d.get('value') is not None and d.get('country', {}).get('value') in included_items]

# def get_output_data(data) -> df:

#     filters = {
#         "country": lambda d: d["country"]["value"] == OPTION,
#         "date":    lambda d: d["date"] == OPTION
#     }
#     data_requested = [
#         (d['country']['value'], d['date'], d['value'])
#         for d in data if filters[TYPE](d)
#     ]
#     return (
#         df(data_requested, columns=['COUNTRY', 'YEAR', 'VALUE'])
#         .sort_values(by=['COUNTRY', 'YEAR'], ascending=[True, False])
#         .drop_duplicates()
#         .dropna()
#     )

# write_json(raw_data, "raw_data.json")
# data_countries = get_countries_data(raw_data, countries) # pasar a spark
# data_requested = get_output_data(data_countries)
# print(data_requested)