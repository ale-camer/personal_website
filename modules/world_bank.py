"""Contain classes for World Bank functionality."""

# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import os
import webbrowser
from abc import ABC, abstractmethod

# --- Third-party ---
import folium
import pandas as pd
import plotly.graph_objects as go
import requests
from branca.colormap import linear

# --- Project/system ---
from modules.utils import read_json

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# =============================================================================
# CONSTANTS
# =============================================================================
VALUE_STR = 'value'
DATE_STR = 'date'
COUNTRY_STR = 'country'
ISO_STR = 'ISO_CODE'
HTML_PLOTLY = 'html_plotly'
HTML_FOLIUM = 'html_folium'
TEMPORARY_FILES_FOLDER = 'static/world_bank/'

# --- Configuration file path ---
CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'static', 'json', 'config.json'
)
STRINGS_TO_EXCLUDE = read_json(CONFIG_PATH)["strings_to_exclude"]

# =============================================================================
# DATA
# =============================================================================
class WorldBankDataHandler:
    
    def __init__(self):
        self.strings_to_exclude = STRINGS_TO_EXCLUDE
    
    def indicator(self, indicator_id: str) -> list | None:
    
        url = f'https://api.worldbank.org/v2/country/all/indicator/{indicator_id}'
        params = {'format': 'json', DATE_STR: '1960:2023', 'per_page': 20000}
        try:
            response = requests.get(url, params=params)
            data = response.json()
            return [
                entry for entry in data[1]
                if entry[COUNTRY_STR][VALUE_STR] not in self.strings_to_exclude 
                and entry[VALUE_STR] is not None
            ]
        except Exception as e:
            print(f"Error fetching data for indicator {indicator_id}: {e}")
            return None
    
    def results(self, data: list, type_selected: str, option_selected: str) -> pd.DataFrame:
        filtered_data = [
            entry for entry in data 
            if (entry[COUNTRY_STR][VALUE_STR] if type_selected == COUNTRY_STR else entry[DATE_STR]) == option_selected
        ]
        return (
            pd.DataFrame(
                [(entry['countryiso3code'], entry[COUNTRY_STR][VALUE_STR], 
                  entry[DATE_STR], entry[VALUE_STR]) for entry in filtered_data], 
                columns=[ISO_STR, COUNTRY_STR.upper(), DATE_STR.upper(), VALUE_STR.upper()]
            )
            .sort_values(by=[COUNTRY_STR.upper(), DATE_STR.upper()], ascending=[True, False])
            .drop_duplicates()
        )

# =============================================================================
# PLOTS
# =============================================================================
class WorldBankPlotter(ABC):
    
    def __init__(self, temporary_folder: str = TEMPORARY_FILES_FOLDER):
        self.temporary_folder = temporary_folder
        os.makedirs(self.temporary_folder, exist_ok=True)
    
    @abstractmethod
    def create_figure(self, df: pd.DataFrame, **kwargs):
        pass
    
    @abstractmethod
    def get_filename(self) -> str:
        pass
    
    @abstractmethod
    def get_format(self) -> str:
        pass
    
    # def save_and_open(self, figure, filepath: str) -> None:
        # if self.get_format() == HTML_PLOTLY:
            # figure.write_html(filepath)
        # elif self.get_format() == HTML_FOLIUM:
            # figure.save(filepath)
        # else:
            # raise ValueError(f"Format '{self.get_format()}' not supported")
        # webbrowser.open(f'file://{os.path.realpath(filepath)}')
        
    def save_and_open(self, figure, filepath: str) -> None:
        if self.get_format() == HTML_PLOTLY:
            logging.info(f"Saving Plotly figure to {filepath}")
            figure.write_html(filepath)
        elif self.get_format() == HTML_FOLIUM:
            logging.info(f"Saving Folium map to {filepath}")
            figure.save(filepath)
        else:
            raise ValueError(f"Format '{self.get_format()}' not supported")
        
        full_path = os.path.realpath(filepath)
        logging.info(f"Opening file in browser: file://{full_path}")
        webbrowser.open(f'file://{full_path}')

    
    # def plot(self, df: pd.DataFrame, **kwargs) -> None:
        # figure = self.create_figure(df, **kwargs)
        # filepath = os.path.join(self.temporary_folder, self.get_filename())
        # self.save_and_open(figure, filepath)

    def plot(self, df: pd.DataFrame, **kwargs) -> None:
        logging.info(f"[{self.__class__.__name__}] Creating figure...")
        figure = self.create_figure(df, **kwargs)
        filepath = os.path.join(self.temporary_folder, self.get_filename())
        logging.info(f"[{self.__class__.__name__}] Saving figure to {filepath}...")
        self.save_and_open(figure, filepath)
        logging.info(f"[{self.__class__.__name__}] Plotting complete.")

class TimeSeriesPlotter(WorldBankPlotter):
    
    def create_figure(self, df: pd.DataFrame, **kwargs) -> go.Figure:
        """Create a Plotly time series figure."""
        logging.info("Generating Plotly time series plot...")

        title = kwargs.get('title', '')
        template = kwargs.get('template', 'plotly')
        
        df_copy = df.copy()
        df_copy[DATE_STR.upper()] = pd.to_datetime(df_copy[DATE_STR.upper()]).dt.year
        
        fig = go.Figure(
            go.Scatter(
                x=df_copy[DATE_STR.upper()], 
                y=df_copy[VALUE_STR.upper()], 
                mode='lines+markers', 
                name='Data'
            )
        )
        fig.update_layout(
            title=title, 
            xaxis_title='Year', 
            yaxis_title=VALUE_STR.title(), 
            template=template
        )
        return fig
    
    def get_filename(self) -> str:
        return 'time_series.html'
    
    def get_format(self) -> str:
        return HTML_PLOTLY

class HeatmapPlotter(WorldBankPlotter):
    
    def __init__(self, geojson_path: str, temporary_folder: str = TEMPORARY_FILES_FOLDER):
        super().__init__(temporary_folder)
        self.geojson_path = geojson_path
    
    def create_figure(self, df: pd.DataFrame, **kwargs) -> folium.Map:
        logging.info("Generating Folium heatmap...")

        geo_df = self._prepare_heatmap_data(df)
        
        m = folium.Map(location=[20, 0], zoom_start=2)
        colormap = linear.YlOrRd_09.scale(
            geo_df[VALUE_STR.upper()].min(), 
            geo_df[VALUE_STR.upper()].max()
        )
        colormap.caption = 'Value by Country'
        
        for _, row in geo_df.iterrows():
            if pd.notna(row[VALUE_STR.upper()]):
                formatted_value = '{:,}'.format(round(row[VALUE_STR.upper()], 2))
                geo_json = folium.GeoJson(
                    row['GEOMETRY'],
                    style_function=lambda x, value=row[VALUE_STR.upper()]: {
                        'fillColor': colormap(value),
                        'color': 'black',
                        'weight': 0.5,
                        'fillOpacity': value / geo_df[VALUE_STR.upper()].max()
                    }
                )
                geo_json.add_child(
                    folium.Tooltip(
                        f"{row[COUNTRY_STR.upper()]} ({row[DATE_STR.upper()].year}): {formatted_value}"
                    )
                )
                geo_json.add_to(m)
        
        colormap.add_to(m)
        return m
    
    def _prepare_heatmap_data(self, df: pd.DataFrame) -> pd.DataFrame:
        return (
            pd.DataFrame(read_json(self.geojson_path))
            .merge(
                df.loc[df.groupby(COUNTRY_STR.upper())[DATE_STR.upper()].idxmax()]
                .assign(DATE=lambda x: pd.to_datetime(x[DATE_STR.upper()])), 
                how='left', 
                on=ISO_STR
            )
            .rename(columns={f'{COUNTRY_STR.upper()}_x': COUNTRY_STR.upper()})
        )
    
    def get_filename(self) -> str:
        return 'heatmap.html'
    
    def get_format(self) -> str:
        return HTML_FOLIUM

# =============================================================================
# MAIN
# =============================================================================
class WorldBankModule:
    
    def __init__(self, geojson_path: str):
        self.data_handler = WorldBankDataHandler()
        self.geojson_path = geojson_path
        self.time_series_plotter = TimeSeriesPlotter()
        self.heatmap_plotter = HeatmapPlotter(geojson_path)
    
    def indicator(self, indicator_id: str) -> list:
        return self.data_handler.indicator(indicator_id)
    
    def results(self, data: list, type_selected: str, option_selected: str) -> pd.DataFrame:
        return self.data_handler.results(data, type_selected, option_selected)
    
    def plot_time_series(self, df: pd.DataFrame, title: str = '', template: str = 'plotly') -> None:
        self.time_series_plotter.plot(df, title=title, template=template)
    
    def plot_heatmap(self, df: pd.DataFrame) -> None:
        self.heatmap_plotter.plot(df)
    
    # def create_visualization(self, df: pd.DataFrame, type_selected: str, **kwargs) -> None:
        # if type_selected == 'country':
            # self.plot_time_series(df, **kwargs)
        # elif type_selected == 'year':
            # self.plot_heatmap(df)
        # else:
            # raise ValueError(f"Visualization type '{type_selected}' not supported")
            
    def create_visualization(self, df: pd.DataFrame, type_selected: str, **kwargs) -> None:
        logging.info(f"Creating visualization of type: {type_selected}")
        if type_selected == 'country':
            self.plot_time_series(df, **kwargs)
        elif type_selected == 'year':
            self.plot_heatmap(df)
        else:
            raise ValueError(f"Visualization type '{type_selected}' not supported")
