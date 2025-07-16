# ===================================================================
# IMPORTAÇÕES
# ===================================================================
from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.db.models import Q
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from weasyprint import HTML
from pathlib import Path
# Importações da API REST (podem ser mantidas)
from rest_framework import viewsets, permissions

# Importações locais do nosso app
from .models import Cliente, Poco, Manutencao
from .forms import PocoForm, ClienteForm, ManutencaoForm
from .serializers import ClienteSerializer, PocoSerializer, ManutencaoSerializer

# Importações adicionais do dashboard
from django.db.models import Count, Avg
from django.db.models.functions import TruncMonth
from django.utils import timezone
import json
from django.conf import settings
import os

# ===================================================================
# GERAR O DASHBOARD
# ===================================================================
@login_required
def dashboard_view(request):
    # --- Cálculos para os Cards de Resumo ---
    total_clientes = Cliente.objects.count()
    total_pocos = Poco.objects.count()
    total_manutencoes = Manutencao.objects.count()
    
    # Métrica de vazão média (evita erro se não houver manutenções)
    vazao_media_data = Manutencao.objects.aggregate(media=Avg('vazao_medida'))
    vazao_media = vazao_media_data['media'] or 0

    # --- Dados para o Gráfico de Manutenções por Mês ---
    # Pega os últimos 12 meses
    doze_meses_atras = timezone.now() - timezone.timedelta(days=365)
    
    manutencoes_por_mes = (
        Manutencao.objects
        .filter(data_manutencao__gte=doze_meses_atras)
        .annotate(mes=TruncMonth('data_manutencao'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )
    # Formata os dados para o Chart.js
    grafico_labels = [m['mes'].strftime('%b/%Y') for m in manutencoes_por_mes]
    grafico_data = [m['total'] for m in manutencoes_por_mes]
    
    # --- Dados para a Tabela de Últimas Atividades ---
    ultimas_manutencoes = Manutencao.objects.select_related('poco', 'poco__cliente').order_by('-data_manutencao')[:5]

    context = {
        'total_clientes': total_clientes,
        'total_pocos': total_pocos,
        'total_manutencoes': total_manutencoes,
        'vazao_media': vazao_media,
        'grafico_labels': json.dumps(grafico_labels), # Converte para string JSON
        'grafico_data': json.dumps(grafico_data),
        'ultimas_manutencoes': ultimas_manutencoes,
        'pagina_ativa': 'dashboard' # Para destacar o link no menu
    }
    return render(request, 'core/dashboard.html', context)

# ===================================================================
# VIEWS DE AUTENTICAÇÃO
# ===================================================================
class CustomLoginView(LoginView):
    template_name = 'core/login.html'

# ===================================================================
# VIEWS DE LISTAGEM E DETALHES (PÁGINAS PRINCIPAIS)
# ===================================================================
class PocoListView(ListView):
    model = Poco
    template_name = 'core/lista_pocos.html'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('cliente')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(identificador_poco__icontains=query) |
                Q(cliente__nome_razao_social__icontains=query)
            )
        return queryset.order_by('-data_perfuração_inicial')

    def get_template_names(self):
        if self.request.htmx:
            return ['core/partials/lista_pocos_tabela.html']
        return [self.template_name]

class ClienteListView(ListView):
    model = Cliente
    template_name = 'core/lista_clientes.html'
    context_object_name = 'clientes'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nome_razao_social__icontains=query) |
                Q(cpf_cnpj__icontains=query) |
                Q(cidade__icontains=query)
            )
        return queryset.order_by('nome_razao_social')

    def get_template_names(self):
        if self.request.htmx:
            return ['core/partials/lista_clientes_tabela.html']
        return [self.template_name]

class PocoDetailView(DetailView):
    model = Poco
    template_name = 'core/detalhes_poco.html'
    context_object_name = 'poco'

# ===================================================================
# VIEWS DE CRUD (CREATE, UPDATE, DELETE)
# Todas protegidas por login e usando o padrão de resposta robusto
# ===================================================================
    
# --- CRUD de Poços ---
@login_required
def poco_create_update(request, pk=None):
    if pk:
        instance = get_object_or_404(Poco, pk=pk)
    else:
        instance = None
    form = PocoForm(request.POST or None, request.FILES or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return render(request, 'core/partials/_success_triggers.html', {
            'toast_message': "Poço salvo com sucesso!",
            'update_event': 'updatePocoList'
        })
    context = {'form': form, 'instance': instance}
    return render(request, 'core/partials/_poco_form.html', context)

@login_required
def poco_delete(request, pk):
    poco = get_object_or_404(Poco, pk=pk)
    if request.method == 'POST':
        nome_poco = poco.identificador_poco
        poco.delete()
        return render(request, 'core/partials/_success_triggers.html', {
            'toast_message': f"Poço '{nome_poco}' excluído com sucesso.",
            'update_event': 'updatePocoList'
        })
    return render(request, 'core/partials/_poco_delete_confirm.html', {'poco': poco})

# --- CRUD de Clientes ---
@login_required
def cliente_create_update(request, pk=None):
    if pk:
        instance = get_object_or_404(Cliente, pk=pk)
    else:
        instance = None
    form = ClienteForm(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return render(request, 'core/partials/_success_triggers.html', {
            'toast_message': "Cliente salvo com sucesso!",
            'update_event': 'updateClienteList'
        })
    context = {'form': form}
    return render(request, 'core/partials/_cliente_form.html', context)

@login_required
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        nome_cliente = cliente.nome_razao_social
        cliente.delete()
        return render(request, 'core/partials/_success_triggers.html', {
            'toast_message': f"Cliente '{nome_cliente}' excluído com sucesso.",
            'update_event': 'updateClienteList'
        })
    context = {'cliente': cliente}
    return render(request, 'core/partials/_cliente_delete_confirm.html', context)

# --- CRUD de Manutenções ---
@login_required
def manutencao_create_update(request, poco_pk, pk=None):
    poco = get_object_or_404(Poco, pk=poco_pk)
    if pk:
        instance = get_object_or_404(Manutencao, pk=pk, poco=poco)
    else:
        instance = None
    form = ManutencaoForm(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        manutencao = form.save(commit=False)
        manutencao.poco = poco
        manutencao.operador_responsavel = request.user
        manutencao.save()
        return render(request, 'core/partials/_success_triggers.html', {
            'toast_message': "Registro de manutenção salvo com sucesso!",
            'update_event': 'updateManutencaoList'
        })
    context = {'form': form, 'poco': poco}
    return render(request, 'core/partials/_manutencao_form.html', context)

@login_required
def manutencao_delete(request, poco_pk, pk):
    manutencao = get_object_or_404(Manutencao, pk=pk, poco_id=poco_pk)
    if request.method == 'POST':
        manutencao.delete()
        return render(request, 'core/partials/_success_triggers.html', {
            'toast_message': "Registro de manutenção excluído com sucesso.",
            'update_event': 'updateManutencaoList'
        })
    context = {'manutencao': manutencao}
    return render(request, 'core/partials/_manutencao_delete_confirm.html', context)


@login_required
def partial_check_manutencoes(request, poco_pk):
    """
    Uma view que retorna apenas o fragmento HTML da tabela de manutenções.
    Usada para atualizar a lista via HTMX.
    """
    poco = get_object_or_404(Poco, pk=poco_pk)
    context = {'manutencoes': poco.historico_manutencoes.all(), 'poco': poco}
    return render(request, 'core/partials/lista_manutencoes_tabela.html', context)
# ===================================================================
# VIEW DE GERAÇÃO DE PDF
# ===================================================================
@login_required
def gerar_relatorio_pdf(request, pk):
    poco = get_object_or_404(Poco, pk=pk)
    
    # --- LÓGICA CORRIGIDA PARA O CAMINHO DA IMAGEM ---
    caminho_imagem = None
    if poco.foto_principal:
        # Cria o caminho completo do arquivo
        caminho_completo = Path(settings.MEDIA_ROOT) / poco.foto_principal.name
        
        # Verifica se o arquivo existe E o transforma em uma URL file://
        if caminho_completo.exists():
            caminho_imagem = caminho_completo.as_uri()    # --------------------------------------------------

    context = {
        'poco': poco,
        'caminho_imagem': caminho_imagem # Passa o caminho para o template
    }
    
    html_string = render_to_string('core/relatorio_poco_pdf.html', context)
    
    # O base_url é importante para que o WeasyPrint possa resolver outros caminhos relativos
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    
    pdf = html.write_pdf()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="relatorio_poco_{poco.id}.pdf"'
    
    return response
# ===================================================================
# VIEWS DA API REST (mantidas para referência ou uso futuro)
# ===================================================================
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]

class PocoViewSet(viewsets.ModelViewSet):
    queryset = Poco.objects.all().order_by('-data_perfuração_inicial')
    serializer_class = PocoSerializer
    permission_classes = [permissions.IsAuthenticated]

class ManutencaoViewSet(viewsets.ModelViewSet):
    queryset = Manutencao.objects.all()
    serializer_class = ManutencaoSerializer
    permission_classes = [permissions.IsAuthenticated]
