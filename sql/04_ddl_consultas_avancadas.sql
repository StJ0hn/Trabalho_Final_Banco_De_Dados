-- 1. Faturamento total por Tipo de Plano (GROUP BY)
SELECT p.tipo, COUNT(c.id_cliente) as qtd_clientes, SUM(p.valor) as total
FROM plano p
JOIN cliente c ON p.id_plano = c.id_plano_atual
GROUP BY p.tipo;

-- 2. Funcionários com salário acima da média (SUBQUERY)
SELECT nome, salario, tipo
FROM funcionario
WHERE salario > (SELECT AVG(salario) FROM funcionario);

-- 3. Clientes com pagamentos atrasados (Lógica de Datas)
SELECT c.nome, p.data_vencimento, p.data_pagamento
FROM pagamento p
JOIN cliente c ON p.id_cliente = c.id_cliente
WHERE p.data_pagamento > p.data_vencimento;

-- 4. Contagem de equipamentos por estado (GROUP BY)
SELECT estado_conservacao, COUNT(*) as quantidade
FROM equipamento
GROUP BY estado_conservacao;

-- 5. Personal Trainer com mais alunos (JOIN Múltiplo + Agregação)
SELECT f.nome, COUNT(t.id_treino) as total_treinos
FROM personal p
JOIN funcionario f ON p.id_funcionario = f.id_funcionario
JOIN treino t ON p.id_funcionario = t.id_personal
GROUP BY f.nome
ORDER BY total_treinos DESC;