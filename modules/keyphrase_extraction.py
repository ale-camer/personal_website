"""
Contain functions for Keyphrase Extraction functionality.
"""

import nltk, re
import pandas as pd
from tqdm import tqdm 
from unidecode import unidecode
from prettytable import PrettyTable

def pretty_table_for_keyphrases(data: pd.DataFrame, title: str, columns: list) -> PrettyTable:
    """Style dataframes"""
    table = PrettyTable()
    table.title = title
    table.field_names = columns
    for i in data.index:
      table.add_row([
        data.loc[i, columns[0]],
        data.loc[i, columns[1]]
      ])
    return table

def generate_keyphrases_tables_string(data: dict) -> str:
    """Generates all tables as a string."""
    result_string = ""
    for _key in list(data.keys()):
        df = pd.DataFrame(data[_key])
        table = pretty_table_for_keyphrases(df, _key, df.columns)
        result_string += str(table) + "\n\n"  # Add each table to the result string
    return result_string
  
def top_ngrams(
        corpus : list, 
        ngram_val : int = 1,
        limit : int = 5, 
        rows_per_table : int = 5
    ) -> pd.DataFrame:
    """
    Function to extract top n-grams from a corpus of text.
    
    Args:
    - corpus (list): List of strings where each string is a document or text.
    - ngram_val (int): Value of n for n-grams (default is 1 for unigrams).
    - limit (int): Number of top n-grams to retrieve.
    - rows_per_table (int): Number of rows per table in the output DataFrame.
    
    Returns:
    - DataFrame: DataFrame containing the top n-grams and their frequencies.
    """
    assert isinstance(corpus, list), "The 'corpus' input must be a list"
    assert isinstance(rows_per_table, int), "The 'rows_per_table' input must be an integer"
    assert isinstance(ngram_val, int), "The 'ngram_val' input must be an integer"
    assert isinstance(limit, int), "The 'limit' input must be an integer"

    def compute_ngrams(sequence, n):
        """Helper function to compute n-grams."""
        return list(zip(*(sequence[index:] for index in range(n))))

    def flatten_corpus(corpus):
        """Helper function to flatten a list of documents into a single string."""
        return ' '.join([document.strip() for document in corpus])
    
    corpus = flatten_corpus(corpus) # flattening
    tokens = nltk.word_tokenize(corpus)  # tokenizing
    ngrams = compute_ngrams(tokens, ngram_val)  # generating n-grams
    ngrams_freq_dist = nltk.FreqDist(ngrams)  # frequency distribution of n-grams
    sorted_ngrams_fd = sorted(ngrams_freq_dist.items(), key=lambda x: x[1], reverse=True)  # sorting n-grams by frequency
    sorted_ngrams = sorted_ngrams_fd[:limit]  # selecting top n-grams
    sorted_ngrams = [(' '.join(text), freq) for text, freq in sorted_ngrams]  # n-gram tokens to strings
    sorted_ngrams = sorted_ngrams[:rows_per_table]  # rows per table
    return pd.DataFrame(sorted_ngrams, columns=['Keywords', '# Appearances'])

def text_normalizer(
        data : str, 
        language : str = 'english', 
        minWordLen : int = 2
    ) -> str:
    """
    Function to normalize text data by removing stopwords, URLs, non-alphanumeric characters,
    and accents, and converting text to lowercase.
    
    Args:
    - data (str): Input text data to be normalized.
    - language (str): Language for stopwords (default is 'english').
    - minWordLen (int): Minimum word length to retain in the normalized text (default is 2).
    
    Returns:
    - str: Normalized text data.
    """
    assert isinstance(data, str), "The 'data' must be a string"
    assert isinstance(language, str), "The 'language' must be a string"
    assert isinstance(minWordLen, int), "The 'minWordLen' must be an integer"
        
    def conti_rep_char(str1):
        """Helper function to handle repeated characters."""
        tchr = str1.group(0)
        if len(tchr) > 1:
            return tchr[0:1]
         
    def check_unique_char(rep, sent_text):
        """Helper function to check for unique characters in the text."""
        convert = re.sub(r'[^a-zA-Z0-9\s]', rep, sent_text)
        return convert

    stopword_list = nltk.corpus.stopwords.words(language)  # stopwords
    urlRegex = re.compile(r'http\S+') # URLs
    
    data = ' '.join([word for word in data.lower().split() if word not in stopword_list]) # removing stopwords
    data = check_unique_char(conti_rep_char, data) # checking repeated characters
    data = ' '.join([word for word in data.split() if not re.match(urlRegex, word)]) # removing URLs
    data = ' '.join([word for word in data.split() if len(word) > minWordLen]) # removing short words
    data = ' '.join([unidecode(word) for word in data.split()]) # removing tildas

    return data

def process_file(
        data : str, 
        num_tables : int = 5,
        num_rows : int = 5
    ) -> dict:
    """
    Function to process a text file or string by tokenizing sentences, normalizing them,
    and generating top n-grams for each n value specified.
    
    Args:
    - data (str): Input text data to be processed.
    - num_tables (int): Number of n-gram tables to generate (default is 5).
    - num_rows (int): Number of rows per table in the output DataFrame (default is 5).
    
    Returns:
    - dict: Dictionary containing n-gram tables for each n value.
    """
    assert isinstance(data, str), "The 'data' must be a string"
    assert isinstance(num_tables, int), "The 'num_tables' must be an integer"
    assert isinstance(num_rows, int), "The 'num_rows' must be an integer"

    nltk.download('punkt', quiet=True) # punkt tokenizer
    sentences = nltk.sent_tokenize(data) # tokenizing
    normalized_sentences = [text_normalizer(sentence) for sentence in tqdm(sentences)] # normalizing
    
    results = {}
    for num in range(1, num_tables + 1):
        temp_data = top_ngrams(corpus=normalized_sentences, ngram_val=num, limit=10, rows_per_table=num_rows)
        results[f"N-Gram Value: {num}"] = temp_data # storing n-gram
    
    return results
