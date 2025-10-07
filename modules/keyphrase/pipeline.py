from modules.common import utils as ut
from . import analyzer as an
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

def _clean_chunk(text_chunk: str) -> list[str]:
    return list(ut.TextCleaner(text_chunk).clean(has_stream=True))

def process(raw_text: str, progress: dict, chunk_size: int = 100_000) -> iter:

    progress["value"] = 0
    text_chunks = list(ut.get_chunks(raw_text, size=chunk_size))
    total_chunks = len(text_chunks)

    if not total_chunks:
        progress["value"] = 100
        return

    processed_count, lock = 0, threading.Lock()
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(_clean_chunk, chunk) for chunk in text_chunks]
        for future in as_completed(futures):
            token_list = future.result()

            with lock:
                processed_count += 1
            progress["value"] = int((processed_count / total_chunks) * 100)
            
            yield from token_list

def pipeline(raw_text: str, progress: dict, top_k: int, max_n: int) -> dict:

    token_iterator = process(raw_text, progress)
    raw_results = an.get_top_ngrams(
        tokens_iterator=token_iterator, top_k=top_k, max_n=max_n
    )

    return {
        label: [(" ".join(ngram), f"{count:,}") for ngram, count in data]
        for label, data in raw_results.items()
    }