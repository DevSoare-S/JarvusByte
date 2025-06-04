"""Funcoes de voz para JarvucasIA."""

from __future__ import annotations

import speech_recognition as sr
import pyttsx3

# Indica se o modo de voz esta ativo ou nao
VOICE_ACTIVE = False


def ativar_voz() -> None:
    """Ativa o modo de captura por voz."""
    global VOICE_ACTIVE
    VOICE_ACTIVE = True


def desativar_voz() -> None:
    """Desativa o modo de captura por voz."""
    global VOICE_ACTIVE
    VOICE_ACTIVE = False

recognizer = sr.Recognizer()
_tts_engine = pyttsx3.init()


def falar(texto: str) -> None:
    """Pronuncia um texto com pyttsx3."""
    _tts_engine.say(texto)
    _tts_engine.runAndWait()


def ouvir() -> str | None:
    """Escuta uma frase do usuario pelo microfone."""
    with sr.Microphone() as source:
        print("🎤 Ouvindo...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        frase = recognizer.recognize_google(audio, language="pt-BR")
        print(f"Você: {frase}")
        return frase
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"Erro no reconhecimento de fala: {e}")
        return None


def esperar_ativacao(palavra: str = "jarvucas") -> None:
    """Aguarda a palavra de ativacao antes de ouvir comandos."""
    while True:
        frase = ouvir()
        if frase and palavra.lower() in frase.lower():
            falar("Sim?")
            return


def entrada_hibrida(ativador: str = "jarvucas") -> str | None:
    """Recebe entrada textual e opcionalmente voz se ativado."""
    texto = input("Você: ").strip()
    if texto:
        if texto.lower() == "k":
            ativar_voz()
            print("[voz ativada]")
            return None
        return texto
    if not VOICE_ACTIVE:
        return None
    esperar_ativacao(ativador)
    return ouvir()
