from django.http import JsonResponse
from chatbot.agent import agent

from django.shortcuts import render

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

    if not user_message:
        return JsonResponse({"error": "No se proporcionó un mensaje"}, status=400)

    # 🔹 Pregunta al agente qué hacer con el mensaje
    response_text = agent.run(user_message)

    return JsonResponse({"response": response_text})

import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt



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
    save_dir = os.path.join(settings.BASE_DIR, "chatbot", "static", "docs")
    os.makedirs(save_dir, exist_ok=True)

    save_path = os.path.join(save_dir, uploaded_file.name)
    

    # 📌 Guardar el archivo
    try:
        with open(save_path, "wb+") as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        print(f"✅ Archivo guardado en: {save_path}")
        return JsonResponse({"message": f"Archivo '{uploaded_file.name}' subido correctamente."})
    except Exception as e:
        print(f"⛔ Error al guardar el archivo: {str(e)}")
        return JsonResponse({"error": f"Error al guardar el archivo: {str(e)}"}, status=500)


