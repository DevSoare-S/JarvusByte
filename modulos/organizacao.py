"""Organiza e refatora arquivos .bit e .bin."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
env_mindbit = os.getenv("JARVUS_MINDBIT")
MINDBIT_DIR = Path(env_mindbit).resolve() if env_mindbit else (SCRIPT_DIR.parent / "core" / "mindbit").resolve()
OBSOLETOS_DIR = MINDBIT_DIR / "obsoletos"


def organizar_conhecimento() -> None:
    """Remove duplicatas e move arquivos vazios para obsoletos."""
    OBSOLETOS_DIR.mkdir(parents=True, exist_ok=True)
    for path in MINDBIT_DIR.glob("*.bit"):
        linhas = []
        vistos = set()
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line in vistos:
                    continue
                vistos.add(line)
                linhas.append(line)
        if not linhas:
            shutil.move(str(path), str(OBSOLETOS_DIR / path.name))
        else:
            with path.open("w", encoding="utf-8") as f:
                for l in linhas:
                    f.write(l + "\n")
