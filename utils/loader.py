"""Carrega dinamicamente modulos pelo caminho."""

from __future__ import annotations

import importlib
from types import ModuleType
from pathlib import Path


def load_module(path: str | Path) -> ModuleType:
    """Importa um modulo a partir de um caminho absoluto."""
    path = Path(path)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    raise ImportError(f"Nao foi possivel carregar {path}")
