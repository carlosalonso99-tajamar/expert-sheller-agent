from azure.ai.vision.imageanalysis.models import VisualFeatures
import fitz  # PyMuPDF para manejar PDFs

def extract_text_from_pdf(self, pdf_path: str) -> str:
    """
    Convierte un archivo PDF en texto utilizando el servicio OCR de Azure.
    
    :param pdf_path: Ruta del archivo PDF a procesar.
    :return: Texto extraído.
    """
    text_result = []
    doc = fitz.open(pdf_path)  # Abrir el PDF

    for page_num in range(len(doc)):
        image = doc[page_num].get_pixmap()
        image_bytes = image.tobytes("png")  # Convertir la página a bytes PNG

        # Enviar la imagen al servicio de OCR de Azure
        result = self.client.analyze(
            image_data=image_bytes,
            visual_features=[VisualFeatures.READ]
        )

        # Extraer el texto si se detecta contenido
        if result.read and result.read.blocks:
            for block in result.read.blocks:
                for line in block.lines:
                    text_result.append(line.text)

    return "\n".join(text_result)  # Retornar el texto extraído en un solo string
