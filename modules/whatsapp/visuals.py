# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import io
import base64
from collections import Counter, defaultdict

# --- Third-party ---
import seaborn as sns
from textblob import TextBlob
from dash import dcc, html
from wordcloud import WordCloud
import plotly.graph_objects as go

# --- Project ---
from . import core

_GRAPH_STYLE = {"width": "48%", "display": "inline-block"}
_FULL_WIDTH_STYLE = {"width": "100%", "display": "inline-block"}
_IMAGE_STYLE = {"width": "48%", "display": "inline-block", "vertical-align": "top"}
_WC_STYLE = {'width': '100%', 'height': 'auto'}

def layout(data: dict = None) -> html.Div:
    return html.Div([
        html.H1("Choose an issuer"),
        dcc.Dropdown(
            id='issuer-dropdown',
            options=[{'label': i, 'value': i} for i in ["GENERAL"] + sorted(data)],
            value="GENERAL" # initial value
        ),
        html.Div(id='general-charts', style=_FULL_WIDTH_STYLE),
        html.Div([
            html.Div(dcc.Graph(id='hour-chart'), style=_GRAPH_STYLE),
            html.Div(dcc.Graph(id='dow-chart'), style=_GRAPH_STYLE),
            html.Div(dcc.Graph(id='dom-chart'), style=_GRAPH_STYLE),
            html.Div(dcc.Graph(id='month-chart'), style=_GRAPH_STYLE),
            html.Div(dcc.Graph(id='sentiment-analysis'), style=_GRAPH_STYLE),
            html.Div(html.Img(id='wordcloud', style=_WC_STYLE),
            style=_IMAGE_STYLE)
        ])
    ])

def get_wordcloud(text: str) -> str:

    wordcloud_inputs = {"width":800, "height":400, "background_color":"white"}
    wordcloud = WordCloud(**wordcloud_inputs).generate(text)
    with io.BytesIO() as buffer:
        wordcloud.to_image().save(buffer, format="PNG")
        encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return f"data:image/png;base64,{encoded}"

def get_sentiments(messages: list) -> go.Figure:

    def get_polarity(string: str) -> float:
        return TextBlob(string).sentiment.polarity
    scores = [get_polarity(m.replace('\n', ' ')) for m in messages]
    mean_p = (sum(scores) / len(scores)) if scores else 0

    figure_inputs = {
        "y":scores,
        "box_visible":True,
        "line_color":'black',
        "meanline_visible":True,
        "fillcolor":'lightseagreen',
        "opacity":0.6,
        "name":'Sentiment Distribution'
    }
    update_input = {
        "title":f'Sentiment Analysis - Mean Polarity: {mean_p * 100:.2f}%',
        "xaxis":dict(title='Sentiment Polarity'),
        "yaxis":dict(title='Density'),
        "template":'plotly_white'
    }

    fig = go.Figure(data=[go.Violin(**figure_inputs)])
    fig.update_layout(**update_input)
    return fig

def get_general_chart(parsed_data: list) -> html.Div:

    def get_pie_chart(labels: list, values: list, title: str) -> dcc.Graph:
        return dcc.Graph(figure={
            'data': [go.Pie(labels=labels, values=values, hole=.5)],
            'layout': go.Layout(title=title.title())
        })

    issuers, msg_values = zip(*Counter(row[2] for row in parsed_data).items())
    word_counts = Counter(row[7] for row in parsed_data for issuer in [row[2]])
    word_values = [word_counts[issuer] for issuer in issuers]

    msg_inputs = (issuers, msg_values, 'proportion of messages by issuer')
    word_inputs = (issuers, word_values, 'proportion of words by issuer')

    return html.Div([
        html.Div(get_pie_chart(*msg_inputs), style=_GRAPH_STYLE),
        html.Div(get_pie_chart(*word_inputs), style=_GRAPH_STYLE)
    ], style={'display': 'flex', 'justify-content': 'space-between'})

def get_bar_chart(counts: dict, group_col: str, title: str, mapper: dict = None) -> dict:

    def aggregate_counts() -> dict[int, int]:
        idx = {'HOUR': 1, 'dow': 2, 'dom': 3, 'month': 4}[group_col]
        agg = defaultdict(int)
        for key, value in counts.items():
            parts = key.split('_')
            group_key = int(parts[idx] if len(parts) == 5 else parts[idx + 1])
            agg[group_key] += value
        return dict(agg)

    def get_values(agg_counts: dict) -> tuple[list, list]:
        sorted_keys = sorted(agg_counts.keys())
        x = [mapper[k] for k in sorted_keys] if mapper else sorted_keys
        y = [agg_counts[k] for k in sorted_keys]
        return x, y

    bar_colors = sns.color_palette("husl", n_colors=31).as_hex()
    x, y = get_values(aggregate_counts())
    return {
        'data': [go.Bar(x=x, y=y, marker={'color': bar_colors})],
        'layout': go.Layout(title=title.title())
    }

# TENGO QUE MODIFICAR PRIMERO EL MODULO PARA QUE SEA MAS ENTENDIBLE
def all_charts(data: core.WhatsAppConfig, issuer: str, weekdays_mapper: dict, months_mapper: dict) -> dict:
    service = core.WhatsAppModule() # ver despues
    service.current_data = data
    filtered_counts, norm_text, is_general, raw_messages = service.filter_chat(issuer)

    return {
        'general_charts': get_general_chart(data.parsed_data) if is_general else "",
        'hour_chart': get_bar_chart(filtered_counts, 'HOUR', 'amount of messages per hour'),
        'dow_chart': get_bar_chart(filtered_counts, 'dow', 'amount of messages per day of the week', weekdays_mapper),
        'dom_chart': get_bar_chart(filtered_counts, 'dom', 'amount of messages per day of the month'),
        'month_chart': get_bar_chart(filtered_counts, 'month', 'amount of messages per month', months_mapper),
        'sentiment_chart': get_sentiments(raw_messages),
        'wordcloud': get_wordcloud(norm_text)
    }