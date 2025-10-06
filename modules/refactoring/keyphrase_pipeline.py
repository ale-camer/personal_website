# =============================================================================
# IMPORTS
# =============================================================================
from utils import TextCleaner, read_txt
from keyphrase import get_top_ngrams
from deployment import get_generic_output

# =============================================================================
# PIPELINE
# =============================================================================
def pipeline(data: str) -> dict:
    cleaned_data = TextCleaner(data).clean()
    return get_top_ngrams(cleaned_data)

def get_ngrams_output(results: dict, top_k: int = 3) -> dict:
    return {
        key: counter.most_common(top_k)
        for key, counter in get_generic_output(results).items()
    }

# =============================================================================
# PARAMETERS
# =============================================================================
input_params = {
    "func": read_txt,
    "filename": "whatsapp_chat.txt"
}

tester_params = {
    "worker": pipeline,
    "combine_fn": get_ngrams_output,
    "input_data": None
}