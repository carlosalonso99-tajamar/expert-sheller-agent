from django.http import JsonResponse
from chatbot.agent import agent
from .services.ocr_service import OCRService

from django.shortcuts import render
import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .services.save_product_services import save_product_service

from chatbot.models import PDFTranscription
from .agent import memory

def chat_ui(request):
    """
    Renderiza la interfaz de chat.
    """
    return render(request, "chat.html")


def chatbot_view(request):
    """
    Vista única que recibe mensajes de los usuarios y decide qué herramienta usar.
    """
    user_message = request.GET.get("message", "")
    # memory.chat_memory.add_user_message(user_message)
    if not user_message:
        return JsonResponse({"error": "No se proporcionó un mensaje"}, status=400)

    # 🔹 Pregunta al agente qué hacer con el mensaje
    response = agent.invoke({
        "input": user_message,
        # "chat_history": memory.load_memory_variables({})
        })
    
    # memory.chat_memory.add_ai_message(str(response))
    print(response)
    # 🔹 Extrae el texto correctamente según el formato del retorno del agente
    if isinstance(response, dict) and "output" in response:
        response_text = response["output"]  # Si el output viene como diccionario
    else:
        response_text = str(response)  # Fallback a string si no tiene "output"

    return JsonResponse({"response": response_text})


import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

ocr_service = OCRService()




@csrf_exempt  # 📌 Evita problemas de CSRF en POST requests
def upload_document(request):
    print("🔹 Recibida solicitud de subida de archivo...")  # Log de depuración

    if request.method != "POST":
        print("⛔ Error: Método no permitido.")
        return JsonResponse({"error": "Método no permitido."}, status=405)

    if "file" not in request.FILES:
        print("⛔ Error: No se recibió ningún archivo.")
        return JsonResponse({"error": "No se recibió ningún archivo."}, status=400)

    uploaded_file = request.FILES["file"]
    print(f"✅ Archivo recibido: {uploaded_file.name}")

    # 📌 Asegurar que la carpeta de destino existe
    save_dir = os.path.join(settings.MEDIA_ROOT, "pdfs")
    os.makedirs(save_dir, exist_ok=True)

    # 📌 Guardar el archivo en la ruta
    save_path = os.path.join(save_dir, uploaded_file.name)
    with open(save_path, "wb") as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)

    print(f"📂 Archivo guardado en: {save_path}")

    try:
        # 📌 Extraer el texto del PDF
        answer = ocr_service.extract_text_from_pdf(save_path)  # Usar la ruta guardada

        # 📌 Obtener el nombre base del archivo
        pdf_filename = os.path.basename(save_path)

        # 📌 Guardar en la base de datos
        transcription_obj, created = PDFTranscription.objects.get_or_create(
            pdf_name=pdf_filename,
            defaults={"pdf_path": save_path}
        )

        # 📌 Guardar la transcripción extraída
        transcription_obj.transcription = answer
        save_product_service(answer)
        
        transcription_obj.save()

        print(f"✅ Transcripción guardada correctamente para {pdf_filename}")

        return JsonResponse({
            "message": f"Archivo {pdf_filename} subido y transcrito correctamente.",
            "pdf_name": pdf_filename,
            "transcription": answer
        })

    except Exception as e:
        print(f"⛔ Error al procesar el archivo: {str(e)}")
        return JsonResponse({"error": f"Error al procesar el archivo: {str(e)}"}, status=500)



def list_pdfs(request):
    """ Devuelve una lista de PDFs subidos en formato JSON """
    pdf_folder = os.path.join(settings.MEDIA_ROOT, "pdfs")  # Ruta donde están los PDFs
    pdf_url = f"{settings.MEDIA_URL}pdfs/"  # URL base de los PDFs

    if not os.path.exists(pdf_folder):
        return JsonResponse({"pdfs": []})

    pdf_files = [
        {"name": pdf, "url": f"{pdf_url}{pdf}"}
        for pdf in os.listdir(pdf_folder) if pdf.endswith(".pdf")
    ]


    return JsonResponse({"pdfs": pdf_files})