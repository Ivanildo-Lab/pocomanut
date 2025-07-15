# core/forms.py (NOVO ARQUIVO)

# core/forms.py

from django import forms
from .models import Poco, Cliente, Manutencao
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, HTML

class PocoForm(forms.ModelForm):
    class Meta:
        model = Poco
        # Lista completa e ordenada de todos os campos do formulário
        fields = [
            'cliente', 'identificador_poco', 'data_perfuração_inicial', 
            'endereco_completo', 'cidade', 'estado', 'foto_principal',
            'profundidade_total', 'diametro_poco', 'profundidade_bomba', 
            'profundidade_injetor', 'cabo_eletrico', 'cabo_nautico', 
            'tubulacao_material', 'modelo_bomba_instalada', 'modelo_gerador', 
            'painel_comando', 'fusivel_disjuntor', 'contator', 
            'rele_termico', 'capacitores', 'equipamento_assistencia'
        ]
        # Widgets para melhorar a experiência de campos específicos
        widgets = {
            'data_perfuração_inicial': forms.DateInput(attrs={'type': 'date'}),
            'equipamento_assistencia': forms.Textarea(attrs={'rows': 4}),
            'observacoes': forms.Textarea(attrs={'rows': 4}), # Caso você tenha um campo 'observacoes' no Poço
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # --- Configuração do Crispy Forms Helper ---
        self.helper = FormHelper(self)
        self.helper.form_tag = False  # Essencial para funcionar com HTMX
        self.helper.disable_csrf = True # O token já está no template do modal
        
        # --- Layout Estruturado do Formulário ---
        self.helper.layout = Layout(
            
            # Seção 1: Identificação do Poço e Cliente
            Row(
                Column('cliente', css_class='form-group col-md-6 mb-0'),
                Column('identificador_poco', css_class='form-group col-md-6 mb-0'),
            ),
            'data_perfuração_inicial',

            HTML('<hr>'),
            HTML('<h6 class="mt-3 mb-3 text-primary">Localização e Foto</h6>'),
            
            # Seção 2: Localização e Foto em Colunas
            Row(
                # Coluna da Esquerda: Endereço
                Column(
                    'endereco_completo',
                    Row(
                        Column('cidade', css_class='form-group col-md-6 mb-0'),
                        Column('estado', css_class='form-group col-md-6 mb-0'),
                    ),
                    css_class='col-md-7'
                ),
                # Coluna da Direita: Preview da Imagem e Upload
                Column(
                    HTML("""
                        <div class="text-center">
                            <label class="form-label">Foto Principal</label>
                            <div class="mb-2">
                                <img id="image-preview" 
                                     src="{% if form.instance.foto_principal %}{{ form.instance.foto_principal.url }}{% else %}https://via.placeholder.com/300x200.png?text=Sem+Foto{% endif %}"
                                     alt="Preview da foto do poço" 
                                     class="img-fluid rounded border" 
                                     style="max-height: 150px; object-fit: cover;">
                            </div>
                        </div>
                    """),
                    'foto_principal',
                    css_class='col-md-5'
                ),
            ),

            HTML('<hr>'),
            HTML('<h6 class="mt-3 mb-3 text-primary">Dados de Instalação e Estrutura</h6>'),

            # Seção 3: Dados Técnicos
            Row(
                Column('profundidade_total', 'diametro_poco', 'profundidade_bomba', 'profundidade_injetor', css_class='form-group col-md-6 mb-0'),
                Column('tubulacao_material', 'cabo_eletrico', 'cabo_nautico', 'modelo_bomba_instalada', css_class='form-group col-md-6 mb-0'),
            ),

            HTML('<hr>'),
            HTML('<h6 class="mt-3 mb-3 text-primary">Equipamentos Elétricos</h6>'),

            # Seção 4: Equipamentos Elétricos
            Row(
                Column('modelo_gerador', 'painel_comando', css_class='form-group col-md-4 mb-0'),
                Column('fusivel_disjuntor', 'contator', css_class='form-group col-md-4 mb-0'),
                Column('rele_termico', 'capacitores', css_class='form-group col-md-4 mb-0'),
            ),

            HTML('<hr>'),
            HTML('<h6 class="mt-3 mb-3 text-primary">Observações de Equipamentos</h6>'),

            # Seção 5: Campo de Texto Longo
            'equipamento_assistencia',
        )
        
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



        