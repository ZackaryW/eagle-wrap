
from dataclasses import dataclass, field
import typing

from .api import libraryInfo

@dataclass
class SentOverCtx:
    folders : typing.List[str] = field(default_factory=list)
    items : typing.List[str] = field(default_factory=list)

@dataclass
class Folder:
    id: str
    name: str
    description: str
    children: typing.List['Folder'] = field(default_factory=list)
    modificationTime: int = 0
    tags: typing.List[str] = field(default_factory=list)
    iconColor: str = ""
    password: str = ""
    passwordTips: str = ""
    coverId: str = ""
    orderBy: str = "MANUAL"
    sortIncrease: bool = True

@dataclass
class SmartFolder:
    id: str
    name: str
    description: str
    modificationTime: int
    icon: str = ""
    conditions: typing.List[dict] = field(default_factory=list)
    orderBy: str = "MANUAL"
    sortIncrease: bool = True

@dataclass
class QuickAccess:
    type: str
    id: str

@dataclass
class TagsGroup:
    id: str
    name: str
    tags: typing.List[str] = field(default_factory=list)
    color: str = ""

@dataclass
class Library:
    folders: typing.List[Folder] = field(default_factory=list)
    smartFolders: typing.List[SmartFolder] = field(default_factory=list)
    quickAccess: typing.List[QuickAccess] = field(default_factory=list)
    tagsGroups: typing.List[TagsGroup] = field(default_factory=list)
    modificationTime: int = 0
    applicationVersion: str = ""

    @classmethod
    def current(cls):
        info = libraryInfo()
        assert info
        return cls(
            folders=[Folder(**folder) for folder in info["folders"]],
            smartFolders=[SmartFolder(**folder) for folder in info["smartFolders"]],
            quickAccess=[QuickAccess(**folder) for folder in info["quickAccess"]],
            tagsGroups=[TagsGroup(**folder) for folder in info["tagsGroups"]],
            modificationTime=info["modificationTime"],
            applicationVersion=info["applicationVersion"],
        )
    
