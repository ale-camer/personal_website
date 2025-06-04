import os
import json
from time import time
from bs4 import BeautifulSoup

allowed_tags = {'h1', 'h2', 'h3', 'h4', 'a', 'p', 'label', 'button', 'th', 'li', 'div'}

def extract_texts_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    texts = []
    seen = set()

    for el in soup.find_all(allowed_tags):
        if len(el.find_all(recursive=False)) > 0:
            text = ''.join(el.find_all(text=True, recursive=False)).strip()
        else:
            text = el.get_text(strip=True)

        if text and len(text) > 1 and '{' not in text and text not in seen:
            texts.append(text)
            seen.add(text)
    return texts

def generate_translation_keys(texts, prefix):
    translations = {}
    for i, text in enumerate(texts):
        key = f"{i+1}_{prefix}"
        translations[key] = text
    return translations

def extract_translations_from_folder(template_folder):
    all_translations = {}
    for root, _, files in os.walk(template_folder):
        for filename in [f for f in files if len(f) < 20 and f.endswith('.html')]:
            full_path = os.path.join(root, filename)
            relative_path = os.path.relpath(full_path, template_folder)
            prefix = os.path.splitext(relative_path.replace(os.sep, '_'))[0]
            texts = extract_texts_from_html(full_path)
            file_translations = generate_translation_keys(texts, prefix)
            all_translations.update(file_translations)
    return all_translations

def get_html_texts(template_folder, output_path):
    start_time = time()
    translations = extract_translations_from_folder(template_folder)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(translations, f, indent=2, ensure_ascii=False)
    print(f"Texts extracted from HTMLs in {round(time() - start_time, 4)} seconds\n")
