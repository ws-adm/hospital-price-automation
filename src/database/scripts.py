"""Execução das stored procedures SQL Server já existentes.

Uma stored procedure para a Brasíndice e outra para o SIMPRO.
Os nomes das procedures devem ser configurados em config/settings.json.
"""

from __future__ import annotations

import json
from pathlib import Path

from .connection import get_connection

CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "settings.json"


def _load_settings() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def run_stored_procedure(revista: str) -> None:
    settings = _load_settings()
    procedure = settings["database"]["stored_procedures"][revista]
    if not procedure:
        raise ValueError(f"Stored procedure não configurada para {revista}")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"EXEC {procedure}")
        conn.commit()
