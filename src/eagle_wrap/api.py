import typing
from .core import request


def applicationInfo():
    return request("application/info", "get")
#

def createFolder(name: str, parentId: str = None):
    return request(
        "folder/create", "post", data={"folderName": name, "parent": parentId}
    )

def renameFolder(folderId: str, newName: str):
    return request(
        "folder/rename", "post", data={"folderId": folderId, "newName": newName}
    )

def updateFolder(
    folderId : str,
    newName : str = None,
    newDescription : str = None,
    newColor : typing.Literal["red","orange","green","yellow","aqua","blue","purple","pink"] = None
):
    return request(
        "folder/update",
        "post",
        data={
            "folderId": folderId,
            "newName": newName,
            "newDescription": newDescription,
            "newColor": newColor,
        },
    )


def listFolders():
    return request("folder/list", "get")

def listRecentFolders():
    return request("folder/listRecent", "get")

# ANCHOR library
def libraryInfo():
    return request("library/info", "get")

def libraryHistory():
    return request("library/history", "get")

def librarySwitch(libraryPath : str):
    return request("library/switch", "post", data={"libraryPath": libraryPath})

def libraryIcon(libraryPath: str):
    return request(
        "library/icon",
        "get",
        params={"libraryPath": libraryPath}
    )

# ANCHOR item
def updateItem(
    itemId: str,
    tags: typing.List[str] = None,
    annotation: str = None,
    url: str = None,
    star: int = None
):
    return request(
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

def itemRefreshThumbnail(itemId: str):
    return request(
        "item/refreshThumbnail",
        "post",
        data={"id": itemId}
    )

def itemRefreshPalette(itemId: str):
    return request(
        "item/refreshPalette",
        "post",
        data={"id": itemId}
    )

def itemMoveToTrash(itemIds: typing.List[str]):
    return request(
        "item/moveToTrash",
        "post",
        data={"itemIds": itemIds}
    )


def listItems(
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

    return request(
        "item/list",
        "get",
        params=params
    )

def getThumbnail(itemId: str):
    return request(
        "item/thumbnail",
        "get",
        params={"id": itemId}
    )

def getItemInfo(itemId: str):
    return request(
        "item/info",
        "get",
        params={"id": itemId}
    )


def itemAddBookmark(
    url: str,
    name: str,
    base64: str = None,
    tags: typing.List[str] = None,
    modificationTime: int = None,
    folderId: str = None
):
    return request(
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

def itemAddFromUrl(
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
    return request(
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

def itemAddFromPaths(
    path: str,
    name: str,
    website: str = None,
    annotation: str = None,
    tags: typing.List[str] = None,
    folderId: str = None
):
    return request(
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

def itemAddFromPath(
    path: str,
    name: str,
    website: str = None,
    annotation: str = None,
    tags: typing.List[str] = None,
    folderId: str = None
):
    return request(
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


def itemAddFromURLs(
    items: typing.List[dict],
    folderId: str = None
):
    return request(
        "item/addFromURLs",
        "post",
        data={
            "items": items,
            "folderId": folderId
        }
    )
