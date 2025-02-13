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

from django.db import models

from django.db import models

class Product(models.Model):
    precio = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, help_text="Precio del producto en EUR/USD"
    )
    modelo = models.CharField(
        max_length=255, null=True, blank=True, help_text="Nombre del modelo del producto"
    )
    almacenamiento = models.CharField(
        max_length=100, null=True, blank=True, help_text="Capacidad de almacenamiento (ej. 512GB SSD)"
    )
    memoria = models.CharField(
        max_length=100, null=True, blank=True, help_text="Capacidad de la memoria RAM (ej. 16GB DDR4)"
    )
    gráfica = models.CharField(
        max_length=100, null=True, blank=True, help_text="Modelo de la tarjeta gráfica (ej. NVIDIA RTX 3060)"
    )
    procesador = models.CharField(
        max_length=100, null=True, blank=True, help_text="Modelo del procesador (ej. Intel Core i7-12700H)"
    )
    pantalla = models.CharField(
        max_length=100, null=True, blank=True, help_text="Tamaño y resolución de la pantalla (ej. 15.6'' 1920x1080)"
    )
    peso = models.CharField(
        max_length=50, null=True, blank=True, help_text="Peso del producto (ej. 1.5kg)"
    )
    color = models.CharField(
        max_length=50, null=True, blank=True, help_text="Color del producto (ej. Negro, Plata)"
    )
    audio = models.CharField(
        max_length=255, null=True, blank=True, help_text="Especificaciones de audio (ej. Dolby Atmos, Altavoces estéreo)"
    )

    created_at = models.DateTimeField(auto_now_add=True, help_text="Fecha de creación del producto")
    updated_at = models.DateTimeField(auto_now=True, help_text="Última actualización del producto")

    def __str__(self):
        return f"{self.modelo or 'Producto sin nombre'} - {self.precio or 'Sin precio'}€"
