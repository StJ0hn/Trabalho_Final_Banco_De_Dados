from src.dao.crud_dao import BaseDAO

class QueryDAO(BaseDAO):
    """
    Implementa a execução das Views (Item 5) e Consultas Avançadas (Item 7).
    """

    # --- ITEM 5: VIEWS ---
    def ver_ficha_treinos(self):
        return self.fetch_data("SELECT * FROM vw_ficha_treino")

    def ver_manutencao(self):
        return self.fetch_data("SELECT * FROM vw_manutencao_equipamentos")

    # --- ITEM 7: CONSULTAS AVANÇADAS ---
    def faturamento_por_plano(self):
        sql = """
            SELECT p.tipo, COUNT(c.id_cliente), SUM(p.valor)
            FROM plano p
            JOIN cliente c ON p.id_plano = c.id_plano_atual
            GROUP BY p.tipo
        """
        return self.fetch_data(sql)

    def funcionarios_salario_alto(self):
        sql = """
            SELECT nome, salario, tipo
            FROM funcionario
            WHERE salario > (SELECT AVG(salario) FROM funcionario)
        """
        return self.fetch_data(sql)

    def clientes_inadimplentes(self):
        sql = """
            SELECT c.nome, p.data_vencimento, p.data_pagamento
            FROM pagamento p
            JOIN cliente c ON p.id_cliente = c.id_cliente
            WHERE p.data_pagamento > p.data_vencimento
        """
        return self.fetch_data(sql)