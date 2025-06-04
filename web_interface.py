"""Interface HTML de conversa para JarvucasIA."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from pathlib import Path
import os

from core.jarvucas_core import JarvucasIA
from modulos.interpretador import interpretar_frase
from modulos.memoria import (
    registrar_memoria,
    registrar_resposta,
    atualizar_contexto,
    detectar_padrao_visao,
)
from modulos.fala import ativar_voz
from modulos.estudo import estudar_tema
from utils.evolucao import progresso_por_area

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = (SCRIPT_DIR / "mindzip").resolve()
env_mindbit = os.getenv("JARVUS_MINDBIT")
MINDBIT_DIR = (
    Path(env_mindbit).resolve()
    if env_mindbit
    else (SCRIPT_DIR / "mindbit").resolve()
)
HTML_FILE = SCRIPT_DIR / "web" / "index.html"
CSS_FILE = SCRIPT_DIR / "web" / "style.css"
JS_FILE = SCRIPT_DIR / "web" / "script.js"
GRAFICOS_FILE = SCRIPT_DIR / "web" / "graficos.js"
CONTROLE_FILE = SCRIPT_DIR / "web" / "controle.js"

ia = JarvucasIA(base_path=str(BASE_DIR), mindbit_path=str(MINDBIT_DIR))
MINDBIT_DIR = Path(ia.get_mindbit_path())
PROPOSITO_FILE = MINDBIT_DIR / "proposito.bit"


def processar_frase(frase: str) -> str:
    analise = interpretar_frase(frase)
    registrar_memoria(analise)
    atualizar_contexto(analise)
    detectar_padrao_visao()
    resposta = ia.conversar(frase)
    registrar_resposta(frase, resposta)
    return resposta


class JarvucasHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/style.css":
            self.send_response(200)
            self.send_header("Content-Type", "text/css")
            self.end_headers()
            self.wfile.write(CSS_FILE.read_bytes())
            return
        if self.path == "/script.js":
            self.send_response(200)
            self.send_header("Content-Type", "application/javascript")
            self.end_headers()
            self.wfile.write(JS_FILE.read_bytes())
            return
        if self.path == "/graficos.js":
            self.send_response(200)
            self.send_header("Content-Type", "application/javascript")
            self.end_headers()
            self.wfile.write(GRAFICOS_FILE.read_bytes())
            return
        if self.path == "/controle.js":
            self.send_response(200)
            self.send_header("Content-Type", "application/javascript")
            self.end_headers()
            self.wfile.write(CONTROLE_FILE.read_bytes())
            return
        if self.path == "/ativar_voz":
            ativar_voz()
            self.send_response(204)
            self.end_headers()
            return
        if self.path.startswith("/estudar"):
            query = parse_qs(self.path.split("?", 1)[1]) if "?" in self.path else {}
            tema = query.get("t", [""])[0]
            if tema:
                estudar_tema(tema)
            self.send_response(204)
            self.end_headers()
            return
        if self.path == "/evolucao":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(progresso_por_area()).encode())
            return
        if self.path == "/proposito":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            texto = PROPOSITO_FILE.read_text(encoding="utf-8") if PROPOSITO_FILE.exists() else ""
            self.wfile.write(texto.encode())
            return
        if self.path.startswith("/perguntar"):
            query = parse_qs(self.path.split("?", 1)[1]) if "?" in self.path else {}
            frase = query.get("q", [""])[0]
            resposta = processar_frase(frase)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"resposta": resposta}).encode())
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_FILE.read_text(encoding="utf-8").encode("utf-8"))


def iniciar_servidor(porta: int = 8000) -> None:
    httpd = HTTPServer(("", porta), JarvucasHandler)
    print(f"💻 Interface web em http://localhost:{porta}")
    httpd.serve_forever()


if __name__ == "__main__":
    iniciar_servidor()
