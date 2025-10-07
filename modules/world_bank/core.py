import requests, json
from datetime import datetime

from modules.common.utils import read_json

def call_api(url: str, params: dict) -> json:
    try:
        return requests.get(url, params=params).json()
    except requests.exceptions.RequestException as e:
        print(f"Connetion error: {e}")

def get_countries(data: list) -> list:
    return [d['name'] for d in data if d.get('region').get('value') != 'Aggregates']

raw_countries = call_api(
    "https://api.worldbank.org/v2/country",
    {"format": "json", "per_page": 500}
)[1]
countries = get_countries(raw_countries)

def download_indicator_data(indicator_id: str) -> list | None:
    url = f"https://api.worldbank.org/v2/country/all/indicator/{indicator_id}"
    params = {"format": "json", "date": f"1960:{datetime.now().year}", "per_page": 20000}
    raw_data = call_api(url, params)[1]
    return [
        entry for entry in raw_data
        if entry.get("value") is not None
        and entry.get("country", {}).get("value") in countries
    ]

def extract_options(data: list, type_selected: str) -> list[str]:
    options = ({
        entry['country']['value'] for entry in data} 
        if type_selected == 'country' 
        else {entry['date'] for entry in data
    })
    return sorted(options, reverse=(type_selected == 'year'))

def filter_data(data: list, type_selected: str, option_selected: str) -> list:

    COUNTRY_STR, DATE_STR, VALUE_STR = "country", "date", "value"

    return [
        {
            "COUNTRY": entry[COUNTRY_STR]["value"],
            "DATE": entry[DATE_STR],
            "VALUE": entry[VALUE_STR]
        }
        for entry in data
        if (
            (entry[COUNTRY_STR]["value"] if type_selected == COUNTRY_STR else entry[DATE_STR])
            == option_selected
        )
    ]

from abc import ABC, abstractmethod
import os
import plotly.graph_objects as go
from branca.colormap import linear
import folium
import pandas as pd

VALUE_STR = 'value'
DATE_STR = 'date'
COUNTRY_STR = 'country'
ISO_STR = 'ISO_CODE'
HTML_PLOTLY = 'html_plotly'
HTML_FOLIUM = 'html_folium'
TEMPORARY_FILES_FOLDER = 'static/world_bank/'

def create_country_iso_map(raw_data: list) -> dict:
    """
    Crea un diccionario que mapea el nombre del país a su código ISO de 3 letras.
    """
    country_map = {}
    for item in raw_data:
        # Extrae la información de forma segura
        country_info = item.get('country')
        iso_code = item.get('countryiso3code')
        
        # Asegúrate de que todos los datos necesarios existen
        if country_info and country_info.get('value') and iso_code:
            country_name = country_info['value']
            # Añade al mapa solo si no ha sido añadido antes
            if country_name not in country_map:
                country_map[country_name] = iso_code
                
    return country_map

class WorldBankPlotter(ABC):

    def __init__(self, temporary_folder: str = TEMPORARY_FILES_FOLDER):
        self.temporary_folder = temporary_folder
        os.makedirs(self.temporary_folder, exist_ok=True)

    @abstractmethod
    def create_figure(self, df, **kwargs):
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

    def plot(self, df, **kwargs) -> str:
        figure = self.create_figure(df, **kwargs)
        filepath = os.path.join(self.temporary_folder, self.get_filename())
        self.save_and_open(figure, filepath)
        return filepath

class TimeSeriesPlotter(WorldBankPlotter):

    def create_figure(self, data_list, **kwargs) -> go.Figure:

        title = kwargs.get('title', '')
        template = kwargs.get('template', 'plotly')

        years = [int(item[DATE_STR.upper()]) for item in data_list]
        values = [item[VALUE_STR.upper()] for item in data_list]

        fig = go.Figure(
            go.Scatter(
                x=years,
                y=values,
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

import folium
from branca.colormap import linear
from datetime import datetime

class HeatmapPlotter(WorldBankPlotter):

    def __init__(self, geojson_path: str, country_iso_map: dict, temporary_folder: str = TEMPORARY_FILES_FOLDER):
        super().__init__(temporary_folder)
        self.geojson_path = geojson_path
        # Acepta el mapa de países en el constructor
        self.country_iso_map = country_iso_map

    def _add_iso_code_to_data(self, data_list: list[dict]) -> list[dict]:
        """
        Función auxiliar para añadir el ISO_CODE a los datos filtrados
        usando el mapa de correspondencia.
        """
        for item in data_list:
            country_name = item.get(COUNTRY_STR.upper())
            iso_code = self.country_iso_map.get(country_name)
            if iso_code:
                item[ISO_STR.upper()] = iso_code
        return data_list

    def _prepare_heatmap_data(self, data_list: list[dict]) -> list[dict]:
        # ¡PRIMER PASO! Re-añadimos el ISO_CODE a los datos.
        data_with_iso = self._add_iso_code_to_data(data_list)

        # 1. El resto de la lógica ahora funciona porque 'ISO_CODE' está presente
        latest_entries = {}
        for item in data_with_iso:
            iso = item.get(ISO_STR.upper())
            if not iso:
                continue
            
            if iso not in latest_entries or item[DATE_STR.upper()] > latest_entries[iso][DATE_STR.upper()]:
                latest_entries[iso] = item

        # El resto de la función no necesita cambios...
        indicator_map = {iso: entry for iso, entry in latest_entries.items()}
        geo_data = read_json(self.geojson_path)
        merged_data = []
        for feature in geo_data:
            iso_code = feature.get(ISO_STR.upper())
            indicator_data = indicator_map.get(iso_code)
            
            combined_item = feature.copy()
            if indicator_data:
                combined_item.update(indicator_data)
            merged_data.append(combined_item)
            
        return merged_data


    def create_figure(self, data_list: list[dict], **kwargs) -> folium.Map:

        geo_data = self._prepare_heatmap_data(data_list)
        m = folium.Map(location=[20, 0], zoom_start=2)

        # Extraer valores para la escala de colores, ignorando nulos
        values = [
            item[VALUE_STR.upper()] for item in geo_data 
            if VALUE_STR.upper() in item and item[VALUE_STR.upper()] is not None
        ]

        if not values: # Si no hay datos, devuelve un mapa vacío
            return m

        min_val, max_val = min(values), max(values)
        colormap = linear.YlOrRd_09.scale(min_val, max_val)
        colormap.caption = 'Value by Country'

        for row in geo_data:
            value = row.get(VALUE_STR.upper())
            if value is not None:
                formatted_value = '{:,}'.format(round(value, 2))
                # Convertir fecha a objeto datetime para poder acceder a .year
                date_obj = datetime.strptime(row[DATE_STR.upper()], '%Y')
                
                geo_json = folium.GeoJson(
                    row['GEOMETRY'],
                    style_function=lambda x, v=value: {
                        'fillColor': colormap(v),
                        'color': 'black',
                        'weight': 0.5,
                        'fillOpacity': (v - min_val) / (max_val - min_val) if max_val > min_val else 0.5
                    }
                )
                geo_json.add_child(
                    folium.Tooltip(
                        f"{row[COUNTRY_STR.upper()]} ({date_obj.year}): {formatted_value}"
                    )
                )
                geo_json.add_to(m)

        colormap.add_to(m)
        return m

    def get_filename(self) -> str:
        return 'heatmap.html'

    def get_format(self) -> str:
        return HTML_FOLIUM

def create_visualization(
        data_list,
        type_selected: str,
        geojson_path: str,
        country_iso_map: dict,
        title: str = '',
        template: str = 'plotly'
    ) -> str:
        if type_selected == 'country':
            plotter = TimeSeriesPlotter()
            return plotter.plot(data_list, title=title, template=template)

        elif type_selected in {'year', 'date'}:
            plotter = HeatmapPlotter(geojson_path, country_iso_map)
            return plotter.plot(data_list)