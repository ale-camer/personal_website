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

def whatsapp_data_preprocessing(data):
    pattern = r".*\/.*\/.*,.*:.* - .*"
    general_list = []
    particular_list = []
    
    for i in range(len(data)):
        if re.match(pattern, data[i]):
            if particular_list:
                general_list[-1] = ' '.join(particular_list)
                particular_list = []
            general_list.append(data[i])
        else:
            if not particular_list:
                particular_list.append(data[i-1])
            particular_list.append(data[i])
    
    general_list = pd.DataFrame(general_list, columns=['DATA'])
    
    general_list['DATE'] = general_list['DATA'].apply(lambda x: x.split(',')[0])
    general_list['HOUR'] = general_list['DATA'].apply(lambda x: x.split(',')[1].split('-')[0].strip())
    general_list['ISSUER'] = general_list['DATA'].apply(lambda x: x.split('- ')[1].split(':')[0])
    general_list['MESSAGE'] = general_list['DATA'].apply(lambda x: x.split(': ')[1] if ': ' in x else 0)
    
    general_list = general_list[general_list['MESSAGE'] != 0]
    general_list['MULTIMEDIA'] = general_list['MESSAGE'].apply(lambda a: 1 if 'Multimedia' in a else 0)
    general_list = general_list.loc[general_list['MULTIMEDIA']==0,:].drop(['DATA','MULTIMEDIA'], axis=1)
    
    general_list['DATE'] = pd.to_datetime(general_list['DATE'], dayfirst=True)
    general_list['dow'] = general_list['DATE'].dt.dayofweek
    general_list['dom'] = general_list['DATE'].dt.day
    general_list['HOUR'] = general_list['HOUR'].apply(lambda a: a.split(':')[0]).astype('int')
    general_list['month'] = general_list['DATE'].dt.month
    general_list['len_message'] = general_list['MESSAGE'].apply(lambda a: len(a.split()))
    
    return general_list

def read_whatsapp_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def text_normalizer(data, language='english'):
    urlRegex = re.compile('http\S+')
    stopword_list = nltk.corpus.stopwords.words(language)
    text = ' '.join([str(word) for word in ' '.join(data['MESSAGE']).lower().split() if word not in stopword_list])
    text = ' '.join([unidecode(str(word)) for word in text.split()])
    text = ' '.join([str(word) for word in text.split() if not re.match(urlRegex, word)])
    return text