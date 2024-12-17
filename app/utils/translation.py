import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

translations = {}
default_lang = "en"

def load_translations():
    translations_dir = Path(__file__).resolve().parent.parent / 'translations'
    if not translations_dir.exists():
        logging.error("Translations directory not found!")
        return

    for file in translations_dir.glob("*.json"):
        if file.is_file():
            lang_code = file.stem  # Extract file name without extension
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    translations[lang_code] = json.load(f)
                logging.info(f"Loaded translations for language: {lang_code}")
            except Exception as e:
                logging.error(f"Failed to load translation file {file}: {e}")

def translate(lang: str, key: str) -> str:
    return translations.get(lang, translations[default_lang]).get(key, key)

# Load translations during module import
load_translations()
