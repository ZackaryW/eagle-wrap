
import base64
from dataclasses import dataclass
from typing import TypedDict
import typing
import json
from eaglewrap.cfg import EagleCfg
from eaglewrap.model import Library
from eaglewrap.api import EagleApi

@dataclass(init=False)
class CtxModel:
    selectedFolders : typing.List[str]
    selectedItems : typing.List[str]
    currentLibrary : Library
    cfg : typing.Type[EagleCfg]
    api : typing.Type[EagleApi]

    def __init__(self, json_str : str):
        _ctx = json.loads(base64.b64decode(json_str).decode())
        self.selectedFolders = _ctx["selectedFolders"]
        self.selectedItems = _ctx["selectedItems"]
        self.currentLibrary = Library.current()
        self.cfg = EagleCfg
        self.api = EagleApi

        for k, v in _ctx.items():
            if k not in self.__dataclass_fields__:
                setattr(self, k, v)

        global ctx
        ctx = self

ctx : CtxModel = None

def _applyCtx() -> CtxModel:
    return ctx


def executePythonScript(script_path : str, ctx : CtxModel):
    with open(script_path, "r") as f:
        code = f.read()
    exec(code, globals())