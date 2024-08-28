from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Aquí puedes definir un enrutador para tus vistas de API basadas en viewsets
router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Puedes agregar tus rutas de API aquí
    path("authentication/", include("apps.authentication.urls")),
    path("", include("apps.home.urls")),
]
