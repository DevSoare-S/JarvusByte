import pickle


def carregar_bin(caminho: str) -> list[dict]:
    """Carrega dados de um arquivo .bin usando pickle."""
    try:
        with open(caminho, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        print(f"[ERRO ao carregar binário] {caminho}: {e}")
        return []


def salvar_bin(caminho: str, dados: list[dict]) -> None:
    """Salva dados em um arquivo .bin usando pickle."""
    try:
        with open(caminho, "wb") as f:
            pickle.dump(dados, f)
    except Exception as e:
        print(f"[ERRO ao salvar binário] {caminho}: {e}")

