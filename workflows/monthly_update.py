"""Orquestrador do fluxo mensal de atualização de preços.

Executa, em sequência:
1. Geração do arquivo Brasíndice
2. Geração do arquivo SIMPRO
3. Execução das stored procedures SQL Server

Esta etapa inicial contém apenas o esqueleto do fluxo.
"""

from src.brasicinde.automation import gerar_arquivo_brasicinde
from src.database.scripts import run_stored_procedure
from src.simpro.automation import gerar_arquivo_simpro
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


def main() -> None:
    logger.info("Iniciando atualização mensal de preços")

    arquivo_brasicinde = gerar_arquivo_brasicinde()
    logger.info("Brasíndice gerado: %s", arquivo_brasicinde)

    arquivo_simpro = gerar_arquivo_simpro()
    logger.info("SIMPRO gerado: %s", arquivo_simpro)

    run_stored_procedure("brasicinde")
    run_stored_procedure("simpro")

    logger.info("Atualização mensal concluída")


if __name__ == "__main__":
    main()
