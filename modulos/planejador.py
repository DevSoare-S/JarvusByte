"""Modulo de planejamento simbolico."""

from __future__ import annotations

from core.jarvucas_memoria import planejar_acao


def planejar() -> str:
    """Obtém uma acao planejada a partir do contexto atual."""
    return planejar_acao()
