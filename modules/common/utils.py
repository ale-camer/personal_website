# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import json
import os
import re
import shutil
import psutil
import xml.etree.ElementTree as ET
import zipfile as zf
from time import time
from datetime import datetime as dt
from collections import defaultdict
from zipfile import ZipFile as zipf

# --- Third-party ---
from flask import g, request
from unidecode import unidecode
from prettytable import PrettyTable as pt
from fpdf import FPDF

# =============================================================================
# CONSTANTS
# =============================================================================
BASE_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))
LANG_PATH = os.path.join(PROJECT_ROOT, 'static', 'json', 'lang')
LANG_OPTIONS_PATH = os.path.join(LANG_PATH, 'lang_options.json')

# =============================================================================
# FILE I/O - BASIC
# =============================================================================
def read_file(file_path: str) -> None:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def read_txt(filename, encoding: str = "utf-8") -> str:
    with open(filename, encoding=encoding) as f:
        return f.read()

def read_json(path: str) -> None:
    return json.load(open(path, 'r', encoding='utf-8'))

def write_file(content: str, file_name: str) -> None:
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(content)

def write_txt(content: str, path: str) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def write_json(data, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_texts(lang: str = 'english', section: str = None) -> dict:
    path = os.path.join(LANG_PATH, f'{lang}.json')
    if not os.path.exists(path):
        raise FileNotFoundError(f"No se encontró el archivo de idioma: {path}")
    data = read_json(path)
    return data.get(section, {}) if section else data

def remove_temp_files(
        folders: str | list[str], files_to_remove: list[str] = None, 
        protected_folders: list[str] = None
    ) -> None:
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
# FILE I/O - EXCEL
# =============================================================================
def read_excel(xlsx_file: str) -> dict:
    ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    rns = "{http://schemas.openxmlformats.org/package/2006/relationships}"
    wb_path = "xl/workbook.xml"
    rels_path  = "xl/_rels/workbook.xml.rels"
    sst_path = "xl/sharedStrings.xml"

    def parse_item(item):
        return ET.parse(item).getroot()

    def parse_cell(c):
        value_node, cell_type = c.find(f"{ns}v"), c.get("t")
        raw_value = value_node.text if value_node is not None else None
        if cell_type == "s" and raw_value is not None:
            value = shared_strings[int(raw_value)]
        else: value = raw_value
        return {
            "ref": c.get("r"), "type": cell_type or "n",
            "value": value, "raw": raw_value,
        }

    with zipf(xlsx_file) as z:
        shared_strings = []
        if sst_path in z.namelist():
            sst_root = parse_item(z.open(sst_path))
            shared_strings = [
                si.find(f"{ns}t").text for si in sst_root.findall(f"{ns}si")
            ]

        sheets = {
            s.get("name"): next(v for k, v in s.attrib.items() if k.endswith("id"))
            for s in parse_item(z.open(wb_path)).find(f"{ns}sheets")
        }

        paths = {
            r.get("Id"): "xl/" + r.get("Target")
            for r in parse_item(z.open(rels_path)).findall(f"{rns}Relationship")
        }

        workbook_data = {}
        for sheet_name, sheet_id in sheets.items():
            root = parse_item(z.open(paths[sheet_id]))
            workbook_data[sheet_name] = [
                parse_cell(c)
                for row in root.iter(f"{ns}row")
                for c in row.findall(f"{ns}c")
            ]
        return workbook_data

def get_first_sheet_name(data):
    return list(data.keys())[0]

def get_sheet_values(data, sheet_name):
    return [d for d in data[sheet_name][0] if d is not None]

def clean_excel_input(workbook_data: dict) -> dict:
    def parse_ref(ref):
        match = re.match(r"([A-Z]+)([0-9]+)", ref)
        if match: col, row = match.groups(); return col, int(row)
        return None, None

    def build_cols_and_max(cells):
        cols, max_row = defaultdict(dict), 0
        for c in cells:
            col, row = parse_ref(c["ref"])
            if col is None or row is None:
                continue
            cols[col][row] = c["value"]
        return cols, max(max_row, row)

    cleaned = {}
    for sheet, cells in workbook_data.items():
        cols, max_row = build_cols_and_max(cells)
        cleaned[sheet] = [
            [cols[col].get(row, None) for row in range(1, max_row + 1)]
            for col in sorted(cols.keys())
        ]

    return cleaned

# =============================================================================
# FILE EXPORT
# =============================================================================
def export_zip(save_dir, filename: str = 'predictions.zip'):
    zip_path = os.path.join(save_dir, filename)
    with zf.ZipFile(zip_path, 'w', zf.ZIP_DEFLATED) as f:
        for root, _, files in os.walk(save_dir):
            for file in files:
                if file != filename:
                    file_path = os.path.join(root, file)
                    f.write(file_path, os.path.relpath(file_path, save_dir))
    return zip_path, filename

def make_markdown_table(headers, rows):
    # Convierte todos los valores a string
    rows = [[str(cell) for cell in row] for row in rows]
    headers = [str(h) for h in headers]

    # Calcula el ancho máximo de cada columna
    widths = [max(len(row[i]) for row in [headers] + rows) for i in range(len(headers))]

    # Función para formatear una fila
    def fmt_row(row):
        return "| " + " | ".join(f"{cell:<{widths[i]}}" for i, cell in enumerate(row)) + " |"

    # Arma la tabla Markdown tipo GitHub
    header_line = fmt_row(headers)
    separator_line = "| " + " | ".join("-" * w for w in widths) + " |"
    data_lines = [fmt_row(r) for r in rows]

    return "\n".join([header_line, separator_line] + data_lines)

class FileExporter:
    def __init__(self, results_data: dict, cols: list[str]):
        self.results = results_data
        self.cols = cols

    def to_txt_string(self) -> str:
        tables = []
        for title, data in self.results.items():
            table = pt(title=title, field_names=self.cols)
            table.add_rows(data)
            tables.append(str(table))
        return "\n\n".join(tables)

    def to_md_string(self) -> str:
        md_tables = []
        for title, data in self.results.items():
            md_tables.append(
                f"## {title}\n" + make_markdown_table(self.cols, data)
                )
        return "\n\n".join(md_tables)

    def to_pdf_bytes(self) -> bytes:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        for title, data in self.results.items():
            pdf.set_font("Arial", size=14, style='B')
            pdf.cell(0, 10, title, ln=True, align='L')
            pdf.ln(2)

            for row in data:
                pdf.set_font("Arial", size=11)
                
                keyword_label = self.cols[0]
                keyword_value = row[0]
                
                count_label = self.cols[1]
                count_value = str(row[1])

                pdf.multi_cell(0, 7, f"{keyword_label}: {keyword_value}")
                pdf.multi_cell(0, 7, f"{count_label}: {count_value}")
                
                pdf.ln(3)

            pdf.ln(8)

        return pdf.output(dest='S').encode('latin-1')

# =============================================================================
# TEXT PROCESSING
# =============================================================================
EMOJI_PATTERN = r'[^\x00-\x7F]+'
LETTER_PATTERN = r'[^a-zA-Z]+'
LETTER_NUMBER_PATTERN = r'[^a-zA-Z0-9]+'
URL_PATTERN = re.compile(r'https?://\S+')

def clean_str(text: str, *, only_letters: bool = False) -> str:
    text = re.sub(EMOJI_PATTERN, '', text)
    text = unidecode(text.lower())
    pattern = LETTER_PATTERN if only_letters else LETTER_NUMBER_PATTERN
    return re.sub(pattern, '', text)
  
def is_valid(
        text, 
        *,
        stopwords: set = None,
        min_str_len: int = 3,
        check_stopwords: bool = True,
        check_length: bool = True,
        check_urls: bool = True
    ) -> bool:

    def stopwords_check(t):
        return stopwords is not None and t in stopwords

    def length_check(t):
        return len(t) < min_str_len

    def urls_check(t):
        return URL_PATTERN.match(t)

    checks = {
        "stopwords": (check_stopwords, stopwords_check),
        "length": (check_length, length_check),
        "urls": (check_urls, urls_check),
    }
    return not any(func(text) for act, func in checks.values() if act)

def normalize_strings(
        text: str, 
        *,
        stopwords: set = None,
        has_stream: bool = True,
        join_result: bool = False,
        clean_options: dict = None,
        valid_options: dict = None
    ) -> "str | list[str] | iter":
    clean_opts = clean_options or {}
    valid_opts = valid_options or {}

    processed_tokens = (
        cleaned_word for word in text.split()
        if is_valid(word, stopwords=stopwords, **valid_opts)
        and (cleaned_word := clean_str(word, **clean_opts).strip())
        if cleaned_word # not empty
    )

    if join_result:
        return ' '.join(processed_tokens)
    return processed_tokens if has_stream else list(processed_tokens)

# =============================================================================
# DATA PROCESSING
# =============================================================================
def get_chunks(iterable: iter, size: int = 100_000, start: int = 0) -> iter:
    if not hasattr(iterable, "__iter__") or not hasattr(iterable, "__len__"):
        raise TypeError(
            (
            "The 'iterable' input must be an iterable with,"
            " length like a list or string"
            )
        )
    if len(iterable) == 0:
        raise ValueError(
            (
                "The 'iterable' input must have a length greater ", 
                "than zero"
            )
        )
    if not isinstance(size, int) or size <= 0:
        raise ValueError("The 'size' input must be a positive integer")

    for i in range(start, len(iterable), size):
        yield iterable[i : i + size]

def data_to_numeric(data):
    return [float(d) for d in data]

def get_mean(data: list) -> float:
    return sum(data) / len(data)

def groupby_lists(list1: list, list2: list) -> dict:
    grouped = defaultdict(list)
    for k, v in [(str(l1), l2) for l1, l2 in zip(list1, list2)]:
        grouped[k].append(v)
    return {k: get_mean(v) for k, v in grouped.items()}

def multiply_lists(list1: list, list2: list) -> list:
    return [l1 * l2 for l1, l2 in zip(list1, list2)]

def divide_lists(list1: list, list2: list) -> list:
    return [a / b for a, b in zip(list1, list2)]

def rolling_mean(serie, window):
    n, results = len(serie), []
    for i in range(n - window + 1):
        mean = sum(serie[i:i+window]) / window
        results.append(mean)
    return results

# =============================================================================
# TIME & PERFORMANCE
# =============================================================================
def timed_run(
        func, *args, in_seconds: bool = False, decimals: int = 4, 
        process_str: str = "", **kwargs
    ):
    process = psutil.Process(os.getpid())
    get_time = lambda: time()
    get_memory = lambda: process.memory_info().rss / (1024 ** 2)
    delta = lambda after, before: after - before

    memory_before, time_before = get_memory(), get_time()
    result = func(*args, **kwargs)
    memory_after, time_after = get_memory(), get_time()
    memory_delta = delta(memory_after, memory_before)
    time_delta = delta(time_after, time_before)

    if in_seconds: time_msg = f"{time_delta:.4f} seconds" 
    else: time_msg = f"{time_delta / 60:.{decimals}f} minutes"    
    msg_to_print = (
        f"{process_str} in {time_msg} "
        f"and with {memory_delta:.4f} MB of memory used."
    )
    print(msg_to_print)

    return result

def job_duration() -> str:

    def calculate_months(days: int) -> int:
        if days > days_per_year:
            return int((days - days_per_year) / days_per_month)
        return int(days / days_per_month) + 1
    
    def calculate_years(days: int) -> int:
        if days > days_per_year:
            return days // days_per_year
        return 0
        
    def get_duration():
        if years == 0:
            return f"{months} {month_text}"
        return f"{years} {year_text} {months} {month_text}"
    
    days_per_month, days_per_year = 30, 365
    today, job_start_date = dt.now(), dt(2025, 2, 1)
    elapsed_days = (today - job_start_date).days

    years = calculate_years(elapsed_days)
    months = calculate_months(elapsed_days)

    year_text = "" if years == 0 else "year" if years == 1 else "years"
    month_text = "month" if months == 1 else "months"
    duration = get_duration()
    return duration

# =============================================================================
# FLASK UTILITIES
# =============================================================================
LANG_OPTIONS = read_json(LANG_OPTIONS_PATH)

def load_language_texts():
    default_lang = list(LANG_OPTIONS.keys())[0]
    g.lang = request.args.get('lang', default_lang)
    g.texts = load_texts(g.lang)

def inject_texts_and_languages():
    available_lang_codes = [
        f.split('.')[0] for f in os.listdir(LANG_PATH) 
        if f.endswith('.json') and f != 'lang_options.json'
    ]
    language_options_to_render = dict(
        ((code, LANG_OPTIONS[code]) 
         for code in available_lang_codes 
         if code in LANG_OPTIONS)
    )
    default_lang = next(iter(LANG_OPTIONS))
    print(default_lang)
    return {
        'texts': getattr(g, 'texts', {}),
        'selected_lang': getattr(g, 'lang', default_lang),
        'language_options': language_options_to_render
    }

# =============================================================================
# UTILITIES
# =============================================================================
def get_input(func, *args, **kwargs):
    return func(*args, **kwargs)

def load_dotenv(path=".env"):
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#"):
                continue
            key, _, value = line.strip().partition("=")
            os.environ[key] = value.strip().strip('"').strip("'")