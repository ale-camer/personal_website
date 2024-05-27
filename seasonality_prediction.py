import matplotlib
matplotlib.use('Agg')

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def forecasting(serie, periodicity=4):
    """
    The purpose of this function is to predict a time series based only on its seasonality.
    Therefore, the modulus between the length of the serie and its periodicity must be zero.

    The following are examples of the different periodicities that can be used:

    - 2: biannual
    - 4: quarterly
    - 6: bimonthly
    - 12: monthly
    - 52: weekly
    - 365: daily    
    """
    if len(serie) % periodicity == 0:
        pass
    else:
        return print("The length of the serie does not match its periodicity.")
        
    # Constants
    ones = [1] * len(serie)
    pastPeriods = np.arange(1, len(serie) + 1)
    nextPeriod = np.arange(pastPeriods[-1] + 1, pastPeriods[-1] + 1 + periodicity)
    seasonal_index = []

    serie_cma = serie.rolling(periodicity).mean().dropna().rolling(2).mean().dropna() # Rolling mean
    
    # Irregular seasonal component
    if len(serie_cma) == periodicity:
        irr_seas_comp = serie[int(periodicity/2):-int(periodicity/2)][-periodicity:].values / serie_cma.values
    else:
        irr_seas_comp = serie[int(periodicity/2):-int(periodicity/2)][-periodicity*int((len(serie)/periodicity)-1):].values / serie_cma.values
    
    # Seasonal index
    if (len(irr_seas_comp) == periodicity) or (len(irr_seas_comp) == periodicity+1): 
        seasonal_index = irr_seas_comp.copy()
    else: 
        for i in range(periodicity):
            seasonal_index.append((irr_seas_comp[i] + irr_seas_comp[i + int(len(irr_seas_comp)/2)]) / 2)
              
    seasonal_index = np.concatenate([seasonal_index[int(periodicity/2):], seasonal_index[:int(periodicity/2)]]) 
    adjustment = len(seasonal_index) / sum(seasonal_index)
    adj_seas_ind = np.concatenate(np.concatenate([[seasonal_index * adjustment] * int(len(serie)/len(seasonal_index))])) # Adjusted seasonal index
    adj_seas_ind = adj_seas_ind[:len(serie)] # Ajuste para que adj_seas_ind tenga la misma longitud que serie
    X, y = np.array([ones, pastPeriods]).T, serie / adj_seas_ind # Data separation

    b = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y) # Linear regression
    future_unseasonal_serie = b[0] + b[1] * nextPeriod # Unseasonal sales
    forecast = [] # Forecast
    for elem in range(len(future_unseasonal_serie)):
        forecast.append(future_unseasonal_serie[elem] * (seasonal_index[elem] * adjustment))
    forecast = [round(float(elem),2) for elem in forecast]

    return forecast

def generate_plots(serie, prediction_next_period, periodicity=4):
    plt.figure(figsize=(10,5))

    # Plot original data
    sns.lineplot(np.concatenate([serie.values, serie[-periodicity:].values]).ravel())
    plt.xticks([])
    plt.ylabel("Value".title(), fontsize=15)
    plt.title("Data Provided".title(), fontsize=20)
    plt.savefig('static/temp_images/original_data.png')
    plt.close()

    # Plot all periods data
    plt.figure(figsize=(10,5))
    sns.lineplot(np.concatenate([serie.values.ravel(), prediction_next_period]), color='green', label='Prediction'.title())
    sns.lineplot(np.concatenate([serie.values, serie[-periodicity:].values]).ravel(), color='red', label='Real'.title())
    plt.xticks([])
    plt.ylabel("Value".title(), fontsize=15)
    plt.title("All Periods Data".title(), fontsize=18)
    plt.savefig('static/temp_images/all_periods_data.png')
    plt.close()

    # Plot current period data
    plt.figure(figsize=(10,5))
    sns.lineplot(x=range(len(serie), len(serie) + len(prediction_next_period)), y=prediction_next_period, color='red')
    sns.lineplot(x=range(len(serie)), y=serie.values.ravel(), color='blue')
    plt.xticks([])
    plt.ylabel("Value".title(), fontsize=15)
    plt.title("Historic and Prediction Data".title(), fontsize=20)
    plt.savefig('static/temp_images/historic_and_prediction_data.png')
    plt.close()

