import uuid
from django.db import models

class QRCode(models.Model):
    CONTENT_TYPES = (
        ("text", "Text"),
        ("image", "Image"),
    )

    ERROR_LEVELS = (
        ("L", "L"),
        ("M", "M"),
        ("Q", "Q"),
        ("H", "H"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES)
    payload = models.TextField()

    fill_color = models.CharField(max_length=7, default="#4f46e5")
    back_color = models.CharField(max_length=7, default="#ffffff")
    transparent_background = models.BooleanField(default=False)

    error_correction = models.CharField(max_length=1, choices=ERROR_LEVELS, default="M")
    box_size = models.PositiveIntegerField(default=10)
    border = models.PositiveIntegerField(default=4)

    uploaded_image = models.ImageField(upload_to="uploads/", blank=True, null=True)
    qr_image = models.ImageField(upload_to="qrcodes/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
