from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from .models import Contestant

# Se obtiene el modelo de usuario activo en el proyecto (ej. Contestant).
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Personaliza el serializador de token para usar el correo electrónico como nombre de usuario.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

    def validate(self, attrs):
        # Valida las credenciales utilizando el correo electrónico.
        # Aquí se obtiene el usuario por email en lugar de username.
        try:
            user = User.objects.get(email=attrs['username'])
        except User.DoesNotExist:
            raise serializers.ValidationError('Correo o contraseña incorrectos.')
        
        attrs['username'] = user.username
        data = super().validate(attrs)
        return data


class ContestantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contestant
        fields = ['full_name', 'email', 'phone']
        read_only_fields = ['is_verified', 'is_staff', 'is_active', 'is_winner', 'date_joined']

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return data

class ContestantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contestant
        fields = ['full_name', 'email', 'is_verified', 'is_winner']