from django.contrib import admin

# Register your models here.
# core/admin.py - Versão Melhorada

from django.contrib import admin
from .models import Cliente, Poco, Manutencao

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome_razao_social', 'cpf_cnpj', 'telefone')
    search_fields = ('nome_razao_social', 'cpf_cnpj')

@admin.register(Poco)
class PocoAdmin(admin.ModelAdmin):
    list_display = ('identificador_poco', 'cliente', 'cidade', 'estado', 'data_perfuração_inicial')
    list_filter = ('estado', 'cidade')
    search_fields = ('identificador_poco', 'cliente__nome_razao_social') # Busca dentro do nome do cliente

@admin.register(Manutencao)
class ManutencaoAdmin(admin.ModelAdmin):
    list_display = ('poco', 'data_manutencao', 'tipo_servico', 'operador_responsavel')
    list_filter = ('data_manutencao', 'tipo_servico', 'operador_responsavel')
    search_fields = ('poco__identificador_poco', 'observacoes')