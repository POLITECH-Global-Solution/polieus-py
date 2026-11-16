"""
PALIEUS - main.py
- Henrique Bonachela    - RM
- Isabelle Ferreira     - RM
- Marina                - RM
- Milena Conegin        - RM
- Murilo Almeida        - RM
"""

from src import (admin as a,
                 citizen as c,
                 config)

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich.console import Console
from rich.panel import Panel

console = Console()

def show_header() -> None:
    """Mostra o cabeçalho de entrada do programa"""
    # printa com estilo um painel que expande apenas conforme conteúdo
    console.print(Panel.fit(
        "\t[bold #B3261E]🏛️ POLIEUS — CITIZENTECH 2026\n[/bold #B3261E]"
        "[dim]Sistema de gestão inteligente para cidades[/dim]"
        ))

def set_name() -> str:
    """Escolhi e trata o nome, colocando ele numa variável global e retornando ele """
    while True:
        try:
            #pergunta o nome em amarelo
            name = console.input("[yellow]Escreva seu nome: [/yellow]").strip().capitalize()
            if name == "":
                raise ValueError("Nome inválido, não pode ser vazio")
        except Exception as e:
            #o config.ERROR já está estilizado com bold e red.
            console.print(config.ERROR, e)
        else:
            # se tudo eu certo salva globalmente e retorna
            config.name = name
            return name

def change_name() -> str:
    """Muda um nome globalmente, pedindo confirmação do usuário"""
    name = config.name
    set_name()
    # warn já tem bold e yellow
    console.print(config.WARN,
                  f"Tem certeza que deseja mudar o nome de [blue]{name}[/blue] para [blue]{config.name}[/blue]?")
    # serve para aparecer Y/n
    proceed = inquirer.confirm(message="Trocar?", default=True).execute()
    if proceed:
        name = config.name
        # INFO já vem com azul e bold
        console.print(config.INFO,
                      f"Nome trocado para {name}")
    else:
        config.name = name
        console.print(config.INFO,
                      f"Nome continuou como: {name}")
    return name

def menu_login() -> None:
    """Menu de entrada onde se decidi o tipo de usuário."""
    # atribuindo as variaveis globais para não precisar ficar config. toda hora
    name = config.name
    while True:
        # cria uma lisa de opções interativa
        option = inquirer.select(
            message=f"{name}, escolha um tipo de acesso:",
            choices=[
                Choice(value=1, name="🧑 1. Acesso cidadão"),
                Choice(value=2, name="🇧🇷  2. Acesso município"),
                Choice(value=3, name="❓ 3. Ajuda"),
                Choice(value=4, name="♻️  4. Trocar nome"),
                Choice(value=0, name="❌ 0. Encerrar")
            ],
            default=1
        ).execute()
        # chama as funçẽs na mesma linha ou encerra
        match option:
            case 1: menu_citizen()
            case 2: menu_admin()
            case 3: menu_help()
            case 4: name = change_name()
            case 0: break

def menu_citizen() -> None:
    """Menu com ações para os cidadãos."""
    name = config.name
    while True:
        console.print(Panel.fit(
            f"[bold]Bem-vindo á área de cidadão {name}![/bold]\n"
            "Aqui você pode realizar ocorrências, e consultar as existentes."
        ))
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
    name = config.name
    console.print(Panel.fit(
        f"[bold]Bem-vindo á área de administrador {name}![/bold]\n"
        "Aqui você pode ver as demandas do povo, ver prioridades e receber auxilio para tomar decisões."
    ))
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

def menu_help() -> None:
    """Mostra um resumo do nosso programa"""
    console.print(Panel.fit(
        "Uma plataforma pública voltada para o cidadão e o gestor público, onde os munícipes podem:[blue]\n- registras ocorrências;\n- acompanhar o andamento delas;\n- monitorar o orçamento e indicadores da prefeitura.[/blue]\n E para a perfeitura:[blue]\n- Ver ocorrências agrupadas e ter ajuda na classificação, criação de prazos e na prioridade, além de auxílio na gestão da verba.[/blue]"
    ))
    # Pra usuário ter tempo de ler
    input("pressione ENTER para voltar.")

def main() -> None:
    """Inicia o programa."""
    show_header()
    set_name()
    menu_login()

if __name__ == "__main__":
    main()