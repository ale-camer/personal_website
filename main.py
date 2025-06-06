"""Main project file."""

# =============================================================================
# IMPORTS
# =============================================================================
import os, warnings
from app import app
from modules.utils import read_json, remove_temp_files, timed_run
from modules.generate_readme import ReadmeGenerator
from modules.generate_translations import main as generate_translations

warnings.filterwarnings("ignore")

# =============================================================================
# VARIABLES
# =============================================================================
TEMPLATE_FOLDER = 'templates'
CONFIG_FILE_PATH = os.path.join('static', 'json', 'config.json')
TEXTS_FILE_PATH = os.path.join('static', 'json', 'texts_en.json')

config = read_json(CONFIG_FILE_PATH)
temp_folders_to_clean = config["temporary_folders"]

g = ReadmeGenerator(output_file="README.md")

# =============================================================================
# RUN
# =============================================================================
def main():
    timed_run(remove_temp_files, temp_folders_to_clean, in_seconds=True, process_str="Temporary folders cleaned")
    # g.generate_readme_file()
    # generate_translations()
    
    # app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
    app.run(debug=True)

if __name__ == '__main__':
    main()
