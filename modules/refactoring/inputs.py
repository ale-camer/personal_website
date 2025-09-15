from zipfile import ZipFile as zipf
import xml.etree.ElementTree as ET

def read_txt(filename, encoding: str = "utf-8") -> str:
    with open(filename, encoding=encoding) as f:
        return f.read()

def read_csv(filename, encoding: str = "utf-8") -> list:
    with open(filename, encoding=encoding) as f:
        return f.readlines()

def read_excel(xlsx_file: str) -> dict:

    def parse_item(item):
        return ET.parse(item).getroot()

    ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    rns = "{http://schemas.openxmlformats.org/package/2006/relationships}"
    wb_path, rels_path = "xl/workbook.xml", "xl/_rels/workbook.xml.rels"

    with zipf(xlsx_file) as z:

        sheets = {
            s.get("name"): next(v for k, v in s.attrib.items()
            if k.endswith("id")) for s
            in parse_item(z.open(wb_path)).find(f"{ns}sheets")
        }

        paths = {
            r.get("Id"): "xl/" + r.get("Target") for r
            in parse_item(z.open(rels_path)).findall(f"{rns}Relationship")
        }

        return {
            name: [
                r.find(f"{ns}v").text for row
                in parse_item(z.open(paths[sheet_id])).iter(f"{ns}row")
                for r in row
            ]
            for name, sheet_id in sheets.items()
        }

worldbank_data = read_csv("wb_results.csv")
keyphrase_data = read_txt("whatsapp_chat.txt")
seasonality_data = read_excel("seasonality_example.xlsx")












