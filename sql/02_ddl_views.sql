-- VIEW 1: Ficha de Treino Detalhada
-- Objetivo: Visualizar treino, cliente e personal numa única tabela virtual.
CREATE OR REPLACE VIEW vw_ficha_treino AS
SELECT
    t.id_treino,
    c.nome AS cliente,
    t.descricao AS treino,
    f.nome AS personal_trainer,
    p.cref
FROM treino t
JOIN cliente c ON t.id_cliente = c.id_cliente
JOIN personal p ON t.id_personal = p.id_funcionario
JOIN funcionario f ON p.id_funcionario = f.id_funcionario;

-- VIEW 2: Relatório de Manutenção e Limpeza
-- Objetivo: Monitorizar equipamentos e seus responsáveis técnicos.
CREATE OR REPLACE VIEW vw_manutencao_equipamentos AS
SELECT
    e.id_equipamento,
    e.nome AS equipamento,
    e.estado_conservacao,
    fm.nome AS mecanico_responsavel,
    m.status_conserto,
    ff.nome AS faxineiro_responsavel
FROM equipamento e
LEFT JOIN mecanico m ON e.id_funcionario_mecanico = m.id_funcionario
LEFT JOIN funcionario fm ON m.id_funcionario = fm.id_funcionario
LEFT JOIN faxineiro fa ON e.id_funcionario_faxineiro = fa.id_funcionario
LEFT JOIN funcionario ff ON fa.id_funcionario = ff.id_funcionario;