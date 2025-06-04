"""Loop principal integrando voz, visao e memoria da JarvucasIA."""

from __future__ import annotations

from pathlib import Path
import os

from core.jarvucas_core import JarvucasIA
from core.gaia import GAIA
from modulos.fala import falar, ouvir, entrada_hibrida
from modulos.interpretador import interpretar_frase
from modulos.visao import consultar_visao
from modulos.memoria import (
    registrar_memoria,
    registrar_resposta,
    atualizar_contexto,
    detectar_padrao_visao,
    registrar_reflexao,
    planejar_acao,
)

# Diretórios base relativos a este arquivo
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = (SCRIPT_DIR / "mindzip").resolve()
env_mindbit = os.getenv("JARVUS_MINDBIT")
MINDBIT_DIR = (
    Path(env_mindbit).resolve()
    if env_mindbit
    else (SCRIPT_DIR / "mindbit").resolve()
)

# Instancia a IA com os caminhos corretos para .bin e .bit
ia = JarvucasIA(base_path=str(BASE_DIR), mindbit_path=str(MINDBIT_DIR))
MINDBIT_DIR = Path(ia.get_mindbit_path())
gaia = GAIA()



def gerar_resposta(analise: dict[str, str]) -> str:
    """Gera a resposta simbolica apropriada."""
    if analise.get("intencao") == "consulta" and analise.get("sujeito"):
        info = consultar_visao(analise["sujeito"])
        if info:
            return f"Detectei {info}."
        return f"Não detectei nenhum {analise['sujeito']} por enquanto."

    return ia.conversar(analise.get("frase", ""))


def responder_logicamente(analise: dict[str, str]) -> str:
    """Envolve a geracao de resposta com planejamento simbolico."""
    resposta = gerar_resposta(analise)
    plano = planejar_acao()
    if plano:
        resposta = f"{resposta} Ação sugerida: {plano}."
    return resposta


def interpretar(frase: str | None) -> str | None:
    """Executa o ciclo completo de interpretacao e registro."""
    if not frase:
        return None

    analise = interpretar_frase(frase)
    registrar_memoria(analise)
    atualizar_contexto(analise)
    detectar_padrao_visao()
    resposta = responder_logicamente(analise)
    registrar_resposta(frase, resposta)
    return resposta


def responder(resposta: str | None) -> None:
    """Imprime e fala a resposta."""
    if resposta:
        print("JarvucasIA:", resposta)
        falar(resposta)
    else:
        mensagem = "Não entendi o que você quis dizer."
        print("JarvucasIA:", mensagem)
        falar(mensagem)


def loop_inteligente() -> None:
    """Loop continuo integrando voz, visao e memoria."""
    print("🧠 JarvucasIA pronta! Diga 'sair' para encerrar.\n")
    while True:
        frase = entrada_hibrida()

        if frase and frase.lower() in {"sair", "exit", "quit"}:
            falar("Até logo!")
            break

        resposta = interpretar(frase)
        responder(resposta)
        gaia.executar_ciclo()
        if resposta:
            falar("Isso te ajudou?")
            feedback = ouvir()
            if feedback and feedback.lower().startswith(("nao", "não", "n")):
                registrar_reflexao(frase or "", feedback)


if __name__ == "__main__":
    loop_inteligente()
