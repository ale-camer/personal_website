# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard Libraries ---
from dataclasses import dataclass

# --- Project/System ---
from . import parsing as p

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))
STOPWORDS_PATH = os.path.join(PROJECT_ROOT, 'static', 'json', 'stopwords.json')
STOPWORDS = read_json(STOPWORDS_PATH)

@dataclass
class Config:
    grouped_data: dict
    parsed_data: list
    language: str
    self.normalized_texts: list = normalized_texts

class ChatSession:

    def __init__(self):
        self.current_data = None

    def parse_chat(self, file, language: str) -> Config:

        raw_lines = file.read().decode('utf-8').splitlines()
        parsed_data = p.parse_messages(raw_lines)
        grouped_data = p.groupby_dict(parsed_data)
        
        issuers = sorted(list(set(d[2] for d in parsed_data)))
        issuers.insert(0, 'GENERAL')
        normalized_texts = {}
        for issuer in issuers:
            if issuer == 'GENERAL':
                msg = [row[3] for row in parsed_data]
            else:
                msg = [row[3] for row in parsed_data if row[2] == issuer]
            norm_text = text_normalizer(
                text=' '.join(msg), stopwords=STOPWORDS[language]
            )
            normalized_texts[issuer] = norm_text
            
        self.current_data = Config(
            grouped_data, parsed_data, language, normalized_texts
        )
        return self.current_data

    def filter_chat(self, issuer: str) -> tuple:
            return p.filter_chat(self.current_data, issuer)