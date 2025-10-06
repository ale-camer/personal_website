from utils import read_excel
import validations as val

from collections import defaultdict
import re

import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
from statsmodels.tsa.stattools import acf, pacf

# =============================================================================
# CLEANING
# =============================================================================
def get_first_sheet_name(data):
    return list(data.keys())[0]

def get_sheet_values(data, sheet_name):
    return [d for d in data[sheet_name][0] if d is not None]

def clean_excel_input(workbook_data: dict) -> dict:

    def parse_ref(ref):
        match = re.match(r"([A-Z]+)([0-9]+)", ref)
        if match: col, row = match.groups(); return col, int(row)
        return None, None

    def build_cols_and_max(cells):
        cols, max_row = defaultdict(dict), 0
        for c in cells:
            col, row = parse_ref(c["ref"])
            if col is None or row is None:
                continue
            cols[col][row] = c["value"]
        return cols, max(max_row, row)

    cleaned = {}
    for sheet, cells in workbook_data.items():
        cols, max_row = build_cols_and_max(cells)
        cleaned[sheet] = [
            [cols[col].get(row, None) for row in range(1, max_row + 1)]
            for col in sorted(cols.keys())
        ]

    return cleaned

# =============================================================================
# SCALAR OPERATIONS
# =============================================================================
def data_to_numeric(data):
    return [float(d) for d in data]

def get_mean(data: list) -> float:
    return sum(data) / len(data)

# =============================================================================
# VECTOR OPERATIONS
# =============================================================================
def groupby_lists(list1: list, list2: list) -> dict:
    grouped = defaultdict(list)
    for k, v in [(str(l1), l2) for l1, l2 in zip(list1, list2)]:
        grouped[k].append(v)
    return {k: get_mean(v) for k, v in grouped.items()}

def multiply_lists(list1: list, list2: list) -> list:
    return [l1 * l2 for l1, l2 in zip(list1, list2)]

def divide_lists(list1: list, list2: list) -> list:
    return [a / b for a, b in zip(list1, list2)]

def rolling_mean(serie, window):
    n, results = len(serie), []
    for i in range(n - window + 1):
        mean = sum(serie[i:i+window]) / window
        results.append(mean)
    return results

def forecast_time_serie(serie, periodicity: int) -> list:

    def compute_indices():
        n_periods = len(serie) // periodicity
        half_p = periodicity // 2
        next_periods = np.arange(len(serie) + 1, len(serie) + 1 + periodicity)
        subperiods = np.tile(np.arange(1, periodicity + 1), n_periods)[half_p : -half_p]
        periods = np.arange(1, len(serie) + 1, 1)
        return n_periods, half_p, next_periods, subperiods, periods

    def seasonal_decomposition(serie, n_periods, half_p, subperiods):
        moving_avgs = rolling_mean(rolling_mean(serie, periodicity), 2)
        irregulars = divide_lists(serie[half_p : -half_p], moving_avgs)
        avg_irrs = list(dict(sorted(
            groupby_lists(subperiods, irregulars).items(),
            key=lambda x: int(x[0])
        )).values())
        seasonal_indices = [g / get_mean(avg_irrs) for g in avg_irrs] * n_periods
        unseasonal_serie = divide_lists(serie, seasonal_indices)
        return seasonal_indices, unseasonal_serie

    def fit_trend(unseasonal_serie, periods):
        unseas_mean, periods_mean = get_mean(unseasonal_serie), get_mean(periods)
        unseas_minus_mean = [e - unseas_mean for e in unseasonal_serie]
        period_minus_mean = [float(p - periods_mean) for p in periods]
        num_serie = multiply_lists(unseas_minus_mean, period_minus_mean)
        den_serie = [float((p - periods_mean) ** 2) for p in periods]
        b1 = sum(num_serie) / sum(den_serie)
        b0 = unseas_mean - b1 * periods_mean
        return b0, b1

    def make_forecast(b0, b1, next_periods, seasonal_indices):
        unseas_forecast = [b0 + b1 * p for p in next_periods]
        seas_forecast = multiply_lists(unseas_forecast, seasonal_indices)
        return [round(float(v), 2) for v in seas_forecast]

    n_periods, half_p, next_periods, subperiods, periods = compute_indices()
    seasonal_indices, unseasonal_serie = seasonal_decomposition(serie, n_periods, half_p, subperiods)
    b0, b1 = fit_trend(unseasonal_serie, periods)
    forecast = make_forecast(b0, b1, next_periods, seasonal_indices)
    return forecast

def autocorrelations(serie: list, nlags: int = 12) -> tuple[list, list]:
    if nlags > len(serie) / 2: nlags = int(len(serie) / 2)
    acf_values = [int(v * 100) for v in acf(serie, nlags=nlags)]
    pacf_values = [int(v * 100) for v in pacf(serie, nlags=nlags, method='ols')]
    return acf_values, pacf_values

# =============================================================================
# PLOTS
# =============================================================================
def plot_forecasts(observed, last_forecast, next_forecast, periodicity):

    TITLE = "Seasonal Forecast Visualization"
    X_LABEL = "Period"
    Y_LABEL = "Value"
    LEGEND_TITLE = "Series"
    GRID_COLOR = 'rgba(200,200,200,0.25)'
    LEGEND_BG_COLOR = 'rgba(255,255,255,0.5)'

    SERIES_CONFIG = {
        "observed": {"name": "Observed Series", "color": "#1f77b4", "dash": "solid", "marker": "circle"},
        "last_fc": {"name": "Forecast (Last Period)", "color": "#d62728", "dash": "dash", "marker": "circle-open"},
        "next_fc": {"name": "Forecast (Next Period)", "color": "#2ca02c", "dash": "dot", "marker": "diamond-open"},
    }

    # X-values
    x_values = list(range(1, len(observed) + 1))
    x_last_fc = [x + 0.15 for x in x_values[-periodicity:]]
    x_next_fc = list(range(len(observed) + 1, len(observed) + 1 + periodicity))

    def create_trace(x, y, config):
        return go.Scatter(
            x=x, y=y, mode='lines+markers', name=config["name"],
            line=dict(color=config["color"], width=3, dash=config["dash"]),
            marker=dict(size=6, symbol=config["marker"])
        )

    fig = go.Figure()

    fig.add_trace(create_trace(x_values, observed, SERIES_CONFIG["observed"]))
    fig.add_trace(create_trace(x_last_fc, last_forecast, SERIES_CONFIG["last_fc"]))
    fig.add_trace(create_trace(x_next_fc, next_forecast, SERIES_CONFIG["next_fc"]))

    fig.update_layout(
        autosize=True,
        title=dict(text=TITLE, x=0.5, xanchor='center', font=dict(size=20, family='Arial', color='#111')),
        xaxis=dict(title=X_LABEL, showgrid=True, gridcolor=GRID_COLOR, zeroline=False),
        yaxis=dict(title=Y_LABEL, showgrid=True, gridcolor=GRID_COLOR, zeroline=False),
        legend=dict(
            title=LEGEND_TITLE,
            orientation='h',
            yanchor='bottom',
            y=-0.2,
            xanchor='center',
            x=0.5,
            bgcolor=LEGEND_BG_COLOR,
            bordercolor='rgba(0,0,0,0.1)',
            borderwidth=1
        ),
        template='plotly_white',
        margin=dict(l=50, r=30, t=70, b=70)
    )

    fig.show()

def plot_acf_pacf(acf_values: list, pacf_values: list):

    BASE_ANNOTATION = dict(
        showarrow=True,
        arrowhead=3,
        ax=0,
        ay=-40,
        font=dict(size=16, color="black")
    )

    def max_non100(values):
        filtered = [(i, v) for i, v in enumerate(values) if v < 100]
        return max(filtered, key=lambda x: x[1]) if filtered else (None, None)

    def add_bar_with_annotation(fig, row, col, values, color):
        max_lag, max_val = max_non100(values)
        annotation_params = {
            **BASE_ANNOTATION, "x": max_lag, "y": max_val,
            "text": f"Lag {max_lag}<br>{max_val}%", "row": row, "col": col
        }

        fig.add_trace(go.Bar(x=lags, y=values, marker_color=color), row=row, col=col)
        fig.add_hline(y=max_val, line=dict(color='black', dash='dash'), row=row, col=col)
        fig.add_annotation(**annotation_params)
        fig.update_xaxes(title_text="Lag", row=row, col=col)
        fig.update_yaxes(title_text="Correlation (%)", row=row, col=col)

    lags = list(range(len(acf_values)))

    fig = make_subplots(rows=1, cols=2, subplot_titles=("ACF", "PACF"))
    add_bar_with_annotation(fig, row=1, col=1, values=acf_values, color="#1f77b4")
    add_bar_with_annotation(fig, row=1, col=2, values=pacf_values, color="#d62728")

    fig.update_layout(
        autosize=True,
        template="plotly_white",
        showlegend=False,
        title=dict(
            text="Autocorrelation and Partial Autocorrelation",
            x=0.5, xanchor='center',
            font=dict(size=20, family='Arial', color='#111')
        ),
        margin=dict(l=50, r=30, t=80, b=50)
    )

    fig.show()

# =============================================================================
# PROCESS
# =============================================================================
def load_and_clean(file: str) -> list:

    data = read_excel(file)

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

    return data_to_numeric(serie)


def pipeline(file: str, p: int = 12) -> None:

    print("\nINITIATING DATA VALIDATION")
    serie = load_and_clean(file)

    print("\nINITIATING PROCESS")
    print("Calculating Predictions")
    pred_last_period = forecast_time_serie(serie[:-p], p)
    pred_next_period = forecast_time_serie(serie, p)

    print("Printing Forecast Plot")
    plot_forecasts_inputs = (serie, pred_last_period, pred_next_period, p)
    plot_forecasts(*plot_forecasts_inputs)

    print("Printing Autocorrelation Plot")
    acf_values, pacf_values = autocorrelations(serie)
    plot_acf_pacf(acf_values, pacf_values)

pio.renderers.default = 'browser'
file, periodicity = "seasonality_example.xlsx", 12
pipeline(file, periodicity)