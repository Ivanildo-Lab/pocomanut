# ===================================================================
# IMPORTAÇÕES
# ===================================================================
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.db.models import Q
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from weasyprint import HTML

# Importações da API REST (podem ser mantidas)
from rest_framework import viewsets, permissions

# Importações locais do nosso app
from .models import Cliente, Poco, Manutencao
from .forms import PocoForm, ClienteForm, ManutencaoForm
from .serializers import ClienteSerializer, PocoSerializer, ManutencaoSerializer

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
    html_string = render_to_string('core/relatorio_poco_pdf.html', {'poco': poco})
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
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
