import modules.common.utils as ut
import modules.common.validations as val

import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
# from statsmodels.tsa.stattools import acf, pacf

import os

import numpy as np

def acf(x, nlags):
    """Autocorrelation function sin usar statsmodels"""
    x = np.asarray(x)
    x = x - np.mean(x)
    result = np.correlate(x, x, mode='full')
    result = result[result.size // 2:]  # quedarse con la mitad positiva
    result = result / result[0]         # normalizar
    return result[:nlags + 1]

def pacf(x, nlags):
    """Partial autocorrelation usando el algoritmo de Levinson–Durbin"""
    x = np.asarray(x)
    acf_vals = acf_np(x, nlags)
    pacf_vals = np.zeros(nlags + 1)
    pacf_vals[0] = 1.0

    phi = np.zeros((nlags + 1, nlags + 1))
    phi[1, 1] = acf_vals[1]
    pacf_vals[1] = acf_vals[1]

    for k in range(2, nlags + 1):
        num = acf_vals[k] - np.sum(phi[j, k - 1] * acf_vals[k - j] for j in range(1, k))
        den = 1 - np.sum(phi[j, k - 1] * acf_vals[j] for j in range(1, k))
        phi[k, k] = num / den
        for j in range(1, k):
            phi[j, k] = phi[j, k - 1] - phi[k, k] * phi[k - j, k - 1]
        pacf_vals[k] = phi[k, k]

    return pacf_vals

# 👇 Reemplazo directo de tu código
# acf_values = [int(v * 100) for v in acf_np(serie, nlags)]
# pacf_values = [int(v * 100) for v in pacf_np(serie, nlags)]


# =============================================================================
# OPERATIONS
# =============================================================================
def forecast_time_serie(serie: list, periodicity: int) -> list:

    def compute_indices():
        n_periods = len(serie) // periodicity
        half_p = periodicity // 2
        next_periods = np.arange(len(serie) + 1, len(serie) + 1 + periodicity)
        subperiods = np.tile(np.arange(1, periodicity + 1), n_periods)[half_p : -half_p]
        periods = np.arange(1, len(serie) + 1, 1)
        return n_periods, half_p, next_periods, subperiods, periods

    def seasonal_decomposition(serie, n_periods, half_p, subperiods):
        moving_avgs = ut.rolling_mean(ut.rolling_mean(serie, periodicity), 2)
        irregulars = ut.divide_lists(serie[half_p : -half_p], moving_avgs)
        avg_irrs = list(dict(sorted(
            ut.groupby_lists(subperiods, irregulars).items(),
            key=lambda x: int(x[0])
        )).values())
        seasonal_indices = [g / ut.get_mean(avg_irrs) for g in avg_irrs] * n_periods
        unseasonal_serie = ut.divide_lists(serie, seasonal_indices)
        return seasonal_indices, unseasonal_serie

    def fit_trend(unseasonal_serie, periods):
        unseas_mean, periods_mean = ut.get_mean(unseasonal_serie), ut.get_mean(periods)
        unseas_minus_mean = [e - unseas_mean for e in unseasonal_serie]
        period_minus_mean = [float(p - periods_mean) for p in periods]
        num_serie = ut.multiply_lists(unseas_minus_mean, period_minus_mean)
        den_serie = [float((p - periods_mean) ** 2) for p in periods]
        b1 = sum(num_serie) / sum(den_serie)
        b0 = unseas_mean - b1 * periods_mean
        return b0, b1

    def make_forecast(b0, b1, next_periods, seasonal_indices):
        unseas_forecast = [b0 + b1 * p for p in next_periods]
        seas_forecast = ut.multiply_lists(unseas_forecast, seasonal_indices)
        return [round(float(v), 2) for v in seas_forecast]

    n_periods, half_p, next_periods, subperiods, periods = compute_indices()
    seasonal_indices, unseasonal_serie = seasonal_decomposition(serie, n_periods, half_p, subperiods)
    b0, b1 = fit_trend(unseasonal_serie, periods)
    forecast = make_forecast(b0, b1, next_periods, seasonal_indices)
    return forecast

def autocorrelations(serie: list, nlags: int = 12) -> tuple[list, list]:
    if nlags > len(serie) / 2: nlags = int(len(serie) / 2)
    acf_values = [int(v * 100) for v in acf(serie, nlags)]
    pacf_values = [int(v * 100) for v in pacf(serie, nlags)]
    return acf_values, pacf_values

# =============================================================================
# PLOTS
# =============================================================================
def plot_forecasts(
        observed: list, last_forecast: list, next_forecast: list, 
        periodicity: int, save_dir: str
    ) -> None:

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

    fig.write_image(os.path.join(save_dir, 'forecast_plot.png'), scale=2)

def plot_acf_pacf(acf_values: list, pacf_values: list, save_dir: str):

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

    fig.write_image(os.path.join(save_dir, 'acf_pacf_plot.png'), scale=2)