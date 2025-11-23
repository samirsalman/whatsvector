from typing import Literal

SupportedLanguages = Literal["en", "es", "fr", "de", "it", "pt"]


def language_code_to_name(code: SupportedLanguages) -> str:
    """
    Converts a language code to its full language name.
    Args:
        code (SupportedLanguages): The language code.
    Returns:
        str: The full language name (e.g., "English", "Spanish").
    """
    language_map = {
        "en": "English",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "it": "Italian",
        "pt": "Portuguese",
    }
    return language_map.get(code, "English")
