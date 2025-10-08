# =============================================================================
# IMPORTS
# =============================================================================
from dash import Dash, Input, Output
from .visuals import layout, generate_charts

# =============================================================================
# INIT
# =============================================================================
def init_dash(server, whatsapp_service, weekdays_mapper, months_mapper):

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

    def update_charts(selected_issuer: str):
        charts = generate_charts(
            whatsapp_service.current_data,
            selected_issuer,
            weekdays_mapper=weekdays_mapper,
            months_mapper=months_mapper
        )
        return tuple(charts.values())

    return dash_app