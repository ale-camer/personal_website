import re
from tqdm import tqdm
from datetime import datetime
from collections import Counter

from utils import read_txt

def clean_message(data: str) -> iter:

    SPLIT_STR = r'^(\d{1,2}/\d{1,2}/\d{2,4}), ([^ ]+) - ([^:]+): (.+)$'
    PARSE_STR = r".*\/.*\/.*,.*:.* - .*"

    def is_valid(line: str) -> bool:
        generic_match = re.compile(PARSE_STR).match(line)
        specific_match = re.compile(SPLIT_STR).match(line)

        if not (generic_match and specific_match):
            return False

        _, _, _, msg = specific_match.groups()
        if msg.strip().startswith('<') and msg.strip().endswith('>'):
            return False
        return True

    def parse_line(line: str) -> tuple:
        generic_match = re.compile(SPLIT_STR).match(line)
        date, time, issuer, msg = generic_match.groups()
        date = datetime.strptime(date, "%d/%m/%Y")
        return (
            date, int(time[:2]), issuer.strip(), msg.strip(),
            date.weekday(), date.day, date.month, msg.count(" ")+1
        )

    yield from (parse_line(d) for d in data if is_valid(d))

class WhatsappFileError(Exception):
    pass

def parse_messages(data):
    MESSAGE = "Cleaning messages"
    cleaned = [msg for msg in tqdm(clean_message(data), desc=MESSAGE)]
    if not cleaned:
        raise WhatsappFileError("Invalid file format")
    return cleaned

def groupby_dict(data):
    return Counter(
        f"{prefix}{'_'.join(str(row[i]) for i in idxs)}"
        for row in tqdm(data, desc="Grouping data")
        for prefix, idxs in [("", [2,1,4,5,6]), ("GENERAL_", [1,4,5,6])]
    )

# data = read_txt("whatsapp_chat.txt").splitlines()
# cleaned_data = parse_messages(data)
# grouped_data = groupby_dict(cleaned_data)
