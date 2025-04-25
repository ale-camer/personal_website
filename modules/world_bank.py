"""
Contain functions for World Bank functionality.
"""

import requests, folium, warnings, os, webbrowser
import pandas as pd
import geopandas as gpd
from branca.colormap import linear
import plotly.graph_objects as go
from modules.utils import reading_json
warnings.filterwarnings("ignore")

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
config_file_path = os.path.join(project_root, 'static', 'json', 'config.json')
strings_to_exclude = reading_json(config_file_path)["strings_to_exclude"]

def get_country_data_for_indicator(indicator_id : str) -> list:
    """
    Fetches country-level data for a specified indicator from the World Bank API.
    
    Parameters:
    indicator_id (str): The ID of the indicator to fetch data for.
    
    Returns:
    list or None: A list of filtered data entries if the request is successful and data is in the expected format, 
    or None if there is an error or unexpected data structure.
    
    This function constructs the API request URL using the provided indicator ID, specifies the desired parameters 
    (data format as JSON, date range from 1960 to 2023, and a large page size to include all data), and sends 
    the request to the World Bank API. If the response is successful (HTTP status code 200) and the data is in 
    the expected format, it filters out entries for excluded countries and entries with None values for the indicator. 
    If the response status code is not 200 or the data structure is not as expected, it prints an error message and 
    returns None.
    """
    assert isinstance(indicator_id, str), "The 'indicator_id' must be a string"

    url = f'https://api.worldbank.org/v2/country/all/indicator/{indicator_id}'
    params = {
        'format': 'json',
        'date': '1960:2023',
        'per_page': 20000
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        # Check if the response is in the expected format and filter out excluded countries and None values
        if isinstance(data, list) and len(data) > 1 and 'country' in data[1][0]:
            filtered_data = [
                entry for entry in data[1]
                if entry['country']['value'] not in strings_to_exclude and entry['value'] is not None
            ]
            return filtered_data
        else:
            print(f'\nError {indicator_id}: Unexpected data structure')
            return None
    else:
        print(f'\nError {indicator_id}: {response.status_code}')
        return None

def plot_time_series(df : pd.DataFrame, title : str = '', template : str = 'plotly') -> None:
    """
    Plots time series data using Plotly and saves the plot as an interactive HTML file.
    
    Parameters:
    df (pandas.DataFrame): The DataFrame containing the time series data with columns 'DATE' and 'VALUE'.
    title (str, optional): The title of the plot. Default is an empty string.
    template (str, optional): The Plotly template to use for the plot. Default is 'plotly'.
    
    This function converts the 'DATE' column in the DataFrame to datetime format and extracts the year. 
    It then creates a Plotly figure with a time series plot (lines and markers) using the 'DATE' and 'VALUE' 
    columns from the DataFrame. The plot is customized with a title and axis labels. The resulting plot is saved 
    as an HTML file in the 'downloads' folder and opened in the default web browser.
    """
    assert isinstance(df, pd.DataFrame), "The 'df' must be a Pandas DataFrame"
    assert isinstance(title, str), "The 'title' must be a string"
    assert isinstance(template, str), "The 'template' must be a string"

    df['DATE'] = pd.to_datetime(df['DATE']) # data
    df['DATE'] = df['DATE'].dt.year
    
    fig = go.Figure() # graph
    fig.add_trace(go.Scatter(x=df['DATE'], y=df['VALUE'], mode='lines+markers', name='Data'))
    fig.update_layout(
        title=title,
        xaxis_title='Year',
        yaxis_title='Value',
        template=template
    )
    
    downloads_folder = 'static/world_bank/' # saving and printing
    if not os.path.exists(downloads_folder):
        os.makedirs(downloads_folder)
    temp_html_path = os.path.join(downloads_folder, 'time_series.html')
    fig.write_html(temp_html_path)
    webbrowser.open('file://' + os.path.realpath(temp_html_path))

def plot_heatmap(df : pd.DataFrame) -> None:
    """
    Plots a heatmap using Folium and GeoPandas, and saves the map as an interactive HTML file.
    
    Parameters:
    df (pandas.DataFrame): The DataFrame containing the data with columns 'COUNTRY', 'DATE', 'ISO_CODE', and 'VALUE'.
    
    This function filters the DataFrame to include only the latest data for each country. It loads the world shapefile 
    from GeoPandas and ensures the country names are in English. The shapefile is merged with the DataFrame's data 
    on country ISO codes. A base Folium map is created and country polygons are added with colors based on data values. 
    A colormap is created and added to the map, which is then saved as an HTML file in the 'downloads' folder and 
    opened in the default web browser.
    """
    assert isinstance(df, pd.DataFrame), "The 'df' must be a Pandas DataFrame"

    df = df.loc[df.groupby('COUNTRY')['DATE'].idxmax()] # data
    df['DATE'] = pd.to_datetime(df['DATE'])
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world = world[['iso_a3', 'geometry', 'name']]
    world = world.merge(df, how='left', left_on='iso_a3', right_on='ISO_CODE')
    
    m = folium.Map(location=[20, 0], zoom_start=2) # map
    colormap = linear.YlOrRd_09.scale(df['VALUE'].min(), df['VALUE'].max())
    colormap.caption = 'Value by Country'
    for _, row in world.iterrows(): # adding countries polygons to map
        if pd.notna(row['VALUE']):
            formatted_value = '{:,}'.format(round(row['VALUE'], 2))
            geo_json = folium.GeoJson(
                row['geometry'],
                style_function=lambda x, value=row['VALUE']: {
                    'fillColor': colormap(value),
                    'color': 'black',
                    'weight': 0.5,
                    'fillOpacity': value / df['VALUE'].max()
                }
            )
            geo_json.add_child(folium.Tooltip(f"{row['name']} ({row['DATE'].year}): {formatted_value}"))
            geo_json.add_to(m)
    colormap.add_to(m)
    
    downloads_folder = 'static/world_bank/' # saving and printing
    if not os.path.exists(downloads_folder):
        os.makedirs(downloads_folder)
    temp_html_path = os.path.join(downloads_folder, 'heatmap.html')
    m.save(temp_html_path)
    webbrowser.open('file://' + os.path.realpath(temp_html_path))
