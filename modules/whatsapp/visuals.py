# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import io
import base64
from collections import Counter, defaultdict

# --- Third-party ---
# import seaborn as sns
from textblob import TextBlob
from dash import dcc, html
from wordcloud import WordCloud
import plotly.graph_objects as go
import plotly.express as px

# --- Project ---
from . import core

_GRAPH_STYLE = {"width": "48%", "display": "inline-block"}
_FULL_WIDTH_STYLE = {"width": "100%", "display": "inline-block"}
_IMAGE_STYLE = {"width": "48%", "display": "inline-block", "vertical-align": "top"}
_WC_STYLE = {'width': '100%', 'height': 'auto'}

def layout(issuers: list = None) -> html.Div:
    if issuers is None or not issuers:
        return html.Div([
            html.H1("Dashboard will be displayed after data upload."),
            html.P("Please upload a file to view the dashboard.")
        ])
    return html.Div([
        html.H1("Choose an issuer"),
        dcc.Dropdown(
            id='issuer-dropdown',
            options=[{'label':i,'value':i} for i in ["GENERAL"]+issuers],
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

def create_wordcloud(text: str) -> str:

    wordcloud_inputs = {"width":800, "height":400, "background_color":"white"}
    wordcloud = WordCloud(**wordcloud_inputs).generate(text)
    with io.BytesIO() as buffer:
        wordcloud.to_image().save(buffer, format="PNG")
        encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return f"data:image/png;base64,{encoded}"

def create_sentiments(messages: list) -> go.Figure:

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

def create_general_chart(parsed_data: list) -> html.Div:

    def _create_pie_chart(labels: list, values: list, title: str) -> dcc.Graph:
        """Crea un componente dcc.Graph para un gráfico de torta."""
        return dcc.Graph(figure={
            'data': [go.Pie(labels=labels, values=values, hole=.5)],
            'layout': go.Layout(title=title.title())
        })

    def _get_chart_inputs(data: list) -> tuple[list, list, list]:
        message_counts = Counter(row[2] for row in data)
        issuers, msg_values_tuple = zip(*message_counts.items())

        word_counts = defaultdict(int, {
            row[2]: sum(r[7] for r in data if r[2] == row[2]) for row in data
        })
        word_values = [word_counts[issuer] for issuer in list(issuers)]
        return list(issuers), list(msg_values_tuple), word_values

    issuers, msg_values, word_values = _get_chart_inputs(parsed_data)
    msg_chart_args = (issuers, msg_values, 'proportion of messages by issuer')
    word_chart_args = (issuers, word_values, 'proportion of words by issuer')

    return html.Div([
        html.Div(_create_pie_chart(*msg_chart_args), style=_GRAPH_STYLE),
        html.Div(_create_pie_chart(*word_chart_args), style=_GRAPH_STYLE)
    ], style={'display': 'flex', 'justify-content': 'space-between'})

def create_bar_chart(
        counts: dict, group_col: str, title: str, mapper: dict = None
    ) -> dict:

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

    # bar_colors = sns.color_palette("husl", n_colors=31).as_hex()
    bar_colors = px.colors.sample_colorscale("HSV", [i/30 for i in range(31)])
    x, y = get_values(aggregate_counts())
    return {
        'data': [go.Bar(x=x, y=y, marker={'color': bar_colors})],
        'layout': go.Layout(title=title.title())
    }

def generate_charts(
        data: core.Config,
        issuer: str,
        weekdays_mapper: dict,
        months_mapper: dict
    ) -> dict:

    service = core.ChatSession()
    service.current_data = data
    counts, _, is_general, msg = service.filter_chat(issuer)
    text = data.normalized_texts[issuer]

    hour_title = 'amount of messages per hour'
    dow_title = 'amount of messages per day of the week'
    dom_title = 'amount of messages per day of the month'
    month_title = 'amount of messages per month'

    gral_chart = create_general_chart(data.parsed_data) if is_general else ""
    hour_chart = create_bar_chart(counts, 'HOUR', hour_title)
    dow_chart = create_bar_chart(counts, 'dow', dow_title, weekdays_mapper)
    dom_chart = create_bar_chart(counts, 'dom', dom_title)
    month_chart = create_bar_chart(counts, 'month', month_title, months_mapper)
    sentiment_chart = create_sentiments(msg)
    wordcloud = create_wordcloud(text)

    chart_keys = [
        "general_charts", "hour_chart", "dow_chart", "dom_chart", "month_chart",
        "sentiment_chart", "wordcloud"
    ]
    chart_values = [
        gral_chart, hour_chart, dow_chart, dom_chart, month_chart,
        sentiment_chart, wordcloud
    ]

    return dict(zip(chart_keys, chart_values))
