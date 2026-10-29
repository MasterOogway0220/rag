"""Null entries from a parser must not become caption text."""

import importlib.util
import logging
import sys
import types
from pathlib import Path
from unittest.mock import patch


def test_normalize_caption_list_skips_null_entries():
    root = Path(__file__).resolve().parents[1]
    lightrag = types.ModuleType("lightrag")
    lightrag_utils = types.ModuleType("lightrag.utils")
    lightrag_utils.logger = logging.getLogger(__name__)
    muserag = types.ModuleType("muserag")
    muserag.__path__ = [str(root / "muserag")]

    with patch.dict(
        sys.modules,
        {
            "lightrag": lightrag,
            "lightrag.utils": lightrag_utils,
            "muserag": muserag,
        },
    ):
        spec = importlib.util.spec_from_file_location(
            "muserag.utils", root / "muserag" / "utils.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

    assert module.normalize_caption_list([None, " Figure 1 ", " ", 0]) == [
        "Figure 1",
        "0",
    ]
