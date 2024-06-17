# Import necessary libraries
import matplotlib
matplotlib.use('Agg')  # Use 'Agg' backend to save plots without displaying them

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def forecasting(serie, periodicity=4):
    """
    Function to predict a time series based on its seasonality.

    Args:
    - serie: Time series data as a pandas Series or DataFrame
    - periodicity: Integer representing the number of periods in the seasonal cycle

    Returns:
    - forecast: List of predicted values for the next cycle
    """

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
    serie_cma = serie.rolling(periodicity).mean().dropna().rolling(2).mean().dropna()

    # Irregular seasonal component calculation
    if len(serie_cma) == periodicity:
        irr_seas_comp = serie[int(periodicity/2):-int(periodicity/2)][-periodicity:].values / serie_cma.values
    else:
        irr_seas_comp = serie[int(periodicity/2):-int(periodicity/2)][-periodicity*int((len(serie)/periodicity)-1):].values / serie_cma.values
    
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

def generate_plots(serie, prediction_last_period, prediction_next_period, periodicity=4):
    """
    Function to generate and save plots of the original data, last period prediction, and next period prediction.

    Args:
    - serie: Time series data as a pandas DataFrame
    - prediction_last_period: Predicted values for the last period
    - prediction_next_period: Predicted values for the next period
    - periodicity: Integer representing the number of periods in the seasonal cycle

    Returns:
    - Plots saved as PNG files in the 'static/temp_images' directory
    """

    # Plot original data
    plt.figure(figsize=(10,5))
    sns.lineplot(np.concatenate([serie.values, serie[-periodicity:].values]).ravel(), color='red')
    plt.xticks([])
    plt.ylabel("Value".title(), fontsize=15)
    plt.title("Original Data".title(), fontsize=20)
    plt.savefig('static/temp_images/original_data.png')
    plt.close()

    # Plot last cycle
    plt.figure(figsize=(10,5))

    plt.subplot(1,2,1)
    sns.lineplot(np.concatenate([serie.iloc[:-4,:].values.ravel(), prediction_last_period]), color='green', label='Prediction'.title())
    sns.lineplot(serie.values.ravel(), color='red', label='Real'.title())
    plt.xticks([])
    plt.ylabel("Value".title(), fontsize=15)
    plt.title("All Periods".title(), fontsize=18)

    plt.subplot(1,2,2)
    sns.lineplot(prediction_last_period, color='green', label='Prediction'.title())
    sns.lineplot(serie.iloc[-4:,:].values.ravel(), color='red', label='Real'.title())
    plt.xticks([])
    plt.ylabel("Value".title(), fontsize=15)
    plt.title("Last Period".title(), fontsize=18)
    plt.suptitle("Last Period Prediction".title(),fontsize=20)
    plt.tight_layout()

    plt.savefig('static/temp_images/all_periods_data.png')
    plt.close()

    # Plot next cycle
    plt.figure(figsize=(10,5))
    sns.lineplot(x=range(len(serie) - 1, len(serie) + len(prediction_next_period)), y=np.concatenate([serie.iloc[-1].values,prediction_next_period]), color='green', label='Prediction'.title())
    sns.lineplot(x=range(len(serie)), y=serie.values.ravel(), color='red', label='Real'.title())
    plt.xticks([])
    plt.ylabel("Value".title(), fontsize=15)
    plt.title("Data and Next Period Prediction".title(), fontsize=20)
    plt.savefig('static/temp_images/historic_and_prediction_data.png')
    plt.close()
