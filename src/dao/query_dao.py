from src.dao.crud_dao import BaseDAO

class QueryDAO(BaseDAO):
    # --- Views (Tabelas Virtuais) ---
    def ver_ficha_treinos(self):
        return self.fetch_data("SELECT * FROM vw_ficha_treino")

    def ver_manutencao(self):
        return self.fetch_data("SELECT * FROM vw_manutencao_equipamentos")

    # --- Relatórios Gerenciais (Aggregation & Complex Joins) ---
    def faturamento_por_plano(self):
        return self.fetch_data("""
            SELECT p.tipo, COUNT(c.id_cliente), SUM(p.valor)
            FROM plano p
            JOIN cliente c ON p.id_plano = c.id_plano_atual
            GROUP BY p.tipo
        """)

    def funcionarios_salario_alto(self):
        return self.fetch_data("""
            SELECT nome, salario, tipo
            FROM funcionario
            WHERE salario > (SELECT AVG(salario) FROM funcionario)
        """)

    def clientes_inadimplentes(self):
        return self.fetch_data("""
            SELECT c.nome, p.data_vencimento, p.data_pagamento
            FROM pagamento p
            JOIN cliente c ON p.id_cliente = c.id_cliente
            WHERE p.data_pagamento > p.data_vencimento
        """)