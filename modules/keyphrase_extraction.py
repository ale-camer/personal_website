import re
import nltk
import pandas as pd
from tqdm import tqdm
from unidecode import unidecode   
from prettytable import PrettyTable

# =============================================================================
# TOP NGRAMS
# =============================================================================
nltk.download('punkt', quiet=True)
URL_REGEX = re.compile(r'http\S+')
STOPWORDS = set(nltk.corpus.stopwords.words('english'))

def text_to_ngrams(data: str, max_ngram: int = 5, num_rows: int = 5) -> dict:
    """
    Generate top n-gram frequency tables from input text.
  
    Args:
        data (str): Input text to analyze.
        max_ngram (int, optional): Maximum size of n-grams (default is 5).
        num_rows (int, optional): Number of top n-grams to include per n-gram table (default is 5).
  
    Returns:
        dict: Dictionary where keys are n-gram size descriptions and values are DataFrames 
              with top n-grams and their frequencies.
    """
    return _generate_ngram_tables(_normalize_sentences(data), max_ngram, num_rows)

def _normalize_sentences(text: str) -> list:
    """
    Tokenize and normalize each sentence from the input text.
  
    Args:
        text (str): Raw input text.
  
    Returns:
        list: List of normalized sentences.
    """
    return [_text_normalizer(sentence) for sentence in tqdm(nltk.sent_tokenize(text))]

def _generate_ngram_tables(sentences: list, max_ngram: int, nrows_per_table: int) -> dict:
    """
    Generate n-gram frequency tables for n from 1 to max_ngram.
  
    Args:
        sentences (list): List of normalized sentences.
        max_ngram (int): Maximum size of n-grams to generate.
        nrows_per_table (int): Number of top n-grams to return per table.
  
    Returns:
        dict: Dictionary mapping n-gram description to DataFrame of top n-grams.
    """
    return {
        f"N-Gram Value: {n}": _top_ngrams(
            corpus=sentences, 
            ngram_val=n, 
            limit=10, 
            nrows=nrows_per_table
        )
        for n in range(1, max_ngram + 1)
    }

def _top_ngrams(corpus: list[str], ngram_val: int = 1, limit: int = 10, nrows: int = 5) -> pd.DataFrame:
    """
    Compute and format the top n-grams from a corpus.
  
    Args:
        corpus (list[str]): List of normalized sentences.
        ngram_val (int, optional): Size of the n-grams (default 1).
        limit (int, optional): Number of n-grams to consider before slicing (default 10).
        nrows (int, optional): Number of rows to return in the DataFrame (default 5).
  
    Returns:
        pd.DataFrame: DataFrame with columns ['Keywords', '# Appearances'] showing top n-grams.
    """
    tokens = nltk.word_tokenize(_flatten_corpus(corpus))
    ngrams_freq = nltk.FreqDist(_compute_ngrams(tokens, ngram_val))
    return _format_top_ngrams(ngrams_freq, limit, nrows)

def _flatten_corpus(corpus: list[str]) -> str:
    """
    Flatten a list of strings into a single string, joining with spaces.
  
    Args:
        corpus (list[str]): List of sentences or documents.
  
    Returns:
        str: Single concatenated string.
    """
    return _transform_words('  '.join(corpus), fn=lambda w: w.strip())
    
def _compute_ngrams(tokens: list[str], n: int) -> list[tuple]:
    """
    Generate n-grams tuples from a list of tokens.
  
    Args:
        tokens (list[str]): List of tokens (words).
        n (int): Size of n-grams.
  
    Returns:
        list[tuple]: List of n-gram tuples.
    """
    return list(zip(*(tokens[i:] for i in range(n))))

def _format_top_ngrams(ngrams_freq: dict[tuple, int], limit: int, nrows: int) -> pd.DataFrame:
    """
    Format the top n-grams frequency dictionary into a DataFrame.
  
    Args:
        ngrams_freq (dict[tuple, int]): Frequency distribution of n-grams.
        limit (int): Number of top n-grams to consider.
        nrows (int): Number of rows to include in the resulting DataFrame.
  
    Returns:
        pd.DataFrame: DataFrame with top n-grams and their counts.
    """
    top = sorted(ngrams_freq.items(), key=lambda x: x[1], reverse=True)[:limit]
    top_formatted = [(' '.join(ngram), freq) for ngram, freq in top][:nrows]
    return pd.DataFrame(top_formatted, columns=['Keywords', '# Appearances'])
    
def _text_normalizer(text: str, stopwords: set = STOPWORDS, min_word_len: int = 2) -> str:
    """
    Normalize text by lowering case, removing stopwords, URLs, and short words,
    and applying Unicode normalization.
  
    Args:
        text (str): Input text to normalize.
        stopwords (set, optional): Set of stopwords to remove (default is STOPWORDS).
        min_word_len (int, optional): Minimum word length to keep (default is 2).
  
    Returns:
        str: Normalized text.
    """
    return _transform_words(
        text=_reduce_repeated_chars(text.lower()),
        fn=unidecode,
        condition=lambda w: (
            w not in stopwords
            and not URL_REGEX.match(w)
            and len(w) > min_word_len
        )
    )

def _transform_words(text: str, fn=lambda x: x, condition=lambda x: True) -> str:
    """
    Apply a transformation function to words in a string if they satisfy a condition.
  
    Args:
        text (str): Input text.
        fn (callable, optional): Function to apply to each word (default is identity).
        condition (callable, optional): Predicate to filter words (default always True).
  
    Returns:
        str: Transformed and filtered text as a string.
    """
    return ' '.join(fn(word) for word in text.split() if condition(word))

def _reduce_repeated_chars(text: str) -> str:
    """
    Replace sequences of repeated non-alphanumeric characters with a single character.
  
    Args:
        text (str): Input text.
  
    Returns:
        str: Text with reduced repeated characters.
    """
    return re.sub(r'[^a-zA-Z0-9\s]', _count_rep_char, text)

def _count_rep_char(match) -> str:
    """
    Return a single character from a regex match group of repeated characters.
  
    Args:
        match (re.Match): Regex match object.
  
    Returns:
        str: Single character string from the matched group.
    """
    return match.group(0)[0]
 
# =============================================================================
# PRINT TOP NGRAMS
# =============================================================================
def get_tables_string(data: dict) -> str:
    """
    Generate a formatted string with pretty tables for each dataset in a dictionary.
  
    Each key-value pair in the dictionary is converted to a PrettyTable with the key 
    as the title and the value (list of records) as the table content.
  
    Args:
        data (dict): Dictionary where keys are table titles and values are lists of records.
  
    Returns:
        str: A string with all tables formatted, separated by double newlines.
    """
    return "\n\n".join(
        str(_create_table(df, title, df.columns.tolist()))
        for title, records in data.items()
        for df in [pd.DataFrame(records)]
    ) + "\n\n"
  
def _create_table(df: pd.DataFrame, title: str, cols: list) -> PrettyTable:
    """
    Create a PrettyTable from a DataFrame with a given title and columns.
  
    Args:
        df (pd.DataFrame): DataFrame containing the table data.
        title (str): Title to display above the table.
        cols (list): List of column names to include in the table.
  
    Returns:
        PrettyTable: Formatted table object ready for printing or conversion to string.
    """
    table = PrettyTable(field_names=cols)
    table.title = title
    table.add_rows(df[cols].values.tolist())
    return table
  