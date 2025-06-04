"""Aprendizado autonomo de conhecimento via navegador."""

from __future__ import annotations

import time
import os
from pathlib import Path
from typing import List

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from modulos.interpretador import interpretar_frase

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = (SCRIPT_DIR.parent / "mindzip").resolve()
env_mindbit = os.getenv("JARVUS_MINDBIT")
MINDBIT_DIR = (
    Path(env_mindbit).resolve()
    if env_mindbit
    else (SCRIPT_DIR.parent / "mindbit").resolve()
)


def buscar_conhecimento_web(topico: str) -> str:
    """Pesquisa o topico no Google e retorna o texto das primeiras paginas."""
    opts = Options()
    opts.add_argument("--headless")
    driver = webdriver.Chrome(options=opts)
    try:
        driver.get(f"https://www.google.com/search?q={topico}")
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        textos = " ".join(p.get_text(" ", strip=True) for p in soup.select("p"))
        return textos
    finally:
        driver.quit()


def converter_texto_em_simbolos(texto: str) -> List[str]:
    """Converte frases de texto em simbolos simples verbo->sujeito."""
    simbolos: List[str] = []
    for frase in texto.split("."):
        frase = frase.strip()
        if not frase:
            continue
        analise = interpretar_frase(frase)
        verbo = analise.get("verbo")
        sujeito = analise.get("sujeito")
        if verbo and sujeito:
            simbolos.append(f"{verbo}->{sujeito}")
    return simbolos


def registrar_conhecimento(tema: str, simbolos: List[str]) -> None:
    """Salva simbolos aprendidos em um arquivo .bit por tema."""
    path = MINDBIT_DIR / f"web_{tema}.bit"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for s in simbolos:
            f.write(s + "\n")
