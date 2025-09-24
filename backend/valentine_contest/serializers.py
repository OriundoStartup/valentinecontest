from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Contestant

# 🔐 Login personalizado con validación y datos extra
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            contestant = Contestant.objects.get(email=email)
        except Contestant.DoesNotExist:
            raise serializers.ValidationError('Correo no registrado.')

        if not contestant.check_password(password):
            raise serializers.ValidationError('Contraseña incorrecta.')

        if not contestant.is_verified:
            raise serializers.ValidationError('Tu cuenta no está verificada.')

        # Validación JWT estándar
        data = super().validate({'username': contestant.email, 'password': password})

        # ✅ Datos extra para el frontend
        data['full_name'] = contestant.full_name
        data['email'] = contestant.email
        data['id'] = contestant.id

        return data

    class Meta:
        fields = ['email', 'password']


# 📝 Registro y edición de concursantes
class ContestantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contestant
        fields = ['full_name', 'email', 'phone']
        read_only_fields = ['is_verified', 'is_staff', 'is_active', 'is_winner', 'date_joined']


# 🔐 Validación de contraseña doble
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


# 📋 Detalle extendido del concursante
class ContestantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contestant
        fields = ['full_name', 'email', 'is_verified', 'is_winner']
