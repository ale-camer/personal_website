# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import os
import warnings

# --- Third-party ---

# --- Project ---
# from app_OLD import app
import modules.common.utils as ut
from app import create_app

# =============================================================================
# CONFIGURATION
# =============================================================================
app = create_app()
ut.load_dotenv()
warnings.filterwarnings("ignore")

config = ut.read_json(os.path.join('static', 'json', 'config.json'))
IS_DEV = os.environ.get('FLASK_ENV') == 'development'
TEMP_FOLDERS_TO_CLEAN = config["temporary_folders"]

# =============================================================================
# RUN
# =============================================================================
if __name__ == '__main__':
    ut.timed_run(
        ut.remove_temp_files, 
        TEMP_FOLDERS_TO_CLEAN, 
        in_seconds=True, 
        process_str="Temporary folders cleaned"
    )
    app.run(
        debug=IS_DEV,
        host='0.0.0.0' if not IS_DEV else None,
        port=int(os.environ.get("PORT", 5000)) if not IS_DEV else 5000
    )