"""
Contain functions for WhatsApp functionality.
"""

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
    """Data class that holds WhatsApp chat data after processing."""
    df: pd.DataFrame
    content: pd.DataFrame
    language: str

class WhatsAppService:
    """Service class for processing and analyzing WhatsApp chat data."""

    
    def __init__(self):
        """Initialize the WhatsAppService with no current data."""
        self.current_data = None
    
    def process_file(self, file, language: str) -> WhatsAppData:
        """
        Process a WhatsApp chat file and generate structured data.
      
        Args:
            file: The uploaded WhatsApp chat file.
            language (str): Language to be used for text processing.
      
        Returns:
            WhatsAppData: Object containing processed DataFrames and language.
        """
        content = self._parse_whatsapp_file(file)
        df = self._agg_message_counts(content)
        self.current_data = WhatsAppData(df=df, content=content, language=language)
        return self.current_data
    
    def get_filtered_data(self, issuer: str) -> tuple:
        """
        Filter chat data for a specific issuer or return general stats.
      
        Args:
            issuer (str): Issuer name to filter by.
      
        Returns:
            tuple: (Filtered aggregated DataFrame, normalized text, is_general flag)
        """
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
    
    def _agg_message_counts(df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate message counts per issuer and time period.
      
        Args:
            df (pd.DataFrame): Raw message data.
      
        Returns:
            pd.DataFrame: Aggregated message count data.
        """
        group_and_count = lambda cols: df.groupby(cols)[MESSAGE].count().reset_index()
        return (
            pd.concat([
                group_and_count([ISSUER] + COLS_TO_GROUP),
                group_and_count(COLS_TO_GROUP).assign(ISSUER=GENERAL)
            ])
        )
    
    def _parse_whatsapp_file(file: str) -> pd.DataFrame:
        """
        Parse a raw WhatsApp chat file into a structured DataFrame.
      
        Args:
            file (str): File object containing WhatsApp messages.
      
        Returns:
            pd.DataFrame: Structured DataFrame of chat messages.
        """
        chat = file.read().decode(UTF8).splitlines()
        messages = WhatsAppService._split_multiline_messages(chat)
        return WhatsAppService._parse_chat_messages(messages)
    
    def _parse_chat_messages(messages: list) -> pd.DataFrame:
        """
        Convert parsed chat message strings into a structured DataFrame.
      
        Args:
            messages (list): List of message strings.
      
        Returns:
            pd.DataFrame: DataFrame containing parsed message data.
        """
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
    
    def _split_multiline_messages(message_lines: list, regex_pattern: str = r".*\/.*\/.*,.*:.* - .*") -> list:
        """
        Combine multi-line messages into single strings based on date-time patterns.
      
        Args:
            message_lines (list): Raw lines from the chat file.
            regex_pattern (str): Regex pattern identifying the start of new messages.
      
        Returns:
            list: List of full message strings.
        """
        messages = []
        for current_line in message_lines:
            if re.match(regex_pattern, current_line): 
                messages.append(current_line)
            elif messages: 
                messages[-1] += ' ' + current_line
        return messages

class ChartGenerator:
    """Utility class to generate various WhatsApp message visualizations."""

    def generate_all_charts(
            whatsapp_data: WhatsAppData, 
            issuer: str, 
            weekdays_mapper: dict[str, str],
            months_mapper: dict[str, str]
        ) -> dict:
        """
        Generate all visual charts for the selected WhatsApp issuer.
      
        Args:
            whatsapp_data (WhatsAppData): The parsed WhatsApp dataset.
            issuer (str): Name of the person or group to filter messages.
            weekdays_mapper (dict[str, str]): Mapping from weekday numbers to names.
            months_mapper (dict[str, str]): Mapping from month numbers to names.
      
        Returns:
            dict: A dictionary containing Plotly/Dash figures and HTML components.
        """        
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
    
    def _generate_wordcloud(text: str) -> str:
        """
        Generate a word cloud image encoded in base64.
      
        Args:
            text (str): Text from which to generate the word cloud.
      
        Returns:
            str: A base64-encoded string representation of the image.
        """
        buffer = io.BytesIO()
        WordCloud(width=800, height=400, background_color='white').generate(text).to_image().save(buffer, format='PNG')
        buffer.seek(0)
        return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode(UTF8)}"
    
    def _sentiment_analysis(data: pd.DataFrame, selected_issuer: str = None) -> go.Figure: 
        """
        Create a sentiment analysis violin plot of message polarity.
      
        Args:
            data (pd.DataFrame): DataFrame containing the messages.
            selected_issuer (str, optional): Issuer to filter by, or None for all.
      
        Returns:
            go.Figure: A Plotly violin chart showing sentiment distribution.
        """
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
    
    def _create_general_charts(df: pd.DataFrame) -> html.Div:
        """
        Create pie charts for general issuer message and word proportions.
      
        Args:
            df (pd.DataFrame): Full message dataset.
      
        Returns:
            html.Div: Dash component containing pie charts.
        """
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

    def _create_pie_chart(labels: pd.Series, values: pd.Series, title: str) -> dcc.Graph:
        """
        Create a pie chart from labels and values.
      
        Args:
            labels (pd.Series): Labels for the pie chart.
            values (pd.Series): Corresponding values for each label.
            title (str): Title of the chart.
      
        Returns:
            dcc.Graph: Dash Graph component with the pie chart.
        """
        return dcc.Graph(
            figure={
                DATA: [go.Pie(labels=labels, values=values, hole=.5)],
                LAYOUT: go.Layout(title=title.title())
            }
        )
    
    def _create_bar_chart(df: pd.DataFrame, group_col: list[str], title: str, mapper: bool = None, color_palette: str = "husl") -> dict:
        """
         Create a grouped bar chart with optional label mapping.
        
           Args:
             df (pd.DataFrame): The DataFrame to use.
             group_col (list[str]): Column to group by.
             title (str): Title for the chart.
             mapper (bool, optional): Mapping for label replacement. Defaults to None.
             color_palette (str): Seaborn color palette to use. Defaults to "husl".
          
         Returns:
             dict: A dictionary representing a Plotly bar chart.
         """
        bar_colors = sns.color_palette(color_palette, n_colors=31).as_hex()
        data = df.groupby(group_col)[MESSAGE].count().reset_index()
        if mapper:
            data[group_col] = data[group_col].map(mapper)
        return {
            DATA: [go.Bar(x=data[group_col], y=data[MESSAGE], marker={'color': bar_colors})],
            LAYOUT: go.Layout(title=title.title())
        }
  