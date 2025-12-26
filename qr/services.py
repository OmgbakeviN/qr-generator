import uuid
from io import BytesIO
import qrcode
from django.core.files.base import ContentFile

def _ec(level):
    return {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H,
    }[level]

def generate_qr_pil_image(data, fill_color, back_color, error_level, box_size, border, transparent_background):
    qr = qrcode.QRCode(
        version=None,
        error_correction=_ec(error_level),
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGBA")

    if transparent_background:
        bg = img.getpixel((0, 0))
        px = img.load()
        w, h = img.size
        for y in range(h):
            for x in range(w):
                if px[x, y] == bg:
                    px[x, y] = (bg[0], bg[1], bg[2], 0)

    return img

def pil_to_contentfile_png(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return ContentFile(buffer.getvalue())

def random_png_name(prefix="qrcodes"):
    return f"{prefix}/{uuid.uuid4().hex}.png"
