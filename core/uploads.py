"""Sécurisation des fichiers envoyés par les visiteurs."""
import os
import uuid

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

TAILLE_MAX_DOCUMENT = 5 * 1024 * 1024  # 5 Mo
EXTENSIONS_DOCUMENT = {'.pdf', '.jpg', '.jpeg', '.png', '.webp'}

# Signatures binaires attendues (empêche un .html ou .svg renommé en .pdf)
_SIGNATURES = {
    '.pdf':  [b'%PDF'],
    '.jpg':  [b'\xff\xd8\xff'],
    '.jpeg': [b'\xff\xd8\xff'],
    '.png':  [b'\x89PNG\r\n\x1a\n'],
    '.webp': [b'RIFF'],
}


@deconstructible
class NomAleatoire:
    """upload_to qui remplace le nom d'origine par un identifiant aléatoire.

    Les documents ne sont plus devinables à partir du nom du candidat (ex. « cni_dupont.jpg »).
    """

    def __init__(self, dossier):
        self.dossier = dossier.rstrip('/') + '/'

    def __call__(self, instance, filename):
        ext = os.path.splitext(filename)[1].lower()[:10]
        return f'{self.dossier}{uuid.uuid4().hex}{ext}'


def valider_document(fichier):
    """Vérifie taille, extension et signature réelle d'un document envoyé."""
    if fichier is None:
        return fichier

    if fichier.size > TAILLE_MAX_DOCUMENT:
        raise ValidationError('Fichier trop volumineux (5 Mo maximum).')

    ext = os.path.splitext(fichier.name)[1].lower()
    if ext not in EXTENSIONS_DOCUMENT:
        raise ValidationError('Format non autorisé. Formats acceptés : PDF, JPG, PNG, WEBP.')

    debut = fichier.read(16)
    fichier.seek(0)
    if not any(debut.startswith(sig) for sig in _SIGNATURES[ext]):
        raise ValidationError("Le contenu du fichier ne correspond pas à son extension.")

    return fichier
