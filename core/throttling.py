"""Limitation de débit par adresse IP (anti brute-force / anti-spam).

Les taux sont définis dans settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'].
"""
from rest_framework.throttling import SimpleRateThrottle


class IPScopeThrottle(SimpleRateThrottle):
    """Limite par IP pour un scope donné, que l'utilisateur soit connecté ou non."""
    post_only = False

    def get_cache_key(self, request, view):
        return self.cache_format % {'scope': self.scope, 'ident': self.get_ident(request)}

    def allow_request(self, request, view):
        # Sur les vues mixtes (ex. liste admin + envoi public), seul l'envoi est limité
        if self.post_only and request.method != 'POST':
            return True
        return super().allow_request(request, view)


class LoginThrottle(IPScopeThrottle):
    scope = 'login'


class RegisterThrottle(IPScopeThrottle):
    scope = 'register'


class ContactThrottle(IPScopeThrottle):
    scope = 'contact'
    post_only = True


class StageSubmitThrottle(IPScopeThrottle):
    scope = 'stage_submit'
    post_only = True


class ChatStartThrottle(IPScopeThrottle):
    scope = 'chat_start'
