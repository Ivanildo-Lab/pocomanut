# core/admin.py

from django.contrib import admin
from .models import Cliente, Poco, Manutencao, Empresa, UserProfile 

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome_fantasia', 'cnpj', 'telefone')
    search_fields = ('nome_fantasia', 'razao_social', 'cnpj')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'empresa')
    list_filter = ('empresa',)
    search_fields = ('user__username', 'empresa__nome_fantasia')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    # Adicionamos 'empresa' à lista para ver a qual empresa cada cliente pertence
    list_display = ('nome_razao_social', 'cpf_cnpj', 'telefone', 'empresa')
    list_filter = ('empresa',) # Permite filtrar clientes por empresa
    search_fields = ('nome_razao_social', 'cpf_cnpj')

@admin.register(Poco)
class PocoAdmin(admin.ModelAdmin):
    # Adicionamos 'cliente__empresa' para ver a empresa indiretamente
    list_display = ('identificador_poco', 'cliente', 'get_empresa', 'cidade', 'estado')
    list_filter = ('cliente__empresa', 'estado', 'cidade')
    search_fields = ('identificador_poco', 'cliente__nome_razao_social')

    # Método para exibir o nome da empresa na lista
    def get_empresa(self, obj):
        return obj.cliente.empresa
    get_empresa.short_description = 'Empresa'
    get_empresa.admin_order_field = 'cliente__empresa'


@admin.register(Manutencao)
class ManutencaoAdmin(admin.ModelAdmin):
    list_display = ('poco', 'data_manutencao', 'tipo_servico', 'operador_responsavel')
    list_filter = ('data_manutencao', 'tipo_servico', 'operador_responsavel')
    search_fields = ('poco__identificador_poco', 'observacoes')