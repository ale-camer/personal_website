from unidecode import unidecode
import re, string

def get_chunks(iterable: iter, size: int = 100_000, start: int = 0) -> iter:
    if not hasattr(iterable, "__iter__") or not hasattr(iterable, "__len__"):
        raise TypeError("The 'iterable' input must be an iterable with length like a list or string")
    if len(iterable) == 0:
        raise ValueError("The 'iterable' input must have a length greater than zero")
    if not isinstance(size, int) or size <= 0:
        raise ValueError("The 'size' input must be a positive integer")

    for i in range(start, len(iterable), size):
        yield iterable[i : i + size]

def read_txt(filename, encoding: str = "utf-8") -> str:
    with open(filename, encoding=encoding) as f:
        return f.read()

class TextCleaner:

    _PUNCTUATION_PATTERN = f"[{re.escape(string.punctuation)}]"
    _NUMBERS_PATTERN = r"\d+"

    def __init__(self, text: str, stopwords: set[str] = None):
        self.text = text
        self.stopwords = stopwords if stopwords is not None else set()

    def get_stopwords():
        pass

    def clean(
        self,
        has_stream: bool = True,
        to_lowercase: bool = True,
        remove_accents: bool = True,
        remove_punctuation: bool = False,
        remove_numbers: bool = False,
        filter_stopwords: bool = True,
        min_token_length: int = 3
    ) -> list[str]:

        text = self.text
        if to_lowercase: text = text.lower()
        if remove_accents: text = unidecode(text)
        if remove_punctuation: text = re.sub(self._PUNCTUATION_PATTERN, ' ', text)
        if remove_numbers: text = re.sub(self._NUMBERS_PATTERN, ' ', text)

        if has_stream:
            yield from (
                token for token in text.split()
                if len(token) > min_token_length
                and not (filter_stopwords and token in self.stopwords)
            )
        else:
            return [
                token for token in text.split()
                if len(token) > min_token_length
                and not (filter_stopwords and token in self.stopwords)
            ]

class FileTooLargeError(Exception):
    pass

def validate_upload_size(uploaded_file, limit_mb: int = 10):

    def _get_file_size_mb(file) -> int:
        size = file.content_length
        if size is None:
            file.seek(0, 2)
            size = file.tell()
            file.seek(0)
        return size / (1024 * 1024)

    file_size_mb = _get_file_size_mb(uploaded_file)
    if file_size_mb > limit_mb:
        raise FileTooLargeError(
            f"The file is too big ({file_size_mb:.2f} MB). "
            f"The limit is {limit_mb} MB."
        )