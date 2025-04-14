# -*- coding: utf-8 -*-
from typing import Any

from pydantic import BaseModel
from sinapsis_core.utils.env_var_keys import EnvVarEntry, doc_str, return_docs_for_vars


class _ElevenlabsKeys(BaseModel):
    """
    Env vars for Elevenlabs
    """

    ELEVENLABS_API_KEY: EnvVarEntry = EnvVarEntry(
        var_name="ELEVENLABS_API_KEY",
        default_value=None,
        allowed_values=None,
        description="set api key for Elevenlabs",
    )


ElevenlabsEnvVars = _ElevenlabsKeys()

doc_str = return_docs_for_vars(ElevenlabsEnvVars, docs=doc_str, string_for_doc="""Elevenlabs env vars available: \n""")
__doc__ = doc_str


def __getattr__(name: str) -> Any:
    """to use as an import, when updating the value is not important"""
    if name in ElevenlabsEnvVars.model_fields:
        return ElevenlabsEnvVars.model_fields[name].default.value

    raise AttributeError(f"Agent does not have `{name}` env var")


_all__ = (*list(ElevenlabsEnvVars.model_fields.keys()), "ElevenlabsEnvVars")
