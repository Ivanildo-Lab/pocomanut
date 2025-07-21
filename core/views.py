# Em core/views.py
# ===================================================================
# IMPORTAÇÕES
# ===================================================================
import json
import os
from pathlib import Path

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.db.models import Avg, Count, Q
from django.db.models.functions import TruncMonth
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.generic import DetailView, ListView
from rest_framework import permissions, viewsets
from weasyprint import HTML

# Importações locais do nosso app
from .forms import ClienteForm, FotoPocoForm, ManutencaoForm, PocoForm
from .models import Cliente, FotoPoco, Manutencao, Poco
from .serializers import (ClienteSerializer, ManutencaoSerializer,
                          PocoSerializer)


# ===================================================================
# VIEW DE ENTRADA E DASHBOARD
# ===================================================================
@login_required
def dashboard_view(request):
    empresa_do_usuario = request.user.profile.empresa
    
    # Filtra os dados pela empresa do usuário
    clientes_da_empresa = Cliente.objects.filter(empresa=empresa_do_usuario)
    pocos_da_empresa = Poco.objects.filter(cliente__empresa=empresa_do_usuario)
    manutencoes_da_empresa = Manutencao.objects.filter(poco__cliente__empresa=empresa_do_usuario)

    total_clientes = clientes_da_empresa.count()
    total_pocos = pocos_da_empresa.count()
    total_manutencoes = manutencoes_da_empresa.count()
    
    vazao_media_data = manutencoes_da_empresa.aggregate(media=Avg('vazao_medida'))
    vazao_media = vazao_media_data['media'] or 0

    doze_meses_atras = timezone.now() - timezone.timedelta(days=365)
    manutencoes_por_mes = (
        manutencoes_da_empresa
        .filter(data_manutencao__gte=doze_meses_atras)
        .annotate(mes=TruncMonth('data_manutencao'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )
    grafico_labels = [m['mes'].strftime('%b/%Y') for m in manutencoes_por_mes]
    grafico_data = [m['total'] for m in manutencoes_por_mes]
    
    ultimas_manutencoes = manutencoes_da_empresa.select_related('poco', 'poco__cliente').order_by('-data_manutencao')[:5]

    context = {
        'total_clientes': total_clientes,
        'total_pocos': total_pocos,
        'total_manutencoes': total_manutencoes,
        'vazao_media': vazao_media,
        'grafico_labels': json.dumps(grafico_labels),
        'grafico_data': json.dumps(grafico_data),
        'ultimas_manutencoes': ultimas_manutencoes,
        'pagina_ativa': 'dashboard'
    }
    return render(request, 'core/dashboard.html', context)

# ===================================================================
# VIEWS DE AUTENTICAÇÃO
# ===================================================================
class CustomLoginView(LoginView):
    template_name = 'core/login.html'

# ===================================================================
# VIEWS DE LISTAGEM E DETALHES
# ===================================================================
class PocoListView(ListView):
    # ... (seu código está correto, mantido como está)
    model = Poco
    template_name = 'core/lista_pocos.html'
    def get_queryset(self):
        empresa_do_usuario = self.request.user.profile.empresa
        queryset = Poco.objects.filter(cliente__empresa=empresa_do_usuario).select_related('cliente')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(identificador_poco__icontains=query) | Q(cliente__nome_razao_social__icontains=query))
        return queryset.order_by('-data_perfuração_inicial')
    def get_template_names(self):
        if self.request.htmx:
            return ['core/partials/lista_pocos_tabela.html']
        return [self.template_name]


class ClienteListView(ListView):
    # ... (seu código está correto, mantido como está)
    model = Cliente
    template_name = 'core/lista_clientes.html'
    context_object_name = 'clientes'
    def get_queryset(self):
        empresa_do_usuario = self.request.user.profile.empresa
        queryset = Cliente.objects.filter(empresa=empresa_do_usuario)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(nome_razao_social__icontains=query) | Q(cpf_cnpj__icontains=query) | Q(cidade__icontains=query))
        return queryset.order_by('nome_razao_social')
    def get_template_names(self):
        if self.request.htmx:
            return ['core/partials/lista_clientes_tabela.html']
        return [self.template_name]


class PocoDetailView(DetailView):
    model = Poco
    template_name = 'core/detalhes_poco.html'
    context_object_name = 'poco'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['foto_form'] = FotoPocoForm()
        return context

# ===================================================================
# VIEWS DE CRUD
# ===================================================================
# --- Poços ---
@login_required
def poco_create_update(request, pk=None):
    empresa_do_usuario = request.user.profile.empresa
    if pk:
        instance = get_object_or_404(Poco, pk=pk, cliente__empresa=empresa_do_usuario)
    else:
        instance = None
    form = PocoForm(request.POST or None, request.FILES or None, instance=instance, empresa=empresa_do_usuario) 
    if request.method == 'POST' and form.is_valid():
        form.save()
        return render(request, 'core/partials/_success_triggers.html', {'toast_message': "Poço salvo com sucesso!", 'update_event': 'updatePocoList'})
    context = {'form': form, 'instance': instance}
    return render(request, 'core/partials/_poco_form.html', context)

@login_required
def poco_delete(request, pk):
    # ... (seu código está correto, mantido como está)
    empresa_do_usuario = request.user.profile.empresa
    poco = get_object_or_404(Poco, pk=pk, cliente__empresa=empresa_do_usuario)
    if request.method == 'POST':
        nome_poco = poco.identificador_poco
        poco.delete()
        return render(request, 'core/partials/_success_triggers.html', {'toast_message': f"Poço '{nome_poco}' excluído com sucesso.",'update_event': 'updatePocoList'})
    return render(request, 'core/partials/_poco_delete_confirm.html', {'poco': poco})

# --- Fotos do Poço ---
@login_required
def adicionar_foto_poco(request, poco_pk):
    # ... (seu código está correto, mantido como está)
    empresa_do_usuario = request.user.profile.empresa
    poco = get_object_or_404(Poco, pk=poco_pk, cliente__empresa=empresa_do_usuario)
    if request.method == 'POST':
        form = FotoPocoForm(request.POST, request.FILES)
        if form.is_valid():
            foto = form.save(commit=False)
            foto.poco = poco
            foto.save()
            return render(request, 'core/partials/_galeria_fotos.html', {'poco': poco})
    return HttpResponseBadRequest("Método inválido ou formulário inválido")

@login_required
def definir_foto_principal(request, poco_pk, pk):
    # ... (seu código está correto, mantido como está)
    empresa_do_usuario = request.user.profile.empresa
    poco = get_object_or_404(Poco, pk=poco_pk, cliente__empresa=empresa_do_usuario)
    foto_a_definir = get_object_or_404(FotoPoco, pk=pk, poco=poco)
    if request.method == 'POST':
        with transaction.atomic():
            poco.fotos.update(is_principal=False)
            foto_a_definir.is_principal = True
            foto_a_definir.save()
        return render(request, 'core/partials/_galeria_fotos.html', {'poco': poco})
    return HttpResponseBadRequest("Método não permitido")

@login_required
def excluir_foto_poco(request, poco_pk, pk):
    empresa_do_usuario = request.user.profile.empresa
    poco = get_object_or_404(Poco, pk=poco_pk, cliente__empresa=empresa_do_usuario)
    foto_a_excluir = get_object_or_404(FotoPoco, pk=pk, poco=poco)
    
    # Se a requisição for GET, mostra a confirmação no modal
    if request.method == 'GET':
        return render(request, 'core/partials/_foto_delete_confirm.html', {'foto': foto_a_excluir})

    # Se a requisição for POST, executa a exclusão
    if request.method == 'POST':
        foto_a_excluir.delete()
        # Retorna os gatilhos para fechar o modal, mostrar o toast e atualizar a galeria
        return render(request, 'core/partials/_success_triggers.html', {
            'toast_message': 'Foto excluída com sucesso.',
            'update_event': 'updateGaleria'
        })
    
    return HttpResponseBadRequest("Método não permitido")

@login_required
def partial_check_fotos(request, poco_pk):
    empresa_do_usuario = request.user.profile.empresa
    poco = get_object_or_404(Poco, pk=poco_pk, cliente__empresa=empresa_do_usuario)
    return render(request, 'core/partials/_galeria_fotos.html', {'poco': poco})

# --- Clientes ---
@login_required
def cliente_create_update(request, pk=None):
    # ... (seu código está correto, mantido como está)
    empresa_do_usuario = request.user.profile.empresa
    if pk:
        instance = get_object_or_404(Cliente, pk=pk, empresa=empresa_do_usuario)
    else:
        instance = None
    form = ClienteForm(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        cliente = form.save(commit=False)
        cliente.empresa = empresa_do_usuario
        cliente.save()
        return render(request, 'core/partials/_success_triggers.html', {'toast_message': "Cliente salvo com sucesso!",'update_event': 'updateClienteList'})
    context = {'form': form}
    return render(request, 'core/partials/_cliente_form.html', context)

@login_required
def cliente_delete(request, pk):
    # ... (seu código está correto, mantido como está)
    empresa_do_usuario = request.user.profile.empresa
    cliente = get_object_or_404(Cliente, pk=pk, empresa=empresa_do_usuario)
    if request.method == 'POST':
        nome_cliente = cliente.nome_razao_social
        cliente.delete()
        return render(request, 'core/partials/_success_triggers.html', {'toast_message': f"Cliente '{nome_cliente}' excluído com sucesso.",'update_event': 'updateClienteList'})
    context = {'cliente': cliente}
    return render(request, 'core/partials/_cliente_delete_confirm.html', context)

# --- Manutenções ---
@login_required
def manutencao_create_update(request, poco_pk, pk=None):
    # ... (seu código está correto, mantido como está)
    empresa_do_usuario = request.user.profile.empresa
    poco = get_object_or_404(Poco, pk=poco_pk, cliente__empresa=empresa_do_usuario)
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
        return render(request, 'core/partials/_success_triggers.html', {'toast_message': "Registro de manutenção salvo com sucesso!", 'update_event': 'updateManutencaoList'})
    context = {'form': form, 'poco': poco}
    return render(request, 'core/partials/_manutencao_form.html', context)

@login_required
def manutencao_delete(request, poco_pk, pk):
    # ... (seu código está correto, mantido como está)
    empresa_do_usuario = request.user.profile.empresa
    poco = get_object_or_404(Poco, pk=poco_pk, cliente__empresa=empresa_do_usuario)
    manutencao = get_object_or_404(Manutencao, pk=pk, poco=poco)
    if request.method == 'POST':
        manutencao.delete()
        return render(request, 'core/partials/_success_triggers.html', {'toast_message': "Registro de manutenção excluído com sucesso.",'update_event': 'updateManutencaoList'})
    context = {'manutencao': manutencao}
    return render(request, 'core/partials/_manutencao_delete_confirm.html', context)

@login_required
def partial_check_manutencoes(request, poco_pk):
    # ... (seu código está correto, mantido como está)
    empresa_do_usuario = request.user.profile.empresa
    poco = get_object_or_404(Poco, pk=poco_pk, cliente__empresa=empresa_do_usuario)
    context = {'manutencoes': poco.historico_manutencoes.all(), 'poco': poco}
    return render(request, 'core/partials/lista_manutencoes_tabela.html', context)

# ===================================================================
# VIEW DE GERAÇÃO DE PDF
# ===================================================================
@login_required
def gerar_relatorio_pdf(request, pk):
    # Garante que o usuário só pode gerar PDF de um poço da sua empresa
    empresa_do_usuario = request.user.profile.empresa
    poco = get_object_or_404(Poco, pk=pk, cliente__empresa=empresa_do_usuario)
    
    # --- LÓGICA PARA A LOGO DA EMPRESA ---
    caminho_logo = None
    if empresa_do_usuario.logo:
        caminho_completo_logo = Path(settings.MEDIA_ROOT) / empresa_do_usuario.logo.name
        if caminho_completo_logo.exists():
            caminho_logo = caminho_completo_logo.as_uri()
    
    # --- LÓGICA PARA A GALERIA DE FOTOS ---
    # Cria uma lista de dicionários, cada um contendo a URL e a descrição da foto
    galeria_fotos = []
    for foto in poco.fotos.all():
        caminho_completo_foto = Path(settings.MEDIA_ROOT) / foto.imagem.name
        if caminho_completo_foto.exists():
            galeria_fotos.append({
                'url': caminho_completo_foto.as_uri(),
                'descricao': foto.descricao,
                'is_principal': foto.is_principal
            })

    context = {
        'empresa': empresa_do_usuario, # Passa o objeto empresa inteiro
        'caminho_logo': caminho_logo,
        'poco': poco,
        'galeria_fotos': galeria_fotos, # Passa a lista de fotos processadas
    }
    
    html_string = render_to_string('core/relatorio_poco_pdf.html', context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    pdf_file = html.write_pdf()
    
    response = HttpResponse(pdf_file, content_type='application/pdf')
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
