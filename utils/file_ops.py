"""Operacoes de arquivo utilizadas pela JarvucasIA."""

from __future__ import annotations

import shutil
from pathlib import Path


def backup_directory(src: str | Path, dest: str | Path) -> Path:
    """Cria um backup compactado de src em dest."""
    src = Path(src)
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    archive = shutil.make_archive(str(dest), 'zip', root_dir=str(src))
    return Path(archive)


def restore_backup(archive: str | Path, target: str | Path) -> None:
    """Restaura um backup para o diretorio target."""
    archive = Path(archive)
    target = Path(target)
    shutil.unpack_archive(str(archive), str(target))

