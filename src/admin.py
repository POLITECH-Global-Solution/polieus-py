"""
Ações que podem ser realizadas pela prefeitura
"""

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from persistence import find_all
from config import WARN

console = Console()


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