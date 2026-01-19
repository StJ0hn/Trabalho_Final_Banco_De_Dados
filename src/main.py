from src.database import Database
from src.dao.crud_dao import ClienteDAO, FuncionarioDAO
from src.dao.query_dao import QueryDAO
from src.utils import limpar_tela, pausar
import sys


# --- FUNÇÕES AUXILIARES DE INPUT SEGURO ---
def ler_inteiro(mensagem):
    """Lê um inteiro do usuário sem quebrar o programa se ele digitar texto."""
    while True:
        valor = input(mensagem)
        if not valor: return None  # Permite cancelar com Enter vazio
        try:
            return int(valor)
        except ValueError:
            print(">> Erro: Por favor, digite um número válido.")


# --- MENUS ---

def menu_clientes():
    dao = ClienteDAO()
    while True:
        limpar_tela()
        print("=== MÓDULO CLIENTES (CRUD - ITEM 6) ===")
        print("1. Listar Clientes")
        print("2. Cadastrar Cliente")
        print("3. Buscar por CPF")
        print("4. Atualizar Cliente")
        print("5. Remover Cliente")
        print("0. Voltar")

        op = input("\nOpção: ")

        if op == '1':
            try:
                dados = dao.listar_todos()
                print(f"\n{'ID':<5} | {'NOME':<25} | {'CPF':<15} | {'PLANO'}")
                print("-" * 60)
                if dados:
                    for d in dados:
                        # Tratamento para plano NULL ou formatação
                        plano_nome = d[3] if len(d) > 3 and d[3] else "Sem Plano"
                        print(f"{d[0]:<5} | {d[1]:<25} | {d[2]:<15} | {plano_nome}")
                else:
                    print(">> Nenhum dado encontrado.")
            except Exception as e:
                print(f">> Erro ao listar: {e}")
            pausar()

        elif op == '2':
            print("\n--- Novo Cadastro ---")
            nome = input("Nome Completo: ")
            if not nome: continue

            cpf = input("CPF (ex: 000.000.000-00): ")

            print("Planos: 1-Mensal, 2-Trimestral")
            plano = ler_inteiro("ID do Plano: ")
            if plano is None: continue

            if dao.criar(nome, cpf, plano):
                print(">> Sucesso! Cliente cadastrado.")
            else:
                print(">> Erro ao cadastrar (Verifique se o CPF já existe).")
            pausar()

        elif op == '3':
            cpf = input("Digite o CPF para busca: ")
            res = dao.buscar_por_cpf(cpf)
            if res:
                print(f"\nENCONTRADO: ID={res[0]} | Nome={res[1]} | PlanoID={res[3]}")
            else:
                print("\n>> Não encontrado.")
            pausar()

        elif op == '4':
            uid = ler_inteiro("ID do Cliente a atualizar: ")
            if uid:
                # Busca o atual para mostrar
                atual = dao.buscar_por_id(uid) if hasattr(dao, 'buscar_por_id') else None
                if atual: print(f"Editando: {atual[1]}")

                nome = input("Novo Nome (Enter para manter): ")
                novo_plano = ler_inteiro("Novo ID Plano (0 para manter): ")

                # Lógica simplificada: se vazio, mantém o antigo (precisaria implementar no DAO,
                # mas aqui forçamos o update para teste)
                if nome and novo_plano:
                    if dao.atualizar(uid, nome, novo_plano): print(">> Atualizado com sucesso!")
                else:
                    print(">> Operação cancelada ou dados incompletos.")
            pausar()

        elif op == '5':
            uid = ler_inteiro("ID do Cliente para remover: ")
            if uid:
                if dao.remover(uid):
                    print(">> Removido com sucesso! (Verifique logs de auditoria no banco)")
                else:
                    print(">> Erro: Cliente não encontrado ou ID inválido.")
            pausar()

        elif op == '0':
            break
        else:
            print(">> Opção inválida.")
            pausar()


def menu_relatorios():
    dao = QueryDAO()
    while True:
        limpar_tela()
        print("=== RELATÓRIOS E CONSULTAS (ITENS 5 e 7) ===")
        print("1. [VIEW] Ficha de Treinos")
        print("2. [VIEW] Manutenção Equipamentos")
        print("3. [QUERY] Faturamento por Plano")
        print("4. [QUERY] Funcionários Salário")
        print("5. [QUERY] Pagamentos em Atraso")
        print("0. Voltar")
        op = input("\nOpção: ")

        try:
            if op == '1':
                dados = dao.ver_ficha_treinos()
                print(f"\n{'TREINO':<25} | {'CLIENTE':<20} | {'PERSONAL'}")
                print("-" * 70)
                if dados:
                    for d in dados: print(f"{d[2]:<25} | {d[1]:<20} | {d[3]}")
                else:
                    print("Sem dados.")

            elif op == '2':
                dados = dao.ver_manutencao()
                if dados:
                    for d in dados: print(d)
                else:
                    print("Sem dados.")

            elif op == '3':
                dados = dao.faturamento_por_plano()
                print("\nPLANO | QTD | TOTAL")
                if dados:
                    for d in dados: print(f"{d[0]} | {d[1]} | R$ {d[2]}")
                else:
                    print("Sem dados.")

            elif op == '4':
                dados = dao.funcionarios_salario_alto()
                print("\nNOME | SALÁRIO | CARGO")
                if dados:
                    for d in dados: print(f"{d[0]} | R$ {d[1]} | {d[2]}")
                else:
                    print("Sem dados.")

            elif op == '5':
                dados = dao.clientes_inadimplentes()
                print("\nCLIENTE | VENCIMENTO | PAGAMENTO")
                if dados:
                    for d in dados: print(f"{d[0]} | {d[1]} | {d[2]}")
                else:
                    print("Nenhum atraso registrado.")

            elif op == '0':
                break
            else:
                print("Opção inválida.")

        except Exception as e:
            print(f">> Erro na consulta: {e}")

        pausar()


def main():
    # Inicialização Robusta
    try:
        Database.initialize()
        # Teste de conexão silencioso
        conn = Database.get_connection()
        Database.return_connection(conn)
    except Exception as e:
        print(f"\n[ERRO CRÍTICO DE INICIALIZAÇÃO]")
        print(f"Não foi possível conectar ao banco de dados.")
        print(f"Erro detalhado: {e}")
        print("\nVerifique em src/database.py:")
        print("1. Se a senha está correta.")
        print("2. Se o nome do banco é 'trabalho_bd'.")
        print("3. Se o PostgreSQL está rodando.")
        sys.exit(1)

    while True:
        limpar_tela()
        print("=== SISTEMA ACADEMIA (TRABALHO FINAL - 2025.2) ===")
        print("1. Gerenciar Clientes (Item 6)")
        print("2. Listar Funcionários (Item 6)")
        print("3. Relatórios Avançados (Itens 5 e 7)")
        print("0. Sair")

        op = input("\nEscolha: ")

        if op == '1':
            menu_clientes()
        elif op == '2':
            limpar_tela()
            print("\n--- LISTA DE FUNCIONÁRIOS ---")
            try:
                dados = FuncionarioDAO().listar_todos()
                if dados:
                    for f in dados: print(f)
                else:
                    print("Nenhum funcionário cadastrado.")
            except Exception as e:
                print(f"Erro ao buscar funcionários: {e}")
            pausar()
        elif op == '3':
            menu_relatorios()
        elif op == '0':
            Database.close_all_connections()
            print("\nSistema encerrado. Até logo!")
            break
        else:
            print("Opção inválida.")
            pausar()


if __name__ == "__main__":
    main()