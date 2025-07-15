-- Habilita o suporte a caracteres especiais como acentos
SET NAMES utf8mb4;

-- =================================================================
--  INSERINDO CLIENTES
-- =================================================================
-- IDs foram definidos manualmente para facilitar a criação dos poços.
INSERT INTO `core_cliente` (`id`, `nome_razao_social`, `cpf_cnpj`, `telefone`, `email`, `endereco_principal`, `cidade`, `estado`) VALUES
(1, 'Fazenda Boa Esperança - Sr. José Carlos', '123.456.789-00', '(99) 98123-4567', 'jose.carlos@email.com', 'Rodovia BR-010, Km 15', 'Imperatriz', 'MA'),
(2, 'Agropecuária Veredas Ltda', '11.222.333/0001-44', '(99) 3538-2030', 'contato@agroveredas.com', 'Av. Industrial, 1020', 'Açailândia', 'MA'),
(3, 'Sítio Recanto Feliz - Dona Maria', '987.654.321-99', '(99) 98876-5432', 'maria.sitio@email.com', 'Estrada Vicinal do Arroz, Km 5', 'Cidelândia', 'MA'),
(4, 'Granja Água Branca S/A', '55.666.777/0001-88', '(99) 3535-1516', 'compras@granjaaguabranca.com', 'Parque Industrial', 'Estreito', 'MA');

-- =================================================================
--  INSERINDO POÇOS
-- =================================================================
-- Cada poço é associado a um cliente_id existente.
-- As imagens são apenas textos, elas não existirão no seu sistema de arquivos.
INSERT INTO `core_poco` (`id`, `cliente_id`, `identificador_poco`, `data_perfuração_inicial`, `endereco_completo`, `cidade`, `estado`, `foto_principal`, `profundidade_total`, `diametro_poco`, `tubulacao_material`, `modelo_bomba_instalada`, `modelo_gerador`, `painel_comando`) VALUES
(1, 1, 'Poço da Sede', '2021-05-10', 'Sede da Fazenda Boa Esperança', 'Imperatriz', 'MA', 'fotos_pocos/sede_fake.jpg', 120.50, 6.00, 'PVC Reforçado', 'Submersa KSB 5.5cv', 'Toyama 15kVA', 'Automático 5.5cv'),
(2, 1, 'Poço do Pivô 01', '2022-08-20', 'Área de Irrigação Norte', 'Imperatriz', 'MA', '', 155.00, 8.00, 'Aço Galvanizado', 'Submersa Franklin 10cv', 'MWM 25kVA', 'Partida Direta 10cv'),
(3, 2, 'Poço Principal (Escritório)', '2020-02-15', 'Pátio Central da Agropecuária', 'Açailândia', 'MA', 'fotos_pocos/agro_fake.jpg', 95.00, 6.00, 'PVC', 'Submersa Leão 3cv', '', 'Automático 3cv'),
(4, 3, 'Poço do Sítio', '2023-11-01', 'Próximo à casa principal', 'Cidelândia', 'MA', 'fotos_pocos/sitio_fake.jpg', 60.00, 4.00, 'PVC', 'Injetora Schneider 1.5cv', '', 'Manual'),
(5, 4, 'Poço Aviário 03', '2022-01-30', 'Setor de Engorda 3', 'Estreito', 'MA', '', 180.00, 8.00, 'Aço Galvanizado', 'Submersa Grundfos 15cv', 'Perkins 40kVA', 'Estrela-Triângulo 15cv');

-- =================================================================
--  INSERINDO HISTÓRICO DE MANUTENÇÕES
-- =================================================================
-- Cada manutenção é associada a um poco_id e a um operador_responsavel_id.
-- IMPORTANTE: O valor '1' em operador_responsavel_id se refere ao usuário com ID=1 na sua tabela 'auth_user'.
INSERT INTO `core_manutencao` (`poco_id`, `data_manutencao`, `tipo_servico`, `nivel_estatico_medido`, `nivel_dinamico_medido`, `vazao_medida`, `amperagem_trabalho`, `tensao_trabalho`, `operador_responsavel_id`, `observacoes`) VALUES
(1, '2023-04-12', 'Manutenção Preventiva', 25.50, 45.80, 8.50, 15.20, 220, 1, 'Limpeza dos filtros e verificação do painel. Tudo OK.'),
(1, '2024-05-20', 'Verificação de Vazão', 26.10, 48.20, 8.10, 15.50, 218, 1, 'Vazão apresentou leve queda. Agendado limpeza química para o próximo semestre.'),
(2, '2024-01-15', 'Troca de Painel de Comando', 30.00, 65.00, 15.20, 25.00, 380, 1, 'Painel antigo apresentava falha no contator. Instalado novo painel com relé de falta de fase.'),
(3, '2023-09-05', 'Limpeza Química', 15.80, 25.10, 12.50, 8.00, 220, 1, 'Realizada limpeza com produtos para remoção de incrustações. Vazão recuperada em 20%.'),
(5, '2024-06-28', 'Troca de Bomba', 40.00, 85.00, 25.00, 35.10, 380, 1, 'Bomba anterior queimou devido a sobrecarga. Substituída por modelo novo e reajustado relé térmico.');