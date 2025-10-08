# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard Libraries ---
from dataclasses import dataclass
import os

# --- Project/System ---
from modules.common.utils import text_normalizer, read_json
from . import parsing as p

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))
STOPWORDS_PATH = os.path.join(PROJECT_ROOT, 'static', 'json', 'stopwords.json')
STOPWORDS = read_json(STOPWORDS_PATH)

@dataclass
class WhatsAppConfig:
    grouped_data: dict
    parsed_data: list
    language: str

class WhatsAppModule:

    def __init__(self):
        self.current_data = None

    def parse_chat(self, file, language: str) -> WhatsAppConfig:

        raw_lines = file.read().decode('utf-8').splitlines()
        parsed_data = p.parse_messages(raw_lines)
        grouped_data = p.groupby_dict(parsed_data)

        self.current_data = WhatsAppConfig(
            grouped_data=grouped_data,
            parsed_data=parsed_data,
            language=language
        )
        return self.current_data

    def filter_chat(self, issuer: str) -> tuple:

        is_general = issuer == 'GENERAL'
        prefix = "GENERAL_" if is_general else f"{issuer}_"
        filtered_counts = {
            k: v for k, v
            in self.current_data.grouped_data.items()
            if k.startswith(prefix)
        }

        if is_general:
            messages_to_process = [
                row[3] for row in self.current_data.parsed_data
            ]
        else:
            messages_to_process = [
                row[3] for row
                in self.current_data.parsed_data
                if row[2] == issuer
            ]

        combined_text = ' '.join(messages_to_process)
        normalized_text = text_normalizer(
            text=combined_text,
            stopwords=STOPWORDS[self.current_data.language]
        )

        return filtered_counts, normalized_text, is_general, messages_to_process