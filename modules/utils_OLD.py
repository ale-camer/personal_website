# """Auxiliary functions."""

# # =============================================================================
# # IMPORTS
# # =============================================================================
# # --- Standard library ---
# import json
# import os
# import re
# import shutil
# import psutil
# import requests
# from time import time
# import logging
# from functools import wraps
# from typing import Any, Callable
# import threading
# from concurrent.futures import ThreadPoolExecutor
# import tracemalloc

# # --- Third-party ---
# # import pandas as pd
# from flask import g, request
# from unidecode import unidecode

# # =============================================================================
# # CONSTANTS
# # =============================================================================
# BASE_DIR = os.path.dirname(__file__)
# PARENT_DIR = os.path.dirname(BASE_DIR)
# LANG_PATH = os.path.join(PARENT_DIR, 'static', 'json', 'lang')

# logger = logging.getLogger(__name__)

# # =============================================================================
# # FILES
# # =============================================================================
# def read_file(file_path: str) -> None:
#     with open(file_path, 'r', encoding='utf-8') as file:
#         return file.read()

# def read_json(path: str) -> None:
#     return json.load(open(path, 'r', encoding='utf-8'))

# def write_file(content: str, file_name: str) -> None:
#     with open(file_name, "w", encoding="utf-8") as f:
#         f.write(content)

# def write_json(data: pd.DataFrame, path: str) -> None:
#     os.makedirs(os.path.dirname(path), exist_ok=True)
#     with open(path, 'w', encoding='utf-8') as f:
#         json.dump(data, f, ensure_ascii=False, indent=2)

# def write_txt(content: str, path: str) -> None:
#     with open(path, 'w', encoding='utf-8') as f:
#         f.write(content)

# def remove_temp_files(folders: str | list[str], files_to_remove: list[str] = None, protected_folders: list[str] = None) -> None:
#     if isinstance(folders, str):
#         folders = [folders]
#     for folder in folders:
#         if os.path.exists(folder):
#             for filename in os.listdir(folder):
#                 file_path = os.path.join(folder, filename)
#                 try:
#                     if os.path.isfile(file_path):
#                         if files_to_remove and filename not in files_to_remove:
#                             continue
#                         os.remove(file_path)
#                         print(f"Deleted file: {file_path}")
#                     elif os.path.isdir(file_path):
#                         if protected_folders and file_path in protected_folders:
#                             continue
#                         shutil.rmtree(file_path)
#                         print(f"Deleted folder: {file_path}")
#                 except Exception as e:
#                     print(f"Error deleting {file_path}: {e}")
#         else:
#             print(f"Folder does not exist: {folder}")

# # =============================================================================
# # TIME
# # =============================================================================
# def timed_run(func, *args, in_seconds: bool = False, decimals: int = 4, process_str: str = "", **kwargs):

#     process = psutil.Process(os.getpid())
#     get_time = lambda: time()
#     get_memory = lambda: process.memory_info().rss / (1024 ** 2)
#     delta = lambda after, before: after - before

#     memory_before, time_before = get_memory(), get_time()
#     result = func(*args, **kwargs)
#     memory_after, time_after = get_memory(), get_time()
#     memory_delta, time_delta = delta(memory_after, memory_before), delta(time_after, time_before)

#     time_msg = f"{time_delta:.4f} seconds" if in_seconds else f"{time_delta / 60:.{decimals}f} minutes"
#     print(f"{process_str} in {time_msg} and with {memory_delta:.4f} MB of memory used.")

#     return result

# def job_duration() -> str:
#     days_per_month, days_per_year = 30, 365
#     today, job_start_date = pd.Timestamp.now(), pd.Timestamp(2025, 2, 1)
#     elapsed_days = (today - job_start_date).days

#     years = elapsed_days // days_per_year if elapsed_days > days_per_year else 0
#     months = int((elapsed_days - days_per_year) / days_per_month) if elapsed_days > days_per_year else int(elapsed_days / days_per_month) + 1

#     year_text = "" if years == 0 else "year" if years == 1 else "years"
#     month_text = "month" if months == 1 else "months"

#     return f"{months} {month_text}" if years == 0 else f"{years} {year_text} {months} {month_text}"

# # =============================================================================
# # LANGUAGES
# # =============================================================================
# def load_texts(lang: str = 'english', section: str = None) -> dict:
#     path = os.path.join('lang', f'{lang}.json') if os.path.exists(os.path.join('lang', f'{lang}.json')) else os.path.join(BASE_DIR, '..', 'static', 'json', 'lang', f'{lang}.json')
#     return read_json(path).get(section, {}) if section else read_json(path)

# def load_language_texts():
#     g.lang = request.args.get('lang', 'english')
#     g.texts = load_texts(g.lang, section='home')

# def inject_texts_and_languages():
#     available_langs = [f.split('.')[0] for f in os.listdir(LANG_PATH) if f.endswith('.json')]
#     return dict(
#         texts=getattr(g, 'texts', {}),
#         selected_lang=getattr(g, 'lang', 'english'),
#         available_langs=available_langs
#     )

# # =============================================================================
# # TEXT
# # =============================================================================
# def text_normalizer(text: str, stopwords: set = None, min_word_len: int = 2) -> str:

#     def _reduce_repeated_chars(text: str) -> str:
#         return re.sub(r'[^a-zA-Z0-9\s]', _count_rep_char, text)

#     def _count_rep_char(match: str) -> str:
#         return match.group(0)[0]

#     return transform_words(
#         text=_reduce_repeated_chars(text.lower()),
#         fn=unidecode,
#         condition=lambda w: (
#             w not in stopwords
#             and not re.compile(r'http\S+').match(w)
#             and len(w) > min_word_len
#         )
#     )

# def transform_words(text: str, fn=lambda x: x, condition=lambda x: True) -> str:
#     return ' '.join(fn(word) for word in text.split() if condition(word))

# # =============================================================================
# # TEST
# # =============================================================================
# def performance_analyzer(process_str=None):
#     def decorator(fn):
#         def wrapper(self, *args, **kwargs):
#             name = process_str or fn.__name__
#             return timed_run(lambda: fn(self, *args, **kwargs), process_str=name, in_seconds=True, decimals=1)
#         return wrapper
#     return decorator

# # =============================================================================
# # WORLD BANK API
# # =============================================================================
# def get_valid_countries() -> set:
#     countries_set = set()
#     url = 'https://api.worldbank.org/v2/country'
#     params = {'format': 'json', 'per_page': 500}

#     response = requests.get(url, params=params)
#     data = response.json()

#     if data and len(data) > 1:
#         for country_data in data[1]:
#             if country_data.get('region', {}).get('value') != 'Aggregates':
#                 countries_set.add(country_data['name'])
#         return countries_set
    
# # =============================================================================
# # REFACTORIZATION
# # =============================================================================

# import re, string
# from collections import defaultdict
# from unidecode import unidecode
# from zipfile import ZipFile as zipf
# import xml.etree.ElementTree as ET
# from prettytable import PrettyTable as pt
# from tabulate import tabulate
# from fpdf import FPDF

# def get_input(func, *args, **kwargs):
#     return func(*args, **kwargs)

# def get_chunks(iterable: iter, size: int = 100_000, start: int = 0) -> iter:
#     if not hasattr(iterable, "__iter__") or not hasattr(iterable, "__len__"):
#         raise TypeError("The 'iterable' input must be an iterable with length like a list or string")
#     if len(iterable) == 0:
#         raise ValueError("The 'iterable' input must have a length greater than zero")
#     if not isinstance(size, int) or size <= 0:
#         raise ValueError("The 'size' input must be a positive integer")

#     for i in range(start, len(iterable), size):
#         yield iterable[i : i + size]

# def read_txt(filename, encoding: str = "utf-8") -> str:
#     with open(filename, encoding=encoding) as f:
#         return f.read()

# def read_excel(xlsx_file: str) -> dict:

#     ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
#     rns = "{http://schemas.openxmlformats.org/package/2006/relationships}"
#     wb_path, rels_path, sst_path = "xl/workbook.xml", "xl/_rels/workbook.xml.rels", "xl/sharedStrings.xml"

#     def parse_item(item):
#         return ET.parse(item).getroot()

#     def parse_cell(c):
#         value_node, cell_type = c.find(f"{ns}v"), c.get("t")
#         raw_value = value_node.text if value_node is not None else None
#         if cell_type == "s" and raw_value is not None:
#             value = shared_strings[int(raw_value)]
#         else: value = raw_value
#         return {
#             "ref": c.get("r"), "type": cell_type or "n",
#             "value": value, "raw": raw_value,
#         }

#     with zipf(xlsx_file) as z:

#         shared_strings = []
#         if sst_path in z.namelist():
#             sst_root = parse_item(z.open(sst_path))
#             shared_strings = [si.find(f"{ns}t").text for si in sst_root.findall(f"{ns}si")]

#         sheets = {
#             s.get("name"): next(v for k, v in s.attrib.items() if k.endswith("id"))
#             for s in parse_item(z.open(wb_path)).find(f"{ns}sheets")
#         }

#         paths = {
#             r.get("Id"): "xl/" + r.get("Target")
#             for r in parse_item(z.open(rels_path)).findall(f"{rns}Relationship")
#         }

#         workbook_data = {}
#         for sheet_name, sheet_id in sheets.items():
#             root = parse_item(z.open(paths[sheet_id]))
#             workbook_data[sheet_name] = [
#                 parse_cell(c)
#                 for row in root.iter(f"{ns}row")
#                 for c in row.findall(f"{ns}c")
#             ]
#         return workbook_data

# class TextCleaner:

#     _PUNCTUATION_PATTERN = f"[{re.escape(string.punctuation)}]"
#     _NUMBERS_PATTERN = r"\d+"

#     def __init__(self, text: str, stopwords: set[str] = None):
#         self.text = text
#         self.stopwords = stopwords if stopwords is not None else set()

#     def get_stopwords():
#         pass

#     def clean(
#         self,
#         has_stream: bool = True,
#         to_lowercase: bool = True,
#         remove_accents: bool = True,
#         remove_punctuation: bool = False,
#         remove_numbers: bool = False,
#         filter_stopwords: bool = True,
#         min_token_length: int = 3
#     ) -> list[str]:

#         text = self.text
#         if to_lowercase: text = text.lower()
#         if remove_accents: text = unidecode(text)
#         if remove_punctuation: text = re.sub(self._PUNCTUATION_PATTERN, ' ', text)
#         if remove_numbers: text = re.sub(self._NUMBERS_PATTERN, ' ', text)

#         if has_stream:
#             yield from (
#                 token for token in text.split()
#                 if len(token) > min_token_length
#                 and not (filter_stopwords and token in self.stopwords)
#             )
#         else:
#             return [
#                 token for token in text.split()
#                 if len(token) > min_token_length
#                 and not (filter_stopwords and token in self.stopwords)
#             ]

# class FileTooLargeError(Exception):
#     pass

# def validate_upload_size(uploaded_file, limit_mb: int = 10):

#     def _get_file_size_mb(file) -> int:
#         size = file.content_length
#         if size is None:
#             file.seek(0, 2)
#             size = file.tell()
#             file.seek(0)
#         return size / (1024 * 1024)

#     file_size_mb = _get_file_size_mb(uploaded_file)
#     if file_size_mb > limit_mb:
#         raise FileTooLargeError(
#             f"The file is too big ({file_size_mb:.2f} MB). "
#             f"The limit is {limit_mb} MB."
#         )

# class FileExporter:
#     def __init__(self, results: dict, cols: list[str], filename: str):
#         self.results = results
#         self.cols = cols
#         self.filename = filename

#     # strings
#     def to_txt_string(self) -> str:
#         tables = []
#         for k, v in self.results.items():
#             table = pt(title=k, field_names=self.cols)
#             table.add_rows([[' '.join(ngram), count] for ngram, count in v])
#             tables.append(str(table))
#         return "\n\n".join(tables)

#     def to_md_string(self) -> str:
#         md_tables = []
#         for k, v in self.results.items():
#             table_data = [[' '.join(ngram), count] for ngram, count in v]
#             md_tables.append(f"## {k}\n" + tabulate(table_data, headers=self.cols, tablefmt="github"))
#         return "\n\n".join(md_tables)

#     # exports
#     def export_txt(self):
#         txt_string = self.to_txt_string()
#         with open(self.filename + '.txt', "w", encoding="utf-8") as f:
#             f.write(txt_string)
#         print(f"TXT saved as {self.filename + '.txt'}")

#     def export_md(self):
#         md_string = self.to_md_string()
#         with open(self.filename + '.md', "w", encoding="utf-8") as f:
#             f.write(md_string)
#         print(f"Markdown saved as {self.filename + '.md'}")

#     def export_pdf(self):
#         pdf = FPDF()
#         pdf.set_auto_page_break(auto=True, margin=15)
#         pdf.add_page()
#         pdf.set_font("Arial", "", 14)

#         for k, v in self.results.items():
#             pdf.cell(0, 10, k, ln=True)
#             pdf.set_font("Arial", "", 12)
#             # Encabezado de tabla
#             pdf.cell(80, 8, self.cols[0], border=1)
#             pdf.cell(30, 8, self.cols[1], border=1)
#             pdf.ln()
#             # Filas de tabla
#             for ngram, count in v:
#                 pdf.cell(80, 8, ' '.join(ngram), border=1)
#                 pdf.cell(30, 8, str(count), border=1)
#                 pdf.ln()
#             pdf.ln(5)

#         pdf.output(self.filename + '.pdf')
#         print(f"PDF saved as {self.filename + '.pdf'}")

# def get_first_sheet_name(data):
#     return list(data.keys())[0]

# def get_sheet_values(data, sheet_name):
#     return [d for d in data[sheet_name][0] if d is not None]

# def clean_excel_input(workbook_data: dict) -> dict:

#     def parse_ref(ref):
#         match = re.match(r"([A-Z]+)([0-9]+)", ref)
#         if match: col, row = match.groups(); return col, int(row)
#         return None, None

#     def build_cols_and_max(cells):
#         cols, max_row = defaultdict(dict), 0
#         for c in cells:
#             col, row = parse_ref(c["ref"])
#             if col is None or row is None:
#                 continue
#             cols[col][row] = c["value"]
#         return cols, max(max_row, row)

#     cleaned = {}
#     for sheet, cells in workbook_data.items():
#         cols, max_row = build_cols_and_max(cells)
#         cleaned[sheet] = [
#             [cols[col].get(row, None) for row in range(1, max_row + 1)]
#             for col in sorted(cols.keys())
#         ]

#     return cleaned

# def data_to_numeric(data):
#     return [float(d) for d in data]

# def get_mean(data: list) -> float:
#     return sum(data) / len(data)

# def groupby_lists(list1: list, list2: list) -> dict:
#     grouped = defaultdict(list)
#     for k, v in [(str(l1), l2) for l1, l2 in zip(list1, list2)]:
#         grouped[k].append(v)
#     return {k: get_mean(v) for k, v in grouped.items()}

# def multiply_lists(list1: list, list2: list) -> list:
#     return [l1 * l2 for l1, l2 in zip(list1, list2)]

# def divide_lists(list1: list, list2: list) -> list:
#     return [a / b for a, b in zip(list1, list2)]

# def rolling_mean(serie, window):
#     n, results = len(serie), []
#     for i in range(n - window + 1):
#         mean = sum(serie[i:i+window]) / window
#         results.append(mean)
#     return results