import re, nltk, random
import numpy as np
import pandas as pd
from unidecode import unidecode
from textblob import TextBlob as tb

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from wordcloud import WordCloud

def whatsapp_data_preprocessing(data):
    """
    Preprocesses WhatsApp chat data.

    Args:
    - data (list): List of strings representing WhatsApp chat lines.

    Returns:
    - pandas.DataFrame: Processed DataFrame with columns DATE, HOUR, ISSUER, MESSAGE, dow, dom, month, len_message.
    """
    # Pattern to identify new messages
    pattern = r".*\/.*\/.*,.*:.* - .*"
    general_list = []
    particular_list = []
    
    for i in range(len(data)):
        if re.match(pattern, data[i]):
            if particular_list:
                # Join the collected multi-line message and add it to general_list
                general_list[-1] = ' '.join(particular_list)
                particular_list = []  # Clear the particular list for new messages
            general_list.append(data[i])
        else:
            # Collect lines that are part of the same message
            if not particular_list:
                particular_list.append(data[i-1])  # Include the previous line which has the timestamp
            particular_list.append(data[i])
    
    # Convert the list to a DataFrame
    general_list = pd.DataFrame(general_list, columns=['DATA'])
    
    # Extract date, time, sender, and message
    general_list['DATE'] = general_list['DATA'].apply(lambda x: x.split(',')[0])
    general_list['HOUR'] = general_list['DATA'].apply(lambda x: x.split(',')[1].split('-')[0].strip())
    general_list['ISSUER'] = general_list['DATA'].apply(lambda x: x.split('- ')[1].split(':')[0])
    general_list['MESSAGE'] = general_list['DATA'].apply(lambda x: x.split(': ')[1] if ': ' in x else 0)
    
    # Filter out rows with invalid messages
    general_list = general_list[general_list['MESSAGE'] != 0]
    general_list['MULTIMEDIA'] = general_list['MESSAGE'].apply(lambda a: 1 if 'Multimedia' in a else 0)
    general_list = general_list.loc[general_list['MULTIMEDIA']==0,:].drop(['DATA','MULTIMEDIA'], axis=1)
    
    # Preprocessing
    general_list['DATE'] = pd.to_datetime(general_list['DATE'], dayfirst=True)
    general_list['dow'] = general_list['DATE'].dt.dayofweek
    general_list['dom'] = general_list['DATE'].dt.day
    general_list['HOUR'] = general_list['HOUR'].apply(lambda a: a.split(':')[0]).astype('int')
    general_list['month'] = general_list['DATE'].dt.month
    general_list['len_message'] = general_list['MESSAGE'].apply(lambda a: len(a.split()))
    
    return general_list

def read_whatsapp_txt(file_path):
    """
    Reads a WhatsApp chat text file.

    Args:
    - file_path (str): File path to the WhatsApp chat text file.

    Returns:
    - list: List of strings representing lines from the WhatsApp chat file.
    """
    # Read the WhatsApp chat file and return lines
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def text_normalizer(data, language='english'):
    """
    Normalizes text by removing stopwords, URLs, and converting to lowercase.

    Args:
    - data (pandas.DataFrame): DataFrame containing WhatsApp message data.
    - language (str): Language for stopwords (default is 'english').

    Returns:
    - str: Normalized text as a single string.
    """
    urlRegex = re.compile('http\S+')
    stopword_list = nltk.corpus.stopwords.words(language)
    text = ' '.join([word for word in ' '.join(data['MESSAGE']).lower().split() if word not in stopword_list])
    text = ' '.join([unidecode(word) for word in text.split()])
    text = ' '.join([word for word in text.split() if not re.match(urlRegex, word)])
    return text

def graphs_time_unit(data, title="distribution of messages by time units".upper(),
                     agg_func='count', col='MESSAGE', ylabel='# MESSAGES', name=''):
    """
    Generates time unit-based distribution plots for WhatsApp chat data.

    Args:
    - data (pandas.DataFrame): DataFrame containing WhatsApp message data.
    - title (str): Title of the plot.
    - agg_func (str): Aggregation function for grouping (default is 'count').
    - col (str): Column to aggregate (default is 'MESSAGE').
    - ylabel (str): Label for the y-axis.
    - name (str): Name suffix for saving the plot image.

    Returns:
    - None
    """
    variables = ['HOUR','dow','dom','month']
    names = ['HOUR','DAY OF THE WEEK','DAY OF THE MONTH','MONTH']
    days_of_the_week = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday',
                        5:'Saturday', 6:'Sunday'}
    months = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June',
              7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 
              12:'December'}
    
    palette = sns.color_palette("husl", n_colors=len(data[variables[0]].unique()))
    plt.figure(figsize=(15,10))
    for var, i, name_ in zip(variables, range(len(variables)), names):
        
        df = data.groupby(var)[col].apply(agg_func).reset_index()
        if var == 'dow': df[var] = df[var].map(days_of_the_week)
        elif var == 'month': df[var] = df[var].map(months)
        else: pass
    
        plt.subplot(2,2,i+1)
        if df[var].dtype == 'object': 
            sns.barplot(data=df, x=var, y=col, palette=palette)
            plt.legend([], [], frameon=False)
        else: 
            sns.barplot(data=df, x=var, y=col, palette=palette)
            plt.legend([], [], frameon=False)

        plt.ylabel(ylabel.upper(), fontsize=15)
        plt.xlabel(name_, fontsize=15)
        plt.xticks(rotation=15)
        
    plt.suptitle(title, fontsize=20)
    plt.savefig(f'static/temp_images/graphs_time_unit_{name}.png')
    plt.close()

def graphs_donuts(data, name=''): 
    """
    Generates donut charts for message and word distributions based on WhatsApp chat data.

    Args:
    - data (pandas.DataFrame): DataFrame containing WhatsApp message data.
    - name (str): Name suffix for saving the plot image.

    Returns:
    - None
    """
    def random_distinct_color():
        h = random.random()  # Tone
        s = random.uniform(0.5, 0.9)  # Saturation
        v = random.uniform(0.6, 0.9)  # Value

        return mcolors.to_hex(mcolors.hsv_to_rgb((h, s, v)))

    # Calculate percentages
    df_messages = data.groupby('ISSUER')['MESSAGE'].count().reset_index().sort_values('MESSAGE', ascending=False)
    df_messages['MESSAGE'] = df_messages['MESSAGE'] / df_messages['MESSAGE'].sum() * 100
    labels_messages = df_messages['ISSUER'].unique()
    colors_messages = [random_distinct_color() for _ in range(len(labels_messages))]
    sizes_messages = np.round(df_messages['MESSAGE'].values, 2)
    labels_messages = [f'{label} - {size}%' for label, size in zip(labels_messages, sizes_messages)]
    
    df_words = data.groupby('ISSUER')['len_message'].sum().reset_index().sort_values('len_message', ascending=False)
    df_words['len_message'] = df_words['len_message'] / df_words['len_message'].sum() * 100
    labels_words = df_words['ISSUER'].unique()
    colors_words = [random_distinct_color() for _ in range(len(labels_words))]
    sizes_words = np.round(df_words['len_message'].values, 2)
    labels_words = [f'{label} - {size}%' for label, size in zip(labels_words, sizes_words)]
    
    # Create subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot for proportion of messages per person
    wedges1, texts1 = ax1.pie(
        df_messages['MESSAGE'], colors=colors_messages, startangle=90, wedgeprops={'width': 0.3})
    ax1.axis('equal')
    ax1.set_title('Proportion of Messages per Person'.upper())
    ax1.legend(wedges1, labels_messages, title="Persons", loc="center left",
               bbox_to_anchor=(1, 0, 0.5, 1))
    
    # Plot for proportion of words per person
    wedges2, texts2 = ax2.pie(
        df_words['len_message'], colors=colors_words, startangle=90, wedgeprops={'width': 0.3})
    ax2.axis('equal')
    ax2.set_title('Proportion of Words per Person'.upper())
    ax2.legend(wedges2, labels_words, title="Persons", loc="center left",
               bbox_to_anchor=(1, 0, 0.5, 1))
    
    # Adjust layout and save the plot
    plt.tight_layout()
    plt.savefig(f'static/temp_images/graphs_donuts_{name}.png')
    plt.close()

def sentiment_analysis(data, title='Sentiment Analysis', xlabel='', x=None, name=''):
    """
    Performs sentiment analysis on WhatsApp chat data and generates a violin plot.

    Args:
    - data (pandas.DataFrame): DataFrame containing WhatsApp message data.
    - title (str): Title of the plot.
    - xlabel (str): Label for the x-axis.
    - x (str): Column name for grouping (e.g., 'ISSUER').
    - name (str): Name suffix for saving the plot image.

    Returns:
    - None
    """
    data['score'] = data['MESSAGE'].apply(lambda a: tb(a.replace('\n',' ')).sentiment.polarity)
    if data[data['score']!=0].shape[0] == 0:
        return None
    else:
        mean_score = round(data['score'].mean()*100, 2)
        
        plt.figure(figsize=(12, 8))
        sns.violinplot(data=data, x=x, y='score', palette="husl")
        
        # Add text with the average polarity value
        plt.text(0.05, 0.9, f'Mean Polarity: {mean_score:.2f}%',
                 fontsize=17, ha='left', va='bottom', bbox=dict(facecolor='white', alpha=0.5))
        
        plt.title(title, fontsize=20)
        plt.xlabel(xlabel)
        plt.ylabel('Polarity', fontsize=15)
        plt.xticks(rotation=15)
        plt.ylim(-1, 1)
        plt.tight_layout()
        plt.savefig(f'static/temp_images/sentiment_analysis_{name}.png')
        plt.close()

def generate_wordcloud(text, title='Word Cloud'.upper(), name=''):
    """
    Generates a word cloud from text.

    Args:
    - text (str): Input text for generating the word cloud.
    - title (str): Title of the word cloud plot.
    - name (str): Name suffix for saving the plot image.

    Returns:
    - None
    """
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title, fontsize=20)
    plt.savefig(f'static/temp_images/generate_wordcloud_{name}.png')
    plt.close()
