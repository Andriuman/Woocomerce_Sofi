from django.urls import path, include
from rest_framework import routers
from tasks import views
from rest_framework.documentation import include_docs_urls

# Importa aquí tu vista si está en otro lugar, ajusta este import según sea necesario
# from miapp.views import vista_script

router = routers.DefaultRouter()


urlpatterns = [
    path("", include(router.urls)),
    path('docs/', include_docs_urls(title="Usuarios API")),
    # Agrega tu vista aquí
    path('ejecutar-script/', views.vista_script, name='ejecutar_script'),
]
