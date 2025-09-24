import os
from celery import Celery

# Establece el módulo de configuración de Django por defecto para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Crea la instancia de la aplicación Celery
app = Celery('valentine_contest')

# Configura Celery usando las configuraciones de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubre y carga las tareas de las aplicaciones registradas
app.autodiscover_tasks()
