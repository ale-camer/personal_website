import nltk
import pandas as pd
from tqdm import tqdm  # For displaying progress bars
from unidecode import unidecode  # For removing accents from characters
import re  # For regular expressions

def top_ngrams(corpus, ngram_val=1, limit=5, rows_per_table=5):
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
    assert isinstance(ngram_val, int), "The 'ngram_val' input must be an integer"
    assert isinstance(limit, int), "The 'limit' input must be an integer"

    def compute_ngrams(sequence, n):
        """Helper function to compute n-grams."""
        return list(zip(*(sequence[index:] for index in range(n))))

    def flatten_corpus(corpus):
        """Helper function to flatten a list of documents into a single string."""
        return ' '.join([document.strip() for document in corpus])
    
    corpus = flatten_corpus(corpus)
    tokens = nltk.word_tokenize(corpus)  # Tokenize the flattened corpus
    ngrams = compute_ngrams(tokens, ngram_val)  # Generate n-grams
    ngrams_freq_dist = nltk.FreqDist(ngrams)  # Calculate frequency distribution of n-grams
    sorted_ngrams_fd = sorted(ngrams_freq_dist.items(), key=lambda x: x[1], reverse=True)  # Sort n-grams by frequency
    sorted_ngrams = sorted_ngrams_fd[:limit]  # Select top 'limit' n-grams
    sorted_ngrams = [(' '.join(text), freq) for text, freq in sorted_ngrams]  # Combine n-gram tokens into strings
    sorted_ngrams = sorted_ngrams[:rows_per_table]  # Limit the number of rows per table
    return pd.DataFrame(sorted_ngrams, columns=['Keywords', '# Appearances'])

def text_normalizer(data, language='english', minWordLen=2):
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
    assert isinstance(language, str), "The 'language' must be a string"
    assert isinstance(minWordLen, int), "The 'minWordLen' must be an integer"
        
    stopword_list = nltk.corpus.stopwords.words(language)  # Get list of stopwords for the specified language
    
    def conti_rep_char(str1):
        """Helper function to handle repeated characters."""
        tchr = str1.group(0)
        if len(tchr) > 1:
            return tchr[0:1]
         
    def check_unique_char(rep, sent_text):
        """Helper function to check for unique characters in the text."""
        convert = re.sub(r'[^a-zA-Z0-9\s]', rep, sent_text)
        return convert
     
    urlRegex = re.compile('http\S+')
    
    # Normalize the input text step by step
    data = ' '.join([word for word in data.lower().split() if word not in stopword_list])  # Remove stopwords
    data = check_unique_char(conti_rep_char, data)  # Handle repeated characters
    data = ' '.join([word for word in data.split() if not re.match(urlRegex, word)])  # Remove URLs
    data = ' '.join([word for word in data.split() if len(word) > minWordLen])  # Remove short words
    data = ' '.join([unidecode(word) for word in data.split()])  # Remove accents using unidecode

    return data

def procesar_archivo(data, num_tables=5, num_rows=5):
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
    nltk.download('punkt', quiet=True)  # Download NLTK punkt tokenizer
    
    sentences = nltk.sent_tokenize(data)  # Tokenize text into sentences
    normalized_sentences = [text_normalizer(sentence) for sentence in tqdm(sentences)]  # Normalize each sentence
    
    results = {}
    for num in range(1, num_tables + 1):
        tempData = top_ngrams(corpus=normalized_sentences, ngram_val=num, limit=10, rows_per_table=num_rows)
        results[f"N-Gram Value: {num}"] = tempData  # Store n-gram table in results dictionary
    
    return results  # Return the dictionary containing all n-gram tables
