from jarvucas_core import JarvucasIA
import os

# Corrige caminho para pegar a pasta "mindzip" fora da pasta "core"
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mindzip"))
ia = JarvucasIA(base_path=base_dir)

print("🧠 JarvucasIA iniciada! Pergunte algo ou digite 'sair' para encerrar.\n")

while True:
    entrada = input("Você: ").strip()
    if entrada.lower() in ["sair", "exit", "quit"]:
        print("JarvucasIA: Até logo!")
        break

    resposta = ia.conversar(entrada)
    print("JarvucasIA:", resposta)
