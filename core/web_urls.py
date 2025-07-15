# core/web_urls.py (VERSÃO FINAL CORRIGIDA)

from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views # Importa o módulo de views para chamar a index_view

app_name = 'web'

urlpatterns = [
    # --- Rota Raiz e Autenticação ---
    # A raiz do site agora aponta para a nossa view de redirecionamento
    path('', views.index_view, name='index'), 
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # --- Módulo de Clientes ---
    path('clientes/', views.ClienteListView.as_view(), name='lista_clientes'),
    path('clientes/novo/', views.cliente_create_update, name='cliente_create'),
    path('clientes/<int:pk>/editar/', views.cliente_create_update, name='cliente_update'),
    path('clientes/<int:pk>/excluir/', views.cliente_delete, name='cliente_delete'),
    
    # --- Módulo de Poços ---
    path('pocos/', views.PocoListView.as_view(), name='lista_pocos'),
    path('pocos/novo/', views.poco_create_update, name='poco_create'),
    path('pocos/<int:pk>/editar/', views.poco_create_update, name='poco_update'),
    path('pocos/<int:pk>/excluir/', views.poco_delete, name='poco_delete'),
    path('pocos/<int:pk>/pdf/', views.gerar_relatorio_pdf, name='gerar_pdf'),
    
    # --- Detalhes do Poço e Manutenções ---
    path('pocos/<int:pk>/', views.PocoDetailView.as_view(), name='detalhes_poco'),
    path('pocos/<int:poco_pk>/check-manutencoes/', views.partial_check_manutencoes, name='partial_check_manutencoes'),
    path('pocos/<int:poco_pk>/manutencoes/nova/', views.manutencao_create_update, name='manutencao_create'),
    path('pocos/<int:poco_pk>/manutencoes/<int:pk>/editar/', views.manutencao_create_update, name='manutencao_update'),
    path('pocos/<int:poco_pk>/manutencoes/<int:pk>/excluir/', views.manutencao_delete, name='manutencao_delete'),
]