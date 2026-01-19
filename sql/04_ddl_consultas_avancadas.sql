-- 1. Faturamento total agrupado por Tipo de Plano
SELECT p.tipo, COUNT(c.id_cliente) as total_clientes, SUM(p.valor) as faturamento_total
FROM plano p
JOIN cliente c ON p.id_plano = c.id_plano_atual
GROUP BY p.tipo;

-- 2. Funcionários com salário acima da média da empresa
SELECT nome, salario, tipo
FROM funcionario
WHERE salario > (SELECT AVG(salario) FROM funcionario);

-- 3. Relatório de Inadimplência (Pagamento realizado após o vencimento)
SELECT c.nome, p.data_vencimento, p.data_pagamento
FROM pagamento p
JOIN cliente c ON p.id_cliente = c.id_cliente
WHERE p.data_pagamento > p.data_vencimento;

-- 4. Quantitativo de equipamentos por estado de conservação
SELECT estado_conservacao, COUNT(*) as quantidade
FROM equipamento
GROUP BY estado_conservacao;

-- 5. Ranking de Personal Trainers por volume de fichas de treino
SELECT f.nome, COUNT(t.id_treino) as total_fichas
FROM personal p
JOIN funcionario f ON p.id_funcionario = f.id_funcionario
JOIN treino t ON p.id_funcionario = t.id_personal
GROUP BY f.nome
ORDER BY total_fichas DESC;