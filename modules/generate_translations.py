# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import time
from os import getenv
from os.path import join, dirname, exists

# --- Third-party ---
from tqdm import tqdm
from dotenv import load_dotenv
from deepl import Translator, TooManyRequestsException

# --- Project/system ---
from modules.common.utils import read_json, write_json

# =============================================================================
# CONSTANTS
# =============================================================================
load_dotenv()
api_key = getenv("DEEPL_API_KEY")
translator = Translator(api_key)

BASE_DIR = dirname(__file__)
PARENT_DIR = dirname(BASE_DIR)
JSON_PATH = join(PARENT_DIR, 'static', 'json')

ORIGINAL_LANG = read_json(join(JSON_PATH, 'lang', 'english.json'))
LANGUAGES = read_json(join(JSON_PATH, 'config.json'))["languages_to_translate"]

# =============================================================================
# AUXILIARY FUNCTIONS
# =============================================================================
def translation_exists(lang_name: str) -> bool:
    path = join(JSON_PATH, 'lang', f"{lang_name}.json")
    if exists(path):
        print(f"{lang_name}.json already exist. Not translating.")
        return True
    return False

# =============================================================================
# CORE
# =============================================================================
def translate_text(
        text: str, target_lang: str, retries: int = 5, delay: float = .01
    ) -> str:
    for i in range(retries):
        try:
            return translator.translate_text(text, target_lang=target_lang).text
        except TooManyRequestsException:
            print(f"Too many requests, retrying in {delay}s... ({i+1}/{retries})")
            time.sleep(delay)
    raise Exception("Max retries reached for translation")

def translate_dict(data: dict, target_lang: str, lang_name: str) -> dict:
    return {
        k: translate_dict(v, target_lang, lang_name) if isinstance(v, dict)
        else translate_text(v, target_lang) if isinstance(v, str)
        else v for k, v in tqdm(data.items(), desc=f"Translating to {lang_name}")
    }

def translate_and_save(lang_name: str, lang_code: str) -> None:
    translated = translate_dict(ORIGINAL_LANG, lang_code, lang_name)
    output_path = join(JSON_PATH, 'lang', f"{lang_name}.json")
    write_json(translated, output_path)

# =============================================================================
# MAIN
# =============================================================================
def main() -> None:
    for lang_name, lang_code in LANGUAGES.items():
        if translation_exists(lang_name):
            continue
        try:
            translate_and_save(lang_name, lang_code)
        except Exception as e:
            print(
                (
                    f"Error translating {lang_name} ({lang_code}): ",
                    "{type(e).__name__}: {e}"
                )
            )