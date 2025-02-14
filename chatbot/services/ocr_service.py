from dotenv import load_dotenv
import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
import fitz  # PyMuPDF para manejar PDFs
import logging

load_dotenv()
client = ImageAnalysisClient(
    endpoint=os.getenv('AI_SERVICE_ENDPOINT'),
    credential=AzureKeyCredential(os.getenv('AI_SERVICE_KEY'))
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Convierte un archivo PDF en texto utilizando el servicio OCR de Azure.
    
    :param pdf_path: Ruta del archivo PDF a procesar.
    :return: Texto extraído.
    """
    logging.info(f"📂 Iniciando extracción de texto desde PDF: {pdf_path}")

    text_result = []
    
    try:
        # 📌 Verificar si el archivo existe antes de abrirlo
        if not os.path.exists(pdf_path):
            logging.error(f"❌ Error: El archivo no existe en la ruta {pdf_path}")
            return ""

        doc = fitz.open(pdf_path)  # Abrir el PDF
        logging.info(f"📖 Archivo PDF abierto con éxito. Páginas detectadas: {len(doc)}")

        for page_num in range(len(doc)):
            logging.info(f"🔍 Procesando página {page_num + 1}/{len(doc)}")

            # Convertir la página a imagen PNG
            image = doc[page_num].get_pixmap()
            image_bytes = image.tobytes("png")

            logging.info(f"📸 Imagen de la página {page_num + 1} convertida a PNG (bytes: {len(image_bytes)})")

            # Enviar la imagen al servicio de OCR de Azure
            logging.info(f"📤 Enviando imagen al servicio OCR de Azure para la página {page_num + 1}...")
            result = client.analyze(
                image_data=image_bytes,
                visual_features=[VisualFeatures.READ]
            )

            # Extraer el texto si se detecta contenido
            if result.read and result.read.blocks:
                logging.info(f"✅ OCR detectó {len(result.read.blocks)} bloques de texto en la página {page_num + 1}")

                for block in result.read.blocks:
                    for line in block.lines:
                        text_result.append(line.text)
                        logging.debug(f"📝 Línea extraída: {line.text}")

            else:
                logging.warning(f"⚠️ No se detectó texto en la página {page_num + 1}")

    except Exception as e:
        logging.error(f"⛔ Error al procesar el PDF {pdf_path}: {str(e)}", exc_info=True)
        return ""

    final_text = "\n".join(text_result)
    logging.info(f"✅ Extracción completada. Total de caracteres extraídos: {len(final_text)}")
    
    return final_text