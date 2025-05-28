"""Main project file."""

# =============================================================================
# IMPORTS
# =============================================================================
import os
from app import app
from modules.utils import read_json, remove_temp_files
from modules.generate_readme import generate_readme_file

# =============================================================================
# CONSTANTS
# =============================================================================
config_path = os.path.join('static', 'json', 'config.json')
config = read_json(config_path)
temp_folders_to_clean = config["temporary_folders"]

# =============================================================================
# RUN
# =============================================================================
def main():
    generate_readme_file(".")
    remove_temp_files(temp_folders_to_clean)
    app.run(debug=True)

if __name__ == '__main__':
    main()
