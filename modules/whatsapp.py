"""Contain functions for WhatsApp functionality."""

# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import base64, io, re, os

# --- Third-party ---
import pandas as pd
import seaborn as sns
import textblob as tb
from tqdm import tqdm
from dash import dcc, html
from datetime import datetime
import plotly.graph_objects as go
from wordcloud import WordCloud

# --- Project/system ---
from dataclasses import dataclass
from modules.utils import text_normalizer, read_json, performance_analyzer

# =============================================================================
# PATHS
# =============================================================================
STOPWORDS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'static', 'json', 'stopwords.json'
)
STOPWORDS = read_json(STOPWORDS_PATH)

# =============================================================================
# DASHBOARD
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
    ISSUER = 'ISSUER'
    
    def __init__(self):
        self.current_data = None

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
        
        issuer_messages = text_normalizer(
            text=combined_text,
            stopwords=STOPWORDS[self.current_data.language]
        )
      
        return filtered_df, issuer_messages, is_general
      
# =============================================================================
# PARSER
# =============================================================================
class WhatsAppParser:
    CHUNK_SIZE = int(1e6)
    RAW_DATA = 'RAW_DATA'
    DATE = 'DATE'
    HOUR = 'HOUR'
    ISSUER = 'ISSUER'
    MESSAGE = 'MESSAGE'
    COLS_TO_GROUP = ['HOUR', 'dow', 'dom', 'month']
    COLUMNS = [DATE, HOUR, ISSUER, MESSAGE, 'dow', 'dom', 'month', 'len_message']
    
    _split_pattern = re.compile(r".*\/.*\/.*,.*:.* - .*")
    _parse_pattern = re.compile(r'^(\d{1,2}/\d{1,2}/\d{2,4}), ([^ ]+) - ([^:]+): (.+)$')

    def __init__(self, file):
        self.file = file
    
    def parse(self) -> pd.DataFrame:
        parsed = []
        raw_lines = self.file.read().decode('utf-8').splitlines()
        for i in tqdm(range(0, len(raw_lines), self.CHUNK_SIZE)):
            chunk_lines = raw_lines[i:i+self.CHUNK_SIZE]
            raw_messages = list(self._split_messages(chunk_lines))
            parsed_chunk = self._parse_all_messages(raw_messages)
            parsed.append(parsed_chunk)
        return pd.concat(parsed, ignore_index=True)

    def group(self, df: pd.DataFrame) -> pd.DataFrame:
        by_issuer = self._group_and_count(df, [self.ISSUER] + self.COLS_TO_GROUP)
        general = self._group_and_count(df, self.COLS_TO_GROUP).assign(ISSUER='GENERAL')
        return pd.concat([by_issuer, general], ignore_index=True)

    def _group_and_count(self, df: pd.DataFrame, group_columns: list) -> pd.DataFrame:
        return df.groupby(group_columns)[self.MESSAGE].count().reset_index()

    def _split_messages(self, raw_lines: list):
        buffer = []
        for line in raw_lines:
            if self._split_pattern.match(line):
                if buffer:
                    yield ' '.join(buffer)
                buffer = [line]
            else:
                buffer.append(line)
        if buffer:
            yield ' '.join(buffer)

    def _parse_all_messages(self, messages: list) -> pd.DataFrame:
        parsed = list(filter(None, map(self._parse_single_message, messages)))
        return pd.DataFrame(parsed, columns=self.COLUMNS)

    def _parse_single_message(self, message: str):
        match = self._parse_pattern.match(message)
        if 'Multimedia' in message or not match:
            return None
        else:
            date_str, time_str, issuer, message_text = match.groups()
            dt = datetime.strptime(date_str, "%d/%m/%Y")
            return (
                dt,
                int(time_str[:2]),
                issuer.strip(),
                message_text.strip(),
                dt.weekday(),
                dt.day,
                dt.month,
                message_text.count(" ") + 1
            )
    
# =============================================================================
# PLOTTING
# =============================================================================
class ChartGenerator:
    LEN_MESSAGE = 'len_message'
    DATA = 'data'
    LAYOUT = 'layout'
    COUNT = 'COUNT'
    SCORE = 'score'
    ISSUER = 'ISSUER'
    MESSAGE = 'MESSAGE'
    GENERAL = 'GENERAL'
    GRAPH_STYLE = {'width': '48%', 'display': 'inline-block'}

    def __init__(self):
        pass
      
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