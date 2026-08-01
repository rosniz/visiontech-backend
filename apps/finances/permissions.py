from rest_framework.permissions import BasePermission

from .models import ROLE_ADMIN


class IsFinanceUser(BasePermission):
    """Autorise tout utilisateur ayant un profil finance actif (admin ou comptable)."""

    message = "Ce compte n'a pas accès au module finances."

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        profile = getattr(user, 'finance_profile', None)
        return bool(profile and profile.actif)


class IsFinanceAdmin(IsFinanceUser):
    """Autorise uniquement les profils finance avec le rôle admin."""

    message = 'Seul un administrateur finance peut effectuer cette action.'

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return request.user.finance_profile.role == ROLE_ADMIN
