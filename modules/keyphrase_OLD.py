"""Contain functions for Keyphrases functionality."""

# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import re
import heapq
from operator import itemgetter
from itertools import islice, chain
from collections import Counter
from dataclasses import dataclass

# --- Third-party ---
import pandas as pd
from tqdm import tqdm
from prettytable import PrettyTable

# --- Project/system ---
from modules.utils import text_normalizer

# =============================================================================
# TOP NGRAMS
# =============================================================================
progress = {"value": 0}

@dataclass
class NGramConfig:
    data: str
    max_ngrams: int = 5
    num_nrows: int = 5
    chunk_size: int = int(1e6)

    @property
    def words(self) -> list:
        return self.data.split()

    @property
    def total_chunks(self) -> int:
        return (len(self.words) + self.chunk_size - 1) // self.chunk_size

class NGramAnalyzer:
    def __init__(self, config: NGramConfig):
        self.config = config
        self.url_regex = re.compile(r'http\S+')
        self._tokens = None

    def generate_ngrams(self) -> dict:
        self._tokens = list(chain.from_iterable(self._token_generator()))
        return self._build_ngram_tables()

    def _chunk_generator(self):
        for i in range(0, len(self.config.words), self.config.chunk_size):
            yield ' '.join(islice(self.config.words, i, i + self.config.chunk_size))

    def _token_generator(self):
        pbar = tqdm(self._chunk_generator(), total=self.config.total_chunks, desc="Normalizing sentences")
        for chunk in pbar:
            normalized = self._normalize_sentences(chunk)
            tokens = self._tokenize_corpus(normalized)
            progress["value"] = int(pbar.n / pbar.total * 100)
            yield tokens

    def _normalize_sentences(self, text: str) -> list:
        sentences = re.split(r'[.!?]\s+', text)
        return [text_normalizer(sentence, set()) for sentence in sentences]

    def _tokenize_corpus(self, sentences: list):
        for sentence in sentences:
            for word in re.findall(r'\b\w+\b', sentence.strip()):
                yield word

    def _build_ngram_tables(self) -> dict:
        tables = {}
        sliced_tokens = [self._tokens[i:] for i in range(self.config.max_ngrams)]
        
        for n in range(1, self.config.max_ngrams + 1):
            ngrams = zip(*sliced_tokens[:n])
            ngram_counts = Counter(ngrams)
            top_ngrams = heapq.nlargest(self.config.num_nrows, ngram_counts.items(), key=itemgetter(1))
            tables[f"N-Gram Value: {n}"] = pd.DataFrame(
                ((" ".join(ng), f"{freq:,}") for ng, freq in top_ngrams),
                columns=["Keywords", "# Appearances"]
            )
        return tables

class NGramModule:
    def __init__(self, raw_text: str, **kwargs):
        self.config = NGramConfig(data=raw_text, **kwargs)
        self.analyzer = NGramAnalyzer(self.config)
        self._ngram_tables = None

    def analyze(self) -> dict:
        self._ngram_tables = self.analyzer.generate_ngrams()
        return self._ngram_tables

    @property
    def summary(self) -> dict:
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