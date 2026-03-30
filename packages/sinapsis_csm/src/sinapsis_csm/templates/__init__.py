# -*- coding: utf-8 -*-
import importlib
from typing import Callable

from sinapsis_csm.templates.csm_tts import CSMTTS

_root_lib_path = "sinapsis_csm.templates"
_template_lookup = {
    "CSMTTS": f"{_root_lib_path}.csm_tts",
}


def __getattr__(name: str) -> Callable:
    if name in _template_lookup:
        module = importlib.import_module(_template_lookup[name])
        return getattr(module, name)
    raise AttributeError(f"Template `{name}` not found in `{_root_lib_path}`.")


__all__ = ["CSMTTS"]
