"""World Bank Auxiliary functions."""

# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import os

# --- Third-party ---
import pandas as pd

# --- Project/system ---
from modules.utils import read_json
from modules.world_bank import WorldBankModule

# =============================================================================
# DIRECTORIES
# =============================================================================
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(FILE_DIR)
STATIC_DIR = os.path.join(BASE_DIR, 'static')
WORLD_BANK_DIR = os.path.join(STATIC_DIR, 'world_bank')
GEO_DATA_PATH = os.path.join(STATIC_DIR, 'json', 'world_administrative_boundaries.json')

# =============================================================================
# MODULE
# =============================================================================
wb_manager = WorldBankModule(GEO_DATA_PATH)

# =============================================================================
# AUXILIARY METHODS
# =============================================================================
def get_file_path(indicator: str) -> str:
    return os.path.join(WORLD_BANK_DIR, f'{indicator}.json')
    
def load_data(indicator: str, type_selected: str | None = None, option: str | None = None) -> list | pd.DataFrame:
    data = read_json(get_file_path(indicator))  
    if type_selected and option:
        return wb_manager.results(data, type_selected, option)
    return data
  
def extract_options(data: list, type_selected: str) -> list[str]:
    options = ({
        entry['country']['value'] for entry in data} 
        if type_selected == 'country' 
        else {entry['date'] for entry in data
    })
    return sorted(options, reverse=(type_selected == 'year'))