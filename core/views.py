# core/views.py
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions
from .models import Cliente, Poco, Manutencao
from .serializers import ClienteSerializer, PocoSerializer, ManutencaoSerializer
from django.views.generic import ListView, DetailView
from .models import Poco
from django.db.models import Q # Importe o objeto Q para buscas complexas
from .forms import PocoForm , ClienteForm, ManutencaoForm
from django.http import HttpResponse 
from django_htmx.http import trigger_client_event 
from django.template.loader import render_to_string
from weasyprint import HTML

# ViewSet para Clientes
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated] # Apenas usuários logados podem acessar

# ViewSet para Poços
class PocoViewSet(viewsets.ModelViewSet):
    queryset = Poco.objects.all().order_by('-data_perfuração_inicial') # Mais recentes primeiro
    serializer_class = PocoSerializer
    permission_classes = [permissions.IsAuthenticated]

# ViewSet para Manutenções
class ManutencaoViewSet(viewsets.ModelViewSet):
    queryset = Manutencao.objects.all()
    serializer_class = ManutencaoSerializer
    permission_classes = [permissions.IsAuthenticated] # Apenas usuários logados podem acessar


# core/views.py (versão final da view)

class PocoListView(ListView):
    model = Poco
    # O template principal, para o primeiro carregamento da página
    template_name = 'core/lista_pocos.html'
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('cliente') # Otimização de consulta
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(identificador_poco__icontains=query) |
                Q(cliente__nome_razao_social__icontains=query)
            )
        return queryset

    def get_template_names(self):
        # Verifica se a requisição veio do HTMX (ele adiciona um header específico)
        if self.request.htmx:
            # Se for HTMX, retorna apenas o fragmento
            return ['core/partials/lista_pocos_tabela.html']
        # Caso contrário, retorna a página completa
        return [self.template_name]
    
def poco_create_update(request, pk=None):
    if pk:
        # Se um 'pk' (primary key) é fornecido, estamos editando.
        poco = get_object_or_404(Poco, pk=pk)
        instance = poco
    else:
        # Caso contrário, estamos criando um novo.
        instance = None

    form = PocoForm(request.POST or None, request.FILES or None, instance=instance)

    if request.method == 'POST' and form.is_valid():
        form.save()
        # CRIA UMA RESPOSTA VAZIA
        response = HttpResponse(status=204)
        # ADICIONA CABEÇALHOS HTMX A ELA
        trigger_client_event(
            response,
            "closeModal", # Nome do evento que vamos ouvir no JS
            { "message": "Poço salvo com sucesso!" }, # Dados opcionais
        )
        trigger_client_event(
            response,
            "updatePocoList", # Outro evento para atualizar a lista
            {},
        )
        return response

    context = {
        'form': form,
        # Passamos a instância para o template saber se estamos criando ou editando
        'instance': instance 
    }
    return render(request, 'core/partials/_poco_form.html', context)
def gerar_relatorio_pdf(request, pk):
    poco = get_object_or_404(Poco, pk=pk)
    
    # Renderiza o template HTML para uma string
    html_string = render_to_string('core/relatorio_poco_pdf.html', {'poco': poco})
    
    # Cria um objeto HTML com a string renderizada
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    
    # Gera o PDF em memória
    pdf = html.write_pdf()
    
    # Cria uma resposta HTTP com o conteúdo do PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    
    # Define o cabeçalho para forçar o download com um nome de arquivo amigável
    response['Content-Disposition'] = f'inline; filename="relatorio_poco_{poco.id}.pdf"'
    
    return response
def poco_delete(request, pk):
    poco = get_object_or_404(Poco, pk=pk)
    if request.method == 'POST':
        # Passo 1: Guardar o nome ANTES de deletar
        nome_poco = poco.identificador_poco
        poco.delete()
        
        response = HttpResponse(status=204)
        
        # Passo 2: Adicionar TODOS os gatilhos necessários
        trigger_client_event(response, "updatePocoList", {})
        trigger_client_event(response, "closeModal", {}) # <-- GATILHO FALTANTE
        trigger_client_event(
            response, 
            "showToast", 
            { "message": f"Poço '{nome_poco}' excluído com sucesso." } # <-- GATILHO FALTANTE
        )
        return response
        
    return render(request, 'core/partials/_poco_delete_confirm.html', {'poco': poco})
# A view acima renderiza um template de confirmação de exclusão
# que pode ser usado com HTMX para mostrar um modal de confirmação.

class ClienteListView(ListView):
    model = Cliente
    template_name = 'core/lista_clientes.html'
    context_object_name = 'clientes' # Um nome mais claro para a variável no template

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

def cliente_create_update(request, pk=None):
    if pk:
        instance = get_object_or_404(Cliente, pk=pk)
    else:
        instance = None
    
    form = ClienteForm(request.POST or None, instance=instance)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        response = HttpResponse(status=204)
        trigger_client_event(response, "closeModal", {})
        trigger_client_event(response, "updateClienteList", {})
        # ---EVENTO PARA A NOTIFICAÇÃO ---
        trigger_client_event(
            response, 
            "showToast", 
            { "message": f"Cliente '{nome_cliente}' excluído com sucesso." }
        )
        return response
        
    context = {'form': form}
    return render(request, 'core/partials/_cliente_form.html', context)

def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        # Passo 1: Guardar o nome ANTES de deletar
        nome_cliente = cliente.nome_razao_social
        cliente.delete()
        
        response = HttpResponse(status=204)
        
        # Passo 2: Adicionar TODOS os gatilhos necessários
        trigger_client_event(response, "updateClienteList", {})
        trigger_client_event(response, "closeModal", {}) # <-- GATILHO FALTANTE
        trigger_client_event(
            response, 
            "showToast", 
            { "message": f"Cliente '{nome_cliente}' excluído com sucesso." } # <-- GATILHO FALTANTE
        )
        return response
    
    context = {'cliente': cliente}
    return render(request, 'core/partials/_cliente_delete_confirm.html', context)   

class PocoDetailView(DetailView):
    model = Poco
    template_name = 'core/detalhes_poco.html'
    # O Django passa o objeto para o template com o nome 'poco' ou 'object'
    context_object_name = 'poco'

def manutencao_create_update(request, poco_pk, pk=None):
    poco = get_object_or_404(Poco, pk=poco_pk)
    if pk:
        instance = get_object_or_404(Manutencao, pk=pk)
    else:
        instance = None
    
    form = ManutencaoForm(request.POST or None, instance=instance)
    
    if request.method == 'POST' and form.is_valid():
        manutencao = form.save(commit=False) # Não salva no banco ainda
        manutencao.poco = poco # Associa a manutenção ao poço correto
        manutencao.operador_responsavel = request.user # Associa ao usuário logado
        manutencao.save() # Agora salva no banco de dados

        response = HttpResponse(status=204)
        trigger_client_event(response, "closeModal", {})
        trigger_client_event(response, "updateManutencaoList", {})
        trigger_client_event(
            response, "showToast", 
            { "message": "Registro de manutenção salvo com sucesso." }
        )
        return response
        
    context = {'form': form, 'poco': poco}
    return render(request, 'core/partials/_manutencao_form.html', context)

def manutencao_delete(request, poco_pk, pk):
    manutencao = get_object_or_404(Manutencao, pk=pk)
    if request.method == 'POST':
        manutencao.delete()
        response = HttpResponse(status=204)
        trigger_client_event(response, "closeModal", {})
        trigger_client_event(response, "updateManutencaoList", {})
        trigger_client_event(
            response, "showToast", 
            { "message": "Registro de manutenção excluído com sucesso." }
        )
        return response
    
    context = {'manutencao': manutencao}
    return render(request, 'core/partials/_manutencao_delete_confirm.html', context)

