from chatbot.services.ocr_service import OCRService
from chatbot.models import PDFTranscription  # Importamos el modelo
import os
from chatbot.services.entity_recognition_service import identify_entities

# Inicializar servicios
ocr_service = OCRService()


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Wrapper para la herramienta OCR, llama al servicio de OCR de Azure y guarda la transcripción.
    """
    answer = ocr_service.extract_text_from_pdf(pdf_path)  # Llamar al OCR

    pdf_filename = os.path.basename(pdf_path)  # Extraer el nombre del archivo

    # Guardar en la base de datos
    transcription_obj, created = PDFTranscription.objects.get_or_create(
        pdf_name=pdf_filename,
        defaults={"pdf_path": pdf_path}
    )

    transcription_obj.transcription = answer  # Guardar la transcripción
    transcription_obj.save()

    return answer  # Devolver la transcripción
