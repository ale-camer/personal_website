import re, string
from collections import defaultdict
from unidecode import unidecode
from zipfile import ZipFile as zipf
import xml.etree.ElementTree as ET
from prettytable import PrettyTable as pt
from tabulate import tabulate
from fpdf import FPDF

def get_input(func, *args, **kwargs):
    return func(*args, **kwargs)

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

class FileExporter:
    def __init__(self, results: dict, cols: list[str], filename: str):
        self.results = results
        self.cols = cols
        self.filename = filename

    # strings
    def to_txt_string(self) -> str:
        tables = []
        for k, v in self.results.items():
            table = pt(title=k, field_names=self.cols)
            table.add_rows([[' '.join(ngram), count] for ngram, count in v])
            tables.append(str(table))
        return "\n\n".join(tables)

    def to_md_string(self) -> str:
        md_tables = []
        for k, v in self.results.items():
            table_data = [[' '.join(ngram), count] for ngram, count in v]
            md_tables.append(f"## {k}\n" + tabulate(table_data, headers=self.cols, tablefmt="github"))
        return "\n\n".join(md_tables)

    # exports
    def export_txt(self):
        txt_string = self.to_txt_string()
        with open(self.filename + '.txt', "w", encoding="utf-8") as f:
            f.write(txt_string)
        print(f"TXT saved as {self.filename + '.txt'}")

    def export_md(self):
        md_string = self.to_md_string()
        with open(self.filename + '.md', "w", encoding="utf-8") as f:
            f.write(md_string)
        print(f"Markdown saved as {self.filename + '.md'}")

    def export_pdf(self):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", "", 14)

        for k, v in self.results.items():
            pdf.cell(0, 10, k, ln=True)
            pdf.set_font("Arial", "", 12)
            # Encabezado de tabla
            pdf.cell(80, 8, self.cols[0], border=1)
            pdf.cell(30, 8, self.cols[1], border=1)
            pdf.ln()
            # Filas de tabla
            for ngram, count in v:
                pdf.cell(80, 8, ' '.join(ngram), border=1)
                pdf.cell(30, 8, str(count), border=1)
                pdf.ln()
            pdf.ln(5)

        pdf.output(self.filename + '.pdf')
        print(f"PDF saved as {self.filename + '.pdf'}")