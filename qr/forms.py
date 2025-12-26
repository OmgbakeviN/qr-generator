import re
from django import forms

HEX_RE = re.compile(r"^#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})$")

class QRGeneratorForm(forms.Form):
    CONTENT_CHOICES = (
        ("text", "Texte / URL"),
        ("image", "Image (upload)"),
    )

    ERROR_CHOICES = (
        ("L", "Faible (L)"),
        ("M", "Moyen (M)"),
        ("Q", "Élevé (Q)"),
        ("H", "Très élevé (H)"),
    )

    content_type = forms.ChoiceField(
        choices=CONTENT_CHOICES,
        widget=forms.Select(attrs={
            "class": "w-full rounded-xl px-3 py-2 border bg-white text-slate-900 border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-400 dark:bg-slate-950 dark:text-slate-100 dark:border-slate-700"
        })
    )

    text = forms.CharField(
        required=False,
        max_length=2000,
        widget=forms.Textarea(attrs={
            "rows": 4,
            "class": "w-full rounded-xl px-3 py-2 border bg-white text-slate-900 border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-400 dark:bg-slate-950 dark:text-slate-100 dark:border-slate-700"
        }),
    )

    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            "class": "w-full rounded-xl px-3 py-2 border bg-white text-slate-900 border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-400 dark:bg-slate-950 dark:text-slate-100 dark:border-slate-700"
        })
    )

    fill_color = forms.CharField(
        required=False,
        initial="#4f46e5",
        widget=forms.TextInput(attrs={
            "type": "color",
            "class": "h-11 w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-950"
        })
    )

    back_color = forms.CharField(
        required=False,
        initial="#ffffff",
        widget=forms.TextInput(attrs={
            "type": "color",
            "class": "h-11 w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-950"
        })
    )

    transparent_background = forms.BooleanField(required=False, initial=False)

    error_correction = forms.ChoiceField(
        choices=ERROR_CHOICES,
        initial="M",
        widget=forms.Select(attrs={
            "class": "w-full rounded-xl px-3 py-2 border bg-white text-slate-900 border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-400 dark:bg-slate-950 dark:text-slate-100 dark:border-slate-700"
        })
    )

    box_size = forms.IntegerField(
        required=False,
        initial=10,
        min_value=4,
        max_value=20,
        widget=forms.NumberInput(attrs={
            "class": "w-full rounded-xl px-3 py-2 border bg-white text-slate-900 border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-400 dark:bg-slate-950 dark:text-slate-100 dark:border-slate-700"
        })
    )

    border = forms.IntegerField(
        required=False,
        initial=4,
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={
            "class": "w-full rounded-xl px-3 py-2 border bg-white text-slate-900 border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-400 dark:bg-slate-950 dark:text-slate-100 dark:border-slate-700"
        })
    )

    def clean(self):
        cleaned = super().clean()
        content_type = cleaned.get("content_type")
        text = (cleaned.get("text") or "").strip()
        image = cleaned.get("image")

        fill_color = (cleaned.get("fill_color") or "#4f46e5").strip()
        back_color = (cleaned.get("back_color") or "#ffffff").strip()
        transparent = bool(cleaned.get("transparent_background"))

        if not HEX_RE.match(fill_color):
            self.add_error("fill_color", "Couleur invalide (hex).")
        if not HEX_RE.match(back_color):
            self.add_error("back_color", "Couleur invalide (hex).")

        if (fill_color.lower() == back_color.lower()) and not transparent:
            self.add_error("back_color", "Le fond ne peut pas être identique à la couleur du QR.")

        if content_type == "text" and not text:
            self.add_error("text", "Entre un texte ou un lien (URL).")

        if content_type == "image" and not image:
            self.add_error("image", "Upload une image pour générer le QR.")

        cleaned["text"] = text
        cleaned["fill_color"] = fill_color
        cleaned["back_color"] = back_color
        return cleaned
