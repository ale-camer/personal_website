"""Main project file."""

# =============================================================================
# IMPORTS
# =============================================================================
import os
from app import app
from modules.utils import read_json, remove_temp_files
from modules.generate_readme import ReadmeGenerator

# =============================================================================
# VARIABLES
# =============================================================================
config_path = os.path.join('static', 'json', 'config.json')
config = read_json(config_path)
temp_folders_to_clean = config["temporary_folders"]
g = ReadmeGenerator(output_file="README.md")

# =============================================================================
# RUN
# =============================================================================
def main():
    # g.generate_readme_file()
    remove_temp_files(temp_folders_to_clean)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
    # app.run(debug=True)

if __name__ == '__main__':
    main()
