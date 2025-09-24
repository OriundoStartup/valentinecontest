from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    ContestantRegisterAPIView,
    ContestantVerifyAPIView,
    VerifiedContestantsListAPIView,
    AllContestantsView,
    DrawWinnerView
)

urlpatterns = [
    # Registro de concursantes
    path('contestants/', ContestantRegisterAPIView.as_view(), name='contestant-register'),

    # Verificación de cuenta (token + contraseña)
    path('verify-account/', ContestantVerifyAPIView.as_view(), name='contestant-verify'),

    path('verified-contestants/', VerifiedContestantsListAPIView.as_view()),
    path('all-contestants/', AllContestantsView.as_view()),  


    # Sorteo del ganador (solo admin)
    path('draw-winner/', DrawWinnerView.as_view(), name='draw-winner'),
    


    # Autenticación con JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
