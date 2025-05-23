"""Contain functions for Keyphrases functionality."""

# --- Standard library ---
import re

# --- Third-party ---
import nltk
import pandas as pd
from prettytable import PrettyTable
from tqdm import tqdm

# --- Project/system ---
from modules.utils import text_normalizer, transform_words

class NGramAnalyzer:
    """
    Class for analyzing n-grams in text, including extraction and formatting
    of key phrases based on frequency.
    """
    
    def __init__(self, language: str = 'english'):
        """
        Initializes the n-gram analyzer.
        
        Args:
            language (str): Language for stopwords (default: 'english')
        """
        nltk.download('punkt', quiet=True)
        self.url_regex = re.compile(r'http\S+')
        self.stopwords = set(nltk.corpus.stopwords.words(language))
    
    def text_to_ngrams(self, data: str, max_ngram: int = 5, num_rows: int = 5) -> dict:
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
        return self._generate_ngram_tables(self._normalize_sentences(data), max_ngram, num_rows)
    
    def _normalize_sentences(self, text: str) -> list:
        """
        Tokenize and normalize each sentence from the input text.
      
        Args:
            text (str): Raw input text.
      
        Returns:
            list: List of normalized sentences.
        """
        return [
            text_normalizer(sentence, self.stopwords) 
            for sentence in tqdm(nltk.sent_tokenize(text))
        ]
    
    def _generate_ngram_tables(self, sentences: list, max_ngram: int, nrows_per_table: int) -> dict:
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
            f"N-Gram Value: {n}": self._top_ngrams(
                corpus=sentences, 
                ngram_val=n, 
                limit=10, 
                nrows=nrows_per_table
            )
            for n in range(1, max_ngram + 1)
        }
    
    def _top_ngrams(self, corpus: list[str], ngram_val: int = 1, limit: int = 10, nrows: int = 5) -> pd.DataFrame:
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
        tokens = nltk.word_tokenize(self._flatten_corpus(corpus))
        ngrams_freq = nltk.FreqDist(self._compute_ngrams(tokens, ngram_val))
        return self._format_top_ngrams(ngrams_freq, limit, nrows)
    
    def _flatten_corpus(self, corpus: list[str]) -> str:
        """
        Flatten a list of strings into a single string, joining with spaces.
      
        Args:
            corpus (list[str]): List of sentences or documents.
      
        Returns:
            str: Single concatenated string.
        """
        return transform_words('  '.join(corpus), fn=lambda w: w.strip())
        
    def _compute_ngrams(self, tokens: list[str], n: int) -> list[tuple]:
        """
        Generate n-gram tuples from a list of tokens.
      
        Args:
            tokens (list[str]): List of tokens (words).
            n (int): Size of n-grams.
      
        Returns:
            list[tuple]: List of n-gram tuples.
        """
        return list(zip(*(tokens[i:] for i in range(n))))
    
    def _format_top_ngrams(self, ngrams_freq: dict[tuple, int], limit: int, nrows: int) -> pd.DataFrame:
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

def text_to_ngrams(data: str, max_ngram: int = 5, num_rows: int = 5) -> dict:
    """
    Wrapper function to maintain compatibility with existing code.
    Creates an instance of NGramAnalyzer and performs the analysis.
    
    Args:
        data (str): Input text to analyze.
        max_ngram (int, optional): Maximum size of n-grams (default is 5).
        num_rows (int, optional): Number of top n-grams to include (default is 5).
    
    Returns:
        dict: Dictionary with n-gram tables.
    """
    analyzer = NGramAnalyzer()
    return analyzer.text_to_ngrams(data, max_ngram, num_rows)

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