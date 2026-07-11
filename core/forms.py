
# core/forms.py

from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Poco, Cliente, Manutencao, FotoPoco, Bomba, FotoBomba, OrdemServico, ItemOS, Orcamento, FotoMovimentacao, Funcionario
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, HTML
from django.templatetags.static import static


# Classe PocoForm
class PocoForm(forms.ModelForm):
    class Meta:
        model = Poco
        fields = [
            'cliente', 'identificador_poco', 'data_perfuração_inicial', 
            'endereco_completo', 'cidade', 'estado', 'localizacao_mapa',
            'profundidade_total', 'diametro_poco', 'profundidade_bomba', 
            'profundidade_injetor', 'cabo_eletrico', 'cabo_nautico', 
            'tubulacao_material', 'modelo_bomba_instalada', 'modelo_gerador', 
            'painel_comando', 'fusivel_disjuntor', 'contator', 
            'rele_termico', 'capacitores', 'equipamento_assistencia'
        ]
        widgets = {
            'data_perfuração_inicial': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),
            'equipamento_assistencia': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)
        if empresa:
            self.fields['cliente'].queryset = Cliente.objects.filter(empresa=empresa)
        
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        
        # Layout simplificado sem a foto
        self.helper.layout = Layout(
            Row(
                Column('cliente', css_class='form-group col-md-6 mb-0'),
                Column('identificador_poco', css_class='form-group col-md-6 mb-0'),
            ),
            'data_perfuração_inicial',

            HTML('<hr>'),
            HTML('<h6 class="mt-3 mb-3 text-primary">Localização</h6>'),
            
            'endereco_completo',
            'localizacao_mapa',
            Row(
                Column('cidade', css_class='form-group col-md-6 mb-0'),
                Column('estado', css_class='form-group col-md-6 mb-0'),
            ),

            HTML('<hr>'),
            HTML('<h6 class="mt-3 mb-3 text-primary">Dados de Instalação e Estrutura</h6>'),
            Row(
                Column('profundidade_total', 'diametro_poco', 'profundidade_bomba', 'profundidade_injetor', css_class='form-group col-md-6 mb-0'),
                Column('tubulacao_material', 'cabo_eletrico', 'cabo_nautico', 'modelo_bomba_instalada', css_class='form-group col-md-6 mb-0'),
            ),

            HTML('<hr>'),
            HTML('<h6 class="mt-3 mb-3 text-primary">Equipamentos Elétricos</h6>'),
            Row(
                Column('modelo_gerador', 'painel_comando', css_class='form-group col-md-4 mb-0'),
                Column('fusivel_disjuntor', 'contator', css_class='form-group col-md-4 mb-0'),
                Column('rele_termico', 'capacitores', css_class='form-group col-md-4 mb-0'),
            ),

            HTML('<hr>'),
            HTML('<h6 class="mt-3 mb-3 text-primary">Observações de Equipamentos</h6>'),
            'equipamento_assistencia',
        )
# Fim da classe PocoForm

class FotoPocoForm(forms.ModelForm):
    class Meta:
        model = FotoPoco
        # Apenas os campos que o usuário preenche
        fields = ['imagem', 'descricao']
        widgets = {
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição (opcional)'}),
        }


# # Classe ClienteForm e ManutencaoForm         
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nome_razao_social',
            'cpf_cnpj',
            'telefone',
            'email',
            'endereco_principal',
            'cidade',
            'estado',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.disable_csrf = True

class ManutencaoForm(forms.ModelForm):
    class Meta:
        model = Manutencao
        # O campo 'poco' será definido na view, não no formulário
        fields = [
            'data_manutencao', 'tipo_servico', 'nivel_estatico_medido',
            'nivel_dinamico_medido', 'vazao_medida', 'amperagem_trabalho',
            'tensao_trabalho', 'observacoes',
        ]
        widgets = {
                'data_manutencao': forms.DateInput(
                    format='%Y-%m-%d',
                    attrs={'type': 'date'}
                ),

            'observacoes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.disable_csrf = True


# ============================================================
# FORMULÁRIOS - SISTEMA DE ORDEM DE SERVIÇO E BOMBAS
# ============================================================

class BombaForm(forms.ModelForm):
    class Meta:
        model = Bomba
        fields = ['descricao', 'modelo', 'marca', 'potencia', 'voltagem', 'numero_nota_fiscal', 
                  'is_reserva', 'cliente_proprietario', 'status', 'ativo']
    
    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)
        if empresa:
            self.fields['cliente_proprietario'].queryset = Cliente.objects.filter(empresa=empresa)
        
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        
        self.helper.layout = Layout(
            HTML('<h6 class="mt-2 mb-3 text-primary">Dados da Bomba</h6>'),
            'descricao',
            Row(
                Column('modelo', css_class='form-group col-md-6 mb-0'),
                Column('marca', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('potencia', css_class='form-group col-md-4 mb-0'),
                Column('voltagem', css_class='form-group col-md-4 mb-0'),
                Column('numero_nota_fiscal', css_class='form-group col-md-4 mb-0'),
            ),
            HTML('<hr>'),
            HTML('<h6 class="mt-2 mb-3 text-primary">Controle e Propriedade</h6>'),
            Row(
                Column('is_reserva', css_class='form-group col-md-4 mb-0'),
                Column('status', css_class='form-group col-md-4 mb-0'),
                Column('ativo', css_class='form-group col-md-4 mb-0'),
            ),
            'cliente_proprietario',
        )


class FotoBombaForm(forms.ModelForm):
    class Meta:
        model = FotoBomba
        fields = ['imagem', 'descricao']
        widgets = {
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição (opcional)'}),
        }


class OrdemServicoForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        fields = [
            'cliente', 'poco', 'bomba', 'prioridade', 
            'data_previsao_entrega', 'data_entrada', 'data_saida',
            'funcionario_responsavel', 'observacoes'
        ]
        widgets = {
            'data_previsao_entrega': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),
            'data_entrada': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={'type': 'datetime-local'}
            ),
            'data_saida': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={'type': 'datetime-local'}
            ),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)
        if empresa:
            self.fields['cliente'].queryset = Cliente.objects.filter(empresa=empresa)
            self.fields['poco'].queryset = Poco.objects.filter(cliente__empresa=empresa)
            self.fields['bomba'].queryset = Bomba.objects.filter(empresa=empresa)
            self.fields['funcionario_responsavel'].queryset = Funcionario.objects.filter(empresa=empresa, ativo=True)
        
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        
        self.helper.layout = Layout(
            HTML('<h6 class="mt-2 mb-3 text-primary">Dados da Ordem de Serviço</h6>'),
            Row(
                Column('cliente', css_class='form-group col-md-6 mb-0'),
                Column('poco', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('bomba', css_class='form-group col-md-6 mb-0'),
                Column('prioridade', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('data_previsao_entrega', css_class='form-group col-md-4 mb-0'),
                Column('funcionario_responsavel', css_class='form-group col-md-8 mb-0'),
            ),
            HTML('<hr>'),
            HTML('<h6 class="mt-2 mb-3 text-primary">Controle de Datas</h6>'),
            Row(
                Column('data_entrada', css_class='form-group col-md-6 mb-0'),
                Column('data_saida', css_class='form-group col-md-6 mb-0'),
            ),
            'observacoes',
        )


class ItemOSForm(forms.ModelForm):
    class Meta:
        model = ItemOS
        fields = ['descricao', 'quantidade', 'valor_unitario']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        
        self.helper.layout = Layout(
            Row(
                Column('descricao', css_class='form-group col-md-5 mb-0'),
                Column('quantidade', css_class='form-group col-md-2 mb-0'),
                Column('valor_unitario', css_class='form-group col-md-3 mb-0'),
                css_class='align-items-end'
            ),
        )


class OrcamentoForm(forms.ModelForm):
    class Meta:
        model = Orcamento
        fields = ['observacoes']
        widgets = {
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        
        self.helper.layout = Layout(
            'observacoes',
        )


class FotoMovimentacaoForm(forms.ModelForm):
    class Meta:
        model = FotoMovimentacao
        fields = ['imagem', 'descricao', 'tipo_foto']
        widgets = {
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição (opcional)'}),
            'tipo_foto': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.disable_csrf = True


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome_completo', 'cpf', 'cargo', 'telefone', 'email', 'ativo']
        widgets = {
            'cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        
        self.helper.layout = Layout(
            HTML('<h6 class="mt-2 mb-3 text-primary">Dados do Funcionário</h6>'),
            'nome_completo',
            Row(
                Column('cpf', css_class='form-group col-md-6 mb-0'),
                Column('cargo', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('telefone', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
            ),
            'ativo',
        )