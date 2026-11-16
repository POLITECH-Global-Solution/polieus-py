import oracledb
import os

from rich.console import Console
from dotenv import load_dotenv
from typing_extensions import Any

from config import ERROR, INFO

console = Console()
load_dotenv()

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

def find_all() -> list[dict[str, Any]] | None:
    """Retorna todas as ocorrências da tabela"""
    con = None
    try:
        # pegar uma conexão com a função criada
        con = get_connection()
        cursor = con.cursor()
        # preparando sql
        sql = """
              SELECT * FROM OCORRENCIA
        """
        # pegar todos os dados da tabela, passando o sql
        cursor.execute(sql)
        #retorna uma 'list of tuples' com os dados que eu quero
        lines = cursor.fetchall()
        demands = []
        #guardar os valores de lines
        for line in lines:
            #guarda cada coluna em seu respectivo atributo num dicionário
            demand = {
                "atr1": line[0],
                "atr2": line[1]
            }
            #guarda esse dicionário na lista
            demands.append(demand)
        return demands
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
              SELECT * FROM OCORRENCIA WHERE id = :id
        """
        params = [id]
        # pegar todos os dados da tabela passando o sql e os parametro
        cursor.execute(sql,params)
        #retorna apenas uma lista
        line = cursor.fetchone()
        #verifica se a lina está vazia, se sim o registro não existe
        if not line:
            raise Exception("Esse ID não existe!")
        demand = {
            "atr1": line[0],
            "atr2": line[1]
        }
        return demand
    except Exception as e:
        #mostra [ERRO] em bold vermelho + mensagem de erro
        console.print(ERROR,e)
    finally:
        #serve para garantir que o con nã́o é none
        if con:
            #fecha a conexão dando erro ou não
            con.close()
    return {}

#já pega um dicionário "desempacotando" ele
def save(atr1:str, atr2:str) -> bool:
    """Salva uma ocorrência no banco"""
    """Retorna uma ocorrência pelo seu ID"""
    con = None
    try:
        # pegar uma conexão com a função criada
        con = get_connection()
        cursor = con.cursor()
        # prepara um sql de insert
        sql = """
        INSERT INTO OCORRENCIA(atr1, atr2)
        VALUES (:atr1, :atr2)
        """
        # passa os valores d eparametros
        params = [atr1, atr2]
        #insere os dados na tabela passando o sql criado e os parametro
        cursor.execute(sql,params)
        # confirma as alterações
        con.commit()
        # printa que deu tudo certo, heuristica 1 de resposta
        console.print(INFO, "inserido com sucesso!")
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

def update(id: int, atr1:str, atr2:str) -> bool:
    """Retorna uma ocorrência pelo seu ID"""
    con = None
    try:
        # pegar uma conexão com a função criada
        con = get_connection()
        cursor = con.cursor()
        # prepara um sql de update
        sql = """
              UPDATE OCORRENCIA
              SET atr1 = :atr1, atr2 = :atr2
              WHERE id = :id
              """
        # passa os valores de parametros
        params = [atr1, atr2, id]
        #atualiza os dados na tabela passando o sql criado e os parametro
        cursor.execute(sql,params)
        # confirma as alterações
        con.commit()
        # printa que deu tudo certo, heuristica 1 de resposta
        console.print(INFO, f"demanda {id} atualizada com sucesso!")
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

def delete(id: int) -> bool:
    """Retorna uma ocorrência pelo seu ID"""
    con = None
    try:
        # pegar uma conexão com a função criada
        con = get_connection()
        cursor = con.cursor()
        # prepara um sql de update
        sql = """
              DELETE FROM OCORRENCIA WHERE id = :id
              """
        # passa os valores de parametros
        params = [id]
        #atualiza os dados na tabela passando o sql criado e os parametro
        cursor.execute(sql,params)
        # confirma as alterações
        con.commit()
        # printa que deu tudo certo, heuristica 1 de resposta
        console.print(INFO, f"demanda {id} excluída com sucesso!")
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
def find_categories() -> tuple[dict[int,str]]:
    """Retorna todas as categorias da tabela"""
    con = None
    try:
        # pegar uma conexão com a função criada
        con = get_connection()
        cursor = con.cursor()
        # preparando sql
        sql = """
              SELECT nm_categoria,cd_categoria FROM CATEGORIA
        """
        # pegar todos os dados da tabela, passando o sql
        cursor.execute(sql)
        #retorna uma 'list of tuples' com os dados que eu quero
        lines = cursor.fetchall()
        categories = []
        #guardar os valores de lines
        for line in lines:
            #guarda cada coluna em seu respectivo atributo num dicionário
            category = {
                "nm_categoria": line[0],
                "cd_categoria": line[1]
            }
            #guarda esse dicionário na lista
            categories.append(category)
        return categories
    except Exception as e:
        #mostra [ERRO] em bold vermelho + mensagem de erro
        console.print(ERROR,e)
    finally:
        #serve para garantir que o con nã́o é none
        if con:
            #fecha a conexão dando erro ou não
            con.close()
    return []