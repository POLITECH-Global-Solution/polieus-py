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
    if not occurrences:
        console.print(WARN,"Ocorrências não foram carregas corretamente")
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

# essa função vai veriicar cada ocorrencia e guardar o bairro e categoria num dicionario
# esse dicionario vai ter do outro ldo uma qauntidade, então e não existir ele ria mse não adiciona nesse valor
def group_occurrence(occurrences:list[dict[str,str]]) -> tuple[dict[str,int],dict[str,int]]:
    count_neighborhoods = {}
    count_categories = {}
    for occurrence in occurrences:
        # pega o nome do bairro, se não existir diz que é NA, e vira contagem também
        n = occurrence.get("nm_bairro", "Bairro não informado")
        # vai adicionar o valor atual, se não houver o deault vai criar um com 0 e o +1 faz virar1
        count_neighborhoods[n] =  count_neighborhoods.setdefault(n, 0) + 1
        #mesmo pra categoria
        c = occurrence.get("nm_categoria", "Sem categoria")
        count_categories[c] = count_categories.setdefault(c, 0) + 1
    return count_neighborhoods,count_categories

def generate_reports() -> None:
    occurrences = [
        {"nm_bairro": "Vila Maria", "nm_categoria": "Pavimentação", "st_ocorrencia": "CONCLUIDA"},
        {"nm_bairro": "Vila Maria", "nm_categoria": "Pavimentação", "st_ocorrencia": "EM_EXECUCAO"},
        {"nm_bairro": "Vila Maria", "nm_categoria": "Acessibilidade", "st_ocorrencia": "REGISTRADA"},
        {"nm_bairro": "Centro", "nm_categoria": "Acessibilidade", "st_ocorrencia": "CONCLUIDA"},
        {"nm_bairro": "Centro", "nm_categoria": "Iluminação", "st_ocorrencia": "NAO_APROVADA"},
        {"nm_bairro": "Pinheiros", "nm_categoria": "Saneamento", "st_ocorrencia": "EM_ANALISE"},
        {"nm_bairro": "Pinheiros", "nm_categoria": "Pavimentação", "st_ocorrencia": "EM_EXECUCAO"},
        {"nm_bairro": "Mooca", "nm_categoria": "Iluminação", "st_ocorrencia": "APROVADA"},
    ]
    if not occurrences:
        console.print(WARN,"Ocorrências não foram carregas corretamente, relatório não pôde ser gerado")
        return
    # o total de ocorrencias no banco
    total = len(occurrences)
    concluded = 0
    progress = 0
    blocked = 0
    others = 0
    for occurrence in occurrences:
        # classificar po status
        if occurrence["st_ocorrencia"] == "CONCLUIDA": concluded += 1
        elif occurrence["st_ocorrencia"] == "EM_EXECUCAO": progress += 1
        elif occurrence["st_ocorrencia"] == "NAO_APROVADA": blocked += 1
        else: others +=1
    # agrupando bairros
    count_n,count_c = group_occurrence(occurrences)
    #formatando pra ficar mais facil
    neighborhoods = "[bold]OCORRÊNCIAS POR BAIRROS:[/bold]\n"
    for k,v in count_n.items():
        neighborhoods +=f"- {k}:\t\t{v}\n"
    categories = "[bold]OCORRÊNCIAS POR CATEGORIAS:[/bold]\n"
    for k,v in count_c.items():
        categories +=f"- {k}:\t\t{v}\n"
    # agora mostrar tudo
    console.print(Panel.fit(
        "📊 RELATÓRIO DE OCORRÊNCIAS\n"
        "===============================================\n"
        f"[bold]TOTAL de ocorrências:[/bold]\t{total}\n"
        f"[bold]Concluídas:[/bold]\t\t {concluded}\n"
        f"[bold]Em andamento:[/bold]\t\t {progress}\n"
        f"[bold]Não aprovadas:[/bold]\t\t {blocked}\n"
        f"[bold]Outras:[/bold]\t\t\t {others}\n"
        "===============================================\n"
        f"{neighborhoods}"
        "===============================================\n"
        f"{categories}"
    ))
    print("Aperte ENTER para continuar...")