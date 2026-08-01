# core/web_urls.py (VERSÃO FINAL CORRIGIDA)

from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views # Importa o módulo de views para chamar a index_view
from .views import (dashboard_view, adicionar_foto_poco, definir_foto_principal, 
                    excluir_foto_poco, partial_check_fotos, adicionar_foto_bomba,
                    definir_foto_principal_bomba, excluir_foto_bomba, partial_check_fotos_bomba,
                    funcionario_create_update)

app_name = 'web'

urlpatterns = [
    # --- Rota Raiz e Autenticação ---
    path('', dashboard_view, name='dashboard'),
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
    path('pocos/<int:poco_pk>/adicionar-foto/', adicionar_foto_poco, name='adicionar_foto_poco'),
    path('pocos/<int:poco_pk>/fotos/<int:pk>/definir-principal/', definir_foto_principal, name='definir_foto_principal'),
    path('pocos/<int:poco_pk>/fotos/<int:pk>/excluir/', excluir_foto_poco, name='excluir_foto_poco'),
    path('pocos/<int:poco_pk>/check-fotos/', views.partial_check_fotos, name='partial_check_fotos'),

    # --- Detalhes do Poço e Manutenções ---
    path('pocos/<int:pk>/', views.PocoDetailView.as_view(), name='detalhes_poco'),
    path('pocos/<int:poco_pk>/check-manutencoes/', views.partial_check_manutencoes, name='partial_check_manutencoes'),
    path('pocos/<int:poco_pk>/manutencoes/nova/', views.manutencao_create_update, name='manutencao_create'),
    path('pocos/<int:poco_pk>/manutencoes/<int:pk>/editar/', views.manutencao_create_update, name='manutencao_update'),
    path('pocos/<int:poco_pk>/manutencoes/<int:pk>/excluir/', views.manutencao_delete, name='manutencao_delete'),

    # --- Módulo de Bombas ---
    path('bombas/', views.BombaListView.as_view(), name='lista_bombas'),
    path('bombas/nova/', views.bomba_create_update, name='bomba_create'),
    path('bombas/<int:pk>/editar/', views.bomba_create_update, name='bomba_update'),
    path('bombas/<int:pk>/excluir/', views.bomba_delete, name='bomba_delete'),
    path('bombas/<int:bomba_pk>/adicionar-foto/', adicionar_foto_bomba, name='adicionar_foto_bomba'),
    path('bombas/<int:bomba_pk>/fotos/<int:pk>/definir-principal/', definir_foto_principal_bomba, name='definir_foto_principal_bomba'),
    path('bombas/<int:bomba_pk>/fotos/<int:pk>/excluir/', excluir_foto_bomba, name='excluir_foto_bomba'),
    path('bombas/<int:bomba_pk>/check-fotos/', views.partial_check_fotos_bomba, name='partial_check_fotos_bomba'),

    # --- Módulo de Ordens de Serviço ---
    path('buscar-cliente/', views.buscar_cliente, name='buscar_cliente'),
    path('buscar-poco/', views.buscar_poco, name='buscar_poco'),
    path('buscar-bomba/', views.buscar_bomba, name='buscar_bomba'),
    path('ordens-servico/', views.OrdemServicoListView.as_view(), name='lista_os'),
    path('ordens-servico/nova/', views.os_create_update, name='os_create'),
    path('ordens-servico/<int:pk>/editar/', views.os_create_update, name='os_update'),
    path('ordens-servico/<int:pk>/excluir/', views.os_delete, name='os_delete'),
    path('ordens-servico/<int:pk>/', views.OrdemServicoDetailView.as_view(), name='detalhes_os'),
    path('ordens-servico/<int:pk>/atualizar-status/', views.os_atualizar_status, name='os_atualizar_status'),
    path('ordens-servico/<int:pk>/pdf/', views.gerar_os_pdf, name='gerar_os_pdf'),
    path('ordens-servico/<int:os_pk>/itens/adicionar/', views.item_os_add, name='item_os_add'),
    path('ordens-servico/<int:os_pk>/itens/<int:pk>/excluir/', views.item_os_delete, name='item_os_delete'),
    path('ordens-servico/<int:os_pk>/orcamento/', views.orcamento_update, name='orcamento_update'),
    path('ordens-servico/<int:os_pk>/orcamento/aprovar/', views.orcamento_aprovar, name='orcamento_aprovar'),
    path('ordens-servico/<int:os_pk>/fotos/adicionar/', views.foto_movimentacao_add, name='foto_movimentacao_add'),
    path('ordens-servico/<int:os_pk>/fotos/<int:pk>/excluir/', views.foto_movimentacao_delete, name='foto_movimentacao_delete'),

    # --- Módulo de Funcionários ---
    path('funcionarios/', views.FuncionarioListView.as_view(), name='lista_funcionarios'),
    path('funcionarios/novo/', views.funcionario_create_update, name='funcionario_create'),
    path('funcionarios/<int:pk>/editar/', views.funcionario_create_update, name='funcionario_update'),
    path('funcionarios/<int:pk>/excluir/', views.funcionario_delete, name='funcionario_delete'),
]