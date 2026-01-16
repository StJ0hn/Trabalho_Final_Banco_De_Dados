import os

def limpar_tela():
    """
    Limpa o console de forma compatível com Windows e Linux.
    Trata a ausência da variável TERM em ambientes de IDE (PyCharm).
    """
    # Verifica se é Windows (NT)
    if os.name == 'nt':
        os.system('cls')
    else:
        # Em ambientes Unix/Linux/Mac ou Git Bash, o comando 'clear' exige TERM.
        # Se não estiver setado (comum em IDEs), definimos um fallback seguro.
        if 'TERM' not in os.environ:
            os.environ['TERM'] = 'xterm'
        os.system('clear')

def pausar():
    """Pausa a execução para leitura do usuário."""
    input("\nPressione ENTER para continuar...")