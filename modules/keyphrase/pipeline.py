from . import core
import modules.common.utils as ut

import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

def _clean_chunk(text_chunk: str) -> list[str]:
    return list(ut.TextCleaner(text_chunk).clean(has_stream=True))

def process(raw_text: str, progress: dict, chunk_size: int = 100_000) -> iter:

    print("\nINITIATING TEXT PROCESSING")
    progress["value"] = 0
    text_chunks = list(ut.get_chunks(raw_text, size=chunk_size))
    total_chunks = len(text_chunks)
    print(f"Total chunks to process: {total_chunks}")

    if not total_chunks:
        progress["value"] = 100
        print("No chunks to process. Skipping.")
        return

    processed_count, lock = 0, threading.Lock()
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(_clean_chunk, chunk) for chunk in text_chunks]
        for future in as_completed(futures):
            token_list = future.result()

            with lock:
                processed_count += 1
                progress["value"] = int((processed_count / total_chunks) * 100)
                print(f"Processed chunk {processed_count}/{total_chunks} "
                      f"({progress['value']}%)")

            yield from token_list

def pipeline(raw_text: str, progress: dict, top_k: int, max_n: int) -> dict:

    print("\nINITIATING PIPELINE EXECUTION")
    print("Cleaning and tokenizing text")
    token_iterator = process(raw_text, progress)

    print("Extracting top n-grams")
    raw_results = core.get_top_ngrams(
        tokens_iterator=token_iterator, top_k=top_k, max_n=max_n
    )

    print("Formatting results")
    results = {
        label: [(" ".join(ngram), f"{count:,}") for ngram, count in data]
        for label, data in raw_results.items()
    }

    print("PIPELINE COMPLETED")
    return results
