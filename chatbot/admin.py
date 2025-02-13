from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import PDFTranscription, Product

@admin.register(PDFTranscription)
class PDFTranscriptionAdmin(admin.ModelAdmin):
    list_display = ("pdf_name", "created_at")
    search_fields = ("pdf_name", "transcription")
    list_filter = ("created_at",)
    ordering = ("-created_at",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("modelo", "precio", "almacenamiento", "memoria", "procesador")
    search_fields = ("modelo", "procesador", "gráfica")
    list_filter = ("color", "precio")
    ordering = ("-created_at",)
