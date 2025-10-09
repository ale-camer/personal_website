# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard Library ---
import re
import os
from datetime import datetime
from collections import Counter

# --- Third-party ---
from tqdm import tqdm

# --- Project ---
from modules.common.validations import WhatsappFileError
from modules.common.utils import read_json, text_normalizer

# =============================================================================
# GLOBAL CONSTANTS
# =============================================================================
_SPLIT_STR = r'^(\d{1,2}/\d{1,2}/\d{2,4}), ([^ ]+) - ([^:]+): (.+)$'
_SPLIT_PATTERN = re.compile(_SPLIT_STR)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))
STOPWORDS_PATH = os.path.join(PROJECT_ROOT, 'static', 'json', 'stopwords.json')
STOPWORDS = read_json(STOPWORDS_PATH)

# =============================================================================
# PRIVATE HELPERS
# =============================================================================
def _is_valid(line: str) -> bool:
    if not (m := _SPLIT_PATTERN.match(line)):
        return False
    if (msg := m.group(4).strip()).startswith("<") and msg.endswith(">"):
        return False
    return True

def _parse(line: str) -> tuple:
    match = _SPLIT_PATTERN.match(line)
    date_str, time_str, issuer, msg = map(str.strip, match.groups())
    date = datetime.strptime(date_str, "%d/%m/%Y")
    return (
        date, int(time_str[:2]), issuer, msg, date.weekday(), date.day,
        date.month, msg.count(" ") + 1,
    )

def _clean(data: list[str]) -> iter:
    for line in data:
        if _is_valid(line):
            yield _parse(line)

# =============================================================================
# PUBLIC INTERFACE
# =============================================================================
def parse_messages(data: list[str]) -> list:
    cleaned = list(tqdm(_clean(data), desc="Cleaning messages"))
    if not cleaned:
        raise WhatsappFileError("Invalid file format")
    return cleaned

def groupby_dict(data: list[tuple]) -> Counter:
    return Counter(
        key for row in tqdm(data, desc="Grouping data")
        for key in (
            f"{row[2]}_{row[1]}_{row[4]}_{row[5]}_{row[6]}",
            f"GENERAL_{row[1]}_{row[4]}_{row[5]}_{row[6]}",
        )
    )

def filter_chat(data: dict, issuer: str) -> tuple[dict, str, bool, str]:
    is_general = issuer == 'GENERAL'
    prefix = "GENERAL_" if is_general else f"{issuer}_"
    filtered_counts = {
        k: v for k, v in data.grouped_data.items() if k.startswith(prefix)
    }

    if is_general: msg = [row[3] for row in data.parsed_data]
    else: msg = [row[3] for row in data.parsed_data if row[2] == issuer]

    norm_text = text_normalizer(
        text=' '.join(msg), stopwords=STOPWORDS[data.language]
    )

    return filtered_counts, norm_text, is_general, msg