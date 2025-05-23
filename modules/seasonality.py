"""Refactored Seasonality Prediction functionality using two classes."""

# --- Standard library ---
import os
import zipfile
from dataclasses import dataclass

# --- Third-party ---
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
import seaborn as sns

@dataclass
class PlotConfig:
    """Configuration for plot appearance and styling."""
    
    save_dir: str = 'static/seasonality'
    fig_size: tuple = (10, 5)
    y_fontsize: int = 15
    subplot_title_fontsize: int = 18
    plot_title_fontsize: int = 20
    real_data_color: str = 'red'
    pred_data_color: str = 'green'
    y_label: str = "Value"
    real_data_label: str = 'Real'
    pred_data_label: str = 'Prediction'

class SeasonalityPredictor:
    """Handle time series seasonality prediction using classical decomposition."""

    def __init__(self, periodicity: int = 4) -> None:
        """
        Initialize the seasonality predictor.

        Args:
            periodicity (int): Number of periods in the seasonal cycle.
        """
        self.periodicity = periodicity

    @staticmethod
    def read_time_series(filepath: str):
        """
        Read the first column of an Excel file and return it as a pandas Series.

        Args:
            filepath (str): Path to the Excel file.

        Returns:
            pd.Series: Time series data from the first column of the Excel file.
        """
        serie = pd.read_excel(filepath)
        return pd.Series(serie[serie.columns[0]])

    def _calculate_centered_moving_average(self, serie):
        """
        Calculate the centered moving average (CMA) for the time series.

        Args:
            serie (pd.Series): Input time series.

        Returns:
            pd.Series: Centered moving average of the series.
        """
        return (
            serie
            .rolling(self.periodicity)
            .mean()
            .dropna()
            .rolling(2)
            .mean()
            .dropna()
        )

    def _compute_seasonal_indices(self, serie, serie_cma):
        """
        Compute seasonal indices from a time series and its centered moving average.

        Args:
            serie (pd.Series): Original time series.
            serie_cma (pd.Series): Centered moving average of the time series.

        Returns:
            list: Seasonal indices normalized to have mean 1.
        """
        num = len(serie)
        half_period = self.periodicity // 2

        periods = (
            np.arange(1, self.periodicity + 1).tolist() * (num // self.periodicity)
        )[half_period:-half_period]

        irr_seas_comp = (
            serie[half_period:-half_period].values / serie_cma.values
        )

        seas_df = pd.DataFrame({'irr': irr_seas_comp, 'period': periods})
        seasonal_indices = seas_df.groupby('period')['irr'].mean()

        return list(seasonal_indices / seasonal_indices.mean()) * int(num / self.periodicity)

    def _forecast_trend_component(self, serie, adj_seas_index):
        """
        Estimate the trend component using linear regression and forecast future periods.

        Args:
            serie (pd.Series): Original time series.
            adj_seas_index (list or np.ndarray): Adjusted seasonal indices.

        Returns:
            np.ndarray: Forecasted trend component for the next seasonal cycle.
        """
        past_periods = np.arange(1, len(serie) + 1)
        next_periods = np.arange(
            past_periods[-1] + 1,
            past_periods[-1] + 1 + self.periodicity
        )

        unseasonal_serie = serie.values / adj_seas_index
        X = np.vstack([np.ones_like(past_periods), past_periods]).T
        b = np.linalg.inv(X.T @ X) @ X.T @ unseasonal_serie

        return b[0] + b[1] * next_periods

    def predict(self, serie):
        """
        Generate forecasts for the next seasonal cycle.

        Args:
            serie (pd.Series): Time series with a length divisible by the periodicity.

        Returns:
            list: Forecasted values for the next seasonal cycle.

        Raises:
            ValueError: If the series length is not divisible by the periodicity.
        """
        if len(serie) % self.periodicity != 0:
            raise ValueError(
                f"Series length ({len(serie)}) is not divisible by "
                f"periodicity ({self.periodicity})"
            )

        cma = self._calculate_centered_moving_average(serie)
        seasonal_indices = self._compute_seasonal_indices(serie, cma)
        trend_forecast = self._forecast_trend_component(serie, seasonal_indices)

        forecast = trend_forecast * seasonal_indices[:self.periodicity]
        return [round(float(v), 2) for v in forecast]

class SeasonalityPlotter:
    """Handle visualization of time series data and seasonality predictions."""

    def __init__(self, config=None):
        """Initialize the SeasonalityPlotter with a plotting configuration.

        Args:
            config (PlotConfig, optional): Configuration for plot styling and saving. 
                If None, a default PlotConfig is used.
        """
        self.config = config or PlotConfig()

    def _ensure_save_directory(self):
        """Ensure the directory to save plots exists.

        Creates the directory specified in the configuration if it does not exist.
        """
        if not os.path.exists(self.config.save_dir):
            os.makedirs(self.config.save_dir)

    def _save_figure(self, fig, filename):
        """Save a matplotlib figure to disk.

        Adjusts layout, saves the figure to the configured directory, and closes it.

        Args:
            fig (matplotlib.figure.Figure): The figure to save.
            filename (str): Name of the output image file.
        """
        self._ensure_save_directory()
        fig.tight_layout()
        fig.savefig(os.path.join(self.config.save_dir, filename))
        plt.close(fig)

    def plot_original_data(self, serie, periodicity):
        """Plot and save the original time series data.

        Args:
            serie (pandas.Series): The time series to plot.
            periodicity (int): Number of periods in a seasonal cycle.
        """
        fig = plt.figure(figsize=self.config.fig_size)

        extended_data = np.concatenate([
            serie.values,
            serie[-periodicity:].values
        ]).ravel()

        sns.lineplot(extended_data, color=self.config.real_data_color)
        plt.xticks([])
        plt.ylabel(self.config.y_label, fontsize=self.config.y_fontsize)
        plt.title("Original Data", fontsize=self.config.plot_title_fontsize)

        self._save_figure(fig, 'original_data.png')

    def plot_last_period_comparison(self, serie, prediction_last_period, periodicity):
        """Plot and save a comparison of the last actual period with its prediction.

        Two subplots are created: one with all data and one with the last period.

        Args:
            serie (pandas.Series): Original time series data.
            prediction_last_period (list or np.ndarray): Predicted values for the last period.
            periodicity (int): Number of periods in a seasonal cycle.
        """
        fig = plt.figure(figsize=self.config.fig_size)

        plt.subplot(1, 2, 1)
        all_periods_pred = np.concatenate([
            serie.values[:-periodicity],
            prediction_last_period
        ])

        sns.lineplot(
            all_periods_pred,
            color=self.config.pred_data_color,
            label=self.config.pred_data_label
        )
        sns.lineplot(
            serie.values.ravel(),
            color=self.config.real_data_color,
            label=self.config.real_data_label
        )

        plt.xticks([])
        plt.ylabel(self.config.y_label, fontsize=self.config.y_fontsize)
        plt.title("All Periods", fontsize=self.config.subplot_title_fontsize)

        plt.subplot(1, 2, 2)
        sns.lineplot(
            prediction_last_period,
            color=self.config.pred_data_color,
            label=self.config.pred_data_label
        )
        sns.lineplot(
            serie.values[-periodicity:],
            color=self.config.real_data_color,
            label=self.config.real_data_label
        )

        plt.xticks([])
        plt.ylabel(self.config.y_label, fontsize=self.config.y_fontsize)
        plt.title("Last Period", fontsize=self.config.subplot_title_fontsize)

        plt.suptitle("Last Period Prediction", fontsize=self.config.plot_title_fontsize)
        self._save_figure(fig, 'all_periods_data.png')

    def plot_next_period_forecast(self, serie, prediction_next_period):
        """Plot and save the next period forecast alongside historical data.

        Args:
            serie (pandas.Series): The historical time series data.
            prediction_next_period (list or np.ndarray): Forecasted values for the next period.
        """
        fig = plt.figure(figsize=self.config.fig_size)

        prediction_x = range(len(serie) - 1, len(serie) + len(prediction_next_period))
        prediction_y = np.concatenate([
            [serie.values[-1]],
            prediction_next_period
        ])

        sns.lineplot(
            x=prediction_x,
            y=prediction_y,
            color=self.config.pred_data_color,
            label=self.config.pred_data_label
        )

        sns.lineplot(
            x=range(len(serie)),
            y=serie.values.ravel(),
            color=self.config.real_data_color,
            label=self.config.real_data_label
        )

        plt.xticks([])
        plt.ylabel(self.config.y_label, fontsize=self.config.y_fontsize)
        plt.title(
            "Original Data and Next Period Prediction",
            fontsize=self.config.plot_title_fontsize
        )

        self._save_figure(fig, 'historic_and_prediction_data.png')

    def generate_all_plots(self, serie: pd.Series, prediction_last_period: list | np.ndarray, prediction_next_period: list | np.ndarray, periodicity: int = 4):
        """Generate and save all plots related to time series and forecast analysis.

        Args:
            serie (pandas.Series): Original time series data.
            prediction_last_period (list or np.ndarray): Forecast for the last observed period.
            prediction_next_period (list or np.ndarray): Forecast for the upcoming period.
            periodicity (int, optional): Number of periods in a season. Defaults to 4.
        """
        self.plot_original_data(serie, periodicity)
        self.plot_next_period_forecast(serie, prediction_next_period)
        self.plot_last_period_comparison(serie, prediction_last_period, periodicity)

class FileManager:
    """Handle file operations related to seasonality prediction results."""

    def __init__(self, base_dir: str = 'static/seasonality'):
        """Initialize the FileManager with a base directory for file storage.

        Args:
            base_dir (str, optional): Base directory where files will be saved.
                Defaults to 'static/seasonality'.
        """
        self.base_dir = base_dir

    def save_predictions_csv(self, predictions, filename: str = 'predictions.csv'):
        """Save prediction data to a CSV file.

        Converts the predictions into a DataFrame with columns 'PERIOD' and 'VALUE',
        and saves it under the specified filename inside the base directory.

        Args:
            predictions (list or array-like): Prediction values to save.
            filename (str, optional): Name of the CSV file to create.
                Defaults to 'predictions.csv'.
        """
        df_to_print = (
            pd.DataFrame(predictions)
            .reset_index()
            .rename(columns={'index': 'PERIOD', 0: 'VALUE'})
        )

        filepath = os.path.join(self.base_dir, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        df_to_print.to_csv(filepath, index=False)

    def create_predictions_zip(self, zip_filename: str = 'predictions.zip'):
        """Create a ZIP archive containing all prediction result files.

        Scans the base directory and adds all files except the ZIP itself into
        a new ZIP archive.

        Args:
            zip_filename (str, optional): Name of the ZIP file to create.
                Defaults to 'predictions.zip'.

        Returns:
            str: The full path to the created ZIP archive.
        """
        zip_path = os.path.join(self.base_dir, zip_filename)

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.base_dir):
                for file in files:
                    if file != zip_filename:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, self.base_dir))

        return zip_path
    
class SeasonalityProcessor:
    """Manage the complete workflow for seasonality analysis, including prediction, plotting, and file handling."""

    def __init__(self, periodicity=4, plot_config=None):
        """Initialize the SeasonalityProcessor with periodicity and optional plot configuration.

        Args:
            periodicity (int, optional): Number of data points per period. Defaults to 4.
            plot_config (PlotConfig or None, optional): Configuration object for plotting.
                Defaults to None.
        """
        self.predictor = SeasonalityPredictor(periodicity)
        self.plotter = SeasonalityPlotter(plot_config)
        self.file_manager = FileManager()
        self.periodicity = periodicity

    def process_file(self, file):
        """Process an uploaded Excel file to extract the time series data,
        validate it, perform seasonality prediction, and generate plots.

        Args:
            file (file-like): Excel file containing a single-column numeric time series.

        Raises:
            ValueError: If the file is empty, contains non-numeric data,
                        has more than one column, or the series length
                        is not divisible by the periodicity.

        Returns:
            dict: A dictionary containing:
                - 'forecasted_last_period': Predictions for the last period based on previous data.
                - 'forecasted_next_period': Predictions for the next period based on entire series.
                - 'serie_data': The original time series data as a pandas Series.
        """
        serie = pd.read_excel(file)

        if serie.empty:
            raise ValueError("File is empty")

        col_name = serie.columns[0]
        serie_data = serie[col_name]

        if not pd.api.types.is_numeric_dtype(serie_data):
            raise ValueError("Data is not numeric")

        if serie.shape[1] != 1:
            raise ValueError(f"Expected 1 column, got {serie.shape[1]}")

        if len(serie_data) % self.periodicity != 0:
            raise ValueError(
                f"Series length ({len(serie_data)}) is not divisible by "
                f"periodicity ({self.periodicity})"
            )

        forecasted_last_period = self.predictor.predict(serie_data.iloc[:-self.periodicity])
        forecasted_next_period = self.predictor.predict(serie_data)

        self.plotter.generate_all_plots(
            serie_data,
            forecasted_last_period,
            forecasted_next_period,
            self.periodicity
        )

        return {
            'forecasted_last_period': forecasted_last_period,
            'forecasted_next_period': forecasted_next_period,
            'serie_data': serie_data
        }

    def save_predictions_csv(self, predictions):
        """Save the given predictions to a CSV file using the FileManager.

        Args:
            predictions (list or array-like): Predictions to save.
        """
        self.file_manager.save_predictions_csv(predictions)

    def create_predictions_zip(self) -> str:
        """Create and return the path to a ZIP file containing all prediction results.

        Returns:
            str: Path to the created ZIP archive.
        """
        return self.file_manager.create_predictions_zip()

    def get_validation_details(self, serie: pd.Series, periodicity: int) -> str:
        """Generate an HTML-formatted string with validation details about the series.

        Useful for reporting data format and length issues.

        Args:
            serie (pandas.DataFrame): The data series to validate.
            periodicity (int): Expected periodicity of the series.

        Returns:
            str: HTML unordered list with validation messages.
        """
        remainder = len(serie) % periodicity

        details = [
            f"<li>Data format: {'OK' if pd.api.types.is_numeric_dtype(serie.iloc[:, 0]) else 'Not OK. Data is not numeric.'}</li>",
            f"<li>Number of columns: {'OK' if serie.shape[1] == 1 else f'Not OK. There are {serie.shape[1]} columns instead of one.'}</li>",
            f"<li>Series length: {len(serie)}</li>",
            f"<li>Periodicity: {'OK' if periodicity > 1 else f'Not OK. The value of the periodicity is {periodicity} and has to be higher than one and when dividing the length of the serie the reminder must be zero.'}</li>",
            f"<li>Remainder: {'OK' if remainder == 0 else f'Not OK. The value of the reminder is {remainder} instead of zero.'}</li>"
        ]

        return f"<ul>{''.join(details)}</ul>"
