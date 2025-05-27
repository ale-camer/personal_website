"""Contain functions for WhatsApp functionality."""

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

# --- Column name constants ---
COUNT = 'COUNT'
SCORE = 'score'
HOUR = 'HOUR'
DATE = 'DATE'
MESSAGE = 'MESSAGE'
ISSUER = 'ISSUER'
GENERAL = 'GENERAL'
RAW_DATA = 'RAW_DATA'
LEN_MESSAGE = 'len_message'

# --- Dash component IDs ---
DROPDOWN_ID = 'issuer-dropdown'
MAIN_DIV_ID = 'general-charts'
HOUR_CHART_ID = 'hour-chart'
DOW_CHART_ID = 'dow-chart'
DOM_CHART_ID = 'dom-chart'
MONTH_CHART_ID = 'month-chart'
SENT_ANAL_ID = 'sentiment-analysis'
WC_ID = 'wordcloud'

# --- CSS style dictionaries ---
GRAPH_STYLE = {'width': '48%', 'display': 'inline-block'}
IMAGE_STYLE = {'width': '100%', 'height': 'auto'}
MAIN_DIV_STYLE = {'width': '100%', 'display': 'inline-block'}

# --- General constants ---
UTF8 = 'utf-8'
LAYOUT = 'layout'
DATA = 'data'
COLS_TO_GROUP = ['HOUR', 'dow', 'dom', 'month']
URL_REGEX = re.compile(r'http\S+')

def build_layout(df: pd.DataFrame = None) -> html.Div:
    if df is None or df.empty:
        return html.Div([
            html.H1("Dashboard will be displayed after data upload.".capitalize()),
            html.P("Please upload a file to view the dashboard.".capitalize()),
            dcc.Dropdown(id=DROPDOWN_ID, options=[], value=None),
            html.Div(id=MAIN_DIV_ID, style=MAIN_DIV_STYLE),
            html.Div([
                dcc.Graph(id=HOUR_CHART_ID),
                dcc.Graph(id=DOW_CHART_ID),
                dcc.Graph(id=DOM_CHART_ID),
                dcc.Graph(id=MONTH_CHART_ID),
                dcc.Graph(id=SENT_ANAL_ID),
                html.Img(id=WC_ID, style=IMAGE_STYLE)
            ])
        ])

    return html.Div([
        html.H1("Choose an issuer".capitalize()),
        dcc.Dropdown(
            id=DROPDOWN_ID,
            options=[{'label': issuer, 'value': issuer} for issuer in df[ISSUER].unique()],
            value=df[ISSUER].unique()[0]
        ),
        html.Div(id=MAIN_DIV_ID, style=MAIN_DIV_STYLE),
        html.Div([
            html.Div(dcc.Graph(id=HOUR_CHART_ID), style=GRAPH_STYLE),
            html.Div(dcc.Graph(id=DOW_CHART_ID), style=GRAPH_STYLE),
            html.Div(dcc.Graph(id=DOM_CHART_ID), style=GRAPH_STYLE),
            html.Div(dcc.Graph(id=MONTH_CHART_ID), style=GRAPH_STYLE),
            html.Div(dcc.Graph(id=SENT_ANAL_ID), style=GRAPH_STYLE),
            html.Div(html.Img(id=WC_ID, style=IMAGE_STYLE), style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'top'})
        ])
    ])
    
@dataclass
class WhatsAppData:
    df: pd.DataFrame
    content: pd.DataFrame
    language: str

class WhatsAppService:
    
    def __init__(self):
        self.current_data = None
    
    def process_file(self, file, language: str) -> WhatsAppData:
        content = self._parse_whatsapp_file(file)
        df = self._agg_message_counts(content)
        self.current_data = WhatsAppData(df=df, content=content, language=language)
        return self.current_data
    
    def get_filtered_data(self, issuer: str) -> tuple:
        is_general = issuer == GENERAL
        
        if is_general:
            filtered_df = self.current_data.df.copy()
            issuer_filter = slice(None)
        else:
            filtered_df = self.current_data.df[
                self.current_data.df[ISSUER] == issuer
            ]
            issuer_filter = self.current_data.content[ISSUER] == issuer
                
        filtered_messages = self.current_data.content[issuer_filter]
        combined_text = ' '.join(filtered_messages[MESSAGE].astype(str))
        
        stopwords = set(nltk.corpus.stopwords.words(self.current_data.language))
        issuer_messages = text_normalizer(
            text=combined_text,
            stopwords=stopwords
        )
      
        return filtered_df, issuer_messages, is_general
    
    @staticmethod
    def _agg_message_counts(df: pd.DataFrame) -> pd.DataFrame:
        group_and_count = lambda cols: df.groupby(cols)[MESSAGE].count().reset_index()
        return (
            pd.concat([
                group_and_count([ISSUER] + COLS_TO_GROUP),
                group_and_count(COLS_TO_GROUP).assign(ISSUER=GENERAL)
            ])
        )
    
    @staticmethod
    def _parse_whatsapp_file(file: str) -> pd.DataFrame:
        chat = file.read().decode(UTF8).splitlines()
        messages = WhatsAppService._split_multiline_messages(chat)
        return WhatsAppService._parse_chat_messages(messages)
    
    @staticmethod
    def _parse_chat_messages(messages: list) -> pd.DataFrame:
        return (
            pd.DataFrame(messages, columns=[RAW_DATA])
            .loc[lambda df: df[RAW_DATA].str.contains(': ') & ~df[RAW_DATA].str.contains('Multimedia')]
            .assign(
                DATE=lambda df: pd.to_datetime(df[RAW_DATA].str.split(',', expand=True)[0], dayfirst=True),
                HOUR=lambda df: df[RAW_DATA].str.split(',', expand=True)[1].str.split('-', expand=True)[0].str.strip(),
                ISSUER=lambda df: df[RAW_DATA].str.split('- ', expand=True)[1].str.split(':', expand=True)[0],
                MESSAGE=lambda df: df[RAW_DATA].str.split(': ', n=1, expand=True)[1],
            )
            .drop(RAW_DATA, axis=1)
            .assign(
                dow=lambda df: df[DATE].dt.dayofweek,
                dom=lambda df: df[DATE].dt.day,
                month=lambda df: df[DATE].dt.month,
                HOUR=lambda df: df[HOUR].apply(lambda h: int(h.split(':')[0])),
                len_message=lambda df: df[MESSAGE].apply(lambda msg: len(msg.split()))
            )
        )
    
    @staticmethod
    def _split_multiline_messages(message_lines: list, regex_pattern: str = r".*\/.*\/.*,.*:.* - .*") -> list:
        messages = []
        for current_line in message_lines:
            if re.match(regex_pattern, current_line): 
                messages.append(current_line)
            elif messages: 
                messages[-1] += ' ' + current_line
        return messages

class ChartGenerator:

    @staticmethod
    def generate_all_charts(whatsapp_data: WhatsAppData, issuer: str, weekdays_mapper: dict[str, str], months_mapper: dict[str, str]) -> dict:    
        
        service = WhatsAppService()
        service.current_data = whatsapp_data
        filtered_df, issuer_messages, is_general = service.get_filtered_data(issuer)
        return {
            'general_charts': (
                ChartGenerator._create_general_charts(whatsapp_data.content) 
                if is_general else ""
            ),
            'hour_chart': ChartGenerator._create_bar_chart(
                filtered_df, HOUR, 'amount of messages per hour'
            ),
            'dow_chart': ChartGenerator._create_bar_chart(
                filtered_df, 'dow', 'amount of messages per day of the week', weekdays_mapper
            ),
            'dom_chart': ChartGenerator._create_bar_chart(
                filtered_df, 'dom', 'amount of messages per day of the month'
            ),
            'month_chart': ChartGenerator._create_bar_chart(
                filtered_df, 'month', 'amount of messages per month', months_mapper
            ),
            'sentiment_chart': ChartGenerator._sentiment_analysis(
                whatsapp_data.content, None if is_general else issuer
            ),
            WC_ID: ChartGenerator._generate_wordcloud(issuer_messages)
        }
    
    @staticmethod
    def _generate_wordcloud(text: str) -> str:
        buffer = io.BytesIO()
        WordCloud(width=800, height=400, background_color='white').generate(text).to_image().save(buffer, format='PNG')
        buffer.seek(0)
        return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode(UTF8)}"
    
    @staticmethod
    def _sentiment_analysis(data: pd.DataFrame, selected_issuer: str = None) -> go.Figure: 
        df = (
            (data[data[ISSUER] == selected_issuer] if selected_issuer and selected_issuer != GENERAL else data.copy())
            .assign(SCORE=lambda d: d[MESSAGE].apply(lambda a: tb.TextBlob(a.replace('\n', ' ')).sentiment.polarity))
        )
        fig = (
            go.Figure(
                data=[go.Violin(
                    y=df[SCORE.upper()],
                    box_visible=True,
                    line_color='black',
                    meanline_visible=True,
                    fillcolor='lightseagreen',
                    opacity=0.6,
                    name='Sentiment Distribution'
                )]
            )
            .update_layout(
                title=f'Sentiment Analysis - Mean Polarity: {round(df[SCORE.upper()].mean() * 100, 2):.2f}%',
                xaxis=dict(title='Sentiment Polarity'),
                yaxis=dict(title='Density'),
                template='plotly_white'
            )
        )
        return fig
    
    @staticmethod
    def _create_general_charts(df: pd.DataFrame) -> html.Div:
        issuer_counts = df[ISSUER].value_counts().reset_index().rename(columns={COUNT.lower(): COUNT})
        message_length_sum = df.groupby(ISSUER)[LEN_MESSAGE].sum().reset_index()
        return html.Div(
            [
                html.Div(
                    ChartGenerator._create_pie_chart(
                        issuer_counts[ISSUER], 
                        issuer_counts[COUNT], 
                        'proportion of messages by issuer'
                    ), 
                    style=GRAPH_STYLE
                ),
                html.Div(
                    ChartGenerator._create_pie_chart(
                        message_length_sum[ISSUER], 
                        message_length_sum[LEN_MESSAGE], 
                        'proportion of words by issuer'
                    ), 
                    style=GRAPH_STYLE
                )
            ], 
            style={'display': 'flex', 'justify-content': 'space-between'}
        )

    @staticmethod
    def _create_pie_chart(labels: pd.Series, values: pd.Series, title: str) -> dcc.Graph:
        return dcc.Graph(
            figure={
                DATA: [go.Pie(labels=labels, values=values, hole=.5)],
                LAYOUT: go.Layout(title=title.title())
            }
        )
    
    @staticmethod
    def _create_bar_chart(df: pd.DataFrame, group_col: list[str], title: str, mapper: bool = None, color_palette: str = "husl") -> dict:
        bar_colors = sns.color_palette(color_palette, n_colors=31).as_hex()
        data = df.groupby(group_col)[MESSAGE].count().reset_index()
        if mapper:
            data[group_col] = data[group_col].map(mapper)
        return {
            DATA: [go.Bar(x=data[group_col], y=data[MESSAGE], marker={'color': bar_colors})],
            LAYOUT: go.Layout(title=title.title())
        }
  