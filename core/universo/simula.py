"""Pequena simulacao para testes simbolicos."""

from __future__ import annotations

import random


ESTADO = {
    'pontuacao': 0,
}


def executar_simulacao(passos: int = 5) -> None:
    """Executa uma simulacao simples de ganhopontos."""
    for _ in range(passos):
        ganho = random.randint(1, 10)
        ESTADO['pontuacao'] += ganho
    print(f"[Simulacao] Pontuacao total: {ESTADO['pontuacao']}")

