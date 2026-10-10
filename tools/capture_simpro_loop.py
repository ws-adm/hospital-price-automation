"""Loop de captura automática da janela ativa do SIMPRO.

A cada 3s captura a árvore de controles da janela ativa
(pywinauto, backend uia com fallback win32) e salva em
tools/captures/ quando o conteúdo muda.

Para parar: crie o arquivo tools/captures/STOP
    type nul > tools/captures/STOP

Uso:
    python tools/capture_simpro_loop.py
"""

from __future__ import annotations

import hashlib
import time
from datetime import datetime
from pathlib import Path

from pywinauto import Desktop

CAPTURE_DIR = Path(__file__).resolve().parent / "captures"
STOP_FILE = CAPTURE_DIR / "STOP"
INTERVAL = 3


def dump_window(backend: str = "uia") -> str:
    window = Desktop(backend=backend).foreground_window()
    lines = [
        f"[{datetime.now():%Y-%m-%d %H:%M:%S}] janela={window.window_text()!r}",
        f"    classe={window.element_info.class_name}",
    ]

    def walk(element, depth: int = 0) -> None:
        for child in element.children():
            info = child.element_info
            try:
                automation_id = child.automation_id or ""
            except Exception:
                automation_id = ""
            lines.append("    " * depth + f"[{info.control_type}] name={info.name!r} id={automation_id!r}")
            if depth < 6:
                walk(child, depth + 1)

    walk(window)
    return "\n".join(lines)


def safe_dump() -> str:
    try:
        return dump_window("uia")
    except Exception:
        try:
            return dump_window("win32")
        except Exception as e:
            return f"ERRO: {e}"


def main() -> None:
    CAPTURE_DIR.mkdir(parents=True, exist_ok=True)
    print("Loop SIMPRO iniciado. Navegue pelas telas; a captura e automatica.")
    print("Para parar, crie o arquivo tools/captures/STOP", flush=True)

    last_hash = ""
    count = 0
    while not STOP_FILE.exists():
        output = safe_dump()
        digest = hashlib.md5(output.encode("utf-8")).hexdigest()
        if digest != last_hash:
            last_hash = digest
            count += 1
            path = CAPTURE_DIR / f"simpro_{datetime.now():%Y%m%d_%H%M%S}.txt"
            path.write_text(output, encoding="utf-8")
            print(f"capturado: {path.name}", flush=True)
        time.sleep(INTERVAL)

    print(f"Loop encerrado. {count} quadros salvos.", flush=True)


if __name__ == "__main__":
    main()
