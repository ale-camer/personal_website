import itertools
from collections import deque, Counter

def get_top_ngrams(
        tokens_iterator: list[str], has_stream: bool = True, top_k: int = 3,
        max_n: int = 3
    ) -> dict:

    def ngram_generator(tokens):
        for token in tokens:
            window.append(token)
            if len(window) == n:
                yield tuple(window)

    if has_stream:
        results = {}
        for n in range(1, max_n + 1):
            window = deque(maxlen=n)
            current_tokens_iterator, tokens_iterator = itertools.tee(tokens_iterator)
            ngram_counts = Counter(ngram_generator(current_tokens_iterator))
            results[f"N-Gram Value: {n}"] = ngram_counts.most_common(top_k)
        return results

    else:
        return {
            f"N-Gram Value: {n}": Counter(
                tuple(tokens_iterator[i:i+n])
                for i in range(len(tokens_iterator)-n+1)
            ).most_common(top_k)
            for n in range(1, max_n + 1)
        }