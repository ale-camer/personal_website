# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard Libraries ---
from dataclasses import dataclass

# --- Project/System ---
from . import parsing as p

@dataclass
class Config:
    grouped_data: dict
    parsed_data: list
    language: str

class ChatSession:

    def __init__(self):
        self.current_data = None

    def parse_chat(self, file, language: str) -> Config:

        raw_lines = file.read().decode('utf-8').splitlines()
        parsed_data = p.parse_messages(raw_lines)
        grouped_data = p.groupby_dict(parsed_data)
        self.current_data = Config(grouped_data, parsed_data, language)
        return self.current_data

    def filter_chat(self, issuer: str) -> tuple:
            return p.filter_chat(self.current_data, issuer)