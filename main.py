"""Main project file."""

# =============================================================================
# IMPORTS
# =============================================================================
import os, warnings
from app import app
from modules.utils import read_json, remove_temp_files
from modules.generate_readme import ReadmeGenerator
from modules.html_texts import get_html_texts
from modules.translations import main as get_translations

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
    remove_temp_files(temp_folders_to_clean)
    # get_html_texts(TEMPLATE_FOLDER, TEXTS_FILE_PATH)
    # get_translations()

    # g.generate_readme_file()
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)

if __name__ == '__main__':
    main()
