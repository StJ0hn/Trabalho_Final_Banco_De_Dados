import os

def limpar_tela():
    if os.name == 'nt':
        os.system('cls')
    else:
        # Fallback para terminais de IDEs que não definem TERM
        os.environ.setdefault('TERM', 'xterm')
        os.system('clear')

def pausar():
    input("\nPressione ENTER para continuar...")