import pandas as pd

from dataclasses import dataclass
import re
from tqdm import tqdm
from datetime import datetime as dt

from utils import read_txt

@dataclass
class WhatsAppConfig:
    df: pd.DataFrame
    content: pd.DataFrame
    language: str

class WhatsAppParser:
    CHUNK_SIZE = 1_000_000
    RAW_DATA = 'RAW_DATA'
    DATE = 'DATE'
    HOUR = 'HOUR'
    ISSUER = 'ISSUER'
    MESSAGE = 'MESSAGE'
    COLS_TO_GROUP = ['HOUR', 'dow', 'dom', 'month']
    COLUMNS = [DATE, HOUR, ISSUER, MESSAGE, 'dow', 'dom', 'month', 'len_message']

    def __init__(self, file):
        self.file = file

    def group(self, df: pd.DataFrame) -> pd.DataFrame: # 2
        by_issuer = self._group_and_count(df, [self.ISSUER] + self.COLS_TO_GROUP)
        general = self._group_and_count(df, self.COLS_TO_GROUP).assign(ISSUER='GENERAL')
        return pd.concat([by_issuer, general], ignore_index=True)

    def _group_and_count(self, df: pd.DataFrame, group_columns: list) -> pd.DataFrame:
        return df.groupby(group_columns)[self.MESSAGE].count().reset_index()

class WhatsAppModule:
    ISSUER = 'ISSUER'

    def __init__(self):
        self.current_data = None

    def parse_chat(self, file, language: str) -> WhatsAppConfig:
        parser = WhatsAppParser(file)
        content = parser.parse()
        df = parser.group(content)
        self.current_data = WhatsAppConfig(df=df, content=content, language=language)
        return self.current_data

#%%

# CHUNK_SIZE = 1_000
# COLS_TO_GROUP = ['HOUR', 'dow', 'dom', 'month']
# ['DATE', 'HOUR', 'ISSUER', 'MESSAGE', 'dow', 'dom', 'month', 'len_message']

#%%

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
        date = dt.strptime(date, "%d/%m/%Y")
        return (
            date, int(time[:2]), issuer.strip(), msg.strip(),
            date.weekday(), date.day, date.month, msg.count(" ")+1
        )

    yield from (parse_line(d) for d in data if is_valid(d))

def parse_messages(data):
    MESSAGE = "Cleaning messages"
    return [msg for msg in tqdm(clean_message(data), desc=MESSAGE+"with list comp")]

data = read_txt("whatsapp_chat.txt").splitlines() * 500
cleaned_data = parse_messages(data)