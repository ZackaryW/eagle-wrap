import json
import requests as req
import typing
from .cfg import EagleCfg

class EagleApi:
    token : str = None

    @classmethod
    def _internalGetToken(cls) -> str:
        if cls.token:
            return cls.token
        
        try:
            res= req.get("http://localhost:41595/api/application/info")
            if res:
                raw = res.json()["data"]
            if not raw:
                with open(EagleCfg.settingsPath(), "r") as f:
                    raw = json.load(f)

            token = raw.get("preferences", {}).get("developer", {}).get("apiToken", None)
            if token:
                cls.token = token
                return token
        except: # noqa
            pass    
        return None

    @classmethod
    def _internalRequest(
        cls,
        path: str, 
        methodname: typing.Literal["get", "post"], 
        data: dict = None,
        params : dict = None
    ) -> dict:
        token = cls._internalGetToken()
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
        return res.json().get("data", {})

    
    @classmethod
    def applicationInfo(cls):
        return cls._internalRequest("application/info", "get")
    #

    @classmethod
    def createFolder(cls, name: str, parentId: str = None):
        return cls._internalRequest(
            "folder/create", "post", data={"folderName": name, "parent": parentId}
        )

    @classmethod
    def renameFolder(cls, folderId: str, newName: str):
        return cls._internalRequest(
            "folder/rename", "post", data={"folderId": folderId, "newName": newName}
        )

    @classmethod
    def updateFolder(
        cls,
        folderId : str,
        newName : str = None,
        newDescription : str = None,
        newColor : typing.Literal["red","orange","green","yellow","aqua","blue","purple","pink"] = None
    ):
        return cls._internalRequest(
            "folder/update",
            "post",
            data={
                "folderId": folderId,
                "newName": newName,
                "newDescription": newDescription,
                "newColor": newColor,
            },
        )


    @classmethod
    def listFolders(cls):
        return cls._internalRequest("folder/list", "get")

    @classmethod
    def listRecentFolders(cls):
        return cls._internalRequest("folder/listRecent", "get")

    # ANCHOR library
    @classmethod
    def libraryInfo(cls):
        return cls._internalRequest("library/info", "get")

    @classmethod
    def libraryHistory(cls):
        return cls._internalRequest("library/history", "get")

    @classmethod
    def librarySwitch(cls, libraryPath : str):
        return cls._internalRequest("library/switch", "post", data={"libraryPath": libraryPath})

    @classmethod
    def libraryIcon(cls, libraryPath: str):
        return cls._internalRequest(
            "library/icon",
            "get",
            params={"libraryPath": libraryPath}
        )

    # ANCHOR item
    @classmethod
    def updateItem(
        cls,
        itemId: str,
        tags: typing.List[str] = None,
        annotation: str = None,
        url: str = None,
        star: int = None
    ):
        return cls._internalRequest(
            "item/update",
            "post",
            data={
                "id": itemId,
                "tags": tags,
                "annotation": annotation,
                "url": url,
                "star": star,
            }
        )

    @classmethod
    def itemRefreshThumbnail(cls, itemId: str):
        return cls._internalRequest(
            "item/refreshThumbnail",
            "post",
            data={"id": itemId}
        )

    @classmethod
    def itemRefreshPalette(cls, itemId: str):
        return cls._internalRequest(
            "item/refreshPalette",
            "post",
            data={"id": itemId}
        )

    @classmethod
    def itemMoveToTrash(cls, itemIds: typing.List[str]):
        return cls._internalRequest(
            "item/moveToTrash",
            "post",
            data={"itemIds": itemIds}
        )


    @classmethod
    def listItems(
        cls,
        limit: int = 200,
        offset: int = 0,
        orderBy: str = None,
        keyword: str = None,
        ext: str = None,
        tags: str = None,
        folders: str = None
    ):
        params = {
            "limit": limit,
            "offset": offset,
            "orderBy": orderBy,
            "keyword": keyword,
            "ext": ext,
            "tags": tags,
            "folders": folders
        }

        return cls._internalRequest(
            "item/list",
            "get",
            params=params
        )

    @classmethod
    def getThumbnail(cls, itemId: str):
        return cls._internalRequest(
            "item/thumbnail",
            "get",
            params={"id": itemId}
        )

    @classmethod
    def getItemInfo(cls, itemId: str):
        return cls._internalRequest(
            "item/info",
            "get",
            params={"id": itemId}
        )


    @classmethod
    def itemAddBookmark(
        cls,
        url: str,
        name: str,
        base64: str = None,
        tags: typing.List[str] = None,
        modificationTime: int = None,
        folderId: str = None
    ):
        return cls._internalRequest(
            "item/addBookmark",
            "post",
            data={
                "url": url,
                "name": name,
                "base64": base64,
                "tags": tags,
                "modificationTime": modificationTime,
                "folderId": folderId
            }
        )

    @classmethod
    def itemAddFromUrl(
        cls,
        url : str, 
        name : str,
        website : str = None,
        tags : typing.List[str] = None,
        star = None, 
        annotation : str = None,
        modificationTime : int = None,
        folderId : str = None,
        headers : dict = None
    ):
        return cls._internalRequest(
            "item/addFromUrl",
            "post",
            data={
                "url": url,
                "name": name,
                "website": website,
                "tags": tags,
                "star": star,
                "annotation": annotation,
                "modificationTime": modificationTime,
                "folderId": folderId,
                "headers": headers,
            },
        )

    @classmethod
    def itemAddFromPaths(
        cls,
        path: str,
        name: str,
        website: str = None,
        annotation: str = None,
        tags: typing.List[str] = None,
        folderId: str = None
    ):
        return cls._internalRequest(
            "item/addFromPaths",
            "post",
            data={
                "path": path,
                "name": name,
                "website": website,
                "annotation": annotation,
                "tags": tags,
                "folderId": folderId
            }
        )

    @classmethod
    def itemAddFromPath(
        cls,
        path: str,
        name: str,
        website: str = None,
        annotation: str = None,
        tags: typing.List[str] = None,
        folderId: str = None
    ):
        return cls._internalRequest(
            "item/addFromPath",
            "post",
            data={
                "path": path,
                "name": name,
                "website": website,
                "annotation": annotation,
                "tags": tags,
                "folderId": folderId
            }
        )


    @classmethod
    def itemAddFromURLs(
        cls,
        items: typing.List[dict],
        folderId: str = None
    ):
        return cls._internalRequest(
            "item/addFromURLs",
            "post",
            data={
                "items": items,
                "folderId": folderId
            }
        )
