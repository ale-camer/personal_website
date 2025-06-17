"""Main project file."""

# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import os
import warnings

# --- Third-party ---
from dotenv import load_dotenv

# --- Project/system ---
from app import app
from modules.utils import read_json, remove_temp_files, timed_run

# =============================================================================
# CONFIGURATION
# =============================================================================
load_dotenv()
warnings.filterwarnings("ignore")

IS_DEV = os.environ.get('FLASK_ENV') == 'development'

CONFIG_FILE_PATH = os.path.join('static', 'json', 'config.json')
config = read_json(CONFIG_FILE_PATH)
TEMP_FOLDERS_TO_CLEAN = config["temporary_folders"]

# =============================================================================
# RUN
# =============================================================================
if __name__ == '__main__':
    timed_run(
        remove_temp_files, 
        TEMP_FOLDERS_TO_CLEAN, 
        in_seconds=True, 
        process_str="Temporary folders cleaned"
    )
    app.run(
        debug=IS_DEV,
        host='0.0.0.0' if not IS_DEV else None,
        port=int(os.environ.get("PORT", 5000)) if not IS_DEV else 5000
    )