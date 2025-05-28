"""Contain functions for WhatsApp functionality."""

# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import base64
import io
import re

# --- Third-party ---
import nltk
import pandas as pd
import seaborn as sns
import textblob as tb
from dash import dcc, html
import plotly.graph_objects as go
from wordcloud import WordCloud

# --- Project/system ---
from dataclasses import dataclass
from modules.utils import text_normalizer

# =============================================================================
# DASHBOAR
# =============================================================================
def layout(df: pd.DataFrame = None) -> html.Div:
  
    ISSUER = 'ISSUER'
    GRAPH_STYLE = {'width': '48%', 'display': 'inline-block'}
    
    if df is None or df.empty:
        return html.Div([
            html.H1("Dashboard will be displayed after data upload."),
            html.P("Please upload a file to view the dashboard.")           
        ])

    return html.Div([
        html.H1("Choose an issuer"),
        dcc.Dropdown(
            id='issuer-dropdown',
            options=[{'label': issuer, 'value': issuer} for issuer in df[ISSUER].unique()],
            value=df[ISSUER].unique()[0]
        ),
        html.Div(
            id='general-charts', 
            style={'width': '100%', 'display': 'inline-block'}
        ),
        html.Div([
            html.Div(dcc.Graph(id='hour-chart'), style=GRAPH_STYLE),
            html.Div(dcc.Graph(id='dow-chart'), style=GRAPH_STYLE),
            html.Div(dcc.Graph(id='dom-chart'), style=GRAPH_STYLE),
            html.Div(dcc.Graph(id='month-chart'), style=GRAPH_STYLE),
            html.Div(dcc.Graph(id='sentiment-analysis'), style=GRAPH_STYLE),
            html.Div(html.Img(
                id='wordcloud',
                style={'width': '100%', 'height': 'auto'}), 
            style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'top'})
        ])
    ])
    
# =============================================================================
# MAIN
# =============================================================================
@dataclass
class WhatsAppConfig:
    df: pd.DataFrame
    content: pd.DataFrame
    language: str

class WhatsAppModule:
    
    def __init__(self):
        self.current_data = None
        self.ISSUER = 'ISSUER'
    
    def parse_chat(self, file, language: str) -> WhatsAppConfig:
        parser = WhatsAppParser(file)
        content = parser.parse()
        df = parser.group(content)
        self.current_data = WhatsAppConfig(df=df, content=content, language=language)
        return self.current_data
    
    def filter_chat(self, issuer: str) -> tuple:
        is_general = issuer == 'GENERAL'
        
        if is_general:
            filtered_df = self.current_data.df.copy()
            issuer_filter = slice(None)
        else:
            filtered_df = self.current_data.df[
                self.current_data.df[self.ISSUER] == issuer
            ]
            issuer_filter = self.current_data.content[self.ISSUER] == issuer
                
        filtered_messages = self.current_data.content[issuer_filter]
        combined_text = ' '.join(filtered_messages['MESSAGE'].astype(str))
        
        stopwords = set(nltk.corpus.stopwords.words(self.current_data.language))
        issuer_messages = text_normalizer(
            text=combined_text,
            stopwords=stopwords
        )
      
        return filtered_df, issuer_messages, is_general
      
# =============================================================================
# PARSER
# =============================================================================
class WhatsAppParser:
  
    def __init__(self, file: str):
        self.file = file
        self.COLS_TO_GROUP = ['HOUR', 'dow', 'dom', 'month']
        self.RAW_DATA = 'RAW_DATA'
        self.MESSAGE = 'MESSAGE'
        self.ISSUER = 'ISSUER'
        self.DATE = 'DATE'
        self.HOUR = 'HOUR'
       
    def group(self, df: pd.DataFrame) -> pd.DataFrame:
        group_and_count = lambda cols: df.groupby(cols)[self.MESSAGE].count().reset_index()
        return (
            pd.concat([
                group_and_count([self.ISSUER] + self.COLS_TO_GROUP),
                group_and_count(self.COLS_TO_GROUP).assign(ISSUER='GENERAL')
            ])
        )      
      
    def parse(self) -> pd.DataFrame:
        chat = self._read_file()
        messages = self._split_messages(chat)
        return self._parse_messages(messages)      
      
    def _read_file(self):
        return self.file.read().decode('utf-8').splitlines()
      
    def _split_messages(self, lines: list[str], pattern: str = r".*\/.*\/.*,.*:.* - .*") -> list:
        messages = []
        for current_line in lines:
            if re.match(pattern, current_line): 
                messages.append(current_line)
            elif messages: 
                messages[-1] += ' ' + current_line
        return messages
    
    def _parse_messages(self, messages: list[str]) -> pd.DataFrame:
        return (
            pd.DataFrame(messages, columns=[self.RAW_DATA])
            .loc[lambda df: df[self.RAW_DATA].str.contains(': ') & ~df[self.RAW_DATA].str.contains('Multimedia')]
            .assign(
                DATE=lambda df: pd.to_datetime(df[self.RAW_DATA].str.split(',', expand=True)[0], dayfirst=True),
                HOUR=lambda df: df[self.RAW_DATA].str.split(',', expand=True)[1].str.split('-', expand=True)[0].str.strip(),
                ISSUER=lambda df: df[self.RAW_DATA].str.split('- ', expand=True)[1].str.split(':', expand=True)[0],
                MESSAGE=lambda df: df[self.RAW_DATA].str.split(': ', n=1, expand=True)[1],
            )
            .drop(self.RAW_DATA, axis=1)
            .assign(
                dow=lambda df: df[self.DATE].dt.dayofweek,
                dom=lambda df: df[self.DATE].dt.day,
                month=lambda df: df[self.DATE].dt.month,
                HOUR=lambda df: df[self.HOUR].apply(lambda h: int(h.split(':')[0])),
                len_message=lambda df: df[self.MESSAGE].apply(lambda msg: len(msg.split()))
            )
        )

# =============================================================================
# PLOTTING
# =============================================================================
class ChartGenerator:

    def __init__(self):
        self.LEN_MESSAGE = 'len_message'
        self.DATA = 'data'
        self.LAYOUT = 'layout'
        self.COUNT = 'COUNT'
        self.SCORE = 'score'
        self.ISSUER = 'ISSUER'
        self.MESSAGE = 'MESSAGE'
        self.GENERAL = 'GENERAL'
        self.GRAPH_STYLE = {'width': '48%', 'display': 'inline-block'}
      
    def all_charts(
            self,
            data: WhatsAppConfig, 
            issuer: str, 
            weekdays_mapper: dict[str, str], 
            months_mapper: dict[str, str]
        ) -> dict:    
            
        service = WhatsAppModule()
        service.current_data = data
        df, messages, is_general = service.filter_chat(issuer)
        return {
            'general_charts': (
                self._general_charts(data.content) 
                if is_general else ""
            ),
            'hour_chart': self._bar_chart(
                df, 'HOUR', 'amount of messages per hour'
            ),
            'dow_chart': self._bar_chart(
                df, 'dow', 'amount of messages per day of the week', weekdays_mapper
            ),
            'dom_chart': self._bar_chart(
                df, 'dom', 'amount of messages per day of the month'
            ),
            'month_chart': self._bar_chart(
                df, 'month', 'amount of messages per month', months_mapper
            ),
            'sentiment_chart': self._sentiments(
                data.content, None if is_general else issuer
            ),
            'wordcloud': self._wordcloud(messages)
        }
        
    def _wordcloud(self, text: str) -> str:
        buffer = io.BytesIO()
        WordCloud(width=800, height=400, background_color='white').generate(text).to_image().save(buffer, format='PNG')
        buffer.seek(0)
        return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
    
    def _sentiments(self, data: pd.DataFrame, selected_issuer: str = None) -> go.Figure: 
        df = (
            (data[data[self.ISSUER] == selected_issuer] if selected_issuer and selected_issuer != self.GENERAL else data.copy())
            .assign(SCORE=lambda d: d[self.MESSAGE].apply(lambda a: tb.TextBlob(a.replace('\n', ' ')).sentiment.polarity))
        )
        fig = (
            go.Figure(
                data=[go.Violin(
                    y=df[self.SCORE.upper()],
                    box_visible=True,
                    line_color='black',
                    meanline_visible=True,
                    fillcolor='lightseagreen',
                    opacity=0.6,
                    name='Sentiment Distribution'
                )]
            )
            .update_layout(
                title=f'Sentiment Analysis - Mean Polarity: {round(df[self.SCORE.upper()].mean() * 100, 2):.2f}%',
                xaxis=dict(title='Sentiment Polarity'),
                yaxis=dict(title='Density'),
                template='plotly_white'
            )
        )
        return fig
    
    def _general_charts(self, df: pd.DataFrame) -> html.Div:
        issuer_counts = df[self.ISSUER].value_counts().reset_index().rename(columns={self.COUNT.lower(): self.COUNT})
        message_length_sum = df.groupby(self.ISSUER)[self.LEN_MESSAGE].sum().reset_index()
        return html.Div(
            [
                html.Div(
                    self._pie_chart(
                        issuer_counts[self.ISSUER], 
                        issuer_counts[self.COUNT], 
                        'proportion of messages by issuer'
                    ), style=self.GRAPH_STYLE
                ),
                html.Div(
                    self._pie_chart(
                        message_length_sum[self.ISSUER], 
                        message_length_sum[self.LEN_MESSAGE], 
                        'proportion of words by issuer'
                    ), style=self.GRAPH_STYLE
                )
            ], style={'display': 'flex', 'justify-content': 'space-between'}
        )

    def _pie_chart(self, labels: pd.Series, values: pd.Series, title: str) -> dcc.Graph:
        return dcc.Graph(
            figure={
                self.DATA: [go.Pie(labels=labels, values=values, hole=.5)],
                self.LAYOUT: go.Layout(title=title.title())
            }
        )
    
    def _bar_chart(self, df: pd.DataFrame, group_col: list[str], title: str, mapper: bool = None, color_palette: str = "husl") -> dict:
        bar_colors = sns.color_palette(color_palette, n_colors=31).as_hex()
        data = df.groupby(group_col)[self.MESSAGE].count().reset_index()
        if mapper:
            data[group_col] = data[group_col].map(mapper)
        return {
            self.DATA: [go.Bar(x=data[group_col], y=data[self.MESSAGE], marker={'color': bar_colors})],
            self.LAYOUT: go.Layout(title=title.title())
        }