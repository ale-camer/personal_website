"""
Custom project functions.
"""

import os, shutil, json
import pandas as pd

def remove_old_files(folder, files_to_remove=None) -> None:
    """
    Remove specific files and folders from a given directory.

    If `files_to_remove` is provided, only those files will be deleted. 
    Otherwise, all contents of the folder will be removed.

    Args:
        folder (str): Path to the folder to clean.
        files_to_remove (list[str], optional): List of filenames to delete. Defaults to None.

    Returns:
        None
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
    """
    Calculate the time elapsed since a fixed job start date (2025-02-01).

    The result is returned as a human-readable string indicating the number 
    of months and years elapsed.

    Returns:
        str: Elapsed time formatted as "X months" or "Y years X months".
    """
    days_per_month, days_per_year = 30, 365
    today, job_start_date = pd.Timestamp.now(), pd.Timestamp(2025, 2, 1)
    elapsed_days = (today - job_start_date).days
    
    years = elapsed_days // days_per_year if elapsed_days > days_per_year else 0
    months = int((elapsed_days - days_per_year) / days_per_month) if elapsed_days > days_per_year else int(elapsed_days / days_per_month) + 1
    
    year_text = "" if years == 0 else "year" if years == 1 else "years"
    month_text = "month" if months == 1 else "months"
    
    return f"{months} {month_text}" if years == 0 else f"{years} {year_text} {months} {month_text}"
  
def reading_json(path: str) -> None:
    """
    Load and return the contents of a JSON file.

    Args:
        path (str): Path to the JSON file.

    Returns:
        dict: Parsed JSON content.
    """
    return json.load(open(path, 'r'))

def writing_json(data: pd.DataFrame, path: str) -> None:
    """
    Save a Python object as a JSON file.

    Args:
        data (Any): Data to serialize as JSON.
        path (str): Destination file path.

    Returns:
        None
    """
    with open(path, 'w') as f:
        json.dump(data, f)