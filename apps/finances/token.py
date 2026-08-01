from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


class FinanceTokenObtainSerializer(TokenObtainPairSerializer):
    """Connexion par email, réservée aux comptes ayant un profil finance actif."""

    username_field = 'email'

    def validate(self, attrs):
        email = attrs.get('email', '').lower().strip()
        password = attrs.get('password', '')

        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'email': 'Aucun compte trouvé avec cet email.'})

        if not user.check_password(password):
            raise serializers.ValidationError({'password': 'Mot de passe incorrect.'})

        if not user.is_active:
            raise serializers.ValidationError({'email': 'Ce compte est désactivé.'})

        profile = getattr(user, 'finance_profile', None)
        if not profile or not profile.actif:
            raise serializers.ValidationError({'email': "Ce compte n'a pas accès au module finances."})

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'email': user.email,
            'role': profile.role,
        }


class FinanceTokenObtainView(TokenObtainPairView):
    serializer_class = FinanceTokenObtainSerializer
