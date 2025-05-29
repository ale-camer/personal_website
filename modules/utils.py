"""Custom project functions."""

# =============================================================================
# IMPORTS
# =============================================================================
import os, shutil, json, re
import pandas as pd
from time import time
from unidecode import unidecode   

# =============================================================================
# FILE OPERATIONS
# =============================================================================
def remove_temp_files(folders: str | list[str], files_to_remove: list[str] = None) -> None:
    start_time = time()
    for folder in folders:
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
    print(f"Temporary folders cleaned in {round(time() - start_time, 4)} seconds.")
    # print(f"Temporary folders cleaned in {time() - start_time} seconds.")
        
def job_duration() -> None:
    days_per_month, days_per_year = 30, 365
    today, job_start_date = pd.Timestamp.now(), pd.Timestamp(2025, 2, 1)
    elapsed_days = (today - job_start_date).days
    
    years = elapsed_days // days_per_year if elapsed_days > days_per_year else 0
    months = int((elapsed_days - days_per_year) / days_per_month) if elapsed_days > days_per_year else int(elapsed_days / days_per_month) + 1
    
    year_text = "" if years == 0 else "year" if years == 1 else "years"
    month_text = "month" if months == 1 else "months"
    
    return f"{months} {month_text}" if years == 0 else f"{years} {year_text} {months} {month_text}"
  
def read_json(path: str) -> None:
    return json.load(open(path, 'r', encoding='utf-8'))

def write_json(data: pd.DataFrame, path: str) -> None:
    with open(path, 'w') as f:
        json.dump(data, f)
        
def write_txt(content: str, path: str) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
      
# =============================================================================
# TEXT PROCESSING
# =============================================================================
def text_normalizer(text: str, stopwords: set = None, min_word_len: int = 2) -> str:
  
    def _reduce_repeated_chars(text: str) -> str:
        return re.sub(r'[^a-zA-Z0-9\s]', _count_rep_char, text)
  
    def _count_rep_char(match: str) -> str:
        return match.group(0)[0]
      
    return transform_words(
        text=_reduce_repeated_chars(text.lower()),
        fn=unidecode,
        condition=lambda w: (
            w not in stopwords
            and not re.compile(r'http\S+').match(w)
            and len(w) > min_word_len
        )
    )

def transform_words(text: str, fn=lambda x: x, condition=lambda x: True) -> str:
    return ' '.join(fn(word) for word in text.split() if condition(word))