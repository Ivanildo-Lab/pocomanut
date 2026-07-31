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


# ============================================================
# MODELOS - SISTEMA DE ORDEM DE SERVIÇO E BOMBAS
# ============================================================

class Bomba(models.Model):
    """Cadastro de bombas/equipamentos disponíveis para manutenção"""
    
    VOLTAGEM_CHOICES = [
        ('110', '110V'),
        ('220', '220V'),
        ('380', '380V'),
    ]
    
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('em_uso', 'Em Uso'),
        ('manutencao', 'Em Manutenção'),
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='bombas')
    descricao = models.CharField(max_length=200, verbose_name="Descrição")
    modelo = models.CharField(max_length=100, verbose_name="Modelo")
    marca = models.CharField(max_length=100, verbose_name="Marca")
    potencia = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Potência (HP)")
    voltagem = models.CharField(max_length=50, verbose_name="Voltagem")
    numero_nota_fiscal = models.CharField(max_length=50, blank=True, verbose_name="Nº Nota Fiscal")
    is_reserva = models.BooleanField(default=False, verbose_name="Bomba de Reserva")
    cliente_proprietario = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, related_name='bombas_proprietarias', verbose_name="Cliente Proprietário")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='disponivel', verbose_name="Status")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Bomba"
        verbose_name_plural = "Bombas"
        ordering = ['descricao']
    
    def __str__(self):
        return f"{self.descricao} - {self.marca} {self.modelo}"
    
    def get_foto_principal(self):
        foto = self.fotos.filter(is_principal=True).first()
        if not foto:
            foto = self.fotos.first()
        return foto


class FotoBomba(models.Model):
    """Fotos das bombas cadastradas"""
    
    bomba = models.ForeignKey(Bomba, on_delete=models.CASCADE, related_name='fotos')
    imagem = models.ImageField(upload_to='fotos_bombas/')
    descricao = models.CharField(max_length=200, blank=True, verbose_name="Descrição (Opcional)")
    is_principal = models.BooleanField(default=False, verbose_name="Marcar como Foto Principal")
    data_upload = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_principal', '-data_upload']
        verbose_name = "Foto da Bomba"
        verbose_name_plural = "Fotos das Bombas"
    
    def __str__(self):
        return f"Foto de {self.bomba.descricao}"


class Funcionario(models.Model):
    """Cadastro de funcionários da empresa"""
    
    CARGO_CHOICES = [
        ('tecnico', 'Técnico'),
        ('mecanico', 'Mecânico'),
        ('eletricista', 'Eletricista'),
        ('motorista', 'Motorista'),
        ('auxiliar', 'Auxiliar'),
        ('supervisor', 'Supervisor'),
        ('administrativo', 'Administrativo'),
        ('outro', 'Outro'),
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='funcionarios')
    nome_completo = models.CharField(max_length=200, verbose_name="Nome Completo")
    cpf = models.CharField(max_length=14, blank=True, verbose_name="CPF")
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES, default='tecnico', verbose_name="Cargo")
    telefone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
        ordering = ['nome_completo']
    
    def __str__(self):
        return f"{self.nome_completo} ({self.get_cargo_display()})"


class OrdemServico(models.Model):
    """Ordem de Serviço para manutenção de bombas"""
    
    STATUS_CHOICES = [
        ('aberta', 'Aberta'),
        ('em_andamento', 'Em Andamento'),
        ('aguardando_peca', 'Aguardando Peça'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]
    
    PRIORIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('normal', 'Normal'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='ordens_servico')
    numero_os = models.CharField(max_length=20, verbose_name="Nº OS")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberta', verbose_name="Status")
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, default='normal', verbose_name="Prioridade")
    
    data_abertura = models.DateTimeField(auto_now_add=True, verbose_name="Data de Abertura")
    data_previsao_entrega = models.DateField(null=True, blank=True, verbose_name="Previsão de Entrega")
    data_entrada = models.DateTimeField(null=True, blank=True, verbose_name="Data/Hora de Entrada")
    data_saida = models.DateTimeField(null=True, blank=True, verbose_name="Data/Hora de Saída")
    data_conclusao = models.DateTimeField(null=True, blank=True, verbose_name="Data de Conclusão")
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='ordens_servico')
    poco = models.ForeignKey(Poco, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordens_servico')
    bomba = models.ForeignKey(Bomba, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordens_servico')
    
    funcionario_responsavel = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True, related_name='os_responsavel', verbose_name="Funcionário Responsável")
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='os_criadas')
    
    observacoes = models.TextField(blank=True, verbose_name="Observações")
    
    class Meta:
        verbose_name = "Ordem de Serviço"
        verbose_name_plural = "Ordens de Serviço"
        ordering = ['-data_abertura']
        unique_together = [['empresa', 'numero_os']]
    
    def __str__(self):
        return f"{self.numero_os} - {self.cliente.nome_razao_social}"
    
    def save(self, *args, **kwargs):
        if not self.numero_os:
            from django.db import transaction
            from django.utils import timezone

            with transaction.atomic():
                ano = timezone.now().year
                ultimo = OrdemServico.objects.select_for_update().filter(
                    empresa=self.empresa,
                    numero_os__startswith=f'OS-{ano}'
                ).count()
                self.numero_os = f'OS-{ano}-{ultimo + 1:04d}'
        super().save(*args, **kwargs)


class ItemOS(models.Model):
    """Itens/peças utilizados na Ordem de Serviço"""
    
    os = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='itens')
    descricao = models.CharField(max_length=200, verbose_name="Descrição do Item")
    quantidade = models.PositiveIntegerField(default=1, verbose_name="Quantidade")
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Unitário (R$)")
    
    class Meta:
        verbose_name = "Item da OS"
        verbose_name_plural = "Itens da OS"
        ordering = ['id']
    
    def __str__(self):
        return f"{self.descricao} x{self.quantidade}"
    
    @property
    def valor_total(self):
        return self.quantidade * self.valor_unitario


class Orcamento(models.Model):
    """Orçamento associado à Ordem de Serviço"""
    
    os = models.OneToOneField(OrdemServico, on_delete=models.CASCADE, related_name='orcamento')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Valor Total (R$)")
    observacoes = models.TextField(blank=True, verbose_name="Observações do Orçamento")
    aprovado = models.BooleanField(default=False, verbose_name="Aprovado")
    data_aprovacao = models.DateTimeField(null=True, blank=True, verbose_name="Data de Aprovação")
    enviado_cliente = models.BooleanField(default=False, verbose_name="Enviado ao Cliente")
    
    class Meta:
        verbose_name = "Orçamento"
        verbose_name_plural = "Orçamentos"
    
    def __str__(self):
        status = "Aprovado" if self.aprovado else "Pendente"
        return f"Orçamento {self.os.numero_os} - {status}"


class FotoMovimentacao(models.Model):
    """Fotos da bomba registradas durante a Ordem de Serviço (entrada/saída)"""
    
    TIPO_FOTO_CHOICES = [
        ('entrada', 'Foto de Entrada'),
        ('saida', 'Foto de Saída'),
        ('servico', 'Foto do Serviço'),
    ]
    
    os = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='fotos_movimentacao')
    imagem = models.ImageField(upload_to='fotos_movimentacao/')
    descricao = models.CharField(max_length=200, blank=True, verbose_name="Descrição")
    tipo_foto = models.CharField(max_length=10, choices=TIPO_FOTO_CHOICES, default='servico', verbose_name="Tipo da Foto")
    data_upload = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Foto de Movimentação"
        verbose_name_plural = "Fotos de Movimentação"
        ordering = ['tipo_foto', '-data_upload']
    
    def __str__(self):
        return f"{self.get_tipo_foto_display()} - {self.os.numero_os}"