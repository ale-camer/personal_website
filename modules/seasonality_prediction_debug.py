# from seasonality_prediction import forecasting
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def forecasting(
        serie : pd.Series, 
        periodicity : int = 4) -> list:
    """
    Function to predict a time series based on its seasonality.

    Args:
    - serie: Time series data as a pandas Series or DataFrame
    - periodicity: Integer representing the number of periods in the seasonal cycle

    Returns:
    - forecast: List of predicted values for the next cycle
    """
    assert isinstance(serie, pd.Series), "The 'serie' must be a Pandas Series"
    assert isinstance(periodicity, int), "The 'periodicity' must be an integer"

    # Check if the length of the series is divisible by the periodicity
    if len(serie) % periodicity == 0:
        pass
    else:
        return print("The length of the serie does not match its periodicity.")
            
    ones = [1] * len(serie)
    pastPeriods = np.arange(1, len(serie) + 1)
    nextPeriod = np.arange(pastPeriods[-1] + 1, pastPeriods[-1] + 1 + periodicity)
    periods = np.arange(1, periodicity + 1, 1).tolist() * int(pastPeriods[-1] / periodicity)
    periods = periods[int(periodicity / 2) : -int(periodicity / 2)]
    
    serie_cma = serie.rolling(periodicity).mean().dropna().rolling(2).mean().dropna()
    print('cma',serie_cma)
    irr_seas_comp = serie[int(periodicity / 2) : -int(periodicity / 2)].values.ravel() / serie_cma.values.ravel()
    seas_index = pd.concat([pd.Series(irr_seas_comp), pd.Series(periods)], axis = 1, keys = ['IRREGULAR_SEASONAL_COMPONENTS', 'PERIOD']).groupby('PERIOD')['IRREGULAR_SEASONAL_COMPONENTS'].mean()
    adj_seas_index = seas_index / np.mean(seas_index.values)
    adj_seas_index = adj_seas_index.tolist() * int(pastPeriods[-1] / periodicity)
    unseas_serie = serie.values.ravel() / adj_seas_index
    X, y = np.array([ones, pastPeriods]).T, unseas_serie # Data separation
    
    # Linear regression to fit unseasonal sales
    b = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y)
    future_unseasonal_serie = b[0] + b[1] * nextPeriod
    forecast = future_unseasonal_serie * adj_seas_index[ : periodicity]
    forecast = [round(float(elem),2) for elem in forecast]

    return forecast

periodicity=4
serie = pd.read_excel("C:/Users/ale_c/OneDrive/Desktop/GitHub/ejemplo.xlsx")
# serie = pd.Series(serie['value'])
col_name = serie.columns[0]

prediction_last_period = forecasting(
    serie[col_name].iloc[:-periodicity], 
    periodicity=periodicity)          

prediction_next_period = forecasting(
    serie[col_name], 
    periodicity=periodicity)

# Plot original data
plt.figure(figsize=(10,5))
sns.lineplot(np.concatenate([serie[col_name].values, serie[col_name][-periodicity:].values]).ravel(), color='red')
plt.xticks([])
plt.ylabel("Value".title(), fontsize=15)
plt.title("Original Data".title(), fontsize=20)
# plt.savefig(os.path.join(save_dir, 'original_data.png'))
plt.show()

# Plot last cycle   
plt.figure(figsize=(10,5))

plt.subplot(1,2,1)
sns.lineplot(np.concatenate([
        serie[col_name].values[:-periodicity], 
        prediction_last_period]),
        color='green', 
    label='Prediction'.title())
sns.lineplot(serie.values.ravel(), color='red', label='Real'.title())
plt.xticks([])
plt.ylabel("Value".title(), fontsize=15)
plt.title("All Periods".title(), fontsize=18)

plt.subplot(1,2,2)
sns.lineplot(
    prediction_last_period, 
    color='green', 
    label='Prediction'.title())
sns.lineplot(
    serie[col_name].values[-periodicity:], 
    color='red', 
    label='Real'.title())
plt.xticks([])
plt.ylabel("Value".title(), fontsize=15)
plt.title("Last Period".title(), fontsize=18)
plt.suptitle("Last Period Prediction".title(),fontsize=20)
plt.tight_layout()

# plt.savefig(os.path.join(save_dir, 'all_periods_data.png'))
plt.show()
'
# Plot next cycle
plt.figure(figsize=(10,5))
sns.lineplot(
    x = range(len(serie) - 1, len(serie) + len(prediction_next_period)), 
    y = np.concatenate([
        serie.values[-1],
        prediction_next_period]), 
    color='green', 
    label='Prediction'.title())
sns.lineplot(
    x = range(len(serie)), 
    y = serie.values.ravel(), 
    color='red', 
    label='Real'.title())
plt.xticks([])
plt.ylabel("Value".title(), fontsize=15)
plt.title("original Data and Next Period Prediction".title(), fontsize=20)
# plt.savefig(os.path.join(save_dir, 'historic_and_prediction_data.png'))
plt.show()
'

