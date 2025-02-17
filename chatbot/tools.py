from chatbot.services.entity_recognition_service import identify_entities
from langchain.tools import Tool

from chatbot.services.search_products_by_entities_service import search_product_by_entities
from chatbot.services.translation_service import translate_text
from chatbot.services.ocr_service import extract_text_from_pdf


from .schemas import DBQueryInputSchema



ocr_tool= Tool(
    name="OCR",
    func= extract_text_from_pdf,
    description="Usa esta herramienta si el usuario proporciona un archivo PDF y necesita extraer su texto.",
)

entity_tool = Tool(
    name="Entidades",
    func=identify_entities,
    description="Usa esta herramienta cuando el usuario aporte alguna caracteristica de ordenador, tenga intencion de compra o de pedir información."
)



db_query_tool = Tool(
    name="Consulta_BD",
    func=search_product_by_entities,
    description="Usa esta herramienta para consultar en la base de datos productos que coincidan con las entidades detectadas.",
    args_schema=DBQueryInputSchema,
)

translation_tool = Tool(
    name="Traduccion",
    func=translate_text,
    description="Usa esta herramienta para traducir el texto proporcionado a otro idioma."
)