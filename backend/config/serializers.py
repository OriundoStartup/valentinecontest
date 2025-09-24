from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Se define una clase llamada 'MyTokenObtainPairSerializer' que hereda de
# 'TokenObtainPairSerializer', la clase base de Django REST Framework Simple JWT.
# Esto nos permite extender su funcionalidad.
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializador personalizado para generar tokens JWT.
    
    Este serializador extiende el TokenObtainPairSerializer para incluir
    información adicional del usuario (como el email) en el token.
    """
    @classmethod
    def get_token(cls, user):
        """
        Sobrescribe el método 'get_token' para añadir datos personalizados.

        Este método se encarga de crear el token y añadirle 'claims' adicionales.
        """
        # Se llama al método get_token de la clase padre para obtener el token
        # JWT estándar, que ya contiene la información básica del usuario.
        token = super().get_token(user)

        # Se accede al token como un diccionario y se le añade una nueva clave
        # 'email' con el valor del email del objeto 'user'.
        token['email'] = user.email

        # Se retorna el token modificado, que ahora incluye el email.
        return token