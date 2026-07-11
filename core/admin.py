# core/admin.py

from django.contrib import admin
from .models import (Cliente, Poco, Manutencao, Empresa, UserProfile, 
                     Bomba, FotoBomba, OrdemServico, ItemOS, Orcamento, FotoMovimentacao, Funcionario)

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
    list_display = ('nome_razao_social', 'cpf_cnpj', 'telefone', 'empresa')
    list_filter = ('empresa',)
    search_fields = ('nome_razao_social', 'cpf_cnpj')

@admin.register(Poco)
class PocoAdmin(admin.ModelAdmin):
    list_display = ('identificador_poco', 'cliente', 'get_empresa', 'cidade', 'estado')
    list_filter = ('cliente__empresa', 'estado', 'cidade')
    search_fields = ('identificador_poco', 'cliente__nome_razao_social')

    def get_empresa(self, obj):
        return obj.cliente.empresa
    get_empresa.short_description = 'Empresa'
    get_empresa.admin_order_field = 'cliente__empresa'


@admin.register(Manutencao)
class ManutencaoAdmin(admin.ModelAdmin):
    list_display = ('poco', 'data_manutencao', 'tipo_servico', 'operador_responsavel')
    list_filter = ('data_manutencao', 'tipo_servico', 'operador_responsavel')
    search_fields = ('poco__identificador_poco', 'observacoes')


@admin.register(Bomba)
class BombaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'modelo', 'marca', 'potencia', 'voltagem', 'empresa', 'ativo')
    list_filter = ('empresa', 'marca', 'voltagem', 'ativo')
    search_fields = ('descricao', 'modelo', 'marca', 'numero_nota_fiscal')


class FotoBombaInline(admin.TabularInline):
    model = FotoBomba
    extra = 1


@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ('numero_os', 'cliente', 'status', 'prioridade', 'data_abertura', 
                    'funcionario_responsavel', 'empresa')
    list_filter = ('empresa', 'status', 'prioridade', 'data_abertura')
    search_fields = ('numero_os', 'cliente__nome_razao_social', 'observacoes')
    readonly_fields = ('numero_os', 'data_abertura', 'data_conclusao')


@admin.register(ItemOS)
class ItemOSAdmin(admin.ModelAdmin):
    list_display = ('os', 'descricao', 'quantidade', 'valor_unitario', 'valor_total')
    list_filter = ('os__status',)
    search_fields = ('os__numero_os', 'descricao')


@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ('os', 'valor_total', 'aprovado', 'data_aprovacao', 'enviado_cliente')
    list_filter = ('aprovado', 'enviado_cliente')
    search_fields = ('os__numero_os', 'observacoes')


@admin.register(FotoMovimentacao)
class FotoMovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('os', 'tipo_foto', 'descricao', 'data_upload')
    list_filter = ('tipo_foto', 'data_upload')
    search_fields = ('os__numero_os', 'descricao')


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'cpf', 'cargo', 'telefone', 'empresa', 'ativo')
    list_filter = ('empresa', 'cargo', 'ativo')
    search_fields = ('nome_completo', 'cpf')