"""
Ações que podem ser realizadas pelos cidadãos
"""

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich.console import Console
from rich.panel import Panel
from config import ERROR, WARN, INFO
from persistence import find_categories

console = Console()

def categories_choices(x) -> Choice:
    return Choice(value=x, name=x)

def register_occurrence() -> None:
    # painel vermelho com bold para separar
    console.print(Panel.fit(
        "[bold red]📝 REGISTRO DE OCORRÊNCIAS[/bold red]"
    ))
    '''
    Aqui eu vou tentar usar o Inquirer para ter a lista de escolhas para cada cam po de um 'formulário', aí vai ficar em cada opção o que foi preenchido dela, no começo NADA.
    Por isso eu vou iniciar as valores com  valor PREENCHER 
    '''
    desc = cep = category = 'PREENCHER'
    completed = False
    while completed == False:
        option = inquirer.select(
            message="Preencha cada opção:",
            choices=[
                Choice(value=1, name=f"[bold]Descrição: {desc}"),
                Choice(value=2, name=f"CEP: {cep}"),
                Choice(value=3, name=f"Categoria: {category}"),
                Choice(value=0, name="ENVIAR")
            ],
            default=0
        ).execute()
        if option == 1:
            while True:
                #try para tratar iunput
                try:
                    #guardando num valor temporario
                    vl = console.input("Digite a descrição da ocorrência: ")
                    if vl == None or vl == "":
                        #jogando excecao
                        raise ValueError("A descrição da ocorrência não pode ser vazia")
                except Exception as e:
                    #error ja vem com estilos
                    console.print(ERROR,e)
                else:
                    desc = vl
                    break
        elif option == 2:
            # o codifo daqui é quase igual, ele só valida se o CEP existe
            while True:
                try:
                    vl = console.input("Digite o CEP: ")
                    if vl == None or vl == "":
                        raise ValueError("O CEP não pode ser vazio")
                except Exception as e:
                    console.print(ERROR,e)
                else:
                    cep = vl
                    break
        elif option == 3:
            # pega as categorias disponiveis
            #categories = find_categories().values()
            categories = ("A", "B", "C")
            category = inquirer.select(
                message="Escolha uma categoria:",
                    # criando uma opção para cada categoria
                choices=list(map(categories_choices,categories)),
                default=0
            ).execute()
        else:
            if not cep == 'PREENCHER' and not desc == 'PREENCHER' and not category == 'PREENCHER':
                completed = True
            else:
                console.print(WARN,"Preencha todo as opções!")
    console.print(INFO,"Preenchido com sucesso!")