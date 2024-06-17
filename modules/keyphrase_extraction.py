import nltk
import pandas as pd
from tqdm import tqdm
from unidecode import unidecode
import re

def top_ngrams(corpus, ngram_val=1, limit=5, rows_per_table=5):
    assert isinstance(ngram_val, int), "The 'ngram_val' input must be an integer"
    assert isinstance(limit, int), "The 'limit' input must be an integer"

    def compute_ngrams(sequence, n):
        return list(zip(*(sequence[index:] for index in range(n))))

    def flatten_corpus(corpus):
        return ' '.join([document.strip() for document in corpus])
    
    corpus = flatten_corpus(corpus)
    tokens = nltk.word_tokenize(corpus)
    ngrams = compute_ngrams(tokens, ngram_val) 
    ngrams_freq_dist = nltk.FreqDist(ngrams)
    sorted_ngrams_fd = sorted(ngrams_freq_dist.items(), key=lambda x: x[1], reverse=True)
    sorted_ngrams = sorted_ngrams_fd[:limit]
    sorted_ngrams = [(' '.join(text), freq) for text, freq in sorted_ngrams]
    sorted_ngrams = sorted_ngrams[:rows_per_table]  # Limitamos el número de filas por tabla
    return pd.DataFrame(sorted_ngrams, columns=['Keywords', '# Appearances'])

def text_normalizer(data, language='english', minWordLen=2):
    assert isinstance(language, str), "The 'language' must be a string"
    assert isinstance(minWordLen, int), "The 'minWordLen' must be an integer"
        
    stopword_list = nltk.corpus.stopwords.words(language) 
    
    def conti_rep_char(str1):
        tchr = str1.group(0)
        if len(tchr) > 1:
          return tchr[0:1]
         
    def check_unique_char(rep, sent_text):
         convert = re.sub(r'[^a-zA-Z0-9\s]',rep,sent_text)
         return convert
     
    urlRegex = re.compile('http\S+')
    
    data = ' '.join([word for word in data.lower().split() if word not in stopword_list])
    data = check_unique_char(conti_rep_char, data)
    data = ' '.join([word for word in data.split() if not re.match(urlRegex, word)])
    data = ' '.join([word for word in data.split() if len(word) > minWordLen])
    data = ' '.join([unidecode(word) for word in data.split()])

    return data

def procesar_archivo(data, num_tables=5, num_rows=5):
    nltk.download('punkt', quiet=True)
    sentences = nltk.sent_tokenize(data)
    normalized_sentences = [text_normalizer(sentence) for sentence in tqdm(sentences)]

    results = {}
    for num in range(1, num_tables + 1):
        tempData = top_ngrams(corpus=normalized_sentences, ngram_val=num, limit=10, rows_per_table=num_rows)
        results[f"N-Gram Value: {num}"] = tempData
    return results
