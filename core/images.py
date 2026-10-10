"""Optimisation des images envoyées (redimensionnement + WebP)."""
import os
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile


def compresser_image(image_field, max_width=1600, quality=82):
    """Redimensionne et compresse une image uploadée (in-place sur le champ)."""
    if not image_field or image_field.name.lower().endswith('.webp'):
        return
    try:
        img = Image.open(image_field)
        img_format = 'WEBP' if img.format != 'GIF' else 'GIF'
        if img_format == 'WEBP' and img.mode not in ('RGB', 'RGBA'):
            # On garde la transparence (logos), WebP la gère
            img = img.convert('RGBA' if img.mode in ('P', 'LA') else 'RGB')
        if img.width > max_width:
            ratio = max_width / float(img.width)
            img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)
        buffer = BytesIO()
        img.save(buffer, format=img_format, quality=quality, optimize=True)
        # Nom de base seulement : upload_to rajoute lui-même le dossier
        name = os.path.basename(image_field.name).rsplit('.', 1)[0] + '.webp'
        image_field.save(name, ContentFile(buffer.getvalue()), save=False)
    except Exception:
        pass
