import json

# Codifica um pensamento (dicionário) em binário puro (string de bits)
def codificar_binario(pensamento: dict) -> str:
    texto = json.dumps(pensamento, ensure_ascii=False)
    return ''.join(format(ord(c), '08b') for c in texto)

# Decodifica uma string de bits de volta para um pensamento (dict)
def decodificar_binario(bits: str) -> dict:
    chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
    texto = ''.join(chars)
    return json.loads(texto)

# Salva um pensamento como arquivo .bit (formato binário puro)
def salvar_pensamento_bit(pensamento: dict, path: str):
    bits = codificar_binario(pensamento)
    # Preenche com zeros pra múltiplos de 8
    bits = bits.ljust((len(bits) + 7) // 8 * 8, '0')
    byte_data = int(bits, 2).to_bytes(len(bits) // 8, byteorder='big')
    with open(path, "wb") as f:
        f.write(byte_data)

# Carrega um pensamento de um arquivo .bit
def carregar_pensamento_bit(path: str) -> dict:
    with open(path, "rb") as f:
        byte_data = f.read()
        bits = bin(int.from_bytes(byte_data, byteorder='big'))[2:]
        bits = bits.zfill(len(byte_data) * 8)  # corrige comprimento
        return decodificar_binario(bits)
