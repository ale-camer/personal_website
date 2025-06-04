import os
from tqdm import tqdm
from transformers import MarianMTModel, MarianTokenizer
from googletrans import Translator as GoogleTranslator
from modules.utils import read_json, write_json

language_code_map = {
    "spanish": "es",
    "mandarin": "zh-CN",  # Google uses zh-CN, Marian uses zh
    "french": "fr",
    "arabic": "ar",
    "portuguese": "pt",
    "russian": "ru",
    "japanese": "ja",
    "korean": "ko",
    "italian": "it",
    "greek": "el",
    "turkish": "tr",
    "dutch": "nl",
    "swedish": "sv",
    "finnish": "fi",
    "norwegian": "no",
    "danish": "da",
    "german": "de",
}

def load_marian_model(from_lang: str, to_lang: str):
    model_name = f"Helsinki-NLP/opus-mt-{from_lang}-{to_lang}"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return tokenizer, model

def batch_translate_marian(texts, tokenizer, model, batch_size=8):
    translated_texts = {}
    items = list(texts.items())
    for i in tqdm(range(0, len(items), batch_size)):
        batch = items[i:i + batch_size]
        keys, batch_texts = zip(*batch)
        inputs = tokenizer(list(batch_texts), return_tensors="pt", padding=True, truncation=True)
        outputs = model.generate(**inputs)
        decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        translated_texts.update(dict(zip(keys, decoded)))
    return translated_texts

def translate_with_google(texts, target_lang_code):
    translated_texts = {}
    translator = GoogleTranslator()
    for key, text in tqdm(texts.items()):
        try:
            translated = translator.translate(text, dest=target_lang_code).text
        except:
            translated = ""
        translated_texts[key] = translated
    return translated_texts

def main():
    JSON_PATH = os.path.join('static', 'json')
    EN_TEXTS_PATH = os.path.join(JSON_PATH, 'texts_en.json')
    STOPWORDS_PATH = os.path.join(JSON_PATH, 'stopwords.json')

    texts_en = read_json(EN_TEXTS_PATH)
    stopwords = read_json(STOPWORDS_PATH)
    languages = [l for l in list(stopwords.keys()) if l != 'english']

    for language in languages:
        print(f"\n🌍 Traduciendo a {language.title()}...")
        target_code = language_code_map.get(language, language)

        marian_code = target_code.split("-")[0]  # e.g., "zh-CN" → "zh" for Marian

        try:
            tokenizer, model = load_marian_model("en", marian_code)
            translations = batch_translate_marian(texts_en, tokenizer, model)
            print("✅ Usando MarianMT")
        except Exception as e:
            print(f"⚠️ MarianMT falló: {e}")
            print("🔁 Usando Google Translate como respaldo...")
            translations = translate_with_google(texts_en, target_code)

        OUTPUT_PATH = os.path.join(JSON_PATH, f'texts_{target_code}.json')
        write_json(translations, OUTPUT_PATH)
        print(f"✅ Guardado: {OUTPUT_PATH}")
