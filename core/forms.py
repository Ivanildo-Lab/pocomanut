# core/forms.py (NOVO ARQUIVO)

# core/forms.py

from django import forms
from .models import Poco, Cliente, Manutencao
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, HTML

class PocoForm(forms.ModelForm):
    class Meta:
        model = Poco
        fields = [
            'cliente', 'identificador_poco', 'data_perfuração_inicial', 'foto_principal',
            'endereco_completo', 'cidade', 'estado', 'profundidade_total',
            'diametro_poco', 'tubulacao_material', 'modelo_bomba_instalada',
            'modelo_gerador', 'painel_comando',
        ]
        widgets = {
            'data_perfuração_inicial': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # O helper controla o layout do formulário
        self.helper = FormHelper(self)
        self.helper.form_tag = False  # Não renderiza a tag <form> automaticamente
        self.helper.disable_csrf = True  # Desabilita CSRF para este formulário, se necessário
        self.helper.layout = Layout(
            Row(
                Column('cliente', css_class='form-group col-md-6 mb-0'),
                Column('identificador_poco', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('data_perfuração_inicial', css_class='form-group col-md-6 mb-0'),
                # Bloco para a imagem, agora controlado pelo Python
                Column(
                    HTML("""
                        <div class="mb-3 text-center">
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
                    'foto_principal', # O campo de input real virá depois
                    css_class='form-group col-md-6 mb-0'
                ),
                css_class='form-row'
            ),
            'endereco_completo',
            Row(
                Column('cidade', css_class='form-group col-md-6 mb-0'),
                Column('estado', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            HTML('<hr>'),
            HTML('<h6 class="mt-3">Dados Técnicos</h6>'),
            Row(
                Column('profundidade_total', 'diametro_poco', 'tubulacao_material', css_class='form-group col-md-6 mb-0'),
                Column('modelo_bomba_instalada', 'modelo_gerador', 'painel_comando', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            )
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
            'data_manutencao': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.disable_csrf = True



        