"""Modulo de aprendizado simbólico via vídeos para JarvucasIA.

Este módulo permite que a IA aprenda observando vídeos. O processo inclui:
1. Download do vídeo do YouTube.
2. Extração e transcrição do áudio.
3. Captura de frames e análise visual com OCR.
4. Interpretação simbólica das frases da transcrição.
5. Registro de todo o conhecimento em arquivos ``.bit`` e ``.bin``.
"""

from __future__ import annotations

import json
import re
import os
from pathlib import Path
from typing import List

import cv2
import pytesseract
import yt_dlp
import whisper

from modulos.interpretador import interpretar_frase, carregar_palavras, _append_to_bit

# Diretórios base do projeto
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = (SCRIPT_DIR.parent / "mindzip").resolve()
env_mindbit = os.getenv("JARVUS_MINDBIT")
MINDBIT_DIR = Path(env_mindbit).resolve() if env_mindbit else (SCRIPT_DIR.parent / "core" / "mindbit").resolve()
VIDEOS_DIR = (SCRIPT_DIR.parent / "videos").resolve()

# Arquivos gerados pelo aprendizado de vídeo
# Arquivo onde as regras/conceitos extraídos serao armazenados
APRENDIZADO_VIDEO_FILE = BASE_DIR / "aprendizado_video.bin"
# Arquivo com a transcrição interpretada de cada vídeo
MEMORIA_VIDEO_FILE = BASE_DIR / "memoria_video.bin"
# Observações visuais provenientes do vídeo
VISAO_VIDEO_FILE = MINDBIT_DIR / "visao_video.bit"


def baixar_video(url: str) -> Path:
    """Baixa o vídeo do YouTube para a pasta ``videos/``.

    Retorna o caminho do arquivo baixado.
    """
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    ydl_opts = {"outtmpl": str(VIDEOS_DIR / "%(id)s.%(ext)s"), "format": "mp4"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    return Path(filename)


def transcrever_audio(video_path: Path) -> str:
    """Transcreve o áudio de ``video_path`` utilizando Whisper."""
    model = whisper.load_model("base")
    result = model.transcribe(str(video_path))
    return result.get("text", "")


def _extrair_frames(video_path: Path, intervalo: int = 2) -> List[Path]:
    """Extrai um frame do vídeo a cada ``intervalo`` segundos."""
    frames_dir = VIDEOS_DIR / video_path.stem
    frames_dir.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 24
    step = int(fps * intervalo)
    frames: List[Path] = []
    idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if idx % step == 0:
            frame_path = frames_dir / f"frame_{idx}.jpg"
            cv2.imwrite(str(frame_path), frame)
            frames.append(frame_path)
        idx += 1
    cap.release()
    return frames


def analisar_frames(video_path: Path) -> List[str]:
    """Executa OCR nos frames do vídeo gerando observações simbólicas."""
    textos: List[str] = []
    for frame_path in _extrair_frames(video_path):
        img = cv2.imread(str(frame_path))
        if img is None:
            continue
        text = pytesseract.image_to_string(img, lang="por")
        for linha in text.splitlines():
            linha = linha.strip()
            if linha:
                textos.append(f"texto:{linha}")
    return textos


def analisar_frases(transcricao: str) -> tuple[List[str], List[str]]:
    """Converte a transcrição em conceitos e registros de memória."""
    verbos = carregar_palavras("100_verbo")
    sujeitos = carregar_palavras("101_sujeito")
    conceitos: List[str] = []
    memoria: List[str] = []
    frases = [f.strip() for f in re.split(r"[.!?]+", transcricao) if f.strip()]
    for frase in frases:
        analise = interpretar_frase(frase)
        memoria.append(json.dumps({"frase": frase, **analise}, ensure_ascii=False))
        if analise.get("verbo") and analise.get("sujeito"):
            conceitos.append(f"{analise['verbo']}->{analise['sujeito']}")
        if analise.get("verbo") and analise["verbo"] not in verbos:
            _append_to_bit(MINDBIT_DIR / "100_verbo.bit", f"{analise['verbo']}:geral")
            verbos.append(analise["verbo"])
        if analise.get("sujeito") and analise["sujeito"] not in sujeitos:
            _append_to_bit(MINDBIT_DIR / "101_sujeito.bit", analise["sujeito"])
            sujeitos.append(analise["sujeito"])
    return conceitos, memoria


def registrar_aprendizado(conceitos: List[str], memoria: List[str], visao: List[str]) -> None:
    """Armazena os dados extraídos do vídeo nos arquivos simbólicos."""
    def _append_lines(path: Path, linhas: List[str]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as f:
            for l in linhas:
                f.write(l + "\n")

    _append_lines(APRENDIZADO_VIDEO_FILE, conceitos)
    _append_lines(MEMORIA_VIDEO_FILE, memoria)
    _append_lines(VISAO_VIDEO_FILE, visao)


def aprender_de_youtube(url: str) -> None:
    """Executa todo o processo de aprendizado simbólico de um vídeo do YouTube."""
    video = baixar_video(url)
    transcricao = transcrever_audio(video)
    conceitos, memoria = analisar_frases(transcricao)
    visao = analisar_frames(video)
    registrar_aprendizado(conceitos, memoria, visao)
