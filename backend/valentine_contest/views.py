from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Contestant
from .serializers import ContestantSerializer, MyTokenObtainPairSerializer
from .tasks import send_verification_email_task, send_winner_notification_task

import random

# 🔐 Login personalizado con JWT
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# 📝 Registro de concursantes
class ContestantRegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        contestants = Contestant.objects.all().order_by('-date_joined')
        serializer = ContestantSerializer(contestants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ContestantSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if Contestant.objects.filter(email=email).exists():
                return Response(
                    {'email': ['Este correo electrónico ya está registrado.']},
                    status=status.HTTP_400_BAD_REQUEST
                )
            contestant = serializer.save()
            verification_url = f"http://127.0.0.1:5173/verify/{str(contestant.verification_token)}"
            send_verification_email_task.delay(contestant.email, verification_url)
            return Response(
                {'message': 'Inscripción exitosa. Revisa tu correo para verificar tu cuenta.'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Verificación de cuenta
class ContestantVerifyAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        password = request.data.get('password')
        if not token or not password:
            return Response({'error': 'Token y contraseña son requeridos.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            contestant = Contestant.objects.get(verification_token=token, is_verified=False)
            contestant.is_verified = True
            contestant.set_password(password)
            contestant.save()
            return Response({'message': 'Tu cuenta ha sido verificada. ¡Ya estás participando en el sorteo!'}, status=status.HTTP_200_OK)
        except Contestant.DoesNotExist:
            return Response({'error': 'Enlace de verificación inválido o expirado.'}, status=status.HTTP_400_BAD_REQUEST)

# 📋 Listado de concursantes verificados
class VerifiedContestantsListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        contestants = Contestant.objects.filter(is_verified=True).order_by('date_joined')
        serializer = ContestantSerializer(contestants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 📋 Listado completo de concursantes
class AllContestantsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        contestants = Contestant.objects.all().order_by('-date_joined')
        serializer = ContestantSerializer(contestants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 🎉 Sorteo del ganador
class DrawWinnerView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        verified_contestants = Contestant.objects.filter(is_verified=True)
        print(f"Número de concursantes verificados: {verified_contestants.count()}")  # Para depuración

        if not verified_contestants.exists():
            return Response({'error': 'No hay concursantes verificados para realizar un sorteo.'}, status=status.HTTP_400_BAD_REQUEST)

        # Reiniciar estado de ganadores anteriores
        Contestant.objects.filter(is_winner=True).update(is_winner=False)

        # Seleccionar nuevo ganador
        winner = random.choice(verified_contestants)
        winner.is_winner = True
        winner.save()

        send_winner_notification_task.delay(winner.email, winner.full_name)

        return Response({
            'full_name': winner.full_name,
            'email': winner.email
        }, status=status.HTTP_200_OK)
