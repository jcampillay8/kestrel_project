from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.translation import get_language

class HomeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Verifica si el usuario es autenticado o invitado
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=status.HTTP_403_FORBIDDEN)

        context = {
            'current_page': 'home',
            'LANGUAGE_CODE': get_language(),
        }
        return Response(context, status=status.HTTP_200_OK)

class WelcomeAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Redirigir al home si el usuario está autenticado
        if request.user.is_authenticated and not request.session.get('is_guest', False):
            return Response({"detail": "Redirecting to home"}, status=status.HTTP_302_FOUND)

        context = {
            'current_page': 'welcome',
        }
        return Response(context, status=status.HTTP_200_OK)
