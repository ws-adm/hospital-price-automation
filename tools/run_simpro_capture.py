# Execute este script para iniciar a captura do SIMPRO em background.
# Ele cria o processo detached e o loop salva automaticamente em tools/captures/.
# Para parar: type nul > tools/captures\STOP

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> None:
    log = open(ROOT / "loop_output.log", "w")
    subprocess.Popen(
        [sys.executable, str(ROOT / "capture_simpro_loop.py")],
        stdout=log,
        stderr=subprocess.STDOUT,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
    )
    print("Loop SIMPRO iniciado em background.")
    print("Navegue pelas telas do SIMPRO — cada tela nova será salva automaticamente.")
    print("Para parar: type nul > tools\\captures\\STOP")


if __name__ == "__main__":
    main()
