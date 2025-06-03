"""Modulo de visao computacional para JarvucasIA."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Dict, List, Tuple

import cv2
import numpy as np
import pyautogui

# Diretórios de recursos
SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = SCRIPT_DIR.parent / "templates"
VISAO_FILE = SCRIPT_DIR / "mindbit" / "visao.bit"


def capturar_tela() -> np.ndarray:
    """Captura a tela atual sem salvar em disco."""
    screenshot = pyautogui.screenshot()
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return frame


def carregar_templates() -> Dict[str, np.ndarray]:
    """Carrega todas as imagens da pasta de templates."""
    templates: Dict[str, np.ndarray] = {}
    for img_path in TEMPLATES_DIR.glob("*.png"):
        template = cv2.imread(str(img_path), cv2.IMREAD_COLOR)
        if template is not None:
            templates[img_path.stem] = template
    return templates


def detectar_objetos(frame: np.ndarray, templates: Dict[str, np.ndarray], threshold: float = 0.8) -> Dict[str, List[Tuple[int, int]]]:
    """Detecta objetos na tela a partir dos templates fornecidos."""
    detections: Dict[str, List[Tuple[int, int]]] = {}
    for name, template in templates.items():
        h, w = template.shape[:2]
        result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        points: List[Tuple[int, int]] = []
        for pt in zip(*loc[::-1]):  # (x, y)
            center = (pt[0] + w // 2, pt[1] + h // 2)
            points.append(center)
        if points:
            detections[name] = points
    return detections


def carregar_visao(path: Path) -> Dict[str, Tuple[int, int]]:
    """Carrega o arquivo de visão mantendo registros existentes."""
    registros: Dict[str, Tuple[int, int]] = {}
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                nome, coords = line.split(":", 1)
                if coords.startswith("x="):
                    x_part, y_part = coords[2:].split(",y=")
                    registros[nome] = (int(x_part), int(y_part))
    return registros


def registrar_visao(detections: Dict[str, List[Tuple[int, int]]], path: Path) -> None:
    """Atualiza o arquivo de visão com as novas posições."""
    registros = carregar_visao(path)

    for nome, pontos in detections.items():
        for idx, (x, y) in enumerate(pontos, start=1):
            chave = nome if len(pontos) == 1 else f"{nome}_{idx}"
            registros[chave] = (x, y)

    with path.open("w", encoding="utf-8") as f:
        for chave, (x, y) in registros.items():
            f.write(f"{chave}:x={x},y={y}\n")


def loop_visao(intervalo: float = 1.0) -> None:
    """Executa o loop continuo de captura e deteccao."""
    templates = carregar_templates()
    print("🔎 Sistema de visão iniciado. Pressione Ctrl+C para encerrar.")
    while True:
        frame = capturar_tela()
        detections = detectar_objetos(frame, templates)
        registrar_visao(detections, VISAO_FILE)
        time.sleep(intervalo)


if __name__ == "__main__":
    try:
        loop_visao()
    except KeyboardInterrupt:
        print("\nVisão encerrada.")

