# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import os

# --- Third-party ---

# --- Project ---
from app_OLD import app
import modules.common.utils as ut
from modules.generate_translations import main as generate_translations

# =============================================================================
# RUN
# =============================================================================
ut.load_dotenv()

def run_dev_tasks():

    if input("Do you want to generate translations? (y/n): ").strip().lower() == 'y':
        ut.timed_run(generate_translations, process_str="Translations generated")

if __name__ == '__main__':
    if os.environ.get('FLASK_ENV') == 'development':
        run_dev_tasks()
    else:
        print("Development tasks can only be run in a development environment.")