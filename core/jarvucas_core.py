import os
import json
import hashlib
import time
import difflib
from mindbit_encoder import carregar_pensamento_bit  # leitura de .bit

class JarvucasIA:
    def __init__(self, base_path="mindzip", mindbit_path=None):
        """Inicializa a IA configurando os diretórios de armazenamento."""

        script_dir = os.path.dirname(__file__)

        self.base_path = os.path.abspath(base_path)

        if mindbit_path is None:
            mindbit_path = os.path.join(script_dir, "mindbit")
        self.mindbit_path = os.path.abspath(mindbit_path)

        os.makedirs(self.base_path, exist_ok=True)
        os.makedirs(self.mindbit_path, exist_ok=True)

    def pensar(self, tipo, topico, conteudo, raciocinio):
        return {
            "tipo": tipo,
            "topico": topico,
            "conteudo": conteudo,
            "raciocinio": raciocinio,
            "timestamp": time.time()
        }

    def falar(self, pensamento):
        if pensamento["tipo"] == "resposta":
            return f"Sobre {pensamento['topico']}: {pensamento['conteudo']} Isso é porque {pensamento['raciocinio']}."
        return "Pensamento não expressável ainda."

    def compactar(self, pensamento):
        return f"@{pensamento['tipo'].upper()}:{pensamento['topico']}->{pensamento['conteudo']}|{pensamento['raciocinio']}"

    def compactar_bytes(self, pensamento):
        return json.dumps(pensamento).encode("utf-8")

    def salvar_pensamento(self, pensamento, nome_id=None):
        if not nome_id:
            nome_id = hashlib.sha1(json.dumps(pensamento).encode()).hexdigest()[:8]
        with open(f"{self.base_path}/{nome_id}.bin", "wb") as f:
            f.write(self.compactar_bytes(pensamento))
        return nome_id

    def carregar_pensamentos(self):
        pensamentos = []

        # 🧠 1. Carrega blocos .bin (JSON simples)
        for file in os.listdir(self.base_path):
            if file.endswith(".bin"):
                try:
                    with open(os.path.join(self.base_path, file), "rb") as f:
                        raw = f.read().decode("utf-8")
                        pensamento = json.loads(raw)
                        pensamentos.append(pensamento)
                except Exception as e:
                    print(f"[ERRO] .bin {file}: {e}")

        # 🧠 2. Carrega blocos .bit (binário puro)
        for file in os.listdir(self.mindbit_path):
            if file.endswith(".bit"):
                try:
                    path = os.path.join(self.mindbit_path, file)
                    pensamento = carregar_pensamento_bit(path)
                    pensamentos.append(pensamento)
                except Exception as e:
                    print(f"[ERRO] .bit {file}: {e}")

        return pensamentos

    def conversar(self, entrada):
        pensamentos = self.carregar_pensamentos()
        perguntas = [p["topico"] for p in pensamentos]
        escolha = difflib.get_close_matches(entrada, perguntas, n=1)
        if escolha:
            for p in pensamentos:
                if p["topico"] == escolha[0]:
                    return self.falar(p)
        return "Ainda não sei responder isso."

    def listar_topicos(self):
        """Lista todos os tópicos que a IA já conhece (debug visual)"""
        return [p["topico"] for p in self.carregar_pensamentos()]
