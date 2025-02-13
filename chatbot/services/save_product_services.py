import json
import re
import logging
from .entity_recognition_service import identify_entities
from ..models import Product  # Importamos el modelo de producto

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def detect_entities(text):
    """
    Llama al modelo de lenguaje para detectar entidades en el texto.
    """
    logger.info("🔍 Detectando entidades en el texto...")
    try:
        response = identify_entities(text)
        logger.info(f"✅ Entidades detectadas: {response}")
        return response
    except Exception as e:
        logger.error(f"⛔ Error en detect_entities: {e}")
        return "{}"  # Retorna JSON vacío en caso de error

def extract_json(response_text):
    """
    Extrae el contenido JSON de una respuesta del modelo de lenguaje,
    eliminando cualquier texto adicional fuera de las llaves {}.
    """
    logger.info("🔍 Intentando extraer JSON de la respuesta del modelo...")
    try:
        # Buscar el primer bloque JSON válido dentro del texto usando expresiones regulares
        match = re.search(r"\{.*\}", response_text, re.DOTALL)

        if match:
            cleaned_json = match.group(0)  # Tomar solo el JSON encontrado
            logger.info(f"✅ JSON extraído correctamente: {cleaned_json}")
            return json.loads(cleaned_json)  # Convertir a diccionario de Python
        else:
            raise ValueError("No se encontró un JSON válido en la respuesta.")

    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"⛔ Error al extraer JSON: {e}")
        return {}  # Retornar un diccionario vacío en caso de error

from decimal import Decimal
import re


def sanitize_price(price_str):
    """
    Convierte una cadena de precio con formato europeo (ej. "2.528,75 €") en un número decimal válido.
    """
    if not price_str:
        return None

    try:
        # 🔹 Eliminar caracteres no numéricos excepto comas y puntos
        cleaned_price = re.sub(r"[^\d,\.]", "", price_str)

        # 🔹 Verificar si el número usa coma decimal (formato europeo)
        if "," in cleaned_price and "." in cleaned_price:
            # Si hay tanto coma como punto, eliminar el punto (para formatos "2.528,75")
            cleaned_price = cleaned_price.replace(".", "")
        
        # 🔹 Convertir coma decimal a punto
        cleaned_price = cleaned_price.replace(",", ".")

        # 🔹 Convertir a decimal y validar que sea un número válido
        decimal_price = Decimal(cleaned_price)
        return decimal_price

    except Exception as e:
        print(f"⛔ Error al convertir precio: {e}")
        return None


def convert_to_object(entities_json):
    """
    Convierte el JSON de entidades en un objeto Product,
    asegurando que los valores sean correctos antes de guardarlos.
    """
    logger.info("🔍 Convirtiendo JSON a objeto Product...")
    try:
        entities = extract_json(entities_json)

        if not isinstance(entities, dict):
            raise ValueError("El JSON no es un diccionario válido.")

        logger.info(f"✅ JSON convertido correctamente: {entities}")

    except Exception as e:
        logger.error(f"⛔ Error al decodificar JSON en convert_to_object: {e}")
        entities = {}

    # 🔹 Verificar si los campos son diccionarios o strings antes de acceder a `.get()`
    grafica_modelo = entities["gráfica"]["modelo"] if isinstance(entities.get("gráfica"), dict) else entities.get("gráfica", "Desconocido")
    procesador_modelo = entities["procesador"]["modelo"] if isinstance(entities.get("procesador"), dict) else entities.get("procesador", "Desconocido")

    pantalla_data = entities.get("pantalla", {})
    if isinstance(pantalla_data, dict):
        pantalla_info = f"{pantalla_data.get('tamaño', 'N/A')} {pantalla_data.get('resolución', 'Desconocido')}"
    else:
        pantalla_info = pantalla_data  # Si ya es un string, lo dejamos como está

    audio_info = entities["audio"]["tipo"] if isinstance(entities.get("audio"), dict) else entities.get("audio", "No disponible")

    # 🔹 Convertir precio antes de asignarlo
    precio_final = sanitize_price(entities.get("precio"))

    # Crear el objeto Product con valores limpios
    product = Product(
        precio=precio_final,
        modelo=entities.get("modelo", "Desconocido"),
        almacenamiento=entities.get("almacenamiento"),
        memoria=entities.get("memoria"),
        gráfica=grafica_modelo,
        procesador=procesador_modelo,
        pantalla=pantalla_info,
        peso=entities.get("peso"),
        color=entities.get("color", "Sin especificar"),
        audio=audio_info,
    )

    return product




def save_product_service(text):
    """
    Extrae entidades del texto, convierte a objeto Product y guarda en la BD.
    """
    logger.info("📝 Iniciando el proceso de extracción y guardado de producto...")
    entities_json = detect_entities(text)

    if not entities_json or entities_json == "{}":
        logger.error("⛔ No se encontraron entidades en el texto.")
        return None

    product = convert_to_object(entities_json)

    # Verificamos si al menos un campo relevante tiene valor antes de guardar
    if any([
        product.precio, product.modelo, product.almacenamiento, product.memoria,
        product.gráfica, product.procesador, product.pantalla, product.peso, product.color, product.audio
    ]):
        try:
            product.save()
            logger.info(f"✅ Producto guardado con éxito: {product}")
            return product
        except Exception as e:
            logger.error(f"⛔ Error al guardar el producto en la BD: {e}")
            return None
    else:
        logger.warning("⚠️ No hay suficientes datos para guardar el producto.")
        return None
