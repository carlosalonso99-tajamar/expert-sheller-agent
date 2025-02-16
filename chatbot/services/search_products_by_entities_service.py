import logging
from ..models import Product

# Configuración de logs
logger = logging.getLogger(__name__)

def search_product_by_entities(entities: dict) -> list:
    """
    Busca productos en la base de datos que coincidan con las entidades extraídas.
    """
    filters = {}

    logger.info(f"🔍 Iniciando búsqueda de productos con entidades: {entities}")

    if "modelo" in entities:
        filters["modelo__icontains"] = entities["modelo"]
    if "almacenamiento" in entities:
        filters["almacenamiento__icontains"] = entities["almacenamiento"]
    if "memoria" in entities:
        filters["memoria__icontains"] = entities["memoria"]
    if "procesador" in entities:
        filters["procesador__icontains"] = entities["procesador"]
    if "gráfica" in entities:
        filters["gráfica__icontains"] = entities["gráfica"]
    if "pantalla" in entities:
        filters["pantalla__icontains"] = entities["pantalla"]
    if "peso" in entities:
        filters["peso__icontains"] = entities["peso"]
    if "color" in entities:
        filters["color__icontains"] = entities["color"]

    logger.info(f"🛠 Aplicando filtros: {filters}")

    results = Product.objects.filter(**filters)

    if results.exists():
        product_list = [f"{p.modelo} - {p.precio}€" for p in results]
        logger.info(f"✅ Productos encontrados: {product_list}")
        return product_list
    else:
        logger.warning("⚠️ No se encontraron productos con esas características.")
        return ["No se encontraron productos con esas características."]
