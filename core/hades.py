"""HADES monitora erros e controla rollback."""

from __future__ import annotations

import traceback
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
LOG_FILE = SCRIPT_DIR / 'universo' / 'logs' / 'hades.log'


def registrar_falha(exc: Exception) -> None:
    """Registra uma falha em arquivo de log."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open('a', encoding='utf-8') as f:
        f.write('---\n')
        f.write(''.join(traceback.format_exception(exc)))

