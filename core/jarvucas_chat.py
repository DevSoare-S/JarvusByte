"""Interface de conversa por voz com a JarvucasIA."""

import os
from pathlib import Path

import pyttsx3
import speech_recognition as sr

from jarvucas_core import JarvucasIA
from jarvucas_memoria import (
    registrar_memoria,
    registrar_resposta,
    atualizar_contexto,
    detectar_padrao_visao,
)


# Corrige caminho para acessar as pastas de dados mesmo quando o script for
# executado a partir de diretórios diferentes

script_dir = os.path.dirname(__file__)
base_dir = os.path.abspath(os.path.join(script_dir, "..", "mindzip"))
env_mindbit = os.getenv("JARVUS_MINDBIT")
mindbit_dir = (
    os.path.abspath(env_mindbit)
    if env_mindbit
    else os.path.abspath(os.path.join(script_dir, "..", "mindbit"))
)

ia = JarvucasIA(base_path=base_dir, mindbit_path=mindbit_dir)
mindbit_dir = ia.get_mindbit_path()

# Inicia ferramentas de voz
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()


def carregar_palavras(nome: str) -> list[str]:
    """Carrega palavras de apoio a partir de arquivos .bit."""
    caminho = Path(mindbit_dir) / f"{nome}.bit"
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
                palavras.append(palavra.strip().lower())
    return palavras


def interpretar_frase(frase: str) -> dict[str, str]:
    """Separa a frase em verbo, sujeito e intencao."""
    tokens = frase.lower().replace("?", "").split()

    verbos = carregar_palavras("100_verbo")
    sujeitos = carregar_palavras("101_sujeito")

    verbo = next((v for v in verbos if v in tokens), "")
    sujeito = next((s for s in sujeitos if s in tokens), "")
    intencao = "consulta" if frase.strip().endswith("?") else "fala"

    return {"verbo": verbo, "sujeito": sujeito, "intencao": intencao, "frase": frase}


def consultar_ambiente(sujeito: str) -> str:
    """Verifica o visao.bit para encontrar a posicao do sujeito."""
    visao_path = Path(mindbit_dir) / "visao.bit"
    if not visao_path.exists() or not sujeito:
        return ""

    encontrados: list[str] = []
    with visao_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            nome, coords = line.split(":", 1)
            if sujeito in nome:
                encontrados.append(f"{nome} em {coords}")

    return ", ".join(encontrados)


def gerar_resposta(analise: dict[str, str]) -> str:
    """Gera uma resposta simbolica com base na analise da frase."""
    if analise.get("intencao") == "consulta" and analise.get("sujeito"):
        info = consultar_ambiente(analise["sujeito"])
        if info:
            return f"Detectei {info}."
        return f"Não detectei nenhum {analise['sujeito']} por enquanto."

    return ia.conversar(analise.get("frase", ""))


def falar(texto: str) -> None:
    """Fala um texto usando pyttsx3."""
    tts_engine.say(texto)
    tts_engine.runAndWait()


def ouvir() -> str | None:
    """Captura a fala do usuário e a transcreve."""
    with sr.Microphone() as source:
        print("🎤 Ouvindo...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        frase = recognizer.recognize_google(audio, language="pt-BR")
        print(f"Você: {frase}")
        return frase
    except sr.UnknownValueError:
        # Falha na compreensão da fala
        return None
    except sr.RequestError as e:
        print(f"Erro no reconhecimento de fala: {e}")
        return None


def interpretar(frase: str | None) -> str | None:
    """Analisa a frase e produz uma resposta inteligente."""
    if not frase:
        return None

    analise = interpretar_frase(frase)
    registrar_memoria(analise)
    resposta = gerar_resposta(analise)
    registrar_resposta(frase, resposta)
    atualizar_contexto(analise)
    detectar_padrao_visao()
    return resposta


def responder(resposta: str | None) -> None:
    """Fala e imprime a resposta para o usuário."""
    if resposta:
        print("JarvucasIA:", resposta)
        falar(resposta)
    else:
        mensagem = "Não entendi o que você quis dizer."
        print("JarvucasIA:", mensagem)
        falar(mensagem)


def loop_conversa() -> None:
    """Executa o loop contínuo de interação por voz."""
    print("🧠 JarvucasIA iniciada! Diga 'sair' para encerrar.\n")
    while True:
        frase = ouvir()

        if frase and frase.lower() in ["sair", "exit", "quit"]:
            print("JarvucasIA: Até logo!")
            falar("Até logo!")
            break

        resposta = interpretar(frase)
        responder(resposta)


if __name__ == "__main__":
    tecla = input("Pressione K para ativar voz ou ENTER para sair: ").strip().lower()
    if tecla == "k":
        loop_conversa()
