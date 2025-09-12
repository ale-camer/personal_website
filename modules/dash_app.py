"""
cambios a realizar:

    - los objetos dentro del decorador deberian estar fuera del mismo
    - whatsapp_service.current_date es llamado dos veces
    - los mappers van a ser siempre los mismos, deberian ir por defecto
    - el layout se actualiza a partir de los datos nuevos
    - el path es reutilizado en el orquestador
"""

# =============================================================================
# IMPORTS
# =============================================================================
from dash import Dash, Input, Output
from modules.whatsapp import layout, ChartGenerator
from modules.utils import performance_analyzer

# =============================================================================
# INIT
# =============================================================================
def init_dash_app(server, whatsapp_service, weekdays_mapper, months_mapper):
    dash_app = Dash(__name__, server=server, url_base_pathname='/dashboard/') # inicializa dashboard
    dash_app.layout = layout(whatsapp_service.current_data) # define interfaz

    @dash_app.callback( # actualiza graficos
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
        chart_generator = ChartGenerator()
        charts = chart_generator.all_charts(
            whatsapp_service.current_data,
            selected_issuer,
            weekdays_mapper=weekdays_mapper,
            months_mapper=months_mapper
        )
        return tuple(charts.values())

    return dash_app