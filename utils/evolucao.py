"""Ferramentas para calcular a evolucao da IA."""

from __future__ import annotations

from pathlib import Path
from collections import defaultdict


EVOLUCAO_LOG = Path(__file__).resolve().parent.parent / 'mindzip' / 'evolucao.log'


def progresso_por_area() -> dict[str, float]:
    """Retorna o progresso total acumulado por area."""
    resultados: dict[str, float] = defaultdict(float)
    if EVOLUCAO_LOG.exists():
        with EVOLUCAO_LOG.open('r', encoding='utf-8') as f:
            for line in f:
                partes = line.strip().split('|')
                if len(partes) == 3:
                    _, area, pct = partes
                    try:
                        resultados[area] += float(pct)
                    except ValueError:
                        continue
    return dict(resultados)

