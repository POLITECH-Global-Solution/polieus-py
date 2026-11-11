import json

from json import JSONDecodeError
from config import ERROR, WARN
from rich.console import Console

console = Console()

def get_json() -> [{str,str|int|boolean}|None]:
    """Pega os dados do data.json de src, ou trunca se não existir"""
    try:
        # abre o arquivo com ewith pra fechar automatico no modo read
        with open('src/data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError as w:
        # se o arquivo nao for envcontrado ao inves de um ERRO mandar um AVISO e truncar o arquivo
        console.print(WARN, w)
        console.print(WARN, 'O arquivo não existe, criando ele.....')
        with open('src/data.json', 'w', encoding='utf-8') as f:
            # cria o arquivo com uma lista vazia
            json.dump([], f, indent=4, ensure_ascii=False)
    except (JSONDecodeError, Except) as e:
        # outros error apenas não tem retorno
        console.print(ERROR, e)
    return []

print(get_json())