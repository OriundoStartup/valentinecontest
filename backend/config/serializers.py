from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Contestant

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
        data['email'] = contestant.email
        data['full_name'] = contestant.full_name
        data['id'] = contestant.id

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # ✅ Claims personalizados dentro del token
        token['email'] = user.email
        token['full_name'] = getattr(user, 'full_name', user.get_full_name())

        return token

    class Meta:
        fields = ['email', 'password']
