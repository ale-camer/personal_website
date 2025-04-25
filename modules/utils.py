"""
Custom functions for the projects.
"""

import os, shutil, json
import pandas as pd
from datetime import datetime

def remove_old_files(folder, files_to_remove=None) -> None:
    """
    Removes specific files and folders in a folder or all files and folders if not specified.

    :param folder: Folder from which files and folders will be removed.
    :param files_to_remove: List of filenames to remove. If None, all files and folders will be removed.
    """
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path):
                    if files_to_remove and filename not in files_to_remove:
                        continue
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"Deleted folder: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
    else:
        print(f"Folder does not exist: {folder}")
        
def delta_time() -> None:
    """"Updates the time since the last job was started"""
    today = datetime.now()
    beging_last_job = datetime(2023, 8, 1)
    delta_days = (today - beging_last_job).days

    years = delta_days // 365
    months = int((delta_days - 365) / 30)

    if years == 1: year_string = "year"
    else: year_string = "years"

    if months == 1: month_string = "month"
    else: month_string = "months"

    string = "%d %s %d %s" % (years, year_string, months, month_string)

    return string
  
def reading_json(path: str) -> None:
    """Loads and returns the contents of a JSON file from the specified path."""
    return json.load(open(path, 'r'))

def writing_json(data: pd.DataFrame, path: str) -> None:
    """Saves a Python object as a JSON file to the specified path."""
    with open(path, 'w') as f:
        json.dump(data, f)

def wb_data_preprocess(data: pd.DataFrame, type_selected: str, option_selected: str) -> pd.DataFrame:
    """Filters and transforms World Bank data into a standardized DataFrame based on the selected type and option."""
    filtered_data = [
        entry for entry in data 
        if (entry['country']['value'] if type_selected == 'country' else entry['date']) == option_selected
    ]
    return (
       pd.DataFrame(
         [(entry['countryiso3code'], entry['country']['value'], entry['date'], entry['value']) for entry in filtered_data], 
         columns=['ISO_CODE', 'COUNTRY', 'DATE', 'VALUE']
       )
      .sort_values(by=['COUNTRY', 'DATE'], ascending=[True, False])
      .drop_duplicates()
    )