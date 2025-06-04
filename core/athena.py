"""ATHENA executa logica e simulacoes internas."""

from __future__ import annotations

from .universo.simula import executar_simulacao


def executar_simulacoes() -> None:
    """Executa simulacoes simples para evoluir a IA."""
    executar_simulacao()

