"""Interface HTML de conversa para JarvucasIA."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from pathlib import Path

from core.jarvucas_core import JarvucasIA
from modulos.interpretador import interpretar_frase
from modulos.memoria import (
    registrar_memoria,
    registrar_resposta,
    atualizar_contexto,
    detectar_padrao_visao,
)

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = (SCRIPT_DIR / "mindzip").resolve()
MINDBIT_DIR = (SCRIPT_DIR / "core" / "mindbit").resolve()
HTML_FILE = SCRIPT_DIR / "web" / "index.html"

ia = JarvucasIA(base_path=str(BASE_DIR), mindbit_path=str(MINDBIT_DIR))


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
