"""Refactored Seasonality Prediction functionality using two classes."""

# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import os
import zipfile as zf
from dataclasses import dataclass

# --- Third-party ---
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# --- Project/system ---
from modules.utils_OLD import read_json

def temp_lang_json(lang: str):
    return read_json(os.path.join('static', 'json', 'lang', f'{lang}.json'))

# =============================================================================
# PREDICTION
# =============================================================================
@dataclass
class PlotConfig:    
    save_dir: str = os.path.join('static', 'seasonality')
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

    def __init__(self, config: PlotConfig, periodicity: int = 4) -> None:
        self.periodicity = periodicity
        self.config = PlotConfig()

    def _calculate_centered_moving_average(self, serie: pd.Series) -> pd.Series:
        return (
            serie
            .rolling(self.periodicity)
            .mean()
            .dropna()
            .rolling(2)
            .mean()
            .dropna()
        )

    def _compute_seasonal_indices(self, serie: pd.Series, serie_cma: pd.Series) -> list[float]:
        num = len(serie)
        half_period = self.periodicity // 2

        periods = (
            np.arange(1, self.periodicity + 1).tolist() * (num // self.periodicity)
        )[half_period:-half_period]

        irr_seas_comp = (
            serie[half_period:-half_period].values / serie_cma.values
        )
        
        seasonal_indices = (
            pd.DataFrame(
                {
                    'irr': irr_seas_comp, 
                    'period': periods
                }
            )
            .groupby('period')['irr']
            .mean()
        )

        return list(seasonal_indices / seasonal_indices.mean()) * int(num / self.periodicity)

    def _forecast_trend_component(self, serie: pd.Series, adj_seas_index: list[float]) -> np.ndarray:
        past_periods = np.arange(1, len(serie) + 1)
        next_periods = np.arange(
            past_periods[-1] + 1,
            past_periods[-1] + 1 + self.periodicity
        )

        unseasonal_serie = serie.values / adj_seas_index
        X = np.vstack([np.ones_like(past_periods), past_periods]).T
        b = np.linalg.inv(X.T @ X) @ X.T @ unseasonal_serie

        return b[0] + b[1] * next_periods

    def predict(self, serie: pd.Series) -> list[float]:
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
      
    def save_predictions(self, forecast: list[float], file_name: str = 'predictions.csv') -> None:
        os.makedirs(self.config.save_dir, exist_ok=True)
        forecast = {'PERIOD': range(1, len(forecast) + 1), 'VALUE': forecast}
        pd.DataFrame(forecast).to_csv(os.path.join(self.config.save_dir, file_name), index=False)

class SeasonalityPlotter:

    def __init__(self, config: PlotConfig) -> None:
        self.config = PlotConfig()

    def _ensure_save_directory(self) -> None:
        if not os.path.exists(self.config.save_dir):
            os.makedirs(self.config.save_dir)

    def _save_figure(self, fig, filename: str) -> None:
        self._ensure_save_directory()
        fig.tight_layout()
        fig.savefig(os.path.join(self.config.save_dir, filename))
        plt.close(fig)

    def plot_original_data(self, serie: pd.Series, periodicity: int) -> None:
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

    def plot_last_period_comparison(self, serie: pd.Series, prediction_last_period: list | np.ndarray, periodicity: int) -> None:
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

    def plot_next_period_forecast(self, serie: pd.Series, prediction_next_period: list | np.ndarray) -> None:
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

    def generate_all_plots(
        self, 
        serie: pd.Series, 
        prediction_last_period: list | np.ndarray, 
        prediction_next_period: list | np.ndarray, 
        periodicity: int = 4
    ) -> None:
        self.plot_original_data(serie, periodicity)
        self.plot_next_period_forecast(serie, prediction_next_period)
        self.plot_last_period_comparison(serie, prediction_last_period, periodicity)

class SeasonalityModule:

    def __init__(self, file: str, periodicity: int = 4, plot_config: PlotConfig | None = None) -> None:
        self.serie = None
        self.file = file
        self.periodicity = periodicity
        self.config = plot_config or PlotConfig()
        self.plotter = SeasonalityPlotter(self.config)
        self.predictor = SeasonalityPredictor(self.config, self.periodicity)

    def is_empty(self, lang: str = 'en') -> str | None:
        self.df = pd.read_excel(self.file)
        if self.df.empty:
            error_message = temp_lang_json(lang)["predict_seasonality"]["error_message"]
            return error_message
        self.serie = self.df.iloc[:, 0]
        return None
        
    def forecast(self) -> dict:
    
        forecasted_last_period = self.predictor.predict(self.serie.iloc[:-self.periodicity])
        forecasted_next_period = self.predictor.predict(self.serie)

        self.predictor.save_predictions(forecasted_next_period)
        self.plotter.generate_all_plots(
            self.serie,
            forecasted_last_period,
            forecasted_next_period,
            self.periodicity
        )
        return forecasted_next_period

    def validation(self, lang: str) -> str:
        return temp_lang_json(lang)["predict_seasonality"]["validation"]
      
# =============================================================================
# DOWNLOAD PREDICTIONS
# =============================================================================
def download_forecast(config: PlotConfig = PlotConfig(), zip_filename: str = 'predictions.zip'):
    base_dir = config.save_dir
    zip_path = os.path.join(base_dir, zip_filename)
    with zf.ZipFile(zip_path, 'w', zf.ZIP_DEFLATED) as f:
        for root, _, files in os.walk(base_dir):
            for file in files:
                if file != zip_filename:
                    file_path = os.path.join(root, file)
                    f.write(file_path, os.path.relpath(file_path, base_dir))
    return zip_path, zip_filename