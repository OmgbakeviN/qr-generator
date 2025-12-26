from django.shortcuts import render, redirect, get_object_or_404
from .forms import QRGeneratorForm
from .models import QRCode
from .services import generate_qr_pil_image, pil_to_contentfile_png, random_png_name

def home(request):
    canonical_url = request.build_absolute_uri("/")

    if request.method == "POST":
        form = QRGeneratorForm(request.POST, request.FILES)
        if form.is_valid():
            content_type = form.cleaned_data["content_type"]

            fill_color = form.cleaned_data["fill_color"]
            back_color = form.cleaned_data["back_color"]
            transparent = bool(form.cleaned_data["transparent_background"])
            error_level = form.cleaned_data["error_correction"]
            box_size = form.cleaned_data["box_size"] or 10
            border = form.cleaned_data["border"] or 4

            if content_type == "text":
                payload = form.cleaned_data["text"]
                obj = QRCode.objects.create(
                    content_type="text",
                    payload=payload,
                    fill_color=fill_color,
                    back_color=back_color,
                    transparent_background=transparent,
                    error_correction=error_level,
                    box_size=box_size,
                    border=border,
                )
            else:
                obj = QRCode.objects.create(
                    content_type="image",
                    payload="",
                    uploaded_image=form.cleaned_data["image"],
                    fill_color=fill_color,
                    back_color=back_color,
                    transparent_background=transparent,
                    error_correction=error_level,
                    box_size=box_size,
                    border=border,
                )
                payload = request.build_absolute_uri(obj.uploaded_image.url)
                obj.payload = payload
                obj.save(update_fields=["payload"])

            img = generate_qr_pil_image(
                payload,
                fill_color=fill_color,
                back_color=back_color,
                error_level=error_level,
                box_size=box_size,
                border=border,
                transparent_background=transparent,
            )
            qr_file = pil_to_contentfile_png(img)
            obj.qr_image.save(random_png_name(), qr_file, save=True)

            return redirect("qr:result", pk=obj.id)
    else:
        form = QRGeneratorForm()

    return render(request, "qr/index.html", {"form": form, "canonical_url": canonical_url})


def result(request, pk):
    obj = get_object_or_404(QRCode, pk=pk)
    share_url = request.build_absolute_uri()
    canonical_url = share_url
    return render(request, "qr/result.html", {"obj": obj, "share_url": share_url, "canonical_url": canonical_url})

from django.http import HttpResponse

def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Allow: /",
        "Disallow: /r/",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
