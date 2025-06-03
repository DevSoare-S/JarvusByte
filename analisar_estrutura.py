"""Analisa a estrutura do projeto e gera sugestoes."""

from __future__ import annotations

from pathlib import Path
from typing import List

RULES_FILE = Path("core/mindbit/200_estrutura_modular.bit")
REPORT_FILE = Path("estrutura_sugerida.bit")


def load_rules(path: Path) -> List[str]:
    """Carrega as regras simbólicas do arquivo .bit."""
    rules: List[str] = []
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("regra:"):
                    rules.append(line.split("regra:", 1)[1].strip())
    return rules


def file_lines(path: Path) -> int:
    """Conta o número de linhas de um arquivo de texto."""
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def file_has_interface_code(path: Path) -> bool:
    """Heurística simples para detectar código de interface em arquivos."""
    keywords = ["pyttsx3", "speech_recognition", "Microphone", "input(", "print("]
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return False
    return any(kw in text for kw in keywords)


def analyze_project(root: Path, rules: List[str]) -> List[str]:
    """Analisa cada arquivo comparando com as regras e gera sugestões."""
    suggestions: List[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        classification = "coerente"

        if any("core" in part for part in rel.parts):
            # Regra: pasta core deve conter apenas lógica interna
            if file_has_interface_code(path):
                classification = "fora de lugar"
                suggestions.append(f"mover:{rel.as_posix()} → interface/{path.name}")
        if any("utils" in part for part in rel.parts):
            # Regra: utils deve conter apenas funções reutilizáveis
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "def " not in text:
                classification = "fora de lugar"
        # Regra: arquivos pequenos
        if file_lines(path) > 300:
            classification = "fora de lugar"

        print(f"{rel}: {classification}")
    return suggestions


def generate_report(suggestions: List[str], dest: Path) -> None:
    """Salva as sugestões em formato simbólico."""
    with dest.open("w", encoding="utf-8") as f:
        for item in suggestions:
            f.write(item + "\n")


def main() -> None:
    rules = load_rules(RULES_FILE)
    root = Path(".")
    suggestions = analyze_project(root, rules)
    generate_report(suggestions, REPORT_FILE)
    print(f"Relatório gerado em {REPORT_FILE}")


if __name__ == "__main__":
    main()
