# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---

# --- Third-party ---
import numpy as np

# --- Project ---
from modules.common.utils import (
    rolling_mean, divide_lists, multiply_lists, get_mean, groupby_lists, timed_run
)

# =============================================================================
# AUXILIARY FUNCTIONS
# =============================================================================
def acf(x, nlags):
    x = np.asarray(x)
    x = x - np.mean(x)
    result = np.correlate(x, x, mode='full')
    result = result[result.size // 2:]
    result = result / result[0]
    return result[:nlags + 1]

def pacf(x, nlags):
    x = np.asarray(x)
    acf_vals = acf(x, nlags)
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

# =============================================================================
# CORE
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
    acf_values = [int(v * 100) for v in acf(serie, nlags)]
    pacf_values = [int(v * 100) for v in pacf(serie, nlags)]
    return acf_values, pacf_values