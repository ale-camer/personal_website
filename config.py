# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import os

# --- Third-party ---

# --- Project ---
from modules.common.utils import read_json

# =============================================================================
# ROUTES
# =============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_DIR = os.path.join(BASE_DIR, 'static')
KEYPHRASE_DIR = os.path.join(STATIC_DIR, 'keyphrase')
SEASONALITY_DIR = os.path.join(STATIC_DIR, 'seasonality')
WORLD_BANK_DIR = os.path.join(STATIC_DIR, 'world_bank')
JSON_DIR = os.path.join(STATIC_DIR, 'json')

CONFIG_PATH = os.path.join(JSON_DIR, 'config.json')
GEO_DATA_PATH = os.path.join(JSON_DIR, 'world_administrative_boundaries.json')

KEYPHRASE_INPUT_PATH = os.path.join(KEYPHRASE_DIR, 'raw_keyphrases_results.json')
KEYPHRASE_OUTPUT_PATH = os.path.join(KEYPHRASE_DIR, 'processed_keyphrases_results.txt')

# =============================================================================
# SETTINGS
# =============================================================================
config = read_json(CONFIG_PATH)
INDICATORS = dict(sorted(config["indicators"].items()))
INDICATOR_NAMES = {v: k for k, v in INDICATORS.items()}
WEEK_DAYS = {int(k): v for k, v in config["days_of_the_week"].items()}
MONTHS = {int(k): v for k, v in config["months"].items()}