# =============================================================================
# LEGACY CALCULATION
# =============================================================================
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acf, pacf

class SeasonalityPredictor:

    def __init__(self, periodicity: int, nlags: int) -> None:
        self.periodicity = periodicity
        self.nlags = nlags

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

    def autocorrelations(self, serie: pd.Series) -> tuple[list]:

        if self.nlags > len(serie) / 2:
            self.nlags = int(self.nlags / 2)

        acf_values = acf(serie, nlags=self.nlags)
        pacf_values = pacf(serie, nlags=self.nlags, method='ols')
        print(acf_values, pacf_values)
        return [int(v * 100) for v in acf_values], [int(v * 100) for v in pacf_values]

class SeasonalityModule:

    def __init__(self, file: str, periodicity = 4, nlags = 10) -> None:
        self.serie = None
        self.file = file
        self.periodicity = periodicity
        self.nlags = nlags
        self.predictor = SeasonalityPredictor(self.periodicity, self.nlags)

    def is_empty(self, lang: str = 'en') -> str | None:
        self.df = pd.read_excel(self.file)
        if self.df.empty:
            error_message = None
            return error_message
        self.serie = self.df.iloc[:, 0]
        return None

    def forecast(self) -> dict:

        forecasted_last_period = self.predictor.predict(self.serie.iloc[:-self.periodicity])
        forecasted_next_period = self.predictor.predict(self.serie)
        acf_values, pacf_values = self.predictor.autocorrelations(self.serie)

        self.plotter.nlags = self.predictor.nlags
        self.predictor.save_predictions(forecasted_next_period, acf_values, pacf_values)

        self.plotter.generate_all_plots(
            self.serie,
            forecasted_last_period,
            forecasted_next_period,
            self.periodicity,
            self.nlags
        )
        return forecasted_next_period, acf_values, pacf_values

# =============================================================================
# REFACTORED CALCULATION
# =============================================================================
from utils import read_excel, clean_excel_input
import validations as val

def data_to_numeric(data):
    return [float(d) for d in data]

def get_first_sheet_name(data):
    return list(data.keys())[0]

def get_sheet_values(data, sheet_name):
    return data[sheet_name][0][0]

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

#%%







#%%
periodicity = 4

def w_pd():
    data = pd.read_excel("seasonality_example.xlsx", header=None)
    return (
        data
        .rolling(periodicity)
        .mean()
        .dropna()
        .rolling(2)
        .mean()
        .dropna()
    )
# _ = w_pd()
# print(_)


# serie = [int(n) for n in data[list(data.keys())[0]]]
# n = len(serie)

# results = []
# for i in range(n - periodicity + 1):
#     mean = sum(serie[i:i+periodicity]) / periodicity
#     results.append(mean)















# print(cma_w_pd(data_w_pd))



# num = len(serie)
# half_period = periodicity // 2

# periods = (
#     np.arange(1, periodicity + 1).tolist() * (num // periodicity)
# )[half_period:-half_period]

# irr_seas_comp = (
#     serie[half_period:-half_period].values / cma.values
# )

# seasonal_indices = (
#     pd.DataFrame(
#         {
#             'irr': irr_seas_comp,
#             'period': periods
#         }
#     )
#     .groupby('period')['irr']
#     .mean()
# )

# seasonal_indices =  list(seasonal_indices / seasonal_indices.mean()) * int(num / periodicity)

# past_periods = np.arange(1, len(serie) + 1)
# next_periods = np.arange(
#     past_periods[-1] + 1,
#     past_periods[-1] + 1 + periodicity
# )

# unseasonal_serie = serie.values / seasonal_indices
# X = np.vstack([np.ones_like(past_periods), past_periods]).T
# b = np.linalg.inv(X.T @ X) @ X.T @ unseasonal_serie

# trend_forecast = b[0] + b[1] * next_periods

# forecast = trend_forecast * seasonal_indices[:periodicity]
# forecast = [round(float(v), 2) for v in forecast]