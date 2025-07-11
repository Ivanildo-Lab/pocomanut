# core/serializers.py

from rest_framework import serializers
from .models import Cliente, Poco, Manutencao
from django.contrib.auth.models import User

# Serializer para o modelo de Usuário (operador)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

# Serializer para o modelo de Cliente
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__' # Expõe todos os campos do modelo

# Serializer para o modelo de Manutenção
class ManutencaoSerializer(serializers.ModelSerializer):
    # Para mostrar o nome do operador, não apenas o ID
    operador_responsavel = UserSerializer(read_only=True) 

    class Meta:
        model = Manutencao
        fields = '__all__'

# Serializer principal para o modelo de Poço
class PocoSerializer(serializers.ModelSerializer):
    # Aninhando serializers: Mostra os dados completos, não apenas os IDs
    cliente = ClienteSerializer(read_only=True)
    historico_manutencoes = ManutencaoSerializer(many=True, read_only=True)

    class Meta:
        model = Poco
        fields = '__all__' # Expõe todos os campos do modelo