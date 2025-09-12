"""Auxiliary functions."""

# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import json
import os
import re
import shutil
import psutil
import requests
from time import time
import logging
from functools import wraps
from typing import Any, Callable
import threading
from concurrent.futures import ThreadPoolExecutor
import tracemalloc

# --- Third-party ---
import pandas as pd
from flask import g, request
from unidecode import unidecode

# =============================================================================
# CONSTANTS
# =============================================================================
BASE_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(BASE_DIR)
LANG_PATH = os.path.join(PARENT_DIR, 'static', 'json', 'lang')

logger = logging.getLogger(__name__)

# =============================================================================
# FILES
# =============================================================================
def read_file(file_path: str) -> None:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def read_json(path: str) -> None:
    return json.load(open(path, 'r', encoding='utf-8'))

def write_file(content: str, file_name: str) -> None:
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(content)

def write_json(data: pd.DataFrame, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def write_txt(content: str, path: str) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def remove_temp_files(folders: str | list[str], files_to_remove: list[str] = None, protected_folders: list[str] = None) -> None:
    if isinstance(folders, str):
        folders = [folders]
    for folder in folders:
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path):
                        if files_to_remove and filename not in files_to_remove:
                            continue
                        os.remove(file_path)
                        print(f"Deleted file: {file_path}")
                    elif os.path.isdir(file_path):
                        if protected_folders and file_path in protected_folders:
                            continue
                        shutil.rmtree(file_path)
                        print(f"Deleted folder: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
        else:
            print(f"Folder does not exist: {folder}")

# =============================================================================
# TIME
# =============================================================================
def timed_run(func, *args, in_seconds: bool = False, decimals: int = 4, process_str: str = "", **kwargs):

    process = psutil.Process(os.getpid())
    get_time = lambda: time()
    get_memory = lambda: process.memory_info().rss / (1024 ** 2)
    delta = lambda after, before: after - before

    memory_before, time_before = get_memory(), get_time()
    result = func(*args, **kwargs)
    memory_after, time_after = get_memory(), get_time()
    memory_delta, time_delta = delta(memory_after, memory_before), delta(time_after, time_before)

    time_msg = f"{time_delta:.4f} seconds" if in_seconds else f"{time_delta / 60:.{decimals}f} minutes"
    print(f"{process_str} in {time_msg} and with {memory_delta:.4f} MB of memory used.")

    return result

def job_duration() -> str:
    days_per_month, days_per_year = 30, 365
    today, job_start_date = pd.Timestamp.now(), pd.Timestamp(2025, 2, 1)
    elapsed_days = (today - job_start_date).days

    years = elapsed_days // days_per_year if elapsed_days > days_per_year else 0
    months = int((elapsed_days - days_per_year) / days_per_month) if elapsed_days > days_per_year else int(elapsed_days / days_per_month) + 1

    year_text = "" if years == 0 else "year" if years == 1 else "years"
    month_text = "month" if months == 1 else "months"

    return f"{months} {month_text}" if years == 0 else f"{years} {year_text} {months} {month_text}"

# =============================================================================
# LANGUAGES
# =============================================================================
def load_texts(lang: str = 'english', section: str = None) -> dict:
    path = os.path.join('lang', f'{lang}.json') if os.path.exists(os.path.join('lang', f'{lang}.json')) else os.path.join(BASE_DIR, '..', 'static', 'json', 'lang', f'{lang}.json')
    return read_json(path).get(section, {}) if section else read_json(path)

def load_language_texts():
    g.lang = request.args.get('lang', 'english')
    g.texts = load_texts(g.lang, section='home')

def inject_texts_and_languages():
    available_langs = [f.split('.')[0] for f in os.listdir(LANG_PATH) if f.endswith('.json')]
    return dict(
        texts=getattr(g, 'texts', {}),
        selected_lang=getattr(g, 'lang', 'english'),
        available_langs=available_langs
    )

# =============================================================================
# TEXT
# =============================================================================
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

# =============================================================================
# TEST
# =============================================================================
def performance_analyzer(process_str=None):
    def decorator(fn):
        def wrapper(self, *args, **kwargs):
            name = process_str or fn.__name__
            return timed_run(lambda: fn(self, *args, **kwargs), process_str=name, in_seconds=True, decimals=1)
        return wrapper
    return decorator

# =============================================================================
# WORLD BANK API
# =============================================================================
def get_valid_countries() -> set:
    countries_set = set()
    url = 'https://api.worldbank.org/v2/country'
    params = {'format': 'json', 'per_page': 500}

    response = requests.get(url, params=params)
    data = response.json()

    if data and len(data) > 1:
        for country_data in data[1]:
            if country_data.get('region', {}).get('value') != 'Aggregates':
                countries_set.add(country_data['name'])
        return countries_set