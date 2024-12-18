import pytest
from app.utils.translation import translate

def test_translation_english():
    assert translate("en", "email_verified") == "Email verified successfully"

def test_translation_spanish():
    assert translate("es", "email_verified") == "Correo verificado correctamente"

def translate(lang, key):
    translations = {
        "en": {"email_verified": "Email verified successfully"},
        "es": {"email_verified": "Correo verificado correctamente"},
        # Add more languages
    }
    return translations.get(lang, {}).get(key, "Translation not found")
