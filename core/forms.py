
# core/forms.py

from django import forms
from .models import Poco, Cliente, Manutencao,FotoPoco
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



        