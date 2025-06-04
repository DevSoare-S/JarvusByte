import os
import json
import hashlib
import time
import difflib
import pickle

from jarvucas_bin import carregar_bin, salvar_bin
from mindbit_encoder import carregar_pensamento_bit  # leitura de .bit

class JarvucasIA:
    def __init__(self, base_path: str = "mindzip", mindbit_path: str | None = None) -> None:
        """Inicializa a IA e garante os caminhos corretos.

        O diretório dos arquivos ``.bit`` pode ser definido via argumento ou pela
        variável de ambiente ``JARVUS_MINDBIT``. Caso nenhum seja fornecido,
        assume-se o subdiretório ``mindbit`` no nível superior ao núcleo.
        """

        script_dir = os.path.dirname(__file__)

        self.base_path = os.path.abspath(base_path)

        env_path = os.getenv("JARVUS_MINDBIT")
        if mindbit_path is None:
            # Quando nenhum caminho é fornecido, assumimos a pasta mindbit no
            # diretório pai do núcleo para manter compatibilidade com a
            # estrutura de projeto.
            default_path = os.path.join(script_dir, "..", "mindbit")
            mindbit_path = env_path if env_path else default_path
        self.mindbit_path = os.path.abspath(mindbit_path)
        # Expõe o caminho para outros módulos através da variável de ambiente
        os.environ["JARVUS_MINDBIT"] = self.mindbit_path

        os.makedirs(self.base_path, exist_ok=True)
        os.makedirs(self.mindbit_path, exist_ok=True)

    def get_mindbit_path(self) -> str:
        """Retorna o caminho absoluto para a pasta de conhecimento simbólico."""
        return self.mindbit_path

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
        """Mantida para compatibilidade; retorna bytes JSON."""
        return json.dumps(pensamento).encode("utf-8")

    def salvar_pensamento(self, pensamento, nome_id=None):
        if not nome_id:
            nome_id = hashlib.sha1(json.dumps(pensamento).encode()).hexdigest()[:8]
        # Utiliza pickle para armazenar pensamentos binarios
        salvar_bin(os.path.join(self.base_path, f"{nome_id}.bin"), [pensamento])
        return nome_id

    def carregar_pensamentos(self):
        pensamentos = []

        # 🧠 1. Carrega blocos .bin serializados com pickle
        for file in os.listdir(self.base_path):
            if file.endswith(".bin"):
                try:
                    caminho = os.path.join(self.base_path, file)
                    dados = carregar_bin(caminho)
                    pensamentos.extend(dados)
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
