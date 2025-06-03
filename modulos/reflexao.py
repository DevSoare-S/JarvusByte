"""Modulo de reflexao simbolica da JarvucasIA."""

from __future__ import annotations

from core.jarvucas_memoria import registrar_reflexao


def refletir(pergunta: str, feedback: str) -> None:
    """Registra o feedback do usuario sobre a resposta dada."""
    registrar_reflexao(pergunta, feedback)
