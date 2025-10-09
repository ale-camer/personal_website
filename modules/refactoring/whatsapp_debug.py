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

import re
from tqdm import tqdm
from datetime import datetime
from unidecode import unidecode

from utils import read_txt

class WhatsappFileError(Exception):
    pass

def text_normalizer(text: str, stopwords: set = None, min_word_len: int = 2) -> str:

    def _reduce_repeated_chars(text: str) -> str:
        return re.sub(r'[^a-zA-Z0-9\s]', _count_rep_char, text)

    def _count_rep_char(match: str) -> str:
        return match.group(0)[0]

    return transform_words(
        text=_reduce_repeated_chars(text.lower()),
        fn=unidecode,
        condition=lambda w: (
            w not in stopwords
            and not re.compile(r'http\S+').match(w)
            and len(w) > min_word_len
        )
    )

def transform_words(text: str, fn=lambda x: x, condition=lambda x: True) -> str:
    return ' '.join(fn(word) for word in text.split() if condition(word))

def clean_message(data: str) -> iter:
    """
    si es valido:
        1. tiene patron de mensaje o
        2. tiene mas de una linea
        3. no es multimedia

    se devuelven datos del mensaje
    """
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

def parse_messages(data):
    """ ejecucion de limpieza """
    MESSAGE = "Cleaning messages"
    cleaned = [msg for msg in tqdm(clean_message(data), desc=MESSAGE)]
    if not cleaned:
        raise WhatsappFileError("Invalid file format")
    return cleaned


data = read_txt("whatsapp_chat.txt").splitlines() # lectura
cleaned_data = parse_messages(data) # limpieza

print(f"Primeros diez mensajes: {[c[3] for c in cleaned_data[:10]]}")

