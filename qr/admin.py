from django.contrib import admin
from .models import QRCode

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ("id", "content_type", "created_at")
    search_fields = ("id", "payload")
    list_filter = ("content_type", "created_at")
