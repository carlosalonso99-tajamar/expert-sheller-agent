import logging
import json
from django.db.models import Q
from ..models import Product

# Configuración de logs
logger = logging.getLogger(__name__)

def search_product_by_entities(entities) -> list:
    """
    Busca productos en la base de datos con una búsqueda flexible y normalizada.
    """

    # Verificar si entities es una cadena JSON y convertirlo a diccionario
    if isinstance(entities, str):
        try:
            entities = json.loads(entities)  # Convertir string a JSON
        except json.JSONDecodeError:
            logger.error("⛔ Error al decodificar JSON en entidades")
            return ["Error al procesar la búsqueda."]
    elif not isinstance(entities, dict):
        logger.error("⛔ Formato inesperado de entidades")
        return ["Error al procesar la búsqueda."]

    logger.info(f"🔍 Iniciando búsqueda de productos con entidades: {entities}")

    query = Q()

    # Aplicar búsqueda flexible para cada entidad
    if "modelo" in entities:
        query |= Q(modelo__icontains=entities["modelo"])
    if "almacenamiento" in entities:
        query |= Q(almacenamiento__icontains=entities["almacenamiento"])
    if "memoria" in entities:
        query |= Q(memoria__icontains=entities["memoria"])
    if "procesador" in entities:
        query |= Q(procesador__icontains=entities["procesador"])
    if "gráfica" in entities:
        query |= Q(gráfica__icontains=entities["gráfica"])
    if "pantalla" in entities:
        query |= Q(pantalla__icontains=entities["pantalla"])
    if "peso" in entities:
        query |= Q(peso__icontains=entities["peso"])
    if "color" in entities:
        query |= Q(color__icontains=entities["color"])

    logger.info(f"🛠 Aplicando filtros avanzados: {query}")

    results = Product.objects.filter(query)

    if results.exists():
        product_list = []
        for p in results:
            product_info = f"""
            - **Modelo:** {p.modelo}
            - **Precio:** {p.precio if p.precio else 'No disponible'}€
            - **Almacenamiento:** {p.almacenamiento if p.almacenamiento else 'No especificado'}
            - **Memoria:** {p.memoria if p.memoria else 'No especificado'}
            - **Gráfica:** {p.gráfica if p.gráfica else 'No especificado'}
            - **Procesador:** {p.procesador if p.procesador else 'No especificado'}
            - **Pantalla:** {p.pantalla if p.pantalla else 'No especificado'}
            - **Peso:** {p.peso if p.peso else 'No especificado'}
            - **Color:** {p.color if p.color else 'No especificado'}
            - **Audio:** {p.audio if p.audio else 'No especificado'}
            """
            product_list.append(product_info.strip())  # Limpia espacios innecesarios

        logger.info(f"✅ Productos encontrados: {product_list}")
        return product_list

    else:
        logger.warning("⚠️ No se encontraron productos con esas características.")
        return ["No se encontraron productos con esas características."]
