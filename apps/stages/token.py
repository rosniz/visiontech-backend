from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


class EmailTokenObtainSerializer(TokenObtainPairSerializer):
    """Connexion par email au lieu de username."""
    username_field = 'email'

    def validate(self, attrs):
        email    = attrs.get('email', '').lower().strip()
        password = attrs.get('password', '')

        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {'email': 'Aucun compte trouvé avec cet email.'}
            )

        if not user.check_password(password):
            raise serializers.ValidationError(
                {'password': 'Mot de passe incorrect.'}
            )

        if not user.is_active:
            raise serializers.ValidationError({'email': 'Ce compte est désactivé.'})

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access':  str(refresh.access_token),
            'email':   user.email,
        }


class EmailTokenObtainView(TokenObtainPairView):
    serializer_class = EmailTokenObtainSerializer
