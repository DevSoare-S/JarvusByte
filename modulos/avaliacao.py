"""Modulo de autoavaliacao simbolica."""

from __future__ import annotations

import json
import random
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
env_mindbit = os.getenv("JARVUS_MINDBIT")
MINDBIT_DIR = Path(env_mindbit).resolve() if env_mindbit else (SCRIPT_DIR.parent / "core" / "mindbit").resolve()
BASE_DIR = (SCRIPT_DIR.parent / "mindzip").resolve()
AVALIACAO_FILE = BASE_DIR / "autoavaliacao.bin"


def gerar_pergunta_simbolica(tema: str) -> str:
    """Retorna uma linha aleatoria do arquivo de tema."""
    path = MINDBIT_DIR / f"{tema}.bit"
    if not path.exists():
        return ""
    linhas = [l.strip() for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    return random.choice(linhas) if linhas else ""


def comparar_com_resposta(pergunta: str, resposta: str) -> bool:
    """Compara de forma simples a resposta dada."""
    return pergunta.lower() in resposta.lower()


def registrar_autoavaliacao(pergunta: str, resposta: str, correta: bool) -> None:
    """Guarda o resultado da autoavaliacao."""
    AVALIACAO_FILE.parent.mkdir(parents=True, exist_ok=True)
    with AVALIACAO_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"pergunta": pergunta, "resposta": resposta, "correta": correta}) + "\n")
