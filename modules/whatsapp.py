"""
Contain functions for WhatsApp functionality.
"""

from dataclasses import dataclass

import io, re, nltk, base64
import pandas as pd
import textblob as tb
from unidecode import unidecode

from dash import dcc, html
import seaborn as sns
from wordcloud import WordCloud
import plotly.graph_objects as go

MESSAGE = 'MESSAGE'
COLS_TO_GROUP = ['HOUR', 'dow', 'dom', 'month']
  
@dataclass
class WhatsAppData:
    df: pd.DataFrame
    content: pd.DataFrame
    language: str

class WhatsAppService:
    
    def __init__(self):
        self.current_data = None
    
    def process_file(self, file, language: str) -> WhatsAppData:
        df, content = process_whatsapp_file(file)
        self.current_data = WhatsAppData(df=df, content=content, language=language)
        return self.current_data
    
    def get_filtered_data(self, issuer: str) -> tuple:
        is_general = issuer == "GENERAL"
        
        if is_general:
            filtered_df = self.current_data.df.copy()
            issuer_filter = slice(None)
        else:
            filtered_df = self.current_data.df[
                self.current_data.df['ISSUER'] == issuer
            ]
            issuer_filter = self.current_data.content['ISSUER'] == issuer
        
        issuer_messages = text_normalizer(
            self.current_data.content[issuer_filter], 
            language=self.current_data.language
        )
        
        return filtered_df, issuer_messages, is_general

class ChartGenerator:
    
    @staticmethod
    def generate_all_charts(
            whatsapp_data: WhatsAppData, 
            issuer: str, 
            weekdays_mapper: dict,
            months_mapper: dict
        ) -> dict:
        
        service = WhatsAppService()
        service.current_data = whatsapp_data
        filtered_df, issuer_messages, is_general = service.get_filtered_data(issuer)
        
        return {
            'general_charts': (
                create_general_charts(whatsapp_data.content) 
                if is_general else ""
            ),
            'hour_chart': create_bar_chart(
                filtered_df, 'HOUR', 'amount of messages per hour'
            ),
            'dow_chart': create_bar_chart(
                filtered_df, 'dow', 'amount of messages per day of the week', weekdays_mapper
            ),
            'dom_chart': create_bar_chart(
                filtered_df, 'dom', 'amount of messages per day of the month'
            ),
            'month_chart': create_bar_chart(
                filtered_df, 'month', 'amount of messages per month', months_mapper
            ),
            'sentiment_chart': sentiment_analysis(
                whatsapp_data.content, None if is_general else issuer
            ),
            'wordcloud': generate_wordcloud(issuer_messages)
        }
      
def create_general_charts(df):
  
  issuer_counts = df['ISSUER'].value_counts().reset_index().rename(columns={'count': 'COUNT'})
  message_length_sum = df.groupby('ISSUER')['len_message'].sum().reset_index()

  return html.Div(
      [
          html.Div(
              _create_pie_chart(
                  issuer_counts['ISSUER'], 
                  issuer_counts['COUNT'], 
                  'proportion of messages by issuer'
              ), 
              style={
                  'width': '48%', 'display': 'inline-block'
                  }
              ),
          html.Div(
              _create_pie_chart(
                  message_length_sum['ISSUER'], 
                  message_length_sum['len_message'], 
                  'proportion of words by issuer'
              ), 
              style={
                   'width': '48%', 'display': 'inline-block'
                   }
              )
        ], 
      style={
          'display': 'flex', 'justify-content': 'space-between'
          }
      )

def _create_pie_chart(labels, values, title):
    return dcc.Graph(
        figure={
            'data': [go.Pie(labels=labels, values=values, hole=.5)],
            'layout': go.Layout(title=title.title())
        }
    )
  
def create_bar_chart(df, group_col, title, mapper=None, color_palette: str = "husl"):
    bar_colors = sns.color_palette(color_palette, n_colors=31).as_hex()
    data = df.groupby(group_col)['MESSAGE'].count().reset_index()
    if mapper:
        data[group_col] = data[group_col].map(mapper)
    return {
        'data': [go.Bar(x=data[group_col], y=data['MESSAGE'], marker={'color': bar_colors})],
        'layout': go.Layout(title=title.title())
    }
  
  
def build_layout(df: pd.DataFrame = None) -> html.Div:
    if df is None or df.empty:
        return html.Div([
            html.H1("Dashboard will be displayed after data upload.".capitalize()),
            html.P("Please upload a file to view the dashboard.".capitalize()),
            dcc.Dropdown(id='issuer-dropdown', options=[], value=None),
            html.Div(id='general-charts', style={'width': '100%', 'display': 'inline-block'}),
            html.Div([
                dcc.Graph(id='hour-chart'),
                dcc.Graph(id='dow-chart'),
                dcc.Graph(id='dom-chart'),
                dcc.Graph(id='month-chart'),
                dcc.Graph(id='sentiment-analysis'),
                html.Img(id='wordcloud', style={'width': '100%', 'height': 'auto'})
            ])
        ])

    return html.Div([
        html.H1("Choose an issuer".capitalize()),
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