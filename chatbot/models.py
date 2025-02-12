from django.db import models

# Create your models here.

from django.db import models

class PDFTranscription(models.Model):
    pdf_name = models.CharField(max_length=255, unique=True)  # Nombre del archivo
    pdf_path = models.CharField(max_length=500)  # Ruta del archivo en el sistema
    transcription = models.TextField(blank=True, null=True)  # Texto extraído
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación

    def __str__(self):
        return f"{self.pdf_name} - {self.created_at}"
