"""Conexão com SQL Server usando pyodbc.

As credenciais são carregadas a partir das variáveis de ambiente (.env).
Nunca armazene senhas diretamente no código.
"""

from __future__ import annotations

import os
from contextlib import contextmanager

import pyodbc
from dotenv import load_dotenv

load_dotenv()


def _connection_string() -> str:
    return (
        f"DRIVER={os.getenv('SQL_SERVER_DRIVER', '{ODBC Driver 17 for SQL Server}')};"
        f"SERVER={os.getenv('SQL_SERVER_HOST', 'localhost')},"
        f"{os.getenv('SQL_SERVER_PORT', '1433')};"
        f"DATABASE={os.getenv('SQL_SERVER_DATABASE', '')};"
        f"UID={os.getenv('SQL_SERVER_USERNAME', '')};"
        f"PWD={os.getenv('SQL_SERVER_PASSWORD', '')};"
    )


@contextmanager
def get_connection():
    conn = pyodbc.connect(_connection_string())
    try:
        yield conn
    finally:
        conn.close()
