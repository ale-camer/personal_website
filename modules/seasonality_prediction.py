"""
Contain functions for Seasonality Prediction functionality.
"""

import matplotlib, os
matplotlib.use('Agg')

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# =============================================================================
# TIME SERIES SEASONALITY PREDICTION
# =============================================================================
def _read_time_series(filepath: str) -> pd.Series:
    """
    Read the first column of an Excel file and return it as a pandas Series.

    Args:
        filepath: The path to the Excel file.
  
    Returns:
        A pandas Series containing the values from the first column of the Excel file.
    """
    serie = pd.read_excel(filepath)
    return pd.Series(serie[serie.columns[0]])

def _centered_moving_average(serie: pd.Series, periodicity: int) -> pd.Series:
    """
    Calculate the centered moving average (CMA) for a given time series.

    This is done by applying a rolling average of the specified periodicity,
    followed by a second rolling average of window size 2 to center the result.
  
    Args:
        serie: The original time series as a pandas Series.
        periodicity: The number of periods in a full seasonal cycle.
  
    Returns:
        A pandas Series containing the centered moving average values.
    """
    return (
        serie
        .rolling(periodicity)
        .mean()
        .dropna()
        .rolling(2)
        .mean()
        .dropna()
    )
  
def _get_seasonal_indices(serie: pd.Series, serie_cma: pd.Series, periodicity: int) -> list[float]:
    """
    Compute seasonal indices from a time series and its centered moving average.

    The irregular-seasonal components are calculated by dividing the series by the CMA.
    Then, for each period (e.g., each quarter or month), the average component is computed
    and normalized to have a mean of 1.
  
    Args:
        serie: The original time series.
        serie_cma: The centered moving average of the time series.
        periodicity: The number of periods in a seasonal cycle.
  
    Returns:
        A list of normalized seasonal indices repeated over the length of the series.
    """
    num = len(serie)
    periods = (np.arange(1, periodicity + 1).tolist() * (num // periodicity))[periodicity // 2 : -(periodicity // 2)]
    irr_seas_comp = serie[int(periodicity / 2):-int(periodicity / 2)].values / serie_cma.values
    seas_df = pd.DataFrame({'irr': irr_seas_comp, 'period': periods})
    seasonal_indices = seas_df.groupby('period')['irr'].mean()
    return list(seasonal_indices / seasonal_indices.mean()) * int(num / periodicity)
  
def _forecast_trend_component(serie: pd.Series, adj_seas_index: np.array, periodicity: int) -> np.ndarray:
    """
    Estimate the trend component using linear regression and forecast future periods.
  
    The trend is isolated by removing the seasonal component, and a linear regression is
    applied over time. This trend is then extrapolated over the next full seasonal cycle.
  
    Args:
        serie: The original time series.
        adj_seas_index: The adjusted seasonal indices.
        periodicity: The number of periods to forecast ahead.
  
    Returns:
        A NumPy array containing the forecasted trend values for the next periods.
    """
    past_periods = np.arange(1, len(serie) + 1)
    next_periods = np.arange(past_periods[-1] + 1, past_periods[-1] + 1 + periodicity)
    unseasonal_serie = serie.values / adj_seas_index
    X = np.vstack([np.ones_like(past_periods), past_periods]).T
    b = np.linalg.inv(X.T @ X) @ X.T @ unseasonal_serie
    return b[0] + b[1] * next_periods
    
def seasonal_forecast(serie: pd.Series, periodicity: int = 4) -> list[float]:
    """
    Generate forecasts for the next seasonal cycle using classical time series decomposition.

    The function computes the centered moving average, derives seasonal indices,
    estimates the underlying trend, and returns the final forecast as the product
    of the trend and seasonal components.
  
    Args:
        serie: The input time series.
        periodicity: The number of periods in a season (e.g., 4 for quarterly data).
  
    Returns:
        A list of forecasted values rounded to two decimal places.
  
    Raises:
        ValueError: If the length of the series is not divisible by the periodicity.
    """
    if len(serie) % periodicity != 0:
        raise ValueError("The length of the serie does not match its periodicity.")

    cma = _centered_moving_average(serie, periodicity)
    seasonal_indices = _get_seasonal_indices(serie, cma, periodicity)
    trend_forecast = _forecast_trend_component(serie, seasonal_indices, periodicity)
    
    return [round(float(v), 2) for v in trend_forecast * seasonal_indices[:periodicity]]

# =============================================================================
# PLOTS
# =============================================================================
SAVE_DIR = 'static/seasonality_prediction'
FIG_SIZE = (10, 5)
Y_FONTSIZE = 15
SUBPLOT_TITLE_FONTSIZE = 18
PLOT_TITLE_FONTSIZE = 20
REAL_DATA_COLOR = 'red'
PRED_DATA_COLOR = 'green'
Y_LABEL = "Value".title()
REAL_DATA_LABEL = 'Real'.title()
PRED_DATA_LABEL = 'Prediction'.title()

def _save_plot(fig: Figure, save_dir: str, filename: str) -> None:
    """
    Adjust layout, save the figure, and close it.

    Creates the save directory if it does not exist.

    Args:
        fig: The matplotlib Figure object to save.
        save_dir: The directory where the figure will be saved.
        filename: The name for the saved figure file.
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    fig.tight_layout()
    fig.savefig(os.path.join(save_dir, filename))
    plt.close(fig)

def _plot_original_data(serie: pd.Series, periodicity: int) -> None:
    """
    Generate and save a plot of the original time series data.

    The plot visually extends the series by appending its last `periodicity`
    points, which can help visualize cyclical patterns.

    Args:
        serie: The original time series data.
        periodicity: The number of data points in a seasonal cycle,
                     used for the visual extension.
    """
    fig = plt.figure(figsize=FIG_SIZE)
    sns.lineplot(
      np.concatenate(
        [
          serie.values,
          serie[-periodicity:].values
        ]
      ).ravel(),
      color=REAL_DATA_COLOR
    )
    plt.xticks([])
    plt.ylabel(Y_LABEL, fontsize=Y_FONTSIZE)
    plt.title("Original Data", fontsize=PLOT_TITLE_FONTSIZE)
    _save_plot(fig, SAVE_DIR, 'original_data.png')

def _plot_last_period(serie: pd.Series, prediction_last_period: list, periodicity: int) -> None:
    """
    Generate and save plots comparing the last period's actual data with its prediction.

    This function creates a figure with two subplots:
    1.  The entire series with the last period replaced by its prediction.
    2.  A focused view of the actual last period versus its prediction.

    Args:
        serie: The original time series data.
        prediction_last_period: Predicted values for the last period of the series.
        periodicity: The number of data points in a seasonal cycle.
    """
    fig = plt.figure(figsize=FIG_SIZE)

    plt.subplot(1, 2, 1)
    sns.lineplot(
      np.concatenate(
        [
          serie.values[:-periodicity],
          prediction_last_period
        ]
      ),
      color=PRED_DATA_COLOR,
      label=PRED_DATA_LABEL
    )
    sns.lineplot(
      serie.values.ravel(),
      color=REAL_DATA_COLOR,
      label=REAL_DATA_LABEL
    )
    plt.xticks([])
    plt.ylabel(Y_LABEL, fontsize=Y_FONTSIZE)
    plt.title("All Periods".title(), fontsize=SUBPLOT_TITLE_FONTSIZE)

    plt.subplot(1, 2, 2)
    sns.lineplot(
      prediction_last_period,
      color=PRED_DATA_COLOR,
      label=PRED_DATA_LABEL
    )
    sns.lineplot(
      serie.values[-periodicity:],
      color=REAL_DATA_COLOR,
      label=REAL_DATA_LABEL
    )
    plt.xticks([])
    plt.ylabel(Y_LABEL, fontsize=Y_FONTSIZE)
    plt.title("Last Period".title(), fontsize=SUBPLOT_TITLE_FONTSIZE)

    plt.suptitle("Last Period Prediction".title(), fontsize=PLOT_TITLE_FONTSIZE)
    _save_plot(fig, SAVE_DIR, 'all_periods_data.png')

def _plot_next_period(serie: pd.Series, prediction_next_period: list) -> None:
    """
    Generate and save a plot of the original data and the next period's prediction.

    This plot shows the historical time series followed by the predicted values
    for the subsequent period.

    Args:
        serie: The original time series data.
        prediction_next_period: Predicted values for the period immediately
                                following the end of the `serie`.
    """
    fig = plt.figure(figsize=FIG_SIZE)
    sns.lineplot(
        x=range(len(serie) - 1, len(serie) + len(prediction_next_period)),
        y=np.concatenate(
          [
            [serie.values[-1]], # Start prediction line from last actual point
            prediction_next_period
          ]
        ),
        color=PRED_DATA_COLOR,
        label=PRED_DATA_LABEL
    )
    sns.lineplot(
        x=range(len(serie)),
        y=serie.values.ravel(),
        color=REAL_DATA_COLOR,
        label=REAL_DATA_LABEL
    )
    plt.xticks([])
    plt.ylabel(Y_LABEL, fontsize=Y_FONTSIZE)
    plt.title("Original Data and Next Period Prediction", fontsize=PLOT_TITLE_FONTSIZE)
    _save_plot(fig, SAVE_DIR, 'historic_and_prediction_data.png')

def generate_plots(
        serie: pd.Series,
        prediction_last_period: list,
        prediction_next_period: list,
        periodicity: int = 4
    ) -> None:
    """
    Generate and save a suite of time series analysis plots.

    This function orchestrates the creation of three types of plots:
    1. The original time series data.
    2. A comparison of the last observed period against its prediction.
    3. The original time series followed by the prediction for the next period.

    All plots are saved as PNG files in the directory specified by `SAVE_DIR`.

    Args:
        serie: The original time series data as a pandas Series.
        prediction_last_period: A list of predicted values for the last
            period of the `serie`.
        prediction_next_period: A list of predicted values for the period
            immediately following the `serie`.
        periodicity: An integer representing the number of data points
            in a seasonal cycle. Defaults to 4.
    """

    _plot_original_data(serie, periodicity)
    _plot_next_period(serie, prediction_next_period)
    _plot_last_period(serie, prediction_last_period, periodicity)