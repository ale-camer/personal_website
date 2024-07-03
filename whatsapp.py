# ESTO TIENE QUE IR A PARAR A whatsapp.py

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import re, os
import pandas as pd
import seaborn as sns
import textblob as tb
from wordcloud import WordCloud
import base64
import io
import numpy as np
import nltk
from unidecode import unidecode

def sentiment_analysis(data, selected_issuer=None):
    if selected_issuer and selected_issuer != "GENERAL":
        filtered_data = data[data['ISSUER'] == selected_issuer]
    else:
        filtered_data = data.copy()

    filtered_data['score'] = filtered_data['MESSAGE'].apply(lambda a: tb.TextBlob(a.replace('\n',' ')).sentiment.polarity)
    if filtered_data[filtered_data['score'] != 0].shape[0] == 0:
        return {'data': [], 'layout': go.Layout(title='Sentiment Analysis', showlegend=False)}

    mean_score = round(filtered_data['score'].mean() * 100, 2)

    fig = go.Figure()
    fig.add_trace(go.Violin(
        y=filtered_data['score'],
        box_visible=True,
        line_color='black',
        meanline_visible=True,
        fillcolor='lightseagreen',
        opacity=0.6,
        name='Sentiment Distribution'
    ))

    fig.update_layout(
        title=f'Sentiment Analysis - Mean Polarity: {mean_score:.2f}%',
        xaxis=dict(title='Sentiment Polarity'),
        yaxis=dict(title='Density'),
        template='plotly_white'
    )

    return fig

def generate_wordcloud(text, title='Word Cloud'):
    if not text.strip():
        return {'src': '', 'title': title}

    wordcloud = WordCloud(width=800, height=800, background_color='white').generate(text)
    img = io.BytesIO()
    wordcloud.to_image().save(img, format='PNG')
    img.seek(0)
    encoded_image = base64.b64encode(img.read()).decode('utf-8')

    return {
        'src': f'data:image/png;base64,{encoded_image}',
        'title': title
    }

def whatsapp_data_preprocessing(data):
    pattern = r".*\/.*\/.*,.*:.* - .*"
    general_list = []
    particular_list = []
    
    for i in range(len(data)):
        if re.match(pattern, data[i]):
            if particular_list:
                general_list[-1] = ' '.join(particular_list)
                particular_list = []
            general_list.append(data[i])
        else:
            if not particular_list:
                particular_list.append(data[i-1])
            particular_list.append(data[i])
    
    general_list = pd.DataFrame(general_list, columns=['DATA'])
    
    general_list['DATE'] = general_list['DATA'].apply(lambda x: x.split(',')[0])
    general_list['HOUR'] = general_list['DATA'].apply(lambda x: x.split(',')[1].split('-')[0].strip())
    general_list['ISSUER'] = general_list['DATA'].apply(lambda x: x.split('- ')[1].split(':')[0])
    general_list['MESSAGE'] = general_list['DATA'].apply(lambda x: x.split(': ')[1] if ': ' in x else 0)
    
    general_list = general_list[general_list['MESSAGE'] != 0]
    general_list['MULTIMEDIA'] = general_list['MESSAGE'].apply(lambda a: 1 if 'Multimedia' in a else 0)
    general_list = general_list.loc[general_list['MULTIMEDIA']==0,:].drop(['DATA','MULTIMEDIA'], axis=1)
    
    general_list['DATE'] = pd.to_datetime(general_list['DATE'], dayfirst=True)
    general_list['dow'] = general_list['DATE'].dt.dayofweek
    general_list['dom'] = general_list['DATE'].dt.day
    general_list['HOUR'] = general_list['HOUR'].apply(lambda a: a.split(':')[0]).astype('int')
    general_list['month'] = general_list['DATE'].dt.month
    general_list['len_message'] = general_list['MESSAGE'].apply(lambda a: len(a.split()))
    
    return general_list

def read_whatsapp_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def text_normalizer(data, language='spanish'):
    urlRegex = re.compile('http\S+')
    stopword_list = nltk.corpus.stopwords.words(language)
    text = ' '.join([word for word in ' '.join(data['MESSAGE']).lower().split() if word not in stopword_list])
    text = ' '.join([unidecode(word) for word in text.split()])
    text = ' '.join([word for word in text.split() if not re.match(urlRegex, word)])
    return text

# ESTO TIENE QUE IR A PARAR A app.py

days_of_the_week = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday',
                    5:'Saturday', 6:'Sunday'}
months = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June',
          7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 
          12:'December'}

path = "C:/Users/ale_c/OneDrive/Desktop/GitHub/"
data = read_whatsapp_txt(os.path.join(path, "Chat.txt"))
data = whatsapp_data_preprocessing(data)
df = data.groupby(['ISSUER', 'HOUR', 'dow', 'dom', 'month'])['MESSAGE'].count().reset_index()
df_ = data.groupby(['HOUR', 'dow', 'dom', 'month'])['MESSAGE'].count().reset_index()
df_['ISSUER'] = 'GENERAL'
df = pd.concat([df, df_])

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div([
    html.H1("Cantidad de Mensajes por Emisor"),
    dcc.Dropdown(
        id='issuer-dropdown',
        options=[{'label': issuer, 'value': issuer} for issuer in df['ISSUER'].unique()],
        value=df['ISSUER'].unique()[0]
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
    print(f"Selected issuer: {selected_issuer}")

    if selected_issuer == "GENERAL":
        filtered_df = df
        issuer_messages = text_normalizer(data)
        sentiment_fig = sentiment_analysis(data)
        issuer_counts = data['ISSUER'].value_counts().reset_index()
        issuer_counts.columns = ['ISSUER', 'COUNT']
        
        pie_chart_messages = dcc.Graph(
            figure={
                'data': [go.Pie(labels=issuer_counts['ISSUER'], values=issuer_counts['COUNT'], hole=.5)],
                'layout': go.Layout(title='Proporción de Mensajes por Emisor')
            }
        )
        # general_charts = html.Div([pie_chart])
        
        # Calcular la suma de la longitud de mensajes por emisor
        message_length_sum = data.groupby('ISSUER')['len_message'].sum().reset_index()
        
        # Gráfico de rosca para proporción de longitud de mensajes por emisor
        pie_chart_message_length = dcc.Graph(
            figure={
                'data': [go.Pie(labels=message_length_sum['ISSUER'], values=message_length_sum['len_message'], hole=.5)],
                'layout': go.Layout(title='Proporción de Longitud de Mensajes por Emisor')
            }
        )
        
        general_charts = html.Div([pie_chart_messages, pie_chart_message_length], style={'width': '100%', 'display': 'inline-block'})
    else:
        filtered_df = df[df['ISSUER'] == selected_issuer]
        issuer_messages = text_normalizer(data[data['ISSUER'] == selected_issuer])
        sentiment_fig = sentiment_analysis(data, selected_issuer)
        general_charts = ""

    print(f"Filtered DataFrame shape: {filtered_df.shape}")

    if filtered_df.empty:
        return (
            general_charts,
            {'data': [], 'layout': {'title': f'No data available for {selected_issuer}'}},
            {'data': [], 'layout': {'title': f'No data available for {selected_issuer}'}},
            {'data': [], 'layout': {'title': f'No data available for {selected_issuer}'}},
            {'data': [], 'layout': {'title': f'No data available for {selected_issuer}'}},
            {'data': [], 'layout': {'title': f'No sentiment analysis available for {selected_issuer}'}},
            ''
        )

    hour_data = filtered_df.groupby('HOUR')['MESSAGE'].sum().reset_index()
    dow_data = filtered_df.groupby('dow')['MESSAGE'].sum().reset_index()
    dow_data['dow'] = dow_data['dow'].map(days_of_the_week)
    dom_data = filtered_df.groupby('dom')['MESSAGE'].sum().reset_index()
    month_data = filtered_df.groupby('month')['MESSAGE'].sum().reset_index()
    month_data['month'] = month_data['month'].map(months)
    wordcloud_src = generate_wordcloud(issuer_messages)

    num_colors = len(dom_data)
    bar_colors = sns.color_palette("husl", n_colors=num_colors).as_hex()

    return (
        general_charts,
        {'data': [go.Bar(x=hour_data['HOUR'], y=hour_data['MESSAGE'], name=selected_issuer, marker={'color': bar_colors})], 'layout': {'title': f'Cantidad de Mensajes por Hora para {selected_issuer}', 'xaxis': {'title': 'Hora'}, 'yaxis': {'title': 'Cantidad de Mensajes'}}},
        {'data': [go.Bar(x=dow_data['dow'], y=dow_data['MESSAGE'], name=selected_issuer, marker={'color': bar_colors})], 'layout': {'title': f'Cantidad de Mensajes por Día de la Semana para {selected_issuer}', 'xaxis': {'title': 'Día de la Semana', 'categoryorder': 'array', 'categoryarray': list(days_of_the_week.values())}, 'yaxis': {'title': 'Cantidad de Mensajes'}}},
        {'data': [go.Bar(x=dom_data['dom'], y=dom_data['MESSAGE'], name=selected_issuer, marker={'color': bar_colors})], 'layout': {'title': f'Cantidad de Mensajes por Día del Mes para {selected_issuer}', 'xaxis': {'title': 'Día del Mes'}, 'yaxis': {'title': 'Cantidad de Mensajes'}}},
        {'data': [go.Bar(x=month_data['month'], y=month_data['MESSAGE'], name=selected_issuer, marker={'color': bar_colors})], 'layout': {'title': f'Cantidad de Mensajes por Mes para {selected_issuer}', 'xaxis': {'title': 'Mes', 'categoryorder': 'array', 'categoryarray': list(months.values())}, 'yaxis': {'title': 'Cantidad de Mensajes'}}},
        sentiment_fig,
        wordcloud_src['src']
    )

if __name__ == '__main__':
    app.run_server(debug=True, port=8060)
