import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

translations = {}
default_lang = "en"

def load_translations():
    translations_dir = Path(__file__).resolve().parent.parent.parent / 'translations'
    for file in translations_dir.glob("*.json"):
        lang_code = file.stem  # For example, "en", "es", etc.
        with open(file, 'r', encoding='utf-8') as f:
            translations[lang_code] = json.load(f)
            logging.info(f"Loaded translations for language: {lang_code}")

# Load translations during module import
load_translations()

def translate(lang: str, key: str) -> str:
    return translations.get(lang, translations[default_lang]).get(key, key)
