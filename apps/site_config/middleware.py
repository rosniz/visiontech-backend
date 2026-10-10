import logging

from django.http import JsonResponse
from django.db.utils import DatabaseError

from .models import ParametresSite

logger = logging.getLogger(__name__)

# Restent accessibles pendant la maintenance : statut du site, connexion admin,
# espaces d'administration et module finances (interne).
CHEMINS_AUTORISES = (
    '/api/v1/site/',
    '/api/v1/stages/auth/login/',
    '/api/v1/stages/auth/refresh/',
    '/api/v1/finances/',
)


def _est_staff(request):
    """Le middleware passe avant DRF : on décode nous-mêmes le JWT éventuel."""
    if getattr(request, 'user', None) is not None and request.user.is_authenticated and request.user.is_staff:
        return True
    try:
        from rest_framework_simplejwt.authentication import JWTAuthentication
        resultat = JWTAuthentication().authenticate(request)
    except Exception:
        return False
    return bool(resultat and resultat[0].is_staff)


class MaintenanceMiddleware:
    """En maintenance, l'API publique répond 503. Les admins connectés passent."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        chemin = request.path
        if (
            chemin.startswith('/api/')
            and not chemin.startswith(CHEMINS_AUTORISES)
            and '/admin/' not in chemin
            and request.method != 'OPTIONS'
        ):
            try:
                etat = ParametresSite.etat_maintenance()
            except DatabaseError:
                logger.exception('Lecture du mode maintenance impossible')
                etat = {'maintenance': False}

            if etat['maintenance'] and not _est_staff(request):
                reponse = JsonResponse({
                    'maintenance': True,
                    'detail': 'Site en maintenance.',
                    'message': etat['message'],
                    'fin': etat['fin'],
                }, status=503)
                reponse['Retry-After'] = '600'
                return reponse

        return self.get_response(request)
