from django.urls import path
from chatbot.views import chatbot_view, chat_ui, upload_document, list_pdfs

urlpatterns = [
    path("", chat_ui, name="chat_ui"),  # UI del chat
    path("api/chatbot/", chatbot_view, name="chatbot_api"),  # API del chatbot
    path("api/upload/", upload_document, name="upload_document"),  # 📌 Ruta de subida de archivos
    path("api/list-pdfs/", list_pdfs, name="list_pdfs"),
]
