from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    ContestantRegisterAPIView,
    ContestantVerifyAPIView,
    VerifiedContestantsListAPIView,
    DrawWinnerAPIView
)

urlpatterns = [
    # Registro y listado de concursantes
    path('contestants/', ContestantRegisterAPIView.as_view(), name='contestant-register'),

    # Verificación de cuenta (token + contraseña)
    path('verify-account/', ContestantVerifyAPIView.as_view(), name='contestant-verify'),

    # Listado de concursantes verificados
    path('verified-contestants/', VerifiedContestantsListAPIView.as_view(), name='verified-contestants'),

    # Sorteo del ganador (solo admin)
    path('draw-winner/', DrawWinnerAPIView.as_view(), name='draw-winner'),

    # Autenticación con JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
