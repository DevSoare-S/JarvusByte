"""Registro simbólico de interações e observações da JarvucasIA."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

# Diretórios base calculados a partir deste arquivo para independência do local de execução
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = (SCRIPT_DIR.parent / "mindzip").resolve()
MINDBIT_DIR = (SCRIPT_DIR / "mindbit").resolve()
VISAO_FILE = MINDBIT_DIR / "visao.bit"

MEMORIA_FILE = BASE_DIR / "memoria.bin"
RESPOSTAS_FILE = BASE_DIR / "respostas.bin"
APRENDIZADO_FILE = BASE_DIR / "aprendizado.bin"
CONTEXTO_FILE = BASE_DIR / "contexto.bin"
REFLEXOES_FILE = BASE_DIR / "reflexoes.bin"
PLANEJAMENTO_FILE = MINDBIT_DIR / "planejamento.bit"


def _append_line(path: Path, line: str) -> None:
    """Acrescenta uma linha a um arquivo criando-o se necessário."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def registrar_memoria(interpretacao: Dict[str, str]) -> None:
    """Registra simbolicamente a interpretação de uma frase."""
    linha = (
        f"verbo:{interpretacao.get('verbo', '')}; "
        f"sujeito:{interpretacao.get('sujeito', '')}; "
        f"intencao:{interpretacao.get('intencao', '')}"
    )
    _append_line(MEMORIA_FILE, linha)


def registrar_resposta(frase: str, resposta: str) -> None:
    """Salva a associação pergunta-resposta de forma simbólica."""
    linha = f"pergunta:{frase} => resposta:{resposta}"
    _append_line(RESPOSTAS_FILE, linha)


def _carregar_aprendizado() -> Dict[str, Dict[str, int]]:
    """Carrega o estado de aprendizado para atualizações posteriores."""
    dados: Dict[str, Dict[str, int]] = {}
    if APRENDIZADO_FILE.exists():
        with APRENDIZADO_FILE.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or "->" not in line:
                    continue
                nome, resto = line.split("->", 1)
                nome = nome.strip()
                if "x=" in resto and ".." in resto:
                    faixa = resto.split("x=")[1]
                    min_x, max_x = faixa.split("..")
                    dados[nome] = {
                        "min_x": int(min_x),
                        "max_x": int(max_x),
                    }
    return dados


def detectar_padrao_visao() -> None:
    """Analisa visao.bit e atualiza ranges recorrentes em aprendizado.bin."""
    registros: Dict[str, list[int]] = {}
    if VISAO_FILE.exists():
        with VISAO_FILE.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or ":" not in line or "," not in line:
                    continue
                nome, coords = line.split(":", 1)
                if coords.startswith("x="):
                    x_str, _ = coords[2:].split(",", 1)
                    registros.setdefault(nome, []).append(int(x_str))

    if not registros:
        return

    padroes = _carregar_aprendizado()
    for nome, xs in registros.items():
        min_x = min(xs)
        max_x = max(xs)
        if nome in padroes:
            padroes[nome]["min_x"] = min(padroes[nome]["min_x"], min_x)
            padroes[nome]["max_x"] = max(padroes[nome]["max_x"], max_x)
        else:
            padroes[nome] = {"min_x": min_x, "max_x": max_x}

    with APRENDIZADO_FILE.open("w", encoding="utf-8") as f:
        for nome, info in padroes.items():
            f.write(f"{nome} -> sempre na área x={info['min_x']}..{info['max_x']}\n")


def _carregar_contexto() -> Dict[str, str]:
    ctx: Dict[str, str] = {}
    if CONTEXTO_FILE.exists():
        with CONTEXTO_FILE.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or ":" not in line:
                    continue
                chave, valor = line.split(":", 1)
                ctx[chave] = valor
    return ctx


def atualizar_contexto(interpretacao: Dict[str, str]) -> None:
    """Atualiza o contexto simbólico com informações recentes."""
    ctx = _carregar_contexto()

    if interpretacao.get("verbo"):
        ctx["ultima_acao"] = interpretacao["verbo"]
    if interpretacao.get("sujeito"):
        ctx["alvo_atual"] = interpretacao["sujeito"]

    if VISAO_FILE.exists():
        with VISAO_FILE.open("r", encoding="utf-8") as f:
            linhas = [l.strip() for l in f if l.strip()]
        if linhas:
            ultimo, _ = linhas[-1].split(":", 1)
            ctx["ultimo_mob"] = ultimo

    with CONTEXTO_FILE.open("w", encoding="utf-8") as f:
        for k, v in ctx.items():
            f.write(f"{k}:{v}\n")


def registrar_reflexao(frase: str, feedback: str) -> None:
    """Guarda o feedback do usuario sobre uma resposta."""
    linha = f"pergunta:{frase} -> feedback:{feedback}"
    _append_line(REFLEXOES_FILE, linha)


def _carregar_regras_planejamento() -> Dict[str, str]:
    """Carrega regras do arquivo planejamento.bit."""
    regras: Dict[str, str] = {}
    if PLANEJAMENTO_FILE.exists():
        with PLANEJAMENTO_FILE.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "->" in line:
                    cond, acao = line.split("->", 1)
                    regras[cond.strip()] = acao.strip()
    return regras


def planejar_acao() -> str:
    """Define uma acao com base no contexto e nas regras."""
    contexto = _carregar_contexto()
    regras = _carregar_regras_planejamento()
    for cond, acao in regras.items():
        termos = [t.strip() for t in cond.replace("&", "+").split("+")]
        if all(t in contexto.values() or contexto.get(t) for t in termos):
            return acao
    return ""
