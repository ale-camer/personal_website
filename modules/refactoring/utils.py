import re, string
from collections import defaultdict
from unidecode import unidecode
from zipfile import ZipFile as zipf
import xml.etree.ElementTree as ET

def get_chunks(iterable: iter, size: int = 100_000, start: int = 0) -> iter:
    if not hasattr(iterable, "__iter__") or not hasattr(iterable, "__len__"):
        raise TypeError("The 'iterable' input must be an iterable with length like a list or string")
    if len(iterable) == 0:
        raise ValueError("The 'iterable' input must have a length greater than zero")
    if not isinstance(size, int) or size <= 0:
        raise ValueError("The 'size' input must be a positive integer")

    for i in range(start, len(iterable), size):
        yield iterable[i : i + size]

def read_txt(filename, encoding: str = "utf-8") -> str:
    with open(filename, encoding=encoding) as f:
        return f.read()

def read_excel(xlsx_file: str) -> dict:

    ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    rns = "{http://schemas.openxmlformats.org/package/2006/relationships}"
    wb_path, rels_path, sst_path = "xl/workbook.xml", "xl/_rels/workbook.xml.rels", "xl/sharedStrings.xml"

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
            shared_strings = [si.find(f"{ns}t").text for si in sst_root.findall(f"{ns}si")]

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

class TextCleaner:

    _PUNCTUATION_PATTERN = f"[{re.escape(string.punctuation)}]"
    _NUMBERS_PATTERN = r"\d+"

    def __init__(self, text: str, stopwords: set[str] = None):
        self.text = text
        self.stopwords = stopwords if stopwords is not None else set()

    def get_stopwords():
        pass

    def clean(
        self,
        has_stream: bool = True,
        to_lowercase: bool = True,
        remove_accents: bool = True,
        remove_punctuation: bool = False,
        remove_numbers: bool = False,
        filter_stopwords: bool = True,
        min_token_length: int = 3
    ) -> list[str]:

        text = self.text
        if to_lowercase: text = text.lower()
        if remove_accents: text = unidecode(text)
        if remove_punctuation: text = re.sub(self._PUNCTUATION_PATTERN, ' ', text)
        if remove_numbers: text = re.sub(self._NUMBERS_PATTERN, ' ', text)

        if has_stream:
            yield from (
                token for token in text.split()
                if len(token) > min_token_length
                and not (filter_stopwords and token in self.stopwords)
            )
        else:
            return [
                token for token in text.split()
                if len(token) > min_token_length
                and not (filter_stopwords and token in self.stopwords)
            ]

class FileTooLargeError(Exception):
    pass

def validate_upload_size(uploaded_file, limit_mb: int = 10):

    def _get_file_size_mb(file) -> int:
        size = file.content_length
        if size is None:
            file.seek(0, 2)
            size = file.tell()
            file.seek(0)
        return size / (1024 * 1024)

    file_size_mb = _get_file_size_mb(uploaded_file)
    if file_size_mb > limit_mb:
        raise FileTooLargeError(
            f"The file is too big ({file_size_mb:.2f} MB). "
            f"The limit is {limit_mb} MB."
        )