"""Guard against deprecated Home Assistant constants.

HA markiert auslaufende Konstanten mit einem ``_DEPRECATED_``-Pendant im
jeweiligen Modul und entfernt sie nach einer Frist. Der Test schlägt an,
sobald die Integration eine solche Konstante importiert - lange bevor sie
mit einem Core-Update tatsächlich wegfällt.
"""

from __future__ import annotations

import ast
import importlib
from pathlib import Path

import custom_components.uba_lqi as integration


def test_no_deprecated_ha_constants() -> None:
    package = Path(integration.__file__).parent
    deprecated: list[str] = []
    for path in sorted(package.glob("*.py")):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if not (
                isinstance(node, ast.ImportFrom)
                and node.module
                and node.module.startswith("homeassistant")
            ):
                continue
            module = importlib.import_module(node.module)
            deprecated.extend(
                f"{path.name}: {node.module}.{alias.name}"
                for alias in node.names
                if hasattr(module, f"_DEPRECATED_{alias.name}")
            )
    assert not deprecated
