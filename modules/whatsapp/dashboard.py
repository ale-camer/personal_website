# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
from flask import Flask
from dash import Dash, Input, Output

# --- Third-party ---

# --- Project ---
from .visuals import layout, generate_charts
from .core import ChatSession

# =============================================================================
# CORE
# =============================================================================
def init_dash(
        server: Flask, whatsapp_service: ChatSession, 
        weekdays_mapper: dict, months_mapper: dict
    ) -> Dash:

    dash_app = Dash(__name__, server=server, url_base_pathname='/dashboard/')
    dash_app.layout = layout(whatsapp_service.current_data)

    charts = [
        Output('general-charts', 'children'),
        Output('hour-chart', 'figure'),
        Output('dow-chart', 'figure'),
        Output('dom-chart', 'figure'),
        Output('month-chart', 'figure'),
        Output('sentiment-analysis', 'figure'),
        Output('wordcloud', 'src')
    ]
    issuers = [Input('issuer-dropdown', 'value')]
    @dash_app.callback(charts, issuers) # update

    def update_charts(selected_issuer: str) -> tuple:
        charts = generate_charts(
            whatsapp_service.current_data,
            selected_issuer,
            weekdays_mapper=weekdays_mapper,
            months_mapper=months_mapper
        )
        return tuple(charts.values())

    return dash_app