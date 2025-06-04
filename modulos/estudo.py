"""Modulo de estudo autonomo para JarvucasIA."""

from __future__ import annotations

import time
from pathlib import Path

from .web_learning import (
    buscar_conhecimento_web,
    converter_texto_em_simbolos,
    registrar_conhecimento,
)

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = (SCRIPT_DIR.parent / "mindzip").resolve()
EVOLUCAO_FILE = BASE_DIR / "evolucao.log"


def registrar_evolucao(porcentagem: float, area: str) -> None:
    """Registra o progresso de aprendizado."""
    EVOLUCAO_FILE.parent.mkdir(parents=True, exist_ok=True)
    with EVOLUCAO_FILE.open("a", encoding="utf-8") as f:
        f.write(f"{time.time()}|{area}|{porcentagem}\n")


def estudar_tema(titulo: str) -> None:
    """Pesquisa o tema e converte em conhecimento simbolico."""
    texto = buscar_conhecimento_web(titulo)
    simbolos = converter_texto_em_simbolos(texto)
    registrar_conhecimento(titulo, simbolos)
    progresso = len(simbolos) / 100.0
    registrar_evolucao(progresso, titulo)
