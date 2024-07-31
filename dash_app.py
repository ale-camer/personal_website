import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from flask import Flask
import os
import seaborn as sns
from modules.whatsapp import text_normalizer, sentiment_analysis, generate_wordcloud

# Define la aplicación Dash
server = Flask(__name__)
app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Variable global para el DataFrame
data = pd.DataFrame()

def load_data():
    """Carga el archivo CSV si está disponible y muestra mensajes de depuración."""
    global data
    file_path = os.path.join(os.getcwd(), 'static', 'whatsapp', 'data.csv')  # Usa ruta absoluta
    if os.path.exists(file_path):
        print("Archivo CSV encontrado. Cargando datos...")
        data = pd.read_csv(file_path)
        print(f"Datos cargados: {data.head()}")
    else:
        print("Archivo CSV no encontrado.")
        data = pd.DataFrame()  # DataFrame vacío si el archivo no está disponible

# Llama a la función `load_data` para asegurarse de que `df` esté disponible
load_data()
print(data.shape)
print(data.iloc[0])

df = data.groupby(['ISSUER', 'HOUR', 'dow', 'dom', 'month'])['MESSAGE'].count().reset_index()
df_ = data.groupby(['HOUR', 'dow', 'dom', 'month'])['MESSAGE'].count().reset_index()
df_['ISSUER'] = 'GENERAL'
df = pd.concat([df, df_])

# Definición de mappings (asegúrate de definir estos diccionarios adecuadamente)
days_of_the_week = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday',
                    5:'Saturday', 6:'Sunday'}
months = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June',
          7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 
          12:'December'}

def create_dash_layout(df, days_of_the_week, months):
    if df.empty:
        return html.Div([
            html.H1("Cantidad de Mensajes por Emisor"),
            html.P("No data available.")
        ])
    return html.Div([
        html.H1("choose an issuer in the dropdown menu".capitalize()),
        dcc.Dropdown(
            id='issuer-dropdown',
            options=[{'label': issuer, 'value': issuer} for issuer in df['ISSUER'].unique()],
            value=df['ISSUER'].unique()[0] if not df.empty else None
        ),
        html.Div(id='general-charts', style={'width': '100%', 'display': 'inline-block'}),
        html.Div([
            html.Div(dcc.Graph(id='hour-chart'), style={'width': '48%', 'display': 'inline-block'}),
            html.Div(dcc.Graph(id='dow-chart'), style={'width': '48%', 'display': 'inline-block'}),
            html.Div(dcc.Graph(id='dom-chart'), style={'width': '48%', 'display': 'inline-block'}),
            html.Div(dcc.Graph(id='month-chart'), style={'width': '48%', 'display': 'inline-block'}),
            html.Div(dcc.Graph(id='sentiment-analysis'), style={'width': '48%', 'display': 'inline-block'}),
            html.Div(html.Img(id='wordcloud', style={'width': '100%', 'height': 'auto'}), style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'top'})
        ])
    ])

# Define el layout de la aplicación Dash
app.layout = create_dash_layout(df, days_of_the_week, months)

@app.callback(
    Output('general-charts', 'children'),
    Output('hour-chart', 'figure'),
    Output('dow-chart', 'figure'),
    Output('dom-chart', 'figure'),
    Output('month-chart', 'figure'),
    Output('sentiment-analysis', 'figure'),
    Output('wordcloud', 'src'),
    [Input('issuer-dropdown', 'value')]
)
def update_charts(selected_issuer):
    global df  # Asegúrate de que df es global

    if df.empty:
        return (
            html.P("No data available."),
            {'data': [], 'layout': {'title': 'No data available'}},
            {'data': [], 'layout': {'title': 'No data available'}},
            {'data': [], 'layout': {'title': 'No data available'}},
            {'data': [], 'layout': {'title': 'No data available'}},
            {'data': [], 'layout': {'title': 'No sentiment analysis available'}},
            ''
        )

    print(f"Selected issuer: {selected_issuer}")

    # Inicializar filtered_df como un DataFrame vacío
    filtered_df = pd.DataFrame()

    if selected_issuer == "GENERAL":

        filtered_df = df.copy()
        # General charts
        issuer_messages = text_normalizer(data)
        sentiment_fig = sentiment_analysis(data)
        issuer_counts = data['ISSUER'].value_counts().reset_index()
        issuer_counts.columns = ['ISSUER', 'COUNT']
        
        # Gráfico de pie para la cantidad de mensajes por emisor
        pie_chart_messages = dcc.Graph(
            figure={
                'data': [go.Pie(labels=issuer_counts['ISSUER'], values=issuer_counts['COUNT'], hole=.5)],
                'layout': go.Layout(title='proportion of messages by issuer'.title())
            }
        )
        
        # Calcular la suma de la longitud de mensajes por emisor
        message_length_sum = data.groupby('ISSUER')['len_message'].sum().reset_index()
        
        # Gráfico de pie para la longitud de mensajes por emisor
        pie_chart_message_length = dcc.Graph(
            figure={
                'data': [go.Pie(labels=message_length_sum['ISSUER'], values=message_length_sum['len_message'], hole=.5)],
                'layout': go.Layout(title='proportion of words by issuer'.title())
            }
        )
        
        general_charts = html.Div([
            html.Div(pie_chart_messages, style={'width': '48%', 'display': 'inline-block'}),
            html.Div(pie_chart_message_length, style={'width': '48%', 'display': 'inline-block'})
        ], style={'display': 'flex', 'justify-content': 'space-between'})

    else:

        filtered_df = df[df['ISSUER'] == selected_issuer]
        issuer_messages = text_normalizer(data[data['ISSUER'] == selected_issuer])
        sentiment_fig = sentiment_analysis(data, selected_issuer)
        general_charts = ""

    print(f"Filtered DataFrame shape: {filtered_df.shape}")

    bar_colors = sns.color_palette("husl", n_colors=31).as_hex()

    # Gráfico de mensajes por hora
    hour_data = filtered_df.groupby('HOUR')['MESSAGE'].count().reset_index()
    hour_chart = {
        'data': [go.Bar(x=hour_data['HOUR'], y=hour_data['MESSAGE'], marker={'color': bar_colors})],
        'layout': go.Layout(title='amount of messages per hour'.title())
    }
    
    # Gráfico de mensajes por día de la semana
    dow_data = filtered_df.groupby('dow')['MESSAGE'].count().reset_index()
    dow_data['dow'] = dow_data['dow'].map(days_of_the_week)
    dow_chart = {
        'data': [go.Bar(x=dow_data['dow'], y=dow_data['MESSAGE'], marker={'color': bar_colors})],
        'layout': go.Layout(title='amount of messages per day of the week'.title())
    }
    
    # Gráfico de mensajes por día del mes
    dom_data = filtered_df.groupby('dom')['MESSAGE'].count().reset_index()
    dom_chart = {
        'data': [go.Bar(x=dom_data['dom'], y=dom_data['MESSAGE'], marker={'color': bar_colors})],
        'layout': go.Layout(title='amount of messages per day of the month'.title())
    }
    
    # Gráfico de mensajes por mes
    month_data = filtered_df.groupby('month')['MESSAGE'].count().reset_index()
    month_data['month'] = month_data['month'].map(months)
    month_chart = {
        'data': [go.Bar(x=month_data['month'], y=month_data['MESSAGE'], marker={'color': bar_colors})],
        'layout': go.Layout(title='amount of messages per month'.title())
    }
    
    # Generar nube de palabras
    wordcloud_src = generate_wordcloud(issuer_messages)

    return general_charts, hour_chart, dow_chart, dom_chart, month_chart, sentiment_fig, wordcloud_src


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
