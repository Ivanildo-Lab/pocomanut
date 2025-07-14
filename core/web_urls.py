# core/web_urls.py (VERSÃO CORRIGIDA E ORGANIZADA)

from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    CustomLoginView,
    PocoListView,
    PocoDetailView,
    poco_create_update,
    poco_delete,
    gerar_relatorio_pdf,
    ClienteListView,
    cliente_create_update,
    cliente_delete,
    manutencao_create_update,
    manutencao_delete,
    partial_check_manutencoes
)

app_name = 'web'

urlpatterns = [
    # --- Autenticação ---
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'), # O redirect já está no settings

    # --- Módulo de Clientes ---
    path('clientes/', ClienteListView.as_view(), name='lista_clientes'),
    path('clientes/novo/', cliente_create_update, name='cliente_create'),
    path('clientes/<int:pk>/editar/', cliente_create_update, name='cliente_update'),
    path('clientes/<int:pk>/excluir/', cliente_delete, name='cliente_delete'),

    # --- Módulo de Poços e Manutenções ---
    # A raiz do app aponta para a lista de poços
    path('', PocoListView.as_view(), name='lista_pocos'),
    path('pocos/novo/', poco_create_update, name='poco_create'),
    # AS ROTAS MAIS ESPECÍFICAS VÊM PRIMEIRO
    path('pocos/<int:pk>/editar/', poco_create_update, name='poco_update'),
    path('pocos/<int:pk>/excluir/', poco_delete, name='poco_delete'),
    path('pocos/<int:pk>/pdf/', gerar_relatorio_pdf, name='gerar_pdf'),

    # --- ROTAS DE MANUTENÇÃO (ESPECÍFICAS) ---
    path('pocos/<int:poco_pk>/manutencoes/nova/', manutencao_create_update, name='manutencao_create'),
    path('pocos/<int:poco_pk>/manutencoes/<int:pk>/editar/', manutencao_create_update, name='manutencao_update'),
    path('pocos/<int:poco_pk>/manutencoes/<int:pk>/excluir/', manutencao_delete, name='manutencao_delete'),
    path('pocos/<int:poco_pk>/check-manutencoes/', partial_check_manutencoes, name='partial_check_manutencoes'),

    # A ROTA MAIS GENÉRICA VEM POR ÚLTIMO
    path('pocos/<int:pk>/', PocoDetailView.as_view(), name='detalhes_poco'),
]