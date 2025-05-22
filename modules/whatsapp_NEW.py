"""
Contain functions for WhatsApp functionality.
"""

import io, re, nltk, base64
import pandas as pd
import textblob as tb
from unidecode import unidecode

from dash import dcc, html
from wordcloud import WordCloud
import plotly.graph_objects as go

MESSAGE = 'MESSAGE'
COLS_TO_GROUP = ['HOUR', 'dow', 'dom', 'month']
 
def process_whatsapp_file(file):
    content = _parse_whatsapp_file(file)
    df = _agg_message_counts(content)
    return df, content
  
def _agg_message_counts(df: pd.DataFrame) -> pd.DataFrame: 
    group_and_count = lambda cols: df.groupby(cols)[MESSAGE].count().reset_index()
    return (
        pd.concat(
          [
            group_and_count(['ISSUER'] + COLS_TO_GROUP),
            group_and_count(COLS_TO_GROUP).assign(ISSUER='GENERAL')
          ]
        )
    )

def _parse_whatsapp_file(file: str) -> pd.DataFrame:
    chat = file.read().decode('utf-8').splitlines()
    messages = _split_multiline_messages(chat)
    return _parse_chat_messages(messages)
  
def _parse_chat_messages(messages: list) -> pd.DataFrame:
    return (
      pd.DataFrame(messages, columns=['RAW_DATA'])
      .loc[lambda df: df['RAW_DATA'].str.contains(': ') & ~df['RAW_DATA'].str.contains('Multimedia')]
      .assign(
          DATE=lambda df: pd.to_datetime(df['RAW_DATA'].str.split(',', expand=True)[0], dayfirst=True),
          HOUR=lambda df: df['RAW_DATA'].str.split(',', expand=True)[1].str.split('-', expand=True)[0].str.strip(),
          ISSUER=lambda df: df['RAW_DATA'].str.split('- ', expand=True)[1].str.split(':', expand=True)[0],
          MESSAGE=lambda df: df['RAW_DATA'].str.split(': ', n=1, expand=True)[1],
      )
      .drop('RAW_DATA', axis=1)
      .assign(
          dow=lambda df: df['DATE'].dt.dayofweek,
          dom=lambda df: df['DATE'].dt.day,
          month=lambda df: df['DATE'].dt.month,
          HOUR=lambda df: df['HOUR'].apply(lambda h: int(h.split(':')[0])),
          len_message=lambda df: df['MESSAGE'].apply(lambda msg: len(msg.split()))
        )
    )

def _split_multiline_messages(message_lines: list, regex_pattern: str = r".*\/.*\/.*,.*:.* - .*") -> list:
    messages = []
    for current_line in message_lines:
        if re.match(regex_pattern, current_line): messages.append(current_line)
        elif messages: messages[-1] += ' ' + current_line
    return messages



def create_dash_layout(df: pd.DataFrame, days_of_the_week: dict, months: dict) -> html.Div:

    if df.empty:
        return html.Div([
            html.H1("Cantidad de Mensajes por Emisor"),
            html.P("No data available.")
        ])
    return html.Div([
        html.H1("choose an issuer".capitalize()),
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
  
def sentiment_analysis(data : pd.DataFrame, selected_issuer : str = None) -> go.Figure:

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

def generate_wordcloud(text : str) -> str:

    wordcloud = WordCloud(width=800, height=400, background_color ='white').generate(text)
    img = io.BytesIO()
    wordcloud.to_image().save(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"

def text_normalizer(data : pd.DataFrame, language : str = 'english') -> str:
    urlRegex = re.compile('http\S+') # URLs
    stopword_list = nltk.corpus.stopwords.words(language) # stopwords
    text = ' '.join([str(word) for word in ' '.join(data['MESSAGE']).lower().split() if word not in stopword_list]) # removing stopwords
    text = ' '.join([unidecode(str(word)) for word in text.split()]) # removing tildas
    text = ' '.join([str(word) for word in text.split() if not re.match(urlRegex, word)]) # removing URLs
    return text