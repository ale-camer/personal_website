"""
Contain functions for World Bank functionality.
"""

# --- Standard library ---
import os
import webbrowser

# --- Third-party ---
import folium
import pandas as pd
import plotly.graph_objects as go
import requests
from branca.colormap import linear

# --- Project/system ---
from modules.utils import reading_json

# --- Constants ---
VALUE_STR = 'value'
DATE_STR = 'date'
COUNTRY_STR = 'country'
ISO_STR = 'ISO_CODE'
HTML_PLOTLY = 'html_plotly'
HTML_FOLIUM = 'html_folium'
TEMPORARY_FILES_FOLDER = 'static/world_bank/'

# --- Configuration file path ---
CONFIG_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'static', 'json', 'config.json'
)

# --- Configuration data loaded from JSON ---
STRINGS_TO_EXCLUDE = reading_json(CONFIG_FILE_PATH)["strings_to_exclude"]

# =============================================================================
# DATA
# =============================================================================
def get_indicator_data(indicator_id : str) -> list | None:
    """
    Fetch data for a specific World Bank indicator for all countries.

    Parameters
    ----------
    indicator_id : str
        The World Bank indicator identifier.

    Returns
    -------
    list or None
        A list of data entries filtered to exclude certain string values and None values,
        or None if the request or parsing fails.
    """
    url = f'https://api.worldbank.org/v2/country/all/indicator/{indicator_id}'
    params = {'format': 'json', DATE_STR: '1960:2023', 'per_page': 20000}
    try:
        data = requests.get(url, params=params).json()
        return [
            entry for entry in data[1]
            if entry[COUNTRY_STR][VALUE_STR] not in STRINGS_TO_EXCLUDE and entry[VALUE_STR] is not None
        ]
    except:
        return None
        
def get_result_data(data: pd.DataFrame, type_selected: str, option_selected: str) -> pd.DataFrame:
    """
    Filter and format World Bank data based on selected type and option.

    Parameters
    ----------
    data : pd.DataFrame
        The input data as a list or DataFrame containing World Bank indicator entries.
    type_selected : str
        The type of filter, typically 'country' or 'date'.
    option_selected : str
        The specific country or date to filter on.

    Returns
    -------
    pd.DataFrame
        A DataFrame filtered by the selected country or date, sorted and deduplicated,
        containing columns ISO code, country name, date, and value.
    """
    filtered_data = [
        entry for entry in data 
        if (entry[COUNTRY_STR][VALUE_STR] if type_selected == COUNTRY_STR else entry[DATE_STR]) == option_selected
    ]
    return (
       pd.DataFrame(
         [(entry['countryiso3code'], entry[COUNTRY_STR][VALUE_STR], entry[DATE_STR], entry[VALUE_STR]) for entry in filtered_data], 
         columns=[ISO_STR, COUNTRY_STR.upper(), DATE_STR.upper(), VALUE_STR.upper()]
       )
      .sort_values(by=[COUNTRY_STR.upper(), DATE_STR.upper()], ascending=[True, False])
      .drop_duplicates()
    )

# =============================================================================
# PLOTS
# =============================================================================
def plot_time_series(df: pd.DataFrame, title: str = '', template: str = 'plotly') -> None:
    """
    Plot a time series graph for the given World Bank data.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing time series data with columns for date and value.
    title : str, optional
        Title of the plot (default is empty string).
    template : str, optional
        Plotly template to use (default is 'plotly').

    Returns
    -------
    None
        The plot is saved as an HTML file and opened in the default web browser.
    """
    df[DATE_STR.upper()] = pd.to_datetime(df[DATE_STR.upper()]).dt.year
    fig = _create_time_series_figure(df, title, template)
    _save_and_open_visualization(fig, f'{TEMPORARY_FILES_FOLDER}ime_series.html', format=HTML_PLOTLY)

def plot_heatmap(df : pd.DataFrame, geojson_path: str) -> None:
    """
    Plot a heatmap on a world map using Folium for the given World Bank data.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing data to plot, including ISO codes and values.
    geojson_path : str
        Path to the GeoJSON file containing country geometries.

    Returns
    -------
    None
        The heatmap is saved as an HTML file and opened in the default web browser.
    """
    geo_df = _heatmap_data(df, geojson_path)
    fig = _create_heatmap_figure(geo_df)
    _save_and_open_visualization(fig, f'{TEMPORARY_FILES_FOLDER}heatmap.html', format=HTML_FOLIUM)

def _create_time_series_figure(df: pd.DataFrame, title: str, template: str) -> go.Figure:
    """
    Create a Plotly figure representing a time series from the data.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing columns for date and value.
    title : str
        Title of the plot.
    template : str
        Plotly template name.

    Returns
    -------
    go.Figure
        The generated Plotly figure.
    """
    fig = go.Figure(
        go.Scatter(x=df[DATE_STR.upper()], y=df[VALUE_STR.upper()], mode='lines+markers', name='Data')
    )
    fig.update_layout(title=title, xaxis_title='Year', yaxis_title=VALUE_STR.title(), template=template)
    return fig

def _create_heatmap_figure(df : pd.DataFrame) -> None:
    """
    Create a Folium heatmap figure from geospatial data.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing country geometries and associated values.

    Returns
    -------
    folium.Map
        A Folium Map object representing the heatmap.
    """
    m = folium.Map(location=[20, 0], zoom_start=2)
    colormap = linear.YlOrRd_09.scale(df[VALUE_STR.upper()].min(), df[VALUE_STR.upper()].max())
    colormap.caption = 'Value by Country'
    for _, row in df.iterrows():
        if pd.notna(row[VALUE_STR.upper()]):
            formatted_value = '{:,}'.format(round(row[VALUE_STR.upper()], 2))
            geo_json = folium.GeoJson(
                row['GEOMETRY'],
                style_function= lambda x, value= row[VALUE_STR.upper()]: {
                    'fillColor': colormap(value),
                    'color': 'black',
                    'weight': 0.5,
                    'fillOpacity': value / df[VALUE_STR.upper()].max()
                }
            )
            geo_json.add_child(folium.Tooltip(f"{row[COUNTRY_STR.upper()]} ({row[DATE_STR.upper()].year}): {formatted_value}"))
            geo_json.add_to(m)
    colormap.add_to(m)
    return m

def _heatmap_data(df: pd.DataFrame, geojson_path: str) -> pd.DataFrame:
    """
    Merge World Bank data with GeoJSON geometries for heatmap plotting.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with World Bank data including ISO codes and dates.
    geojson_path : str
        Path to the GeoJSON file with country geometries.

    Returns
    -------
    pd.DataFrame
        DataFrame merged with geometries, filtered for the most recent date per country.
    """
    return (
        pd.DataFrame(
          reading_json(
            geojson_path
          )
        )
        .merge(
            df
            .loc[
                df
                .groupby(COUNTRY_STR.upper())
                [DATE_STR.upper()]
                .idxmax()
            ]
            .assign(
                DATE=lambda x: pd.to_datetime(x[DATE_STR.upper()])
            ), 
            how='left', 
            on=ISO_STR
        )
      .rename(
        columns = {
          f'{COUNTRY_STR.upper()}_x' : COUNTRY_STR.upper()  
        }  
      )
    )   
  
def _save_and_open_visualization(obj, filepath: str, format: str) -> None:
    """
    Save a plotly or folium visualization object as an HTML file and open it in the web browser.

    Parameters
    ----------
    obj : plotly.graph_objects.Figure or folium.Map
        The visualization object to save.
    filepath : str
        The path where the HTML file will be saved.
    format : str
        Format specifier, either 'html_plotly' or 'html_folium'.

    Raises
    ------
    ValueError
        If an unsupported format string is provided.

    Returns
    -------
    None
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if format == HTML_PLOTLY: obj.write_html(filepath)
    elif format == HTML_FOLIUM: obj.save(filepath)
    else: raise ValueError(f"Format '{format}' not supported")
    webbrowser.open(f'file://{os.path.realpath(filepath)}')