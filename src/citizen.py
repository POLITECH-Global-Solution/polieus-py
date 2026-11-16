"""
Ações que podem ser realizadas pelos cidadãos
"""

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich.console import Console
from rich.panel import Panel
from config import ERROR, WARN, INFO
from persistence import find_categories, save
from validation import valid_occurrence
import re
import service
import random


console = Console()

def insert_desc() -> str:
    while True:
        #try para tratar iunput
        try:
            #guardando num valor temporario
            desc = console.input("Digite a descrição da ocorrência: ")
            if desc == None or desc == "":
                #jogando excecao
                raise ValueError("A descrição da ocorrência não pode ser vazia")
        except Exception as e:
            #error ja vem com estilos
            console.print(ERROR,e)
        else:
            return desc

def insert_cep() -> tuple[list[str,str]]:
    # o codifo daqui é quase igual, ele só valida se o CEP existe
    while True:
        try:
            cep = console.input("Digite o CEP (ou SAIR): ").strip()
            # previ uma tela infinita presa no cep se dr algum problema
            if cep == 'SAIR':
                cep = 'PREENCHER'
                break
            if cep== None or cep == "":
                raise ValueError("O CEP não pode ser vazio")
            # pedi para a IA fazer, ele remove traços e espaços
            cep = re.sub(r"\D", "", cep)
            #agora vou verificar se ele mantem um tamanho de CEP, se não jogar excecao
            if cep < 8:
                raise ValueError("O CEP tem 8 dígitos. Verifique e tente novamente.")
            address = get_address()
        except Exception as e:
            console.print(ERROR,e)
        else:
            return cep

def insert_category()-> str:
    # só vai ser usada aqui, naquele map
    def categories_choices(x) -> Choice:
        return Choice(value=x, name=x)
    # pega as categorias disponiveis
    categories = find_categories().values()
    category = inquirer.select(
        message="Escolha uma categoria:",
        # criando uma opção para cada categoria
        choices=list(map(categories_choices,categories)),
        default=0
    ).execute()
    return category

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
    address = {}
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
        if option == 1: desc = insert_desc()
        elif option == 2: cep, address = insert_cep()
        elif option == 3: category = insert_category()
        else:
            if not cep == 'PREENCHER' and not desc == 'PREENCHER' and not category == 'PREENCHER':
                completed = True
            else:
                console.print(WARN,"Preencha todo as opções!")
    console.print(INFO,"Preenchido com sucesso!")
    #crio o dict com todas as informaçẽs, gerando um PRotoclo aleatorio
    occurrence = {
        "st_ocorrencia": "REGISTRADA",
        "ds_protocolo": f"PRO-{random.randint(1000000, 9999999)}",
        "ds_ocorrencia": desc,
        "nm_bairro": address["nm_bairro"],
        "nm_categoria": category,
        "ds_endereco": address["ds_endereco"]
    }
    # validando as regras, usando o kwargs pra desempacotar
    confirmation, response = valid_occurrence(**occurrence)
    if confirmation:
        console.print(INFO,msg)
        save(**occurrence)
    else: console.print(ERROR,"Algo deu errado na validação. Corrija os dados e tente novamente.")

