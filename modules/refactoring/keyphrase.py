import re, heapq, os, json
from tqdm import tqdm
from operator import itemgetter
from unidecode import unidecode
from collections import Counter
from itertools import islice, chain
from dataclasses import dataclass

import pandas as pd

_progress = {"value": 0}

def read_txt(filename, encoding: str = "utf-8") -> str:
    with open(filename, encoding=encoding) as f:
        return f.read()

def write_json(data: pd.DataFrame, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def text_normalizer(text: str, stopwords: set = None, min_word_len: int = 2) -> str:

    def _reduce_repeated_chars(text: str) -> str:
        return re.sub(r'[^a-zA-Z0-9\s]', _count_rep_char, text)

    def _count_rep_char(match: str) -> str:
        return match.group(0)[0]

    return transform_words(
        text=_reduce_repeated_chars(text.lower()),
        fn=unidecode,
        condition=lambda w: (
            w not in stopwords
            and not re.compile(r'http\S+').match(w)
            and len(w) > min_word_len
        )
    )

def transform_words(text: str, fn=lambda x: x, condition=lambda x: True) -> str:
    return ' '.join(fn(word) for word in text.split() if condition(word))

@dataclass
class NGramConfig:
    data: str
    max_ngrams: int = 3
    num_nrows: int = 3
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

    def generate_ngrams(self) -> dict: # 1
        self._tokens = list(chain.from_iterable(self._token_generator()))
        return self._build_ngram_tables()

    def _token_generator(self): # 2.1 DONE
        pbar = tqdm(self._chunk_generator(), total=self.config.total_chunks, desc="Normalizing sentences")
        for chunk in pbar:
            normalized = self._normalize_sentences(chunk)
            tokens = self._tokenize_corpus(normalized)
            _progress["value"] = int(pbar.n / pbar.total * 100)
            yield tokens

    def _chunk_generator(self): # 2.1.1 DONE
        for i in range(0, len(self.config.words), self.config.chunk_size):
            yield ' '.join(islice(self.config.words, i, i + self.config.chunk_size))

    def _normalize_sentences(self, text: str) -> list: # 2.1.2 DONE
        sentences = re.split(r'[.!?]\s+', text)
        return [text_normalizer(sentence, set()) for sentence in sentences]

    def _tokenize_corpus(self, sentences: list): # 2.1.3 DONE
        for sentence in sentences:
            for word in re.findall(r'\b\w+\b', sentence.strip()):
                yield word

    def _build_ngram_tables(self) -> dict: # 2.2
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

data = read_txt("whatsapp_chat.txt")
# results = NGramAnalyzer(NGramConfig(data)).generate_ngrams()

"""
tengo que generar una clase que me limpie los datos y otra que me genere los ngrams, teniendo en cuenta
potenciales problemas de dimensionalidad.

la funcion que genera los chunks puede ser algo generico y que vaya mas alla de los strings.

una vez esto, hacer un analisis de complejidad y paralelizacion.
"""


class Ngrams:

    def __init__(self, data, stopwords=[], chunk_size=1_000_000, max_n=3, top_k=3):
        self.data = data
        self.stopwords = stopwords
        self.chunk_size = chunk_size
        self.max_n = max_n
        self.top_k = top_k
        self.cleaned_tokens = []

    def string_chunks(self):
        tokens = self.data.split()
        for i in range(0, len(tokens), self.chunk_size):
            yield ' '.join(tokens[i : i + self.chunk_size])

    def cleaning(self, chunk):
        return [
            s for s in unidecode(chunk.lower()).split()
            if len(s) > 3 and s not in self.stopwords
        ]

    def process_chunks(self):
        for chunk in self.string_chunks():
            self.cleaned_tokens.extend(self.cleaning(chunk))

    def top_ngrams(self):
        return {
            f"N-Gram Value: {n}": Counter(
                tuple(self.cleaned_tokens[i:i+n])
                for i in range(len(self.cleaned_tokens)-n+1)
            ).most_common(self.top_k)
            for n in range(1, self.max_n + 1)
        }

    def run(self):
        self.process_chunks()
        return self.top_ngrams()

# results = Ngrams(data).run()

# whatsapp_pattern = r'(\d{1,2}/\d{1,2}/\d{4}, \d{2}:\d{2} .*?)(?=\d{1,2}/\d{1,2}/\d{4}, \d{2}:\d{2}|$)'
# whatsapp_chunk = re.findall(whatsapp_pattern, clean_chunk)
# print(whatsapp_chunk)

import timeit

t1 = timeit.timeit('NGramAnalyzer(NGramConfig(data)).generate_ngrams()', globals=globals(), number=1)
t2 = timeit.timeit('Ngrams(data).run()', globals=globals(), number=1)

print()
print(f"Clase 1 promedio: {t1/3:.4f} segundos")
print(f"Clase 2 promedio: {t2/3:.4f} segundos")
