"""Despeja a árvore de controles da janela ativa (para mapear o SIMPRO).

Uso:
    python tools/dump_simpro_ui.py [uia|win32]

Fluxo:
    1. Abra o SIMPRO e navegue até a tela desejada.
    2. Neste terminal, pressione ENTER para capturar a janela ativa.
    3. Repita para cada tela do fluxo.
    4. Digite 'q' para sair e salvar o relatório.

A saída mostra, para cada controle: tipo, nome (texto visível) e
automation_id. Usamos esses identificadores para escrever os cliques
com pywinauto de forma estável (sem depender de coordenadas de tela).
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

from pywinauto import Desktop

CAPTURE_DIR = Path(__file__).resolve().parent / "captures"


def dump_window(backend: str = "uia") -> str:
    try:
        window = Desktop(backend=backend).foreground_window()
    except Exception as e:  # janela ativa inacessível
        return f"Erro ao obter janela ativa: {e}"

    lines = [
        f"=== {datetime.now():%Y-%m-%d %H:%M:%S} ===",
        f"Janela: {window.window_text()!r}",
        f"Classe: {window.element_info.class_name}",
        f"Processo PID: {window.process_id()}",
    ]

    def walk(element, depth: int = 0) -> None:
        for child in element.children():
            info = child.element_info
            automation_id = ""
            try:
                automation_id = child.automation_id or ""
            except Exception:
                automation_id = ""
            label = f"[{info.control_type}] name={info.name!r} id={automation_id!r}"
            lines.append("    " * depth + label)
            if depth < 6:
                walk(child, depth + 1)

    walk(window)
    return "\n".join(lines)


def main() -> None:
    backend = sys.argv[1] if len(sys.argv) > 1 else "uia"
    CAPTURE_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = CAPTURE_DIR / f"simpro_dump_{stamp}.txt"

    print(f"Backend: {backend}")
    print("Navegue pelas telas do SIMPRO e pressione ENTER para capturar a janela ativa.")
    print("Digite 'q' e ENTER para sair e salvar.\n")

    chunks: list[str] = []
    while True:
        cmd = input("ENTER = capturar | q = sair > ").strip().lower()
        if cmd == "q":
            break
        output = dump_window(backend)
        print(output)
        print("-" * 60)
        chunks.append(output)

    if chunks:
        path.write_text("\n\n".join(chunks), encoding="utf-8")
        print(f"\nCaptura salva em: {path}")


if __name__ == "__main__":
    main()
