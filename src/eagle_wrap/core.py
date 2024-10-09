from functools import cache
import json
import os
import typing
import requests as req


@cache
def getSettingPath():
    roaming = os.getenv("APPDATA")
    return os.path.join(roaming, "Eagle", "Settings")

TOKEN = None

def setToken(token: str):
    global TOKEN
    TOKEN = token
    getToken.cache_clear()


@cache
def getToken():
    if TOKEN:
        return TOKEN
    
    raw = None
    try:
        res= req.get("http://localhost:41595/api/application/info")
        if res:
            raw = res.json()["data"]
        if not raw:
            with open(getSettingPath(), "r") as f:
                raw = json.load(f)

        return raw.get("preferences", {}).get("developer", {}).get("apiToken", None)
    except: # noqa
        return None

def request(
    path: str, 
    methodname: typing.Literal["get", "post"], 
    data: dict = None,
    params : dict = None
) -> dict:
    token = getToken()
    if not token:
        raise RuntimeError("No token found")

    method = getattr(req, methodname)
    url = f"http://localhost:41595/api/{path}?token={token}"
    if params:
        params = {k: v for k, v in params.items() if v is not None}
        url += "&" + "&".join([f"{k}={v}" for k, v in params.items()])

    if methodname == "post":
        if data:
            data = {k: v for k, v in data.items() if v is not None}

        res = method(url, json=data)
    else:
        res = method(url)
    return res.json()

