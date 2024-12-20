
import os
from eaglewrap.api import EagleApi
from eaglewrap.cfg import EagleCfg

@EagleCfg._changeBasedOnSettingSignature()
def getOpenedLibraryNames()-> dict:
    history = EagleCfg.libraryHistory()
    return {os.path.splitext(os.path.basename(path))[0]: path for path in history}

def switchLibrary(name : str):
    history = getOpenedLibraryNames()
    if name not in history:
        raise ValueError(f"Library {name} not found")
    EagleApi.librarySwitch(history[name])
