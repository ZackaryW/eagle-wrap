
from eagle_wrap.model import Library, SentOverCtx

CTX : SentOverCtx = None
INIT_LIB : Library = None 

def CURRENT_FOLDERS():
    for folder in INIT_LIB.folders:
        if folder.id in CTX.folders:
            yield folder

def CURRENT_ITEMS():
        for folder in CURRENT_FOLDERS():
            for item in folder.children:
                if item.id in CTX.items:
                    yield item