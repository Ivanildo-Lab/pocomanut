# core/web_urls.py (NOVO ARQUIVO)

from django.urls import path
from .views import PocoListView,poco_create_update, gerar_relatorio_pdf, poco_delete,ClienteListView 
from .views import cliente_create_update, cliente_delete, PocoDetailView, manutencao_create_update, manutencao_delete


# O nome 'app_name' é uma boa prática para organizar URLs
app_name = 'web'

urlpatterns = [
    # Lista de poços (página principal)
    path('', PocoListView.as_view(), name='lista_pocos'),
     # URL para abrir o formulário de criação
    path('pocos/novo/', poco_create_update, name='poco_create'),
    # URL para abrir o formulário de edição (passando o 'pk' do poço)
    path('pocos/<int:pk>/editar/', poco_create_update, name='poco_update'),
    # URL para gerar o relatório PDF
    path('pocos/<int:pk>/pdf/', gerar_relatorio_pdf, name='gerar_pdf'),
    # URL para deletar um poço
    path('pocos/<int:pk>/excluir/', poco_delete, name='poco_delete'),
    path('clientes/', ClienteListView.as_view(), name='lista_clientes'),
    path('clientes/', ClienteListView.as_view(), name='lista_clientes'),
    path('clientes/novo/', cliente_create_update, name='cliente_create'),
    path('clientes/<int:pk>/editar/', cliente_create_update, name='cliente_update'),
    path('clientes/<int:pk>/excluir/', cliente_delete, name='cliente_delete'),
    path('pocos/<int:pk>/', PocoDetailView.as_view(), name='detalhes_poco'),
    path('pocos/<int:poco_pk>/manutencoes/nova/', manutencao_create_update, name='manutencao_create'),
    path('pocos/<int:poco_pk>/manutencoes/<int:pk>/editar/', manutencao_create_update, name='manutencao_update'),
    path('pocos/<int:poco_pk>/manutencoes/<int:pk>/excluir/', manutencao_delete, name='manutencao_delete'),
    ]