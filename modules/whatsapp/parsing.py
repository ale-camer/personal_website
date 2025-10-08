# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard Library ---
import re
from datetime import datetime
from collections import Counter

# --- Third-party ---
from tqdm import tqdm

# --- Project ---
from modules.common.validations import WhatsappFileError

# =============================================================================
# GLOBAL CONSTANTS
# =============================================================================
_SPLIT_STR = r'^(\d{1,2}/\d{1,2}/\d{2,4}), ([^ ]+) - ([^:]+): (.+)$'
_PARSE_STR = r".*/.*/,.*:.* - .*"
_SPLIT_PATTERN = re.compile(_SPLIT_STR)
_PARSE_PATTERN = re.compile(_PARSE_STR)

# =============================================================================
# PRIVATE HELPERS
# =============================================================================
def _is_valid(line: str) -> bool:
    if not (_PARSE_PATTERN.match(line) and (m := _SPLIT_PATTERN.match(line))):
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
