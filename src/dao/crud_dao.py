from src.database import Database


class BaseDAO:
    def execute_action(self, sql, params=None):
        conn = None
        cursor = None
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            return True, cursor.rowcount
        except Exception as e:
            if conn: conn.rollback()
            print(f"Erro SQL (Escrita): {e}")
            return False, 0
        finally:
            if cursor: cursor.close()
            if conn: Database.return_connection(conn)

    def fetch_data(self, sql, params=None, one=False):
        conn = None
        cursor = None
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            return cursor.fetchone() if one else cursor.fetchall()
        except Exception as e:
            print(f"Erro SQL (Leitura): {e}")
            return None
        finally:
            if cursor: cursor.close()
            if conn: Database.return_connection(conn)


class ClienteDAO(BaseDAO):
    def criar(self, nome, cpf, id_plano):
        sql = "INSERT INTO cliente (nome, cpf, id_plano_atual) VALUES (%s, %s, %s)"
        success, _ = self.execute_action(sql, (nome, cpf, id_plano))
        return success

    def listar_todos(self):
        sql = """
            SELECT c.id_cliente, c.nome, c.cpf, p.tipo, p.valor 
            FROM cliente c 
            LEFT JOIN plano p ON c.id_plano_atual = p.id_plano 
            ORDER BY c.id_cliente
        """
        return self.fetch_data(sql)

    def buscar_por_cpf(self, cpf):
        sql = "SELECT * FROM cliente WHERE cpf = %s"
        return self.fetch_data(sql, (cpf,), one=True)

    def buscar_por_id(self, uid):
        sql = "SELECT * FROM cliente WHERE id_cliente = %s"
        return self.fetch_data(sql, (uid,), one=True)

    def atualizar(self, id_cliente, nome, id_plano):
        # Lógica de atualização condicional simples para a apresentação
        if not nome and not id_plano: return False

        # Num cenário real, montaríamos a query dinamicamente.
        # Aqui, assumimos que ambos são passados para simplificar o DML fixo.
        sql = "UPDATE cliente SET nome = %s, id_plano_atual = %s WHERE id_cliente = %s"
        success, rows = self.execute_action(sql, (nome, id_plano, id_cliente))
        return success and rows > 0

    def remover(self, id_cliente):
        sql = "DELETE FROM cliente WHERE id_cliente = %s"
        success, rows = self.execute_action(sql, (id_cliente,))
        return success and rows > 0


class FuncionarioDAO(BaseDAO):
    def listar_todos(self):
        sql = """
            SELECT f.id_funcionario, f.nome, f.tipo, f.salario 
            FROM funcionario f 
            ORDER BY f.id_funcionario
        """
        return self.fetch_data(sql)