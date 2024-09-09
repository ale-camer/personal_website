# Import necessary libraries
import matplotlib, os
matplotlib.use('Agg')  # Use 'Agg' backend to save plots without displaying them

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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

def generate_plots(
        serie : pd.Series, 
        prediction_last_period : list, 
        prediction_next_period : list, 
        periodicity : int = 4) -> None:
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
    assert isinstance(serie, pd.Series), "The 'serie' must be a Pandas Series"
    assert isinstance(prediction_last_period, list), "The 'prediction_last_period' must be a list"
    assert isinstance(prediction_next_period, list), "The 'prediction_next_period' must be a list"
    assert isinstance(periodicity, int), "The 'periodicity' must be an integer"

    # Create directory if it doesn't exist
    save_dir = 'static/seasonality_prediction'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # Plot original data
    plt.figure(figsize=(10,5))
    sns.lineplot(np.concatenate([
            serie.values, 
            serie[-periodicity:].values]).ravel(), 
        color='red')
    plt.xticks([])
    plt.ylabel("Value".title(), fontsize=15)
    plt.title("Original Data".title(), fontsize=20)
    plt.savefig(os.path.join(save_dir, 'original_data.png'))
    plt.close()

    # Plot last cycle   
    plt.figure(figsize=(10,5))
 
    plt.subplot(1,2,1)
    sns.lineplot(np.concatenate([
            serie.values[:-periodicity], 
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
        serie.values[-periodicity:], 
        color='red', 
        label='Real'.title())
    plt.xticks([])
    plt.ylabel("Value".title(), fontsize=15)
    plt.title("Last Period".title(), fontsize=18)
    plt.suptitle("Last Period Prediction".title(),fontsize=20)
    plt.tight_layout()

    plt.savefig(os.path.join(save_dir, 'all_periods_data.png'))
    plt.close()

    # Plot next cycle
    plt.figure(figsize=(10,5))
    sns.lineplot(
        x = range(len(serie) - 1, len(serie) + len(prediction_next_period)), 
        y = np.concatenate([
                [serie.values[-1]],
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
    plt.savefig(os.path.join(save_dir, 'historic_and_prediction_data.png'))
    plt.close()
