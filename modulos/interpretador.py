"""Modulos de interpretacao simbolica para JarvucasIA."""

from __future__ import annotations

from pathlib import Path

from modulos.fala import falar

SCRIPT_DIR = Path(__file__).resolve().parent
MINDBIT_DIR = (SCRIPT_DIR.parent / "core" / "mindbit").resolve()


def _append_to_bit(path: Path, line: str) -> None:
    """Adiciona uma linha a um arquivo .bit criando diretorios se necessario."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def carregar_palavras(nome: str) -> list[str]:
    """Carrega palavras de um arquivo .bit para suporte ao parser."""
    caminho = MINDBIT_DIR / f"{nome}.bit"
    palavras: list[str] = []
    if caminho.exists():
        with caminho.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if ":" in line:
                    _, palavra = line.split(":", 1)
                else:
                    palavra = line
                palavras.append(palavra.lower())
    return palavras


def autoaprender(token: str) -> None:
    """Solicita ao usuario a classificacao de uma palavra desconhecida."""
    falar(f"O que significa '{token}'? É verbo ou sujeito?")
    classificacao = input(f"Classificação para '{token}' (verbo/sujeito): ").strip().lower()
    if classificacao.startswith("v"):
        categoria = input(f"Categoria para o verbo '{token}': ").strip().lower()
        _append_to_bit(MINDBIT_DIR / "100_verbo.bit", f"{token}:{categoria}")
    else:
        _append_to_bit(MINDBIT_DIR / "101_sujeito.bit", token)
    falar("Entendido, obrigado!")


def interpretar_frase(frase: str) -> dict[str, str]:
    """Analisa a frase separando verbo, sujeito e intencao."""
    tokens = frase.lower().replace("?", "").split()

    verbos = carregar_palavras("100_verbo")
    sujeitos = carregar_palavras("101_sujeito")

    verbo = next((v for v in verbos if v in tokens), "")
    if not verbo:
        for t in tokens:
            if t not in sujeitos:
                autoaprender(t)
                verbos = carregar_palavras("100_verbo")
                verbo = next((v for v in verbos if v in tokens), "")
                break

    sujeito = next((s for s in sujeitos if s in tokens), "")
    if not sujeito:
        for t in tokens:
            if t not in verbos:
                autoaprender(t)
                sujeitos = carregar_palavras("101_sujeito")
                sujeito = next((s for s in sujeitos if s in tokens), "")
                break

    intencao = "consulta" if frase.strip().endswith("?") else "fala"
    return {"verbo": verbo, "sujeito": sujeito, "intencao": intencao, "frase": frase}


def identificar_estrutura(frase: str) -> tuple[str, str, str]:
    """Interface simplificada para obter verbo, sujeito e intencao."""
    res = interpretar_frase(frase)
    return res["verbo"], res["sujeito"], res["intencao"]
