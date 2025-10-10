# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import os

# --- Third-party ---

# --- Project ---
from modules.common.utils import timed_run, load_dotenv
from modules.generate_translations import main as generate_translations

# =============================================================================
# RUN
# =============================================================================
load_dotenv()

def run_dev_tasks():
    if input("Do you want to generate translations? (y/n): ").strip().lower() == 'y':
        timed_run(generate_translations, process_str="Translations generated")

if __name__ == '__main__':
    if os.environ.get('FLASK_ENV') == 'development':
        run_dev_tasks()
    else:
        print("Development tasks can only be run in a development environment.")