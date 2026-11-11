import json
import oracledb
import os

from json import JSONDecodeError
from config import ERROR, WARN
from rich.console import Console
from dotenv import load_dotenv
from config import ERROR

console = Console()
load_dotenv()

def get_connection():
    """Tenta conectar ao banco de dados Oracle"""
    USER = os.getenv("ORACLE_USER")
    PASSWORD = os.getenv("ORACLE_PASSWORD")
    DSN = os.getenv("ORACLE_DSN")
    try:
        connection = oracledb.connect(user=USER, password=PASSWORD, dsn=DSN)
        return connection
    except Exception as e:
        console.print(f"{ERROR} Problema na Conexão Oracle.\n{e}")
        return
