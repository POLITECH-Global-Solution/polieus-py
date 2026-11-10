"""
PALIEUS - main.py
- Henrique Bonachela    - RM
- Isabelle Ferreira     - RM
- Marina                - RM
- Milena Conegin        - RM
- Murilo Almeida        - RM
"""

from src import admin, citizen

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich.console import Console
from rich.panel import Panel

console = Console()

def show_header() -> None:
    """Mostra o cabeçalho de entrada do programa"""
    console.print(Panel.fit(
        "\t[bold #B3261E]🏛️ POLIEUS — CITIZENTECH 2026\n[/bold #B3261E]"
        "[dim]Sistema de gestão inteligente para cidades[/dim]"
        ))

def menu_login() -> int:
    """Menu de entrada onde se decidi o tipo de usuário."""
    option = inquirer.select(
        message="Escolha um acesso:",
        choices=[
            Choice(value=1, name="🧑 1. Acesso cidadão"),
            Choice(value=2, name="🇧🇷  2. Acesso município"),
            Choice(value=3, name="❓ 3. Ajuda"),
            Choice(value=4, name="❌ 0. Encerrar")
        ],
        default=0
    ).execute()
    return option

def menu_citizen() -> None:
    """Menu com ações para os cidadãos."""
    while True:
        option = inquirer.select(
            message="Selecione uma opção:",
            choices=[
                Choice(value=1, name="📝 1. Registrar ocorrência"),
                Choice(value=2, name="🔍 2. Consultar ocorrências"),
                Choice(value=0, name="↩️ 0. Voltar")
            ],
            default=0
        ).execute()
        if option == 1: print("A") #função de registrar ocorrência
        elif option == 2: print("B") #função de consultar ocorrências
        else: break

def menu_admin() -> None:
    """Menu com ações para a prefeitura/administradora do município."""
    while True:
        option = inquirer.select(
            message="Selecione uma opção:",
            choices=[
                Choice(value=1, name="🔍 1. Consultar ocorrências"),
                Choice(value=2, name="⚡ 2. Analisar prioridades"),
                Choice(value=3, name="🔄 3. Atualizar situação"),
                Choice(value=4, name="📊 4. Gerar relatórios"),
                Choice(value=5, name="🚨 5. Consultar recorrências"),
                Choice(value=0, name="↩️ 0. Voltar")
            ],
            default=0
        ).execute()
        match option:
            case 1: print("1") #função de consultar ocorrências
            case 2: print("2") #função de analisar prioridade
            case 3: print("3") #função de analisar situação
            case 4: print("4") #função de gerar relatórios
            case 5: print("5") #função de consultar recorrencias
            case _: break

def menu_ajuda() -> None:
    """Mostra um resumo do nosso programa"""
    console.print(Panel.fit(
        "Uma plataforma pública voltada para o cidadão e o gestor público, onde os munícipes podem:[blue]\n- registras ocorrências;\n- acompanhar o andamento delas;\n- monitorar o orçamento e indicadores da prefeitura.[/blue]\n E para a perfeitura:[blue]\n- Ver ocorrências agrupadas e ter ajuda na classificação, criação de prazos e na prioridade, além de auxílio na gestão da verba.[/blue]"
    ))
    input("pressione ENTER para voltar.")

def main() -> None:
    """Inicia o programa."""
    show_header()
    while True:
        option = menu_login()
        if option == 1:
            menu_citizen()
        elif option == 2:
            menu_admin()
        elif option == 3:
            menu_ajuda()
        else: break

if __name__ == "__main__":
    main()