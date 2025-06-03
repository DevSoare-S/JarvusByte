import os
import time
from mindbit_encoder import salvar_pensamento_bit

# Cria a pasta mindbit/ se não existir
mindbit_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mindbit"))
os.makedirs(mindbit_dir, exist_ok=True)

# Lista de pensamentos úteis
blocos = [
    {
        "tipo": "resposta",
        "topico": "farm_cabal",
        "conteudo": "Use skill F1 a cada 10 segundos para farmar monstros.",
        "raciocinio": "Essa repetição otimiza o drop e mantém o buff ativo."
    },
    {
        "tipo": "resposta",
        "topico": "buff_pve",
        "conteudo": "O melhor buff para PvE é o Buff X.",
        "raciocinio": "Buff X aumenta dano e reduz tempo de cooldown."
    },
    {
        "tipo": "resposta",
        "topico": "soma_basica",
        "conteudo": "2 + 2 = 4",
        "raciocinio": "Adição de dois valores iguais."
    },
    {
        "tipo": "resposta",
        "topico": "loop_de_ataque",
        "conteudo": "Execute F1, depois clique no mob, e repita a cada 10s.",
        "raciocinio": "Sequência básica para grind automático em Cabal."
    },
    {
        "tipo": "resposta",
        "topico": "movimento_esquiva",
        "conteudo": "Use a tecla de dash para esquivar rapidamente.",
        "raciocinio": "Ajuda a evitar ataques pesados e manter mobilidade."
    }
]

# Salvar todos os blocos como .bit
for i, bloco in enumerate(blocos, start=1):
    nome = f"{i:03d}_{bloco['topico']}.bit"
    caminho = os.path.join(mindbit_dir, nome)
    salvar_pensamento_bit(bloco, caminho)
    print(f"✅ Salvo: {nome}")
    time.sleep(0.1)
