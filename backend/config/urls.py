"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from valentine_contest.serializers import MyTokenObtainPairSerializer

urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),

    # Rutas principales del concurso
    path('api/contest/', include('valentine_contest.urls')),

    # Autenticación con JWT usando tu serializador personalizado
    path('api/token/', TokenObtainPairView.as_view(serializer_class=MyTokenObtainPairSerializer), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
