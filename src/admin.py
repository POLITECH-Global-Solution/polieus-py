"""
Ações que podem ser realizadas pela prefeitura
"""
import os
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from persistence import find_all
from config import WARN, ERROR, INFO

console = Console()
PROTOCOLS_PATH = os.path.join("dados", "protocols.txt")

def create_table() -> Table:
    # vou criar uma tabela com o rich, essa função vai ficarpras colunas/estrutura
    table = Table(title="\n[reverse][bold]Ocorrências[/bold][/reverse]")
    table.add_column("Protocolo",justify="center",style="purple",no_wrap=True)
    table.add_column("Status",justify="center",style="blue",no_wrap=True)
    table.add_column("Categoria",justify="center",style="cyan",no_wrap=True)
    table.add_column("Bairro",justify="center",style="green",no_wrap=True)
    table.add_column("Descrição",justify="center",style="yellow",no_wrap=False)
    table.add_column("Data de criação",justify="center",style="red",no_wrap=True)
    return table

def consult_occurrence() -> None:
    """Consulta ocorrências."""
    occurrences = find_all()
    # aqui vou usar a tabela do rich
    table = create_table()
    #colocar cada linha da tabela para cada ocorrencia
    if not occurrences: console.print(WARN,"Ocorrências não puderam ser carregadas")
    for occurrence in occurrences:
        table.add_row(
            str(occurrence["ds_protocolo"]),
            str(occurrence["st_ocorrencia"]),
            str(occurrence["nm_categoria"]),
            str(occurrence["nm_bairro"]),
            str(occurrence["ds_ocorrencia"]),
            str(occurrence["dt_abertura"]))
    console.print(table)
    input("Aperte ENTER para continuar...")

#usei IA aqui tambem
def select_protocol() -> str | None:
    """
    Lê o arquivo protocols.txt e abre uma barra de pesquisa interativa (fuzzy).
    Retorna apenas a string do protocolo selecionado (ex: 'POL-2026-0001').
    """
    if not os.path.exists(PROTOCOLS_PATH):
        console.print(WARN,"arquivo de protocolos não encontrado. Carregando do banco...")
        find_all()
    options = []
    try:
        with open(PROTOCOLS_PATH, "r", encoding="utf-8") as file:
            for line in file:
                clean_line = line.strip()
                if not clean_line:
                    continue
                # Extrai apenas o código antes do primeiro '|' para ser o valor retornado [IA]
                protocol = clean_line.split("|")[0].strip()
                options.append(Choice(value=protocol, name=clean_line))
    except OSError as e:
        console.print(ERROR, f"Erro ao ler arquivo de protocolos: {e}")
        return None
    if not options:
        console.print(WARN,"Nenhuma ocorrência registrada para atualizar.")
        return None
    # Barra de pesquisa interativa com filtro em tempo real
    choice = inquirer.fuzzy(
        message="Digite o protocolo ou bairro para filtrar:",
        choices=options,
        max_height="70%",
        validate=lambda res: bool(res) or "Selecione uma ocorrência válida."
    ).execute()
    return choice

def update_status() -> None:
    """Atualiza o status de uma ocorrência"""
    console.print(Panel.fit("[bold red]🔄 2. ATUALIZAR STATUS DE OCORRÊNCIA[/bold red]"))
    # SINCRONIZAR BANCO COM O ARQUIVO
    occurrences = find_all()
    if occurrences == None:
        return
    protocol = select_protocol()
    if not protocol:
        return
    console.print(f'{INFO}Protocolo selecionado para atualização: [bold]{protocol}[/bold]')

    for occurrence in occurrences:
        if occurrence["ds_protocol"] == protocol:
            option = inquirer.select(
                message="Selecione um novo status:",
                choices=[
                    Choice(value='EM_EXECUCAO', name="Em execução"),
                    Choice(value='CONCLUIDA', name="Concluída"),
                    Choice(value='NAO_APROVADA', name="Não aprovada"),
                    Choice(value=0, name="✖️ Cancelar")
                ],
                default=0
            ).execute()
            if option == 0:
                console.print(WARN,"Status não foi atualizado por cancelamento.")
                return
            occurrence["st_ocorrencia"] = option
            console.print(INFO,f"Status de {protocol} atualizado para {option}")
            return