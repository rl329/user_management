import pytest
from app.utils.translation import translate

def test_translation_english():
    assert translate("en", "email_verified") == "Email verified successfully"

def test_translation_spanish():
    assert translate("es", "email_verified") == "Correo verificado correctamente"

def test_translation_invalid_language():
    result = translate("invalid_lang", "email_verified")
    assert result == "Translation not found"
