# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import os
from abc import ABC, abstractmethod

# --- Third-party ---
import folium
import plotly.graph_objects as go
from branca.colormap import linear

# --- Project ---
from modules.common.utils import read_json

# =============================================================================
# CORE
# =============================================================================
class WorldBankPlotter(ABC):
    def __init__(self, temporary_folder: str = 'static/world_bank/'):
        self.temporary_folder = temporary_folder
        os.makedirs(self.temporary_folder, exist_ok=True)

    @abstractmethod
    def create_figure(self, data: list[dict], **kwargs):
        pass

    @abstractmethod
    def get_filename(self) -> str:
        pass

    @abstractmethod
    def save_figure(self, figure, filepath: str) -> None:
        pass

    def plot(self, data: list, **kwargs) -> str:
        filename = self.get_filename()
        full_filepath = os.path.join(self.temporary_folder, filename)
        figure = self.create_figure(data, **kwargs)
        self.save_figure(figure, full_filepath)
        return os.path.join(os.path.basename(self.temporary_folder), filename).replace(os.sep, '/')

class TimeSeriesPlotter(WorldBankPlotter):
    def create_figure(self, data: list, **kwargs) -> go.Figure:
        fig = go.Figure(go.Scatter(
            x=[int(d['DATE']) for d in data], 
            y=[d['VALUE'] for d in data], 
            mode='lines+markers'
        ))
        fig.update_layout(
            title=kwargs.get('title', ''), xaxis_title='Year',
            yaxis_title='Value', template=kwargs.get('template', 'plotly')
        )
        return fig

    def save_figure(self, figure, filepath: str) -> None:
        figure.write_html(filepath)

    def get_filename(self) -> str:
        return 'time_series.html'

class HeatmapPlotter(WorldBankPlotter):
    def __init__(self, geofile: str):
        super().__init__()
        self.geofile = geofile

    def _prepare_heatmap_data(self, data: list[dict]) -> list[dict]:
        def get_latest(data: list[dict]) -> dict:
            return {
                iso: max(
                    (item for item in data if item.get('ISO_CODE') == iso),
                    key=lambda x: x['DATE']
                )
                for iso in {item.get('ISO_CODE') for item in data if item.get('ISO_CODE')}
            }

        def merge_data(geo_data: list[dict], latest_entries: dict) -> list[dict]:
            return [
                {**feature, **latest_entries.get(feature.get('ISO_CODE'), {})}
                for feature in geo_data
            ]

        latest_entries, geo_data = get_latest(data), read_json(self.geofile)
        return merge_data(geo_data, latest_entries)

    def create_figure(self, data: list[dict], **kwargs) -> folium.Map:
        geo_data = self._prepare_heatmap_data(data)
        values = [g['VALUE'] for g in geo_data if 'VALUE' in g and g['VALUE'] is not None]
        min_val, max_val = min(values), max(values)
        
        m = folium.Map(location=[20, 0], zoom_start=2)
        colormap = linear.YlOrRd_09.scale(min_val, max_val if max_val > min_val else min_val + 1)
        colormap.caption = kwargs.get('title')

        for row in geo_data:
            value = row.get('VALUE')
            if value is not None:
                geo_json = folium.GeoJson(
                    row['GEOMETRY'],
                    style_function = lambda x, v = value: {
                        'fillColor': colormap(v), 'color': 'black', 'weight': 0.5,
                        'fillOpacity': (v - min_val) / (max_val - min_val) if max_val > min_val else 0.5
                })
                tag = f"{row['COUNTRY']} ({int(row['DATE'])}): {round(row['VALUE'], 2):,}"
                geo_json.add_child(folium.Tooltip(tag))
                geo_json.add_to(m)
        colormap.add_to(m)
        return m

    def save_figure(self, figure, filepath: str) -> None:
        figure.save(filepath)

    def get_filename(self) -> str:
        return 'heatmap.html'