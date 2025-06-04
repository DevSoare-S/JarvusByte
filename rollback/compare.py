"""Compara duas versoes de GAIA e sinaliza diferencas."""

from __future__ import annotations

import difflib
from pathlib import Path


def comparar(v1: str | Path, v2: str | Path) -> str:
    """Retorna um diff textual entre duas versoes."""
    t1 = Path(v1).read_text(encoding='utf-8').splitlines()
    t2 = Path(v2).read_text(encoding='utf-8').splitlines()
    diff = difflib.unified_diff(t1, t2, fromfile=str(v1), tofile=str(v2))
    return '\n'.join(diff)


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 3:
        print(comparar(sys.argv[1], sys.argv[2]))
    else:
        print('Usage: compare.py file1 file2')

