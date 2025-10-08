"""Contain functions for WhatsApp functionality."""

# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import base64, io, re, os
from datetime import datetime
from collections import Counter, defaultdict

# --- Third-party ---
import seaborn as sns
import textblob as tb
from tqdm import tqdm
from dash import dcc, html
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
def layout(data: dict = None) -> html.Div:
    GRAPH_STYLE = {'width': '48%', 'display': 'inline-block'}
    
    if data is None or not data:
        return html.Div([
            html.H1("Dashboard will be displayed after data upload."),
            html.P("Please upload a file to view the dashboard.")           
        ])
    
    issuers = sorted(list({key.split('_')[0] for key in data if not key.startswith('GENERAL_')}))
    if any(key.startswith('GENERAL_') for key in data):
        issuers.insert(0, 'GENERAL')
    
    initial_value = issuers[0] if issuers else None

    return html.Div([
        html.H1("Choose an issuer"),
        dcc.Dropdown(
            id='issuer-dropdown',
            options=[{'label': issuer, 'value': issuer} for issuer in issuers],
            value=initial_value
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
    grouped_data: dict
    parsed_data: list
    language: str

class WhatsAppModule:
    def __init__(self):
        self.current_data = None

    def parse_chat(self, file, language: str) -> WhatsAppConfig:
        raw_lines = file.read().decode('utf-8').splitlines()
        parsed_data = parse_messages(raw_lines)
        grouped_data = groupby_dict(parsed_data)
        
        self.current_data = WhatsAppConfig(
            grouped_data=grouped_data,
            parsed_data=parsed_data,
            language=language
        )
        return self.current_data
    
    def filter_chat(self, issuer: str) -> tuple:
        is_general = issuer == 'GENERAL'
        
        prefix = "GENERAL_" if is_general else f"{issuer}_"
        filtered_counts = {k: v for k, v in self.current_data.grouped_data.items() if k.startswith(prefix)}

        if is_general:
            messages_to_process = [row[3] for row in self.current_data.parsed_data]
        else:
            messages_to_process = [row[3] for row in self.current_data.parsed_data if row[2] == issuer]
        
        combined_text = ' '.join(messages_to_process)
        normalized_text = text_normalizer(text=combined_text, stopwords=STOPWORDS[self.current_data.language])
      
        return filtered_counts, normalized_text, is_general, messages_to_process
      
# =============================================================================
# PARSER
# =============================================================================
def clean_message(data: str) -> iter:

    SPLIT_STR = r'^(\d{1,2}/\d{1,2}/\d{2,4}), ([^ ]+) - ([^:]+): (.+)$'
    PARSE_STR = r".*\/.*\/.*,.*:.* - .*"

    def is_valid(line: str) -> bool:
        generic_match = re.compile(PARSE_STR).match(line)
        specific_match = re.compile(SPLIT_STR).match(line)

        if not (generic_match and specific_match):
            return False

        _, _, _, msg = specific_match.groups()
        if msg.strip().startswith('<') and msg.strip().endswith('>'):
            return False
        return True

    def parse_line(line: str) -> tuple:
        generic_match = re.compile(SPLIT_STR).match(line)
        date, time, issuer, msg = generic_match.groups()
        date = datetime.strptime(date, "%d/%m/%Y")
        return (
            date, int(time[:2]), issuer.strip(), msg.strip(),
            date.weekday(), date.day, date.month, msg.count(" ")+1
        )

    yield from (parse_line(d) for d in data if is_valid(d))

class WhatsappFileError(Exception):
    pass

def parse_messages(data):
    MESSAGE = "Cleaning messages"
    cleaned = [msg for msg in tqdm(clean_message(data), desc=MESSAGE)]
    if not cleaned:
        raise WhatsappFileError("Invalid file format")
    return cleaned

def groupby_dict(data):
    return Counter(
        f"{prefix}{'_'.join(str(row[i]) for i in idxs)}"
        for row in tqdm(data, desc="Grouping data")
        for prefix, idxs in [("", [2,1,4,5,6]), ("GENERAL_", [1,4,5,6])]
    )
    
# =============================================================================
# PLOTTING
# =============================================================================
class ChartGenerator:
    DATA = 'data'
    LAYOUT = 'layout'
    GRAPH_STYLE = {'width': '48%', 'display': 'inline-block'}
    GROUP_COL_MAP = {'HOUR': 1, 'dow': 2, 'dom': 3, 'month': 4}

    def all_charts(self, data: WhatsAppConfig, issuer: str, weekdays_mapper: dict, months_mapper: dict) -> dict:    
        service = WhatsAppModule()
        service.current_data = data
        filtered_counts, norm_text, is_general, raw_messages = service.filter_chat(issuer)
        
        return {
            'general_charts': self._general_charts(data.parsed_data) if is_general else "",
            'hour_chart': self._bar_chart(filtered_counts, 'HOUR', 'amount of messages per hour'),
            'dow_chart': self._bar_chart(filtered_counts, 'dow', 'amount of messages per day of the week', weekdays_mapper),
            'dom_chart': self._bar_chart(filtered_counts, 'dom', 'amount of messages per day of the month'),
            'month_chart': self._bar_chart(filtered_counts, 'month', 'amount of messages per month', months_mapper),
            'sentiment_chart': self._sentiments(raw_messages),
            'wordcloud': self._wordcloud(norm_text)
        }
        
    def _wordcloud(self, text: str) -> str:
        if not text.strip():
            return ""
        buffer = io.BytesIO()
        WordCloud(width=800, height=400, background_color='white').generate(text).to_image().save(buffer, format='PNG')
        buffer.seek(0)
        return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
    
    def _sentiments(self, messages: list) -> go.Figure: 
        scores = [tb.TextBlob(msg.replace('\n', ' ')).sentiment.polarity for msg in messages]
        mean_polarity = (sum(scores) / len(scores)) if scores else 0
        fig = go.Figure(data=[go.Violin(y=scores, box_visible=True, line_color='black', meanline_visible=True, fillcolor='lightseagreen', opacity=0.6, name='Sentiment Distribution')])
        fig.update_layout(title=f'Sentiment Analysis - Mean Polarity: {mean_polarity * 100:.2f}%', xaxis=dict(title='Sentiment Polarity'), yaxis=dict(title='Density'), template='plotly_white')
        return fig
    
    def _general_charts(self, parsed_data: list) -> html.Div:
        issuer_counts = Counter(row[2] for row in parsed_data)
        word_counts = defaultdict(int)
        for row in parsed_data:
            word_counts[row[2]] += row[7]
        
        issuers = list(issuer_counts.keys())
        msg_values = list(issuer_counts.values())
        word_values = [word_counts[issuer] for issuer in issuers]

        return html.Div([
            html.Div(self._pie_chart(issuers, msg_values, 'proportion of messages by issuer'), style=self.GRAPH_STYLE),
            html.Div(self._pie_chart(issuers, word_values, 'proportion of words by issuer'), style=self.GRAPH_STYLE)
        ], style={'display': 'flex', 'justify-content': 'space-between'})

    def _pie_chart(self, labels: list, values: list, title: str) -> dcc.Graph:
        return dcc.Graph(figure={
            self.DATA: [go.Pie(labels=labels, values=values, hole=.5)],
            self.LAYOUT: go.Layout(title=title.title())
        })
    
    def _bar_chart(self, counts: dict, group_col: str, title: str, mapper: dict = None, color_palette: str = "husl") -> dict:
        bar_colors = sns.color_palette(color_palette, n_colors=31).as_hex()
        aggregated_data = defaultdict(int)
        idx_in_key = self.GROUP_COL_MAP[group_col]

        for key, value in counts.items():
            parts = key.split('_')
            group_key = int(parts[idx_in_key] if len(parts) == 5 else parts[idx_in_key+1])
            aggregated_data[group_key] += value
        
        sorted_keys = sorted(aggregated_data.keys())
        x_values = [mapper[k] for k in sorted_keys] if mapper else sorted_keys
        y_values = [aggregated_data[k] for k in sorted_keys]
        
        return {
            self.DATA: [go.Bar(x=x_values, y=y_values, marker={'color': bar_colors})],
            self.LAYOUT: go.Layout(title=title.title())
        }