"""Modulo de consulta da visao simbolica."""

from __future__ import annotations


import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
env_mindbit = os.getenv("JARVUS_MINDBIT")
MINDBIT_DIR = (
    Path(env_mindbit).resolve()
    if env_mindbit
    else (SCRIPT_DIR.parent / "mindbit").resolve()
)

VISAO_FILE = MINDBIT_DIR / "visao.bit"


def consultar_visao(sujeito: str) -> str:
    """Procura informacoes do sujeito no arquivo visao.bit."""
    if not VISAO_FILE.exists() or not sujeito:
        return ""

    encontrados: list[str] = []
    with VISAO_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            nome, coords = line.split(":", 1)
            if sujeito in nome:
                encontrados.append(f"{nome} em {coords}")

    return ", ".join(encontrados)
