import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar credenciales de Azure Translator
TRANSLATOR_KEY = os.getenv('TRANSLATOR_KEY')
TRANSLATOR_REGION = os.getenv('TRANSLATOR_REGION')

TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com/translate"

# Idiomas soportados por defecto
SUPPORTED_LANGUAGES = {
    "es": "Español",
    "en": "Inglés",
    "fr": "Francés",
    "de": "Alemán",
    "it": "Italiano",
    "pt": "Portugués"
}

def translate_text(text, target_language="en"):
    """
    Traduce el texto a un idioma específico usando Azure Translator.
    :param text: Texto a traducir.
    :param target_language: Código del idioma destino (ej. "es", "fr", "de").
    :return: Texto traducido.
    """
    if not TRANSLATOR_KEY or not TRANSLATOR_REGION:
        raise ValueError("⚠️ Claves de Azure Translator no configuradas en el entorno.")

    if target_language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"⚠️ Idioma no soportado: {target_language}. Usa uno de {list(SUPPORTED_LANGUAGES.keys())}")

    headers = {
        "Ocp-Apim-Subscription-Key": TRANSLATOR_KEY,
        "Ocp-Apim-Subscription-Region": TRANSLATOR_REGION,
        "Content-Type": "application/json"
    }

    params = {
        "api-version": "3.0",
        "to": target_language
    }

    body = [{"text": text}]

    try:
        response = requests.post(TRANSLATOR_ENDPOINT, headers=headers, params=params, json=body)
        response.raise_for_status()
        translations = response.json()
        return translations[0]['translations'][0]['text']
    
    except requests.exceptions.RequestException as e:
        print(f"⛔ Error al traducir: {e}")
        return None
