import pandas as pd
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io, re, nltk
import base64
from unidecode import unidecode
import textblob as tb

def sentiment_analysis(
        data : pd.DataFrame, 
        selected_issuer : str = None) -> go.Figure:
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

def preprocess_whatsapp_data(file) -> pd.DataFrame:
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
    
    for i in range(len(chat_lines)):
        if re.match(message_pattern, chat_lines[i]):
            if pending_lines:
                processed_lines[-1] = ' '.join(pending_lines)
                pending_lines = []
            processed_lines.append(chat_lines[i])
        else:
            if not pending_lines:
                pending_lines.append(chat_lines[i-1])
            pending_lines.append(chat_lines[i])
    
    df_chat = pd.DataFrame(processed_lines, columns=['RAW_DATA'])
    df_chat['DATE'] = df_chat['RAW_DATA'].apply(lambda x: x.split(',')[0])
    df_chat['HOUR'] = df_chat['RAW_DATA'].apply(lambda x: x.split(',')[1].split('-')[0].strip())
    df_chat['ISSUER'] = df_chat['RAW_DATA'].apply(lambda x: x.split('- ')[1].split(':')[0])
    df_chat['MESSAGE'] = df_chat['RAW_DATA'].apply(lambda x: x.split(': ')[1] if ': ' in x else None)
    
    df_chat = df_chat[df_chat['MESSAGE'].notna()]
    df_chat['IS_MULTIMEDIA'] = df_chat['MESSAGE'].apply(lambda msg: 1 if 'Multimedia' in msg else 0)
    df_chat = df_chat[df_chat['IS_MULTIMEDIA'] == 0].drop(['RAW_DATA', 'IS_MULTIMEDIA'], axis=1)
    
    df_chat['DATE'] = pd.to_datetime(df_chat['DATE'], dayfirst=True)
    df_chat['dow'] = df_chat['DATE'].dt.dayofweek
    df_chat['dom'] = df_chat['DATE'].dt.day
    df_chat['month'] = df_chat['DATE'].dt.month
    df_chat['HOUR'] = df_chat['HOUR'].apply(lambda hour: int(hour.split(':')[0]))
    df_chat['len_message'] = df_chat['MESSAGE'].apply(lambda msg: len(msg.split()))
    
    return df_chat

def text_normalizer(
        data : pd.DataFrame, 
        language : str = 'english') -> str:
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

    urlRegex = re.compile('http\S+')
    stopword_list = nltk.corpus.stopwords.words(language)
    text = ' '.join([str(word) for word in ' '.join(data['MESSAGE']).lower().split() if word not in stopword_list])
    text = ' '.join([unidecode(str(word)) for word in text.split()])
    text = ' '.join([str(word) for word in text.split() if not re.match(urlRegex, word)])
    return text