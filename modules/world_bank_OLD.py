"""Contain classes for World Bank functionality."""

# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import os
from abc import ABC, abstractmethod

# --- Third-party ---
import folium
import pandas as pd
import plotly.graph_objects as go
import requests
from branca.colormap import linear

# --- Project/system ---
from modules.utils_OLD import read_json, get_valid_countries

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

# =============================================================================
# DATA
# =============================================================================
class WorldBankDataHandler:

    VALID_COUNTRIES = get_valid_countries()

    def indicator(self, indicator_id: str) -> list | None:

        url = f'https://api.worldbank.org/v2/country/all/indicator/{indicator_id}'
        params = {'format': 'json', DATE_STR: f'1960:{pd.to_datetime("today").year}', 'per_page': 20000}
        
        response = requests.get(url, params=params)
        data = response.json()

        return [
            entry for entry in data[1]
            if entry.get(VALUE_STR) is not None
            and entry.get(COUNTRY_STR, {}).get(VALUE_STR) in self.VALID_COUNTRIES
        ]

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

    def save_and_open(self, figure, filepath: str) -> None:
        if self.get_format() == HTML_PLOTLY:
            figure.write_html(filepath)
        elif self.get_format() == HTML_FOLIUM:
            figure.save(filepath)
        else:
            raise ValueError(f"Format '{self.get_format()}' not supported")

    def plot(self, df: pd.DataFrame, **kwargs) -> str: # Asegúrate que devuelve str
        figure = self.create_figure(df, **kwargs)
        filepath = os.path.join(self.temporary_folder, self.get_filename())
        self.save_and_open(figure, filepath)
        return filepath

class TimeSeriesPlotter(WorldBankPlotter):

    def create_figure(self, df: pd.DataFrame, **kwargs) -> go.Figure:

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

    def indicator(self, indicator_id: str) -> list | None:
        return self.data_handler.indicator(indicator_id)

    def results(self, data: list, type_selected: str, option_selected: str) -> pd.DataFrame:
        return self.data_handler.results(data, type_selected, option_selected)

    def plot_time_series(self, df: pd.DataFrame, title: str = '', template: str = 'plotly') -> str:
        return self.time_series_plotter.plot(df, title=title, template=template)

    def plot_heatmap(self, df: pd.DataFrame) -> str:
        return self.heatmap_plotter.plot(df)

    def create_visualization(self, df: pd.DataFrame, type_selected: str, **kwargs) -> str:
        if type_selected == 'country':
            return self.plot_time_series(df, **kwargs)
        elif type_selected == 'year':
            return self.plot_heatmap(df)
        else:
            raise ValueError(f"Visualization type '{type_selected}' not supported")