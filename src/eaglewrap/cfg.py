from functools import cache
import os
import json
import subprocess
import typing

class EagleCfg:
    __settings_cache = None
    __settings_lastModified = None
    __otherFuncsCache = {}
    
    @classmethod
    @cache
    def settingsPath(cls) -> str:
        roaming = os.getenv("APPDATA")
        return os.path.join(roaming, "Eagle", "Settings")
    
    @classmethod
    def launchApp(cls):
        eagle_path = os.path.join(os.getenv("PROGRAMFILES"), "Eagle", "Eagle.exe")
        proc = subprocess.Popen([eagle_path], creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
        return proc
    
    @classmethod
    def settings(cls) -> dict:
        if not cls.__settings_cache or os.path.getmtime(cls.settingsPath()) != cls.__settings_lastModified:
            with open(cls.settingsPath(), "r") as f:
                cls.__settings_cache = json.load(f)
                cls.__settings_lastModified = os.path.getmtime(cls.settingsPath())
        return cls.__settings_cache

    @classmethod
    def libraryHistory(cls)-> typing.List[str]:
        return cls.settings().get("libraryHistory", [])
    
    @classmethod
    def __isExpired(cls):
        if not cls.__settings_cache or os.path.getmtime(cls.settingsPath()) != cls.__settings_lastModified:
            cls.__settings_cache = None
            return True
        return False

    @classmethod
    def _changeBasedOnSettingSignature(cls):
        def decorator(func):
            def wrapper(*args, **kwargs):
                if cls.__isExpired():
                    res = func(*args, **kwargs)
                    cls.__otherFuncsCache[func.__name__] = res
                    return res
                return cls.__otherFuncsCache.get(func.__name__, None)
            return wrapper
        return decorator
