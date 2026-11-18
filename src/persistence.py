import oracledb
import os

from rich.console import Console
from dotenv import load_dotenv
from typing_extensions import Any
from config import ERROR, INFO

console = Console()
load_dotenv()
PROTOCOLS_PATH = os.path.join("dados", "protocols.txt")

def get_connection():
    """Tenta conectar ao banco de dados Oracle
    retorna: Conexão, ou nada, se der erro"""
    # pego as variaveis do .env
    USER = os.getenv("ORACLE_USER")
    PASSWORD = os.getenv("ORACLE_PASSWORD")
    DSN = os.getenv("ORACLE_DSN")
    try:
        #conexão com as variaveis
        connection = oracledb.connect(user=USER, password=PASSWORD, dsn=DSN)
        console.print(INFO, "Conexão aberta!")
        return connection
    except oracledb.Error as e:
        raise ConnectionError(f"Falha na conexão: {e}")
    except Exception as e:
        raise Exception(e)

# isso aqui eu peguei na ia como registrado no 012
def save_protocols(occurrences: list[dict[str, Any]]) -> None:
    """Reescreve o arquivo .txt com os protocolos atualizados para a busca fuzzy."""
    os.makedirs(os.path.dirname(PROTOCOLS_PATH), exist_ok=True)

    with open(PROTOCOLS_PATH, "w", encoding="utf-8") as file:
        for oc in occurrences:
            # Salva no formato: PRO-2026001 | Vila Maria | Registrada [IA]
            # vai dar pra pesquisar por bairro e status então
            line = f"{oc['ds_protocolo']} | {oc['nm_bairro']} | {oc['st_ocorrencia']}\n"
            file.write(line)

def find_all() -> list[dict[str, Any]] | None:
    """Retorna todas as ocorrências da tabela"""
    con = None
    try:
        # pegar uma conexão com a função criada
        con = get_connection()
        cursor = con.cursor()
        # preparando sql
        sql = """
              SELECT cd_ocorrencia,st_ocorrencia,ds_protocolo,ds_ocorrencia,
                     cd_categoria,nm_bairro,ds_endereco,dt_abertura 
              FROM OCORRENCIA
        """
        # pegar todos os dados da tabela, passando o sql
        cursor.execute(sql)
        #retorna uma 'list of tuples' com os dados que eu quero
        lines = cursor.fetchall()
        occurrences = []
        # para prcurar a categoria correspondente ao pk.
        categories = find_categories()
        #guardar os valores de lines
        for line in lines:
            #guarda cada coluna em seu respectivo atributo num dicionário
            occurrence = {
                "cd_ocorrencia": line[0],
                "st_ocorrencia": line[1],
                "ds_protocolo": line[2],
                "ds_ocorrencia": line[3],
                "nm_categoria": categories.get(line[4]),
                "nm_bairro": line[5],
                "ds_endereco": line[6],
                "dt_abertura": line[7]
            }
            #guarda esse dicionário na lista
            occurrences.append(occurrence)

        save_protocols(occurrences)
        return occurrences
    except Exception as e:
        #mostra [ERRO] em bold vermelho + mensagem de erro
        console.print(ERROR,e)
    finally:
        #serve para garantir que o con nã́o é none
        if con:
            #fecha a conexão dando erro ou não
            con.close()
    return []

def find_by_id(id:int) -> dict[str,Any] | None:
    """Retorna uma ocorrência pelo seu ID"""
    con = None
    try:
        # pegar uma conexão com a função criada
        con = get_connection()
        cursor = con.cursor()
        # preparando sql de select e os parametros necessários
        sql = """
              SELECT cd_ocorrencia,st_ocorrencia,ds_protocolo,ds_ocorrencia,
                     cd_categoria,nm_bairro,ds_endereco,dt_abertura 
              FROM OCORRENCIA WHERE cd_ocorrencia = :cd_ocorrencia
        """
        params = [id]
        # pegar todos os dados da tabela passando o sql e os parametro
        cursor.execute(sql,params)
        #retorna apenas uma lista
        line = cursor.fetchone()
        # para prcurar a categoria correspondente ao pk.
        categories = find_categories()
        #verifica se a lina está vazia, se sim o registro não existe
        if not line:
            raise Exception("Esse usuário não existe!")
        occurrence = {
            "cd_ocorrencia": line[0],
            "st_ocorrencia": line[1],
            "ds_protocolo": line[2],
            "ds_ocorrencia": line[3],
            "nm_categoria": categories.get(line[4]),
            "nm_bairro": line[5],
            "ds_endereco": line[6],
            "dt_abertura": line[7]
        }
        return occurrence
    except Exception as e:
        #mostra [ERRO] em bold vermelho + mensagem de erro
        console.print(ERROR,e)
    finally:
        #serve para garantir que o con nã́o é none
        if con:
            #fecha a conexão dando erro ou não
            con.close()
    return {}

# consulta apenas ocorrencias do cidadão 67 (padrão com dados registrados) no banco
def find_by_citizen(cd_cidadao:int=67) -> list[dict[str,Any]]:
    """Retorna todas as ocorrências da tabela do usuário padrão citizen"""
    con = None
    try:
        # pegar uma conexão com a função criada
        con = get_connection()
        cursor = con.cursor()
        # preparando sql
        sql = """
              SELECT cd_ocorrencia,st_ocorrencia,ds_protocolo,ds_ocorrencia,
                     cd_categoria,nm_bairro,ds_endereco,dt_abertura
              FROM OCORRENCIA WHERE cd_cidadao = :cd_cidadao
              """
        params = [cd_cidadao]
        # pegar todos os dados da tabela, passando o sql
        cursor.execute(sql, params)
        #retorna uma 'list of tuples' com os dados que eu quero
        lines = cursor.fetchall()
        occurrences = []
        # para prcurar a categoria correspondente ao pk.
        categories = find_categories()
        #guardar os valores de lines
        for line in lines:
            #guarda cada coluna em seu respectivo atributo num dicionário
            occurrence = {
                "cd_ocorrencia": line[0],
                "st_ocorrencia": line[1],
                "ds_protocolo": line[2],
                "ds_ocorrencia": line[3],
                "nm_categoria": categories.get(line[4]),
                "nm_bairro": line[5],
                "ds_endereco": line[6],
                "dt_abertura": line[7]
            }
            #guarda esse dicionário na lista
            occurrences.append(occurrence)
        return occurrences
    except Exception as e:
        #mostra [ERRO] em bold vermelho + mensagem de erro
        console.print(ERROR,e)
    finally:
        #serve para garantir que o con nã́o é none
        if con:
            #fecha a conexão dando erro ou não
            con.close()
    return []

#já pega um dicionário "desempacotando" ele
def save(st_ocorrencia:str,ds_protocolo:str,ds_ocorrencia,nm_bairro:str,nm_categoria:str,ds_endereco:str) -> bool:
    """Salva uma ocorrência no banco"""
    con = None
    try:
        # pegar uma conexão com a função criada
        con = get_connection()
        cursor = con.cursor()
        # prepara um sql de insert
        sql = """
        INSERT INTO OCORRENCIA(st_ocorrencia,ds_protocolo,ds_ocorrencia,cd_cidadao,
                               cd_categoria,nm_bairro,ds_endereco,dt_abertura)
        VALUES ('PENDENTE',:ds_protocolo,:ds_ocorrencia,67,
                :cd_categoria,:nm_bairro,:ds_endereco,current_date)
        """
        # para pegar a PK certa da categoria no banco, vai retornar uma tupla de pares
        categories = find_categories().items()
        cd_categoria = 0
        for cd,nm in categories:
            if nm == nm_categoria: cd_categoria = cd
        # passa os valores de parametros
        params = [ds_protocolo,
                  ds_ocorrencia,cd_categoria,nm_bairro,ds_endereco]
        #insere os dados na tabela passando o sql criado e os parametro
        cursor.execute(sql,params)
        # confirma as alterações
        con.commit()
        # printa que deu tudo certo, heuristica 1 de resposta
        console.print(INFO, "[green]inserido com sucesso![/green]")
        return True
    except Exception as e:
        #mostra [ERRO] em bold vermelho + mensagem de erro
        console.print(ERROR,e)
    finally:
        #serve para garantir que o con não é none
        if con:
            #fecha a conexão dando erro ou não
            con.close()
    return False

def update(cd_ocorrencia:str,st_ocorrencia:str,ds_protocolo:str,ds_ocorrencia,
           nm_bairro:str,nm_categoria:str,ds_endereco:str,dt_abertura:str) -> bool:
    """Retorna uma ocorrência pelo seu ID"""
    con = None
    try:
        # pegar uma conexão com a função criada
        con = get_connection()
        cursor = con.cursor()
        # prepara um sql de update
        sql = """
              UPDATE OCORRENCIA 
              SET cd_ocorrencia = :cd_ocorrencia,
                  st_ocorrencia = :st_ocorrencia,
                  ds_ocorrencia = :ds_ocorrencia,cd_categoria = :cd_categoria,
                  nm_bairro = :nm_bairro,ds_endereco = :ds_endereco
              WHERE ds_protocolo = :ds_protocolo
              """
        #procurar categoria certa
        categories = find_categories().items()
        cd_categoria = 0
        for cd,nm in categories:
            if nm == nm_categoria: cd_categoria = cd
        # passa os valores de parametros
        params = [cd_ocorrencia,st_ocorrencia,ds_ocorrencia,cd_categoria,nm_bairro,ds_endereco,ds_protocolo]
        #atualiza os dados na tabela passando o sql criado e os parametro
        cursor.execute(sql,params)
        # confirma as alterações
        con.commit()
        # printa que deu tudo certo, heuristica 1 de resposta
        console.print(INFO, f"[green]ocorrência {ds_protocolo} atualizada com sucesso![/green]")
        return True
    except Exception as e:
        #mostra [ERRO] em bold vermelho + mensagem de erro
        console.print(ERROR,e)
    finally:
        #serve para garantir que o con não é none
        if con:
            #fecha a conexão dando erro ou não
            con.close()
    return False

def delete(cd_ocorrencia: int) -> bool:
    """Retorna uma ocorrência pelo seu ID"""
    con = None
    try:
        # pegar uma conexão com a função criada
        con = get_connection()
        cursor = con.cursor()
        # prepara um sql de update
        sql = """
              DELETE FROM OCORRENCIA WHERE cd_ocorrencia = :cd_ocorrencia
              """
        # passa os valores de parametros
        params = [cd_ocorrencia]
        #atualiza os dados na tabela passando o sql criado e os parametro
        cursor.execute(sql,params)
        # confirma as alterações
        con.commit()
        # printa que deu tudo certo, heuristica 1 de resposta
        console.print(INFO, f"[green]ocorrência excluída com sucesso![/green]")
        return True
    except Exception as e:
        #mostra [ERRO] em bold vermelho + mensagem de erro
        console.print(ERROR,e)
    finally:
        #serve para garantir que o con não é none
        if con:
            #fecha a conexão dando erro ou não
            con.close()
    return False

# serve para o usuário ter as opções das categorias disponiveis e validacao tbm
# vai retornar a pk e o nome, a pk vai servir dps para trocar o nome por ela
def find_categories() -> dict[int,str]:
    """Retorna todas as categorias da tabela"""
    con = None
    try:
        # pegar uma conexão com a função criada
        con = get_connection()
        cursor = con.cursor()
        # preparando sql
        sql = """
              SELECT cd_categoria,nm_categoria FROM CATEGORIA
        """
        # pegar todos os dados da tabela, passando o sql
        cursor.execute(sql)
        #retorna uma 'list of tuples' com os dados que eu quero
        lines = cursor.fetchall()
        categories = {}
        for line in lines:
            #guarda cada linha como uma cahve e item no dict
            categories[line[0]] = line[1]
        console.print(INFO, f"[green]categorias encontradas com sucesso![/green]")
        return categories
    except Exception as e:
        #mostra [ERRO] em bold vermelho + mensagem de erro
        console.print(ERROR,e)
    finally:
        #serve para garantir que o con nã́o é none
        if con:
            #fecha a conexão dando erro ou não
            con.close()
    return {}