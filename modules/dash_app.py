"""Dash App project file."""

from dash import Dash, Input, Output
from modules.whatsapp import build_layout, ChartGenerator

def init_dash_app(server, whatsapp_service, weekdays_mapper, months_mapper):
    dash_app = Dash(__name__, server=server, url_base_pathname='/dashboard/')
    dash_app.layout = build_layout(whatsapp_service.current_data)

    @dash_app.callback(
        [Output('general-charts', 'children'),
         Output('hour-chart', 'figure'),
         Output('dow-chart', 'figure'),
         Output('dom-chart', 'figure'),
         Output('month-chart', 'figure'),
         Output('sentiment-analysis', 'figure'),
         Output('wordcloud', 'src')],
        [Input('issuer-dropdown', 'value')]
    )
    def update_charts(selected_issuer: str):
        charts = ChartGenerator.generate_all_charts(
            whatsapp_service.current_data,
            selected_issuer,
            weekdays_mapper=weekdays_mapper,
            months_mapper=months_mapper
        )
        return tuple(charts.values())

    return dash_app