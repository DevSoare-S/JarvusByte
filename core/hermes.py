"""HERMES intermedia a comunicacao entre subsistemas."""

from __future__ import annotations


def enviar_mensagem(destino: str, conteudo: str) -> None:
    """Faz log simples de mensagens trocadas."""
    print(f"[HERMES] -> {destino}: {conteudo}")

