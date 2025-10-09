"""
PROBLEMAS

    1. No esta incorpoado al principio sino a la demanda DONE
    2. No limpia correctamente

PASOS

    1. se consideran mensajes validos DONE
    2. se obtienen datos de estos para su conteo DONE
    3. se limpia el texto del mensaje
    4. se calcula sentimiento y nube de palabras
"""

import re, sys, os
from tqdm import tqdm
from datetime import datetime
from unidecode import unidecode
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from common.utils import read_txt, read_json
from common.validations import WhatsappFileError

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))
STOPWORDS_PATH = os.path.join(PROJECT_ROOT, 'static', 'json', 'stopwords.json')
STOPWORDS = read_json(STOPWORDS_PATH)["spanish"]

def text_normalizer(text: str, stopwords: set = None, min_word_len: int = 2) -> str:

    def clean_word(word: str) -> str:
        word = re.sub(r'[^\x00-\x7F]+', '', word) # remove non-ASCII / emojis
        word = unidecode(word) # remove tildes
        return re.sub(r'[^a-zA-Z]', '', word) # keep only letters

    def is_valid(text):
        return not (
            text in stopwords
            or len(text) <= min_word_len
            or delete_url.match(text)
        )

    def normalize_words(words):
        return [
            cw for word in words
            if is_valid(word) and (cw := clean_word(word))
        ]

    stopwords = stopwords if stopwords is not None else STOPWORDS
    delete_url = re.compile(r'http\S+')
    return ' '.join(normalize_words(text.lower().split()))

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

def parse_messages(data, stopwords: set = None):

    MESSAGE = "Cleaning messages"
    cleaned = [msg for msg in tqdm(clean_message(data), desc=MESSAGE)]
    if not cleaned:
        raise WhatsappFileError("Invalid file format")

    normalized = []
    for row in cleaned:
        date, hour, issuer, msg, weekday, day, month, word_count = row
        msg_norm = text_normalizer(msg, stopwords=stopwords)
        normalized.append((date, hour, issuer, msg_norm, weekday, day, month, word_count))

    return normalized

data = read_txt("whatsapp_chat.txt").splitlines() # lectura
cleaned_data = parse_messages(data) # limpieza
print(f"Primeros diez mensajes: {[c[3] for c in cleaned_data[:10]]}")