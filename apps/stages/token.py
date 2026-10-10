import logging

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework import serializers
from rest_framework.exceptions import Throttled
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from core.throttling import LoginThrottle

security_log = logging.getLogger('security')

# Verrouillage par compte (complète la limite par IP : bloque aussi les attaques
# distribuées sur plusieurs IP contre un même email).
MAX_ECHECS      = 5
DUREE_VERROU    = 15 * 60  # secondes
MESSAGE_ECHEC   = 'Email ou mot de passe incorrect.'


def _cle_echecs(email):
    return f'login_fail:{email}'


class EmailTokenObtainSerializer(TokenObtainPairSerializer):
    """Connexion par email au lieu de username."""
    username_field = 'email'

    def validate(self, attrs):
        email    = attrs.get('email', '').lower().strip()
        password = attrs.get('password', '')
        cle      = _cle_echecs(email)
        requete  = self.context.get('request')
        ip       = LoginThrottle().get_ident(requete) if requete else '?'

        if cache.get(cle, 0) >= MAX_ECHECS:
            security_log.warning('Connexion bloquée (compte verrouillé) : %s depuis %s', email, ip)
            raise Throttled(wait=DUREE_VERROU, detail='Trop de tentatives. Compte temporairement verrouillé, réessayez dans 15 minutes.')

        user = User.objects.filter(username=email).first()
        if user is None:
            # Hachage factice : même temps de réponse que pour un compte existant
            make_password(password)
            valide = False
        else:
            valide = user.check_password(password) and user.is_active

        if not valide:
            echecs = cache.get(cle, 0) + 1
            cache.set(cle, echecs, DUREE_VERROU)
            security_log.warning('Échec de connexion %d/%d : %s depuis %s', echecs, MAX_ECHECS, email, ip)
            # Message identique dans tous les cas : ne révèle pas si l'email existe
            raise serializers.ValidationError({'detail': MESSAGE_ECHEC})

        cache.delete(cle)
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access':  str(refresh.access_token),
            'email':   user.email,
            'is_staff': user.is_staff,
        }


class EmailTokenObtainView(TokenObtainPairView):
    serializer_class = EmailTokenObtainSerializer
    throttle_classes = [LoginThrottle]
