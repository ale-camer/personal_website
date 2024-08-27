import pandas as pd
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io, re, nltk
import base64
from unidecode import unidecode
import textblob as tb

def sentiment_analysis(data, selected_issuer=None):
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

def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color ='white').generate(text)
    img = io.BytesIO()
    wordcloud.to_image().save(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"

def preprocess_whatsapp_data(file):
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

def text_normalizer(data, language='english'):
    urlRegex = re.compile('http\S+')
    stopword_list = nltk.corpus.stopwords.words(language)
    text = ' '.join([str(word) for word in ' '.join(data['MESSAGE']).lower().split() if word not in stopword_list])
    text = ' '.join([unidecode(str(word)) for word in text.split()])
    text = ' '.join([str(word) for word in text.split() if not re.match(urlRegex, word)])
    return text