"""GAIA coordena todos os subsistemas da JarvucasIA."""

from __future__ import annotations

from pathlib import Path
from datetime import datetime

from . import hades, demeter, athena, hermes
from utils.file_ops import backup_directory

SCRIPT_DIR = Path(__file__).resolve().parent
BACKUP_DIR = SCRIPT_DIR.parent / 'backups'


class GAIA:
    """Classe principal que gerencia a IA e seus subsistemas."""

    def __init__(self) -> None:
        self.subsistemas = {
            'hades': hades,
            'demeter': demeter,
            'athena': athena,
            'hermes': hermes,
        }

    def executar_ciclo(self) -> None:
        """Executa um ciclo padrao de evolucao."""
        try:
            self.subsistemas['athena'].executar_simulacoes()
            self.subsistemas['demeter'].refatorar()
        except Exception as exc:  # delega tratamento a HADES
            hades.registrar_falha(exc)

    def backup(self) -> Path:
        """Gera um backup completo do estado atual."""
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        dest = BACKUP_DIR / f'backup_{timestamp}'
        return backup_directory(SCRIPT_DIR.parent, dest)

