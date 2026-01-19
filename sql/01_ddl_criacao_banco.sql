-- Limpeza inicial
DROP TABLE IF EXISTS pagamento, treino, cliente, plano, equipamento, atendente, faxineiro, mecanico, personal, funcionario, proprietario, log_auditoria CASCADE;

-- Tabelas
CREATE TABLE proprietario (
    cpf VARCHAR(14) PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    saldo DECIMAL(10, 2) NOT NULL DEFAULT 0.00
);

CREATE TABLE funcionario (
    id_funcionario SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    salario DECIMAL(10, 2) NOT NULL,
    data_admissao DATE NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    cpf_proprietario VARCHAR(14) NOT NULL
);

CREATE TABLE personal (
    id_funcionario INTEGER PRIMARY KEY,
    cref VARCHAR(20) NOT NULL
);

CREATE TABLE mecanico (
    id_funcionario INTEGER PRIMARY KEY,
    status_conserto VARCHAR(255)
);

CREATE TABLE faxineiro (
    id_funcionario INTEGER PRIMARY KEY,
    status_limpeza VARCHAR(255)
);

CREATE TABLE atendente (
    id_funcionario INTEGER PRIMARY KEY,
    turno VARCHAR(50) NOT NULL
);

CREATE TABLE equipamento (
    id_equipamento SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    estado_conservacao VARCHAR(255) NOT NULL,
    cpf_proprietario VARCHAR(14) NOT NULL,
    id_funcionario_mecanico INTEGER,
    id_funcionario_faxineiro INTEGER
);

CREATE TABLE plano (
    id_plano SERIAL PRIMARY KEY,
    tipo VARCHAR(150) NOT NULL,
    valor DECIMAL(10, 2) NOT NULL,
    id_funcionario_atendente INTEGER NOT NULL
);

CREATE TABLE cliente (
    id_cliente SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    id_plano_atual INTEGER
);

CREATE TABLE treino (
    id_treino SERIAL PRIMARY KEY,
    descricao VARCHAR(255) NOT NULL,
    id_cliente INTEGER NOT NULL,
    id_personal INTEGER NOT NULL
);

CREATE TABLE pagamento (
    id_pagamento SERIAL PRIMARY KEY,
    valor DECIMAL(10, 2) NOT NULL,
    forma_pagamento VARCHAR(50) NOT NULL,
    data_pagamento DATE NOT NULL,
    data_vencimento DATE NOT NULL,
    id_cliente INTEGER NOT NULL
);

-- Relacionamentos (FKs)
ALTER TABLE funcionario ADD FOREIGN KEY (cpf_proprietario) REFERENCES proprietario(cpf);

-- Herança
ALTER TABLE personal ADD FOREIGN KEY (id_funcionario) REFERENCES funcionario(id_funcionario) ON DELETE CASCADE;
ALTER TABLE mecanico ADD FOREIGN KEY (id_funcionario) REFERENCES funcionario(id_funcionario) ON DELETE CASCADE;
ALTER TABLE faxineiro ADD FOREIGN KEY (id_funcionario) REFERENCES funcionario(id_funcionario) ON DELETE CASCADE;
ALTER TABLE atendente ADD FOREIGN KEY (id_funcionario) REFERENCES funcionario(id_funcionario) ON DELETE CASCADE;

-- Operacional
ALTER TABLE equipamento ADD FOREIGN KEY (cpf_proprietario) REFERENCES proprietario(cpf);
ALTER TABLE equipamento ADD FOREIGN KEY (id_funcionario_mecanico) REFERENCES mecanico(id_funcionario);
ALTER TABLE equipamento ADD FOREIGN KEY (id_funcionario_faxineiro) REFERENCES faxineiro(id_funcionario);

ALTER TABLE plano ADD FOREIGN KEY (id_funcionario_atendente) REFERENCES atendente(id_funcionario);
ALTER TABLE cliente ADD FOREIGN KEY (id_plano_atual) REFERENCES plano(id_plano);
ALTER TABLE treino ADD FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE;
ALTER TABLE treino ADD FOREIGN KEY (id_personal) REFERENCES personal(id_funcionario);
ALTER TABLE pagamento ADD FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente);

-- Dados Iniciais (Seed)
INSERT INTO proprietario (cpf, nome, saldo) VALUES ('092.533.444-05', 'Raquel Santos', 2500.00);

-- Funcionários
INSERT INTO funcionario (nome, salario, data_admissao, tipo, cpf_proprietario) VALUES
('Carlos Silva', 3500.00, '2022-01-10', 'PERSONAL', '092.533.444-05'),
('Ana Souza', 2500.00, '2023-03-15', 'FAXINEIRO', '092.533.444-05'),
('Marcos Lima', 3000.00, '2021-08-20', 'MECANICO', '092.533.444-05'),
('Julia Atendente', 2000.00, '2024-01-01', 'ATENDENTE', '092.533.444-05');

-- Especializações (IDs sequenciais 1, 2, 3, 4)
INSERT INTO personal (id_funcionario, cref) VALUES (1, '123456-G/CE');
INSERT INTO faxineiro (id_funcionario, status_limpeza) VALUES (2, 'Geral');
INSERT INTO mecanico (id_funcionario, status_conserto) VALUES (3, 'Ok');
INSERT INTO atendente (id_funcionario, turno) VALUES (4, 'Manhã');

-- Equipamentos
INSERT INTO equipamento (nome, estado_conservacao, cpf_proprietario, id_funcionario_mecanico, id_funcionario_faxineiro) VALUES
('Esteira Ergométrica', 'Bom', '092.533.444-05', 3, 2),
('Bicicleta Ergométrica', 'Regular', '092.533.444-05', 3, 2),
('Supino Reto', 'Excelente', '092.533.444-05', NULL, 2);

-- Planos
INSERT INTO plano (tipo, valor, id_funcionario_atendente) VALUES
('Mensal', 120.00, 4),
('Trimestral', 330.00, 4);

-- Clientes
INSERT INTO cliente (nome, cpf, id_plano_atual) VALUES
('Jonh Miguel', '111.222.333-44', 1),
('Enzo Anjos', '555.666.777-88', 2);

-- Treinos
INSERT INTO treino (descricao, id_cliente, id_personal) VALUES
('Treino A - Hipertrofia', 1, 1),
('Treino B - Cardio', 2, 1);

-- Pagamentos
INSERT INTO pagamento (valor, forma_pagamento, data_pagamento, data_vencimento, id_cliente) VALUES
(120.00, 'PIX', '2025-01-05', '2025-01-10', 1);

-- Reset de sequências (Importante para o sistema não falhar nos inserts)
SELECT setval(pg_get_serial_sequence('funcionario', 'id_funcionario'), coalesce(max(id_funcionario), 1)) FROM funcionario;
SELECT setval(pg_get_serial_sequence('cliente', 'id_cliente'), coalesce(max(id_cliente), 1)) FROM cliente;
SELECT setval(pg_get_serial_sequence('plano', 'id_plano'), coalesce(max(id_plano), 1)) FROM plano;
SELECT setval(pg_get_serial_sequence('treino', 'id_treino'), coalesce(max(id_treino), 1)) FROM treino;
SELECT setval(pg_get_serial_sequence('pagamento', 'id_pagamento'), coalesce(max(id_pagamento), 1)) FROM pagamento;
SELECT setval(pg_get_serial_sequence('equipamento', 'id_equipamento'), coalesce(max(id_equipamento), 1)) FROM equipamento;