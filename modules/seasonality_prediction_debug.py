def forecasting(
        serie, 
        periodicity : int = 4) -> list:
    """
    Function to predict a time series based on its seasonality.

    Args:
    - serie: Time series data as a pandas Series or DataFrame
    - periodicity: Integer representing the number of periods in the seasonal cycle

    Returns:
    - forecast: List of predicted values for the next cycle
    """
    # assert isinstance(serie, pd.Series), "The 'serie' must be a Pandas Series"
    assert isinstance(periodicity, int), "The 'periodicity' must be an integer"

    # Check if the length of the series is divisible by the periodicity
    if len(serie) % periodicity == 0:
        pass
    else:
        return print("The length of the serie does not match its periodicity.")
        
    # Constants and initializations
    ones = [1] * len(serie)
    pastPeriods = np.arange(1, len(serie) + 1)
    nextPeriod = np.arange(pastPeriods[-1] + 1, pastPeriods[-1] + 1 + periodicity)
    seasonal_index = []

    # Calculate centered moving average (CMA)
    serie_cma = pd.Series(serie).rolling(periodicity).mean().dropna().rolling(2).mean().dropna()

    # Irregular seasonal component calculation
    if len(serie_cma) == periodicity:
        irr_seas_comp = serie[int(periodicity/2):-int(periodicity/2)][-periodicity:] / serie_cma
    else:
        irr_seas_comp = serie[int(periodicity/2):-int(periodicity/2)][-periodicity*int((len(serie)/periodicity)-1):] / serie_cma
    
    # Seasonal index calculation
    if (len(irr_seas_comp) == periodicity) or (len(irr_seas_comp) == periodicity+1): 
        seasonal_index = irr_seas_comp.copy()
    else: 
        for i in range(periodicity):
            seasonal_index.append((irr_seas_comp[i] + irr_seas_comp[i + int(len(irr_seas_comp)/2)]) / 2)
              
    seasonal_index = np.concatenate([seasonal_index[int(periodicity/2):], seasonal_index[:int(periodicity/2)]]) 
    adjustment = len(seasonal_index) / sum(seasonal_index)
    adj_seas_ind = np.concatenate(np.concatenate([[seasonal_index * adjustment] * int(len(serie)/len(seasonal_index))])) # Adjusted seasonal index
    adj_seas_ind = adj_seas_ind[:len(serie)] # Adjust adj_seas_ind to match the length of serie
    X, y = np.array([ones, pastPeriods]).T, serie / adj_seas_ind # Data separation

    # Linear regression to fit unseasonal sales
    b = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y)
    future_unseasonal_serie = b[0] + b[1] * nextPeriod

    # Multiply unseasonal sales by seasonal index to get forecast
    forecast = []
    for elem in range(len(future_unseasonal_serie)):
        forecast.append(future_unseasonal_serie[elem] * (seasonal_index[elem] * adjustment))
    forecast = [round(float(elem),2) for elem in forecast]

    return forecast

import pandas as pd
import numpy as np
periodicity = 4

serie = pd.read_excel("C:/Users/ale_c/OneDrive/Desktop/GitHub/ejemplo.xlsx")
# forecasting(data)

# Constants and initializations
ones = [1] * len(serie)
pastPeriods = np.arange(1, len(serie) + 1)
nextPeriod = np.arange(pastPeriods[-1] + 1, pastPeriods[-1] + 1 + periodicity)
seasonal_index = []

# Calculate centered moving average (CMA)
serie_cma = serie.rolling(periodicity).mean().dropna().rolling(2).mean().dropna()
irr_seas_comp = serie[int(periodicity / 2) : -int(periodicity / 2)].values.ravel() / serie_cma.values.ravel()


# Seasonal index calculation
if (len(irr_seas_comp) == periodicity) or (len(irr_seas_comp) == periodicity+1): 
    seasonal_index = irr_seas_comp.copy()
else: 
    for i in range(periodicity):
        seasonal_index.append((irr_seas_comp.iloc[i] + irr_seas_comp.iloc[i + int(len(irr_seas_comp)/2)]) / 2)
          
seasonal_index = np.concatenate([seasonal_index[int(periodicity/2):], seasonal_index[:int(periodicity/2)]]) 
adjustment = len(seasonal_index) / sum(seasonal_index)
adj_seas_ind = np.concatenate(np.concatenate([[seasonal_index * adjustment] * int(len(serie)/len(seasonal_index))])) # Adjusted seasonal index
adj_seas_ind = adj_seas_ind[:len(serie)] # Adjust adj_seas_ind to match the length of serie
X, y = np.array([ones, pastPeriods]).T, serie / adj_seas_ind # Data separation

# Linear regression to fit unseasonal sales
b = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y)
future_unseasonal_serie = b[0] + b[1] * nextPeriod

# Multiply unseasonal sales by seasonal index to get forecast
forecast = []
for elem in range(len(future_unseasonal_serie)):
    forecast.append(future_unseasonal_serie[elem] * (seasonal_index[elem] * adjustment))
forecast = [round(float(elem),2) for elem in forecast]
forecast