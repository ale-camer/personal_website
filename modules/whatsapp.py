"""
Contain functions for WhatsApp functionality.
"""

import io, re, nltk, base64
import pandas as pd
import textblob as tb
from unidecode import unidecode

from dash import dcc, html
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def concatenate_dfs(df: pd.DataFrame) -> pd.DataFrame: 
    """
    Returns message counts by issuer and time features, plus a 'GENERAL' group without issuer breakdown.
    """
    assert isinstance(df, pd.DataFrame), "'df' must be a pandas DataFrame"
    required_cols = {'ISSUER', 'HOUR', 'dow', 'dom', 'month', 'MESSAGE'}
    assert required_cols.issubset(df.columns), f"Missing required columns: {required_cols - set(df.columns)}"

    return (
        pd.concat(
          [
            df.groupby(['ISSUER', 'HOUR', 'dow', 'dom', 'month'])['MESSAGE'].count().reset_index(),
            df.groupby(['HOUR', 'dow', 'dom', 'month'])['MESSAGE'].count().reset_index().assign(ISSUER='GENERAL')
          ]
        )
    )

def create_dash_layout(df: pd.DataFrame, days_of_the_week: dict, months: dict) -> html.Div:
    """
    Build the Dash layout for visualizing message statistics. Displays dropdown to select issuer
    and charts for hour, weekday, day, month, sentiment, and a word cloud.

    Parameters:
    - df (pd.DataFrame): Data to visualize.
    - days_of_the_week (dict): Mapping of day indices to names.
    - months (dict): Mapping of month numbers to names.

    Returns:
    - html.Div: Dash layout container.
    """
    assert isinstance(df, pd.DataFrame), "'df' must be a Pandas DataFrame"
    assert isinstance(days_of_the_week, dict), "'days_of_the_week' must be a dict"
    assert isinstance(months, dict), "'months' must be a dict"
    assert 'ISSUER' in df.columns, "'df' must contain an 'ISSUER' column"

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
    """
    Perform sentiment analysis on the provided dataset. If a specific issuer is selected, 
    the function filters the dataset by that issuer. The sentiment polarity is calculated 
    using TextBlob for each message, and a violin plot is generated to visualize the sentiment 
    distribution.
    
    Parameters:
    - data (pd.DataFrame): The input data containing messages and issuer information.
    - selected_issuer (str): The issuer to filter by (optional). If 'GENERAL' or None, 
      all issuers are included.
    
    Returns:
    - plotly.graph_objects.Figure: A Plotly figure with a violin plot showing sentiment polarity.
    """
    assert isinstance(data, pd.DataFrame), "The 'data' must be a Pandas DataFrame"
    # assert isinstance(selected_issuer, str), "The 'selected_issuer' must be a string"

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
    """
    Generate a word cloud from the input text and return it as a base64-encoded image.
    
    Parameters:
    - text (str): The input text from which to generate the word cloud.
    
    Returns:
    - str: A base64-encoded string representing the word cloud image.
    """
    assert isinstance(text, str), "The 'text' must be a string"

    wordcloud = WordCloud(width=800, height=400, background_color ='white').generate(text)
    img = io.BytesIO()
    wordcloud.to_image().save(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"

def preprocess_whatsapp_data(file: str) -> pd.DataFrame:
    """
    Preprocess raw WhatsApp chat data by extracting relevant fields such as date, time, 
    sender (issuer), and message. It handles multiline messages and filters out multimedia messages.
    
    Parameters:
    - file (file-like object): The WhatsApp chat file to process.
    
    Returns:
    - pd.DataFrame: A DataFrame containing processed chat data with columns for date, time, 
      sender (issuer), message, and message length.
    """
    chat_lines = file.read().decode('utf-8').splitlines()
    message_pattern = r".*\/.*\/.*,.*:.* - .*"
    processed_lines = []
    pending_lines = []
    
    for i in range(len(chat_lines)): # checking regex
        if re.match(message_pattern, chat_lines[i]):
            if pending_lines:
                processed_lines[-1] = ' '.join(pending_lines)
                pending_lines = []
            processed_lines.append(chat_lines[i])
        else:
            if not pending_lines:
                pending_lines.append(chat_lines[i-1])
            pending_lines.append(chat_lines[i])
    
    df_chat = pd.DataFrame(processed_lines, columns=['RAW_DATA']) # preprocessing key columns
    df_chat['DATE'] = df_chat['RAW_DATA'].apply(lambda x: x.split(',')[0])
    df_chat['HOUR'] = df_chat['RAW_DATA'].apply(lambda x: x.split(',')[1].split('-')[0].strip())
    df_chat['ISSUER'] = df_chat['RAW_DATA'].apply(lambda x: x.split('- ')[1].split(':')[0])
    df_chat['MESSAGE'] = df_chat['RAW_DATA'].apply(lambda x: x.split(': ')[1] if ': ' in x else None)
    
    df_chat = df_chat[df_chat['MESSAGE'].notna()] # deleting unnecessary data
    df_chat['IS_MULTIMEDIA'] = df_chat['MESSAGE'].apply(lambda msg: 1 if 'Multimedia' in msg else 0)
    df_chat = df_chat[df_chat['IS_MULTIMEDIA'] == 0].drop(['RAW_DATA', 'IS_MULTIMEDIA'], axis=1)
    
    df_chat['DATE'] = pd.to_datetime(df_chat['DATE'], dayfirst=True) # formatting key columns
    df_chat['dow'] = df_chat['DATE'].dt.dayofweek
    df_chat['dom'] = df_chat['DATE'].dt.day
    df_chat['month'] = df_chat['DATE'].dt.month
    df_chat['HOUR'] = df_chat['HOUR'].apply(lambda hour: int(hour.split(':')[0]))
    df_chat['len_message'] = df_chat['MESSAGE'].apply(lambda msg: len(msg.split()))
    
    return df_chat

def text_normalizer(data : pd.DataFrame, language : str = 'english') -> str:
    """
    Normalize text data by converting it to lowercase, removing stopwords, URLs, 
    and diacritics, and preparing the text for further analysis.
    
    Parameters:
    - data (pd.DataFrame): The input DataFrame containing a 'MESSAGE' column with the text to normalize.
    - language (str): The language for the stopword list (default is 'english').
    
    Returns:
    - str: A string containing the normalized text.
    """
    assert isinstance(data, pd.DataFrame), "The 'data' must be a Pandas DataFrame"
    assert isinstance(language, str), "The 'language' must be a string"

    urlRegex = re.compile('http\S+') # URLs
    stopword_list = nltk.corpus.stopwords.words(language) # stopwords
    text = ' '.join([str(word) for word in ' '.join(data['MESSAGE']).lower().split() if word not in stopword_list]) # removing stopwords
    text = ' '.join([unidecode(str(word)) for word in text.split()]) # removing tildas
    text = ' '.join([str(word) for word in text.split() if not re.match(urlRegex, word)]) # removing URLs
    return text