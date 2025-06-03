"""Funcoes de voz para JarvucasIA."""

from __future__ import annotations

import speech_recognition as sr
import pyttsx3

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
    """Recebe entrada textual ou por voz apos a palavra de ativacao."""
    texto = input("Você: ").strip()
    if texto:
        return texto
    esperar_ativacao(ativador)
    return ouvir()
