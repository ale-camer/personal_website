"""Utility project tasks: translations and readme files generation."""

# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import os

# --- Third-party ---
from dotenv import load_dotenv

# --- Project/system ---
from app import app
from modules.utils import timed_run
from modules.generate_readme import ReadmeGenerator
from modules.generate_translations import main as generate_translations
from modules.generate_requirements import main as generate_requirements

# =============================================================================
# RUN
# =============================================================================
load_dotenv()

def run_dev_tasks():

    readme_generator = ReadmeGenerator()

    if input("Do you want to generate readme file? (y/n): ").strip().lower() == 'y':
        timed_run(readme_generator.generate_readme_file, process_str="Readme file generated")
        
    if input("Do you want to generate translations? (y/n): ").strip().lower() == 'y':
        timed_run(generate_translations, process_str="Translations generated")

    if input("Do you want to generate requirements.txt? (y/n): ").strip().lower() == 'y':
        timed_run(generate_requirements, process_str="requirements.txt generated")

if __name__ == '__main__':
    if os.environ.get('FLASK_ENV') == 'development':
        run_dev_tasks()
    else:
        print("Development tasks can only be run in a development environment.")