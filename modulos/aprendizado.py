"""Ferramentas de aprendizado simbólico."""

from __future__ import annotations

from pathlib import Path

from core.jarvucas_memoria import detectar_padrao_visao

SCRIPT_DIR = Path(__file__).resolve().parent
MINDBIT_DIR = (SCRIPT_DIR.parent / "core" / "mindbit").resolve()


def criar_bit(nome: str, conteudo: str) -> None:
    """Gera um novo arquivo .bit com o conteudo fornecido."""
    caminho = MINDBIT_DIR / f"{nome}.bit"
    caminho.write_text(conteudo, encoding="utf-8")


def analisar_visao() -> None:
    """Atualiza aprendizado a partir de visao.bit."""
    detectar_padrao_visao()
