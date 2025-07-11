# core/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, PocoViewSet, ManutencaoViewSet

# Cria uma instância do router
router = DefaultRouter()

# Registra nossas ViewSets com o router
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'pocos', PocoViewSet, basename='poco')
router.register(r'manutencoes', ManutencaoViewSet, basename='manutencao')

# As URLs da API são agora determinadas automaticamente pelo router
urlpatterns = [
    path('', include(router.urls)),
]