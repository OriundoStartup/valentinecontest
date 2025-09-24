# valentine_contest/models.py
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Se define un administrador de modelos personalizado para la clase 'Contestant'.
# Hereda de 'BaseUserManager', que proporciona los métodos base para manejar usuarios.
class ContestantManager(BaseUserManager):
    """
    Manager de modelo personalizado para la clase Contestant.
    
    Proporciona métodos para la creación de usuarios y superusuarios,
    asegurando un manejo seguro y correcto de los campos.
    """
    def create_user(self, email, full_name, password, phone=None):
        """
        Crea y guarda un usuario 'Contestant' con el email y contraseña dados.
        """
        # Se asegura de que el campo de email no esté vacío, lo cual es crucial para la autenticación.
        if not email:
            raise ValueError('The Email field must be set')
        
        # Se normaliza el email para estandarizarlo (por ejemplo, 'example@DOMAIN.com' -> 'example@domain.com').
        # Esto previene problemas de autenticación debido a mayúsculas.
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            phone=phone,
        )
        
        # Se usa 'set_password' para hashear la contraseña de forma segura.
        # Nunca se debe guardar la contraseña en texto plano en la base de datos.
        user.set_password(password)
        
        # Se guarda el objeto de usuario en la base de datos.
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, full_name='Admin', phone=None):
        """
        Crea y guarda un superusuario 'Contestant' con privilegios de administrador.
        """
        # Se usa el método 'create_user' para evitar la duplicación de código.
        user = self.create_user(
            email=email,
            full_name=full_name,
            phone=phone,
            password=password,
        )
        
        # Se establecen los campos de privilegios para que el usuario sea un superusuario
        # y tenga acceso al panel de administración de Django.
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True # Un superusuario siempre debe considerarse verificado.
        
        # Se guardan los cambios en el objeto del usuario.
        user.save(using=self._db)
        return user


# Se define el modelo de usuario personalizado 'Contestant'.
# Hereda de 'AbstractBaseUser' y 'PermissionsMixin' para un control total
# sobre el modelo de usuario y sus permisos.
class Contestant(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuario personalizado para el concurso.
    
    Utiliza un ID de UUID para mayor seguridad y privacidad,
    evitando que los IDs de usuario sean predecibles.
    """
    # El campo 'id' se establece como un UUID, lo que es una buena práctica
    # para evitar ataques de enumeración de IDs.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255, verbose_name="Nombre Completo")
    # El campo 'email' es único para asegurar que no haya dos usuarios con el mismo email.
    email = models.EmailField(unique=True, verbose_name="Dirección de Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Número de Teléfono")
    
    # Campos de estado del usuario.
    is_verified = models.BooleanField(default=False, verbose_name="Verificado")
    # 'verification_token' se usa para la confirmación de email y es único para cada usuario.
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_staff = models.BooleanField(default=False, verbose_name="Es Miembro del Staff")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    is_winner = models.BooleanField(default=False, verbose_name="Es Ganador")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    # Define el campo de autenticación principal.
    USERNAME_FIELD = 'email'
    # Define los campos que se requerirán al crear un usuario a través de 'createsuperuser'.
    REQUIRED_FIELDS = ['full_name']

    # Se asocia el manager de modelo personalizado a este modelo.
    objects = ContestantManager()

    # Define la representación de cadena del objeto, útil para la administración de Django.
    def __str__(self):
        return self.email

    # Se agregan los campos de 'groups' y 'user_permissions' de forma explícita.
    # Esto es una buena práctica al usar un modelo de usuario personalizado.
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='contestant_groups_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='contestant_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )