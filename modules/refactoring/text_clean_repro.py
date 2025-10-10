"""
PASOS

    1. armar funciones auxiliares a ejecutar en ambos procesos
    2. orquestarlas para que funcionen al codigo actual
    3. cambiar ejecucion actual por una homogenea
    4. VERIFICAR FLUJOS DE EJECUCION
"""

# =============================================================================
# REFACTOR (Gemini)
# =============================================================================
import re
import string
from unidecode import unidecode

EMOJI_PATTERN = r'[^\x00-\x7F]+'
LETTER_PATTERN = r'[^a-zA-Z]+'
LETTER_NUMBER_PATTERN = r'[^a-zA-Z0-9]+'
URL_PATTERN = re.compile(r'https?://\S+')

def clean_str(text: str, *, only_letters: bool = False) -> str:
    text = unidecode(text.lower())
    text = re.sub(EMOJI_PATTERN, '', text)
    pattern = LETTER_PATTERN if only_letters else LETTER_NUMBER_PATTERN
    return re.sub(pattern, ' ', text) # o ''?

def stopwords_check(t):
    return stopwords is not None and t in stopwords

def length_check(t):
    return len(t) < min_str_len

def urls_check(t):
    return URL_PATTERN.match(t)
    
def is_valid(
        text, 
        *,
        stopwords: set = None,
        min_str_len: int = 3,
        check_stopwords: bool = True,
        check_length: bool = True,
        check_urls: bool = True
    ) -> bool:
    checks = {
        "stopwords": (check_stopwords, stopwords_check),
        "length": (check_length, length_check),
        "urls": (check_urls, urls_check),
    }
    return not any(func(text) for act, func in checks.values() if act)

def normalize_strings(
        text: str, 
        *,
        stopwords: set = None,
        has_stream: bool = True,
        join_result: bool = False,
        clean_options: dict = None,
        valid_options: dict = None
    ) -> str | list[str] | iter:
    clean_opts = clean_options or {}
    valid_opts = valid_options or {}

    processed_tokens = (
        cleaned_word for word in text.split()
        if is_valid(word, stopwords=stopwords, **valid_opts)
        and (cleaned_word := clean_str(word, **clean_opts).strip())
        if cleaned_word # not empty
    )

    if join_result:
        return ' '.join(processed_tokens)
    return processed_tokens if has_stream else list(processed_tokens)

# =============================================================================
# REFACTOR
# =============================================================================
import re
import string
from unidecode import unidecode

EMOJI_PATTERN = r'[^\x00-\x7F]+'
LETTER_PATTERN = r'[^a-zA-Z]+'
LETTER_NUMBER_PATTERN = r'[^a-zA-Z0-9]+'
URL_PATTERN = r'https?://\S+'

def clean_str(
        text: str, *,
        only_letters: bool = False
    ) -> str:
    text = unidecode(text.lower()) # delete tildas
    text = re.sub(EMOJI_PATTERN, '', text) # delete emojis
    pattern = LETTER_PATTERN if only_letters else LETTER_NUMBER_PATTERN
    return re.sub(pattern, '', text) # delete patters

def is_valid(
        _str, *,
        stopwords: set = None,
        min_str_len: int = 4,
        pattern: str = URL_PATTERN,
        check_stopwords: bool = True,
        check_length: bool = True,
        check_urls: bool = True
    ) -> bool:

    if check_stopwords and stopwords is not None:
        if _str in stopwords:
            return False

    if check_length:
        if len(_str) < min_str_len:
            return False

    if check_urls and pattern is not None:
        if pattern.match(_str):
            return False

    return True

def normalize_strings(
        text: str, 
        stopwords: set = None, 
        *,
        has_stream: bool = True,
        join_result: bool = False
    ) -> str | list[str] | iter: # stopwords?

    processed_tokens = (
        ct for t in text.split() 
        if is_valid(t, stopwords)
        and (ct := clean_str(t))
    )
    
    if join_result:
        return ' '.join(processed_tokens)
    return processed_tokens if has_stream else list(processed_tokens)

# =============================================================================
# ORIGINAL
# =============================================================================
EMOJIS_PATTERN = r'[^\x00-\x7F]+'
ONLY_LETTERS_PATTERN = r'[^a-zA-Z]'
URL_PATTERN = r'http\S+'
PUNCTUATION_PATTERN = f"[{re.escape(string.punctuation)}]"
NON_NUMBER_PATTERN = r"\d+"

def text_normalizer(
        text: str, stopwords: set = None, min_word_len: int = 2
    ) -> str:
    def clean_word(word: str) -> str:
        word = re.sub(EMOJIS_PATTERN, '', word) # delete emojis
        word = unidecode(word) # delete tildas
        return re.sub(ONLY_LETTERS_PATTERN, '', word) # delete non letters

    def is_valid(text):
        return not (
            text in stopwords # delete stopwords
            or len(text) <= min_word_len # delete small words
            or delete_url.match(text) # delete urls
        )

    # execution
    def normalize_words(words):
        return [
            cw for word in words
            if is_valid(word) and (cw := clean_word(word))
        ]

    stopwords = stopwords if stopwords is not None else stopwords
    delete_url = re.compile(URL_PATTERN)
    return ' '.join(normalize_words(text.lower().split()))

class TextCleaner:

    def __init__(self, text: str, stopwords: set[str] = None):
        self.text = text
        self.stopwords = stopwords if stopwords is not None else set()

    def get_stopwords():
        pass

    def clean(
        self,
        has_stream: bool = True,
        to_lowercase: bool = True,
        rm_accents: bool = True,
        rm_punctuation: bool = False,
        rm_numbers: bool = False,
        filter_stopwords: bool = True,
        min_token_length: int = 3
    ) -> iter:

        text = self.text
        if to_lowercase: text = text.lower()
        if rm_accents: text = unidecode(text) # delete tildas
        if rm_punctuation: text = re.sub(self.PUNCTUATION_PATTERN, ' ', text) # delete punctuations
        if rm_numbers: text = re.sub(self.NON_NUMBER_PATTERN, ' ', text) # delete numbers

        # execution
        if has_stream:
            yield from (
                token for token in text.split()
                if len(token) > min_token_length # delete small words
                and not (filter_stopwords and token in self.stopwords) # delete stopwords
            )
        else:
            return [
                token for token in text.split()
                if len(token) > min_token_length
                and not (filter_stopwords and token in self.stopwords)
            ]