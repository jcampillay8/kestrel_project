from django.urls import path
from .views import HomeAPIView, WelcomeAPIView

urlpatterns = [
    path('', WelcomeAPIView.as_view(), name='welcome'),  # Ruta para welcome
    path('home/', HomeAPIView.as_view(), name='home'),  # Ruta para home
]
