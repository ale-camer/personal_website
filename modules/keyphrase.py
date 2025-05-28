"""Contain functions for Keyphrases functionality."""

# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import re

# --- Third-party ---
import nltk
import pandas as pd
from prettytable import PrettyTable
from tqdm import tqdm

# --- Project/system ---
from dataclasses import dataclass
from modules.utils import text_normalizer, transform_words

# =============================================================================
# TOP NGRAMS
# =============================================================================
@dataclass
class NGramConfig:
    data: str
    max_ngrams: int = 5
    num_nrows: int = 5

class NGramAnalyzer:
    
    def __init__(self, language: str = 'english'):
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        self.url_regex = re.compile(r'http\S+')
        self.stopwords = set(nltk.corpus.stopwords.words(language))
    
    def analyze(self, config: NGramConfig) -> dict:
        normalized_sentences = self._normalize_sentences(config.data)
        return self._build_ngram_tables(
          normalized_sentences, 
          config.max_ngrams, 
          config.num_nrows
        )
      
    def _normalize_sentences(self, text: str) -> list:
        return [
            text_normalizer(sentence, self.stopwords) 
            for sentence in tqdm(nltk.sent_tokenize(text))
        ]
    
    def _build_ngram_tables(self, sentences: list, max_ngram: int, nrows_per_table: int) -> dict:
        return {
            f"N-Gram Value: {n}": self._get_top_ngrams(
                corpus=sentences, 
                ngram_val=n, 
                limit=10, 
                nrows=nrows_per_table
            )
            for n in range(1, max_ngram + 1)
        }
    
    def _get_top_ngrams(self, corpus: list[str], ngram_val: int = 1, limit: int = 10, nrows: int = 5) -> pd.DataFrame:
        tokens = nltk.word_tokenize(self._flatten_sentences(corpus))
        ngrams_freq = nltk.FreqDist(self._generate_ngrams(tokens, ngram_val))
        return self._format_ngrams_table(ngrams_freq, limit, nrows)
    
    def _flatten_sentences(self, corpus: list[str]) -> str:
        return transform_words('  '.join(corpus), fn=lambda w: w.strip())
        
    def _generate_ngrams(self, tokens: list[str], n: int) -> list[tuple]:
        return list(zip(*(tokens[i:] for i in range(n))))
    
    def _format_ngrams_table(self, ngrams_freq: dict[tuple, int], limit: int, nrows: int) -> pd.DataFrame:
        top_ngrams = sorted(ngrams_freq.items(), key=lambda x: x[1], reverse=True)[:limit]
        top_ngrams_formatted = [(' '.join(ngram), freq) for ngram, freq in top_ngrams][:nrows]
        return pd.DataFrame(top_ngrams_formatted, columns=['Keywords', '# Appearances'])

class NGramModule:
    def __init__(self, raw_text: str, max_ngrams: int = 5, num_nrows: int = 5):
        self.config = NGramConfig(data=raw_text, max_ngrams=max_ngrams, num_nrows=num_nrows)
        self.analyzer = NGramAnalyzer()
        self._ngram_tables = None

    def analyze(self) -> None:
        self._ngram_tables = self.analyzer.analyze(self.config)
        return self._ngram_tables

    @property
    def summary(self) -> dict:
        if self._ngram_tables is None:
            raise RuntimeError("Must call `analyze()` before accessing the summary.")
        return {
            ngram_label: df.to_dict(orient='records')
            for ngram_label, df in self._ngram_tables.items()
        }

# =============================================================================
# DOWNLOAD TOP NGRAMS
# =============================================================================
def get_tables_string(data: dict) -> str:
    return "\n\n".join(
        str(_create_table(df, title, df.columns.tolist()))
        for title, records in data.items()
        for df in [pd.DataFrame(records)]
    ) + "\n\n"
  
def _create_table(df: pd.DataFrame, title: str, cols: list) -> PrettyTable:
    table = PrettyTable(field_names=cols)
    table.title = title
    table.add_rows(df[cols].values.tolist())
    return table