from src.database import Database
from src.dao.crud_dao import ClienteDAO, FuncionarioDAO
from src.dao.query_dao import QueryDAO
from src.utils import limpar_tela, pausar
import sys


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
            dados = dao.listar_todos()
            print(f"\n{'ID':<5} | {'NOME':<25} | {'CPF':<15} | {'PLANO'}")
            print("-" * 60)
            if dados:
                for d in dados:
                    plano = d[3] if d[3] else "Sem Plano"
                    print(f"{d[0]:<5} | {d[1]:<25} | {d[2]:<15} | {plano}")
            else:
                print("Nenhum dado encontrado.")
            pausar()

        elif op == '2':
            nome = input("Nome Completo: ")
            cpf = input("CPF (ex: 000.000.000-00): ")
            plano = input("ID do Plano (1 ou 2): ")
            if dao.criar(nome, cpf, plano): print(">> Sucesso!")
            pausar()

        elif op == '3':
            cpf = input("CPF para busca: ")
            res = dao.buscar_por_cpf(cpf)
            print(f"\nResultado: {res}" if res else "\n>> Não encontrado.")
            pausar()

        elif op == '4':
            try:
                uid = int(input("ID do Cliente: "))
                nome = input("Novo Nome: ")
                plano = int(input("Novo ID Plano: "))
                if dao.atualizar(uid, nome, plano): print(">> Atualizado com sucesso!")
            except ValueError:
                print(">> Erro: ID inválido.")
            pausar()

        elif op == '5':
            try:
                uid = int(input("ID do Cliente para remover: "))
                if dao.remover(uid): print(">> Removido com sucesso!")
            except ValueError:
                print(">> Erro: ID inválido.")
            pausar()

        elif op == '0':
            break


def menu_relatorios():
    dao = QueryDAO()
    while True:
        limpar_tela()
        print("=== RELATÓRIOS E CONSULTAS (ITENS 5 e 7) ===")
        print("1. [VIEW] Ficha de Treinos")
        print("2. [VIEW] Manutenção Equipamentos")
        print("3. [QUERY] Faturamento por Plano")
        print("4. [QUERY] Funcionários Salário > Média")
        print("5. [QUERY] Pagamentos em Atraso")
        print("0. Voltar")
        op = input("\nOpção: ")

        if op == '1':
            dados = dao.ver_ficha_treinos()
            print(f"\n{'TREINO':<20} | {'CLIENTE':<20} | {'PERSONAL'}")
            if dados:
                for d in dados: print(f"{d[2]:<20} | {d[1]:<20} | {d[3]}")
            pausar()

        elif op == '2':
            dados = dao.ver_manutencao()
            if dados:
                for d in dados: print(d)
            pausar()

        elif op == '3':
            dados = dao.faturamento_por_plano()
            print("\nPLANO | QTD | TOTAL")
            if dados:
                for d in dados: print(f"{d[0]} | {d[1]} | R$ {d[2]}")
            pausar()

        elif op == '4':
            dados = dao.funcionarios_salario_alto()
            print("\nNOME | SALÁRIO | CARGO")
            if dados:
                for d in dados: print(f"{d[0]} | R$ {d[1]} | {d[2]}")
            pausar()

        elif op == '5':
            dados = dao.clientes_inadimplentes()
            print("\nCLIENTE | VENCIMENTO | PAGAMENTO")
            if dados:
                for d in dados: print(f"{d[0]} | {d[1]} | {d[2]}")
            else:
                print("Nenhum atraso registrado.")
            pausar()

        elif op == '0':
            break


def main():
    try:
        Database.initialize()
    except Exception as e:
        print(f"Erro Crítico de Conexão: {e}")
        sys.exit(1)

    while True:
        limpar_tela()
        print("=== SISTEMA ACADEMIA (TRABALHO FINAL) ===")
        print("1. Módulo Clientes (Item 6)")
        print("2. Listar Funcionários (Item 6)")
        print("3. Relatórios Avançados (Itens 5 e 7)")
        print("0. Sair")
        op = input("\nEscolha: ")

        if op == '1':
            menu_clientes()
        elif op == '2':
            print("\n--- FUNCIONÁRIOS ---")
            for f in FuncionarioDAO().listar_todos(): print(f)
            pausar()
        elif op == '3':
            menu_relatorios()
        elif op == '0':
            Database.close_all_connections()
            print("Sistema encerrado.")
            break
        else:
            pausar()


if __name__ == "__main__":
    main()