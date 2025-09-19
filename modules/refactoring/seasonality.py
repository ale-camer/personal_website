from utils import read_excel, clean_excel_input
import validations as val

from collections import defaultdict

import numpy as np

def data_to_numeric(data):
    return [float(d) for d in data]

def get_first_sheet_name(data):
    return list(data.keys())[0]

def get_sheet_values(data, sheet_name):
    return data[sheet_name][0]

def get_mean(data: list) -> float:
    return sum(data) / len(data)

def groupby_lists(list1: list, list2: list) -> dict:
    grouped = defaultdict(list)
    for k, v in [(str(l1), l2) for l1, l2 in zip(list1, list2)]:
        grouped[k].append(v)
    return {k: get_mean(v) for k, v in grouped.items()}

def divide_lists(list1: list, list2: list) -> list:
    return [a / b for a, b in zip(list1, list2)]

def rolling_mean(serie, window):
    n, results = len(serie), []
    for i in range(n - window + 1):
        mean = sum(serie[i:i+window]) / window
        results.append(mean)
    return results

def forecast_time_serie(serie, periodicity: int) -> list:

    # indices
    periods, half_p = len(serie) // periodicity, periodicity // 2
    next_periods = np.arange(len(serie)+1, len(serie)+1+periodicity)
    subperiods = np.tile(np.arange(1, periodicity+1), periods)[half_p : -half_p]

    # decomposition
    moving_avgs = rolling_mean(rolling_mean(serie, periodicity), 2)
    irregulars = divide_lists(serie[half_p : -half_p], moving_avgs)
    avg_irrs = list(groupby_lists(subperiods, irregulars).values())
    seasonal_indices = [g / get_mean(avg_irrs) for g in avg_irrs] * periods
    unseasonal_serie = divide_lists(serie, seasonal_indices)

    # forecast
    X = np.vstack([np.ones(len(serie)), np.arange(1, len(serie)+1)]).T
    b = np.linalg.inv(X.T @ X) @ X.T @ unseasonal_serie
    forecast = b[0] + b[1] * next_periods * seasonal_indices[:periodicity]
    return [round(float(v), 2) for v in forecast]

data = read_excel("seasonality_example.xlsx")

try:
    val.validate_number_of_sheets(data)
except val.TooManySheetsError as e:
    print("Caught error:", e)

cleaned_data = clean_excel_input(data)

try:
    val.validate_number_of_columns(cleaned_data)
except val.TooManyColumnsError as e:
    print("Caught error:", e)

sheet_name = get_first_sheet_name(cleaned_data)
serie = get_sheet_values(cleaned_data, sheet_name)

try:
    val.validate_data_type(serie)
except val.NonNumericValueError as e:
    print("Caught error:", e)

serie = data_to_numeric(serie)
periodicity = 4
forecast = forecast_time_serie(serie, periodicity)
print(f"Forecast: {forecast}")
