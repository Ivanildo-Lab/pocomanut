from django.db import models

# Create your models here.
# Em models.py - Versão Final para Desenvolvimento Inicial

from django.db import models
from django.contrib.auth.models import User

# Modelo 00: UserProfile
# Este modelo estende o User do Django para incluir informações adicionais sobre o usuário, como a empresa associada.
# Ele cria uma relação de um-para-um com o modelo User e uma relação de muitos-para-um com o modelo Empresa.
# Modelo 0: Empresa

class Empresa(models.Model):
    nome_fantasia = models.CharField(max_length=200, unique=True)
    razao_social = models.CharField(max_length=200, blank=True)
    cidade = models.CharField(max_length=200, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    email = models.EmailField(blank=True,default='')
    cnpj = models.CharField(max_length=18, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    logo = models.ImageField(upload_to='logos_empresas/', null=True, blank=True)

    def __str__(self):
        return self.nome_fantasia
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.empresa.nome_fantasia}"


# Modelo 1: Cliente
class Cliente(models.Model):
    nome_razao_social = models.CharField(max_length=200, verbose_name="Nome / Razão Social")
    cpf_cnpj = models.CharField(max_length=18, unique=True, verbose_name="CPF/CNPJ")
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    endereco_principal = models.CharField(max_length=255, blank=True, verbose_name="Endereço Principal")
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.nome_razao_social

# Modelo 2: Poço
class Poco(models.Model):
    # --- DADOS DE IDENTIFICAÇÃO E LOCALIZAÇÃO ---
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pocos')
    identificador_poco = models.CharField(max_length=100, help_text="Ex: 'Poço Sede da Fazenda', 'Poço Filial 1'", verbose_name="Identificador do Poço")
    data_perfuração_inicial = models.DateField(verbose_name="Data da Perfuração")
    endereco_completo = models.CharField(max_length=255, verbose_name="Endereço do Poço")
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    # --- CAMPO DE FOTO PRINCIPAL DO POÇO ---
    #foto_principal = models.ImageField(upload_to='fotos_pocos/', null=True, blank=True, verbose_name="Foto do Poço")
    localizacao_mapa = models.CharField(max_length=255, null=True,blank=True,verbose_name="Localização Geografica")

    # --- CARACTERÍSTICAS CONSTRUTIVAS (Estado Atual do Equipamento) ---
    profundidade_total = models.DecimalField(max_digits=7, decimal_places=2, help_text="Em metros")
    diametro_poco = models.DecimalField(max_digits=5, decimal_places=2, help_text="Em polegadas")
    tubulacao_material = models.CharField(max_length=50, blank=True, help_text="Ex: PVC, Aço Galvanizado", verbose_name="Material da Tubulação")
    modelo_bomba_instalada = models.CharField(max_length=100, blank=True, verbose_name="Modelo da Bomba")
    modelo_gerador = models.CharField(max_length=100, blank=True, verbose_name="Modelo do Gerador")
    painel_comando = models.CharField(max_length=100, blank=True, verbose_name="Painel de Comando")
    profundidade_bomba = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name="Profundidade da Bomba (metros)")
    profundidade_injetor = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name="Profundidade do Injetor (metros)")
    cabo_eletrico = models.CharField(max_length=100, blank=True, verbose_name="Cabo Elétrico")
    cabo_nautico = models.CharField(max_length=100, blank=True, verbose_name="Cabo Náutico (Segurança)")
    fusivel_disjuntor = models.CharField(max_length=100, blank=True, verbose_name="Fusível / Disjuntor")
    contator = models.CharField(max_length=100, blank=True, verbose_name="Contator")
    rele_termico = models.CharField(max_length=100, blank=True, verbose_name="Relé Térmico")
    capacitores = models.CharField(max_length=100, blank=True, verbose_name="Capacitores")
    equipamento_assistencia = models.TextField(blank=True, verbose_name="Equipamento de Assistência Utilizado")
    
    # --- RELACIONAMENTO COM FOTOS ---
    def get_foto_principal(self):
        # Tenta encontrar uma foto marcada como principal,
        # ou pega a primeira foto se nenhuma for marcada.
        foto = self.fotos.filter(is_principal=True).first()
        if not foto:
            foto = self.fotos.first()
        return foto
    
    class Meta:
        verbose_name = "Poço"
        verbose_name_plural = "Poços"

    def __str__(self):
        return f"{self.identificador_poco} ({self.cliente.nome_razao_social})"

class FotoPoco(models.Model):
    poco = models.ForeignKey(Poco, on_delete=models.CASCADE, related_name='fotos')
    imagem = models.ImageField(upload_to='fotos_pocos/')
    descricao = models.CharField(max_length=200, blank=True, verbose_name="Descrição (Opcional)")
    is_principal = models.BooleanField(default=False, verbose_name="Marcar como Foto Principal")
    data_upload = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_principal', '-data_upload'] # Principais e mais recentes primeiro

    def __str__(self):
        return f"Foto de {self.poco.identificador_poco}"
    
# Modelo 3: Manutenção
class Manutencao(models.Model):
    # --- RELACIONAMENTO E DADOS GERAIS ---
    poco = models.ForeignKey(Poco, on_delete=models.CASCADE, related_name='historico_manutencoes', verbose_name="Poço")
    data_manutencao = models.DateField(verbose_name="Data da Manutenção")
    tipo_servico = models.CharField(max_length=100, help_text="Ex: Manutenção Preventiva, Troca de Bomba, Limpeza")

    # --- DADOS MEDIDOS NA VISITA ---
    nivel_estatico_medido = models.DecimalField(max_digits=7, decimal_places=2, help_text="Em metros", verbose_name="Nível Estático")
    nivel_dinamico_medido = models.DecimalField(max_digits=7, decimal_places=2, help_text="Em metros", verbose_name="Nível Dinâmico")
    vazao_medida = models.DecimalField(max_digits=7, decimal_places=2, help_text="Em m³/h", verbose_name="Vazão")
    amperagem_trabalho = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Amperagem")
    tensao_trabalho = models.IntegerField(null=True, blank=True, verbose_name="Tensão (Volts)")

    # --- OPERACIONAL ---
    operador_responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Operador Responsável")
    observacoes = models.TextField(blank=True, verbose_name="Observações do Serviço")

    class Meta:
        verbose_name = "Registro de Manutenção"
        verbose_name_plural = "Registros de Manutenção"
        ordering = ['-data_manutencao']

    def __str__(self):
        return f"{self.tipo_servico} em {self.data_manutencao} - {self.poco.identificador_poco}"