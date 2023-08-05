import sys
from _typeshed import Self
from datetime import datetime
from enum import Enum
from typing import IO, Any, Mapping, MutableMapping

if sys.version_info >= (3, 9):
    __all__ = ["InvalidFileException", "FMT_XML", "FMT_BINARY", "load", "dump", "loads", "dumps", "UID"]
elif sys.version_info >= (3, 8):
    __all__ = [
        "readPlist",
        "writePlist",
        "readPlistFromBytes",
        "writePlistToBytes",
        "Data",
        "InvalidFileException",
        "FMT_XML",
        "FMT_BINARY",
        "load",
        "dump",
        "loads",
        "dumps",
        "UID",
    ]
elif sys.version_info >= (3, 7):
    __all__ = [
        "readPlist",
        "writePlist",
        "readPlistFromBytes",
        "writePlistToBytes",
        "Data",
        "InvalidFileException",
        "FMT_XML",
        "FMT_BINARY",
        "load",
        "dump",
        "loads",
        "dumps",
    ]
else:
    __all__ = [
        "readPlist",
        "writePlist",
        "readPlistFromBytes",
        "writePlistToBytes",
        "Plist",
        "Data",
        "Dict",
        "InvalidFileException",
        "FMT_XML",
        "FMT_BINARY",
        "load",
        "dump",
        "loads",
        "dumps",
    ]

class PlistFormat(Enum):
    FMT_XML: int
    FMT_BINARY: int

FMT_XML = PlistFormat.FMT_XML
FMT_BINARY = PlistFormat.FMT_BINARY

if sys.version_info >= (3, 9):
    def load(fp: IO[bytes], *, fmt: PlistFormat | None = ..., dict_type: type[MutableMapping[str, Any]] = ...) -> Any: ...
    def loads(value: bytes, *, fmt: PlistFormat | None = ..., dict_type: type[MutableMapping[str, Any]] = ...) -> Any: ...

else:
    def load(
        fp: IO[bytes],
        *,
        fmt: PlistFormat | None = ...,
        use_builtin_types: bool = ...,
        dict_type: type[MutableMapping[str, Any]] = ...,
    ) -> Any: ...
    def loads(
        value: bytes,
        *,
        fmt: PlistFormat | None = ...,
        use_builtin_types: bool = ...,
        dict_type: type[MutableMapping[str, Any]] = ...,
    ) -> Any: ...

def dump(
    value: Mapping[str, Any] | list[Any] | tuple[Any, ...] | str | bool | float | bytes | datetime,
    fp: IO[bytes],
    *,
    fmt: PlistFormat = ...,
    sort_keys: bool = ...,
    skipkeys: bool = ...,
) -> None: ...
def dumps(
    value: Mapping[str, Any] | list[Any] | tuple[Any, ...] | str | bool | float | bytes | datetime,
    *,
    fmt: PlistFormat = ...,
    skipkeys: bool = ...,
    sort_keys: bool = ...,
) -> bytes: ...

if sys.version_info < (3, 9):
    def readPlist(pathOrFile: str | IO[bytes]) -> Any: ...
    def writePlist(value: Mapping[str, Any], pathOrFile: str | IO[bytes]) -> None: ...
    def readPlistFromBytes(data: bytes) -> Any: ...
    def writePlistToBytes(value: Mapping[str, Any]) -> bytes: ...

if sys.version_info < (3, 7):
    class _InternalDict(dict[str, Any]):
        def __getattr__(self, attr: str) -> Any: ...
        def __setattr__(self, attr: str, value: Any) -> None: ...
        def __delattr__(self, attr: str) -> None: ...

    class Dict(_InternalDict):  # deprecated
        def __init__(self, **kwargs: Any) -> None: ...

    class Plist(_InternalDict):  # deprecated
        def __init__(self, **kwargs: Any) -> None: ...
        @classmethod
        def fromFile(cls: type[Self], pathOrFile: str | IO[bytes]) -> Self: ...
        def write(self, pathOrFile: str | IO[bytes]) -> None: ...

if sys.version_info < (3, 9):
    class Data:
        data: bytes
        def __init__(self, data: bytes) -> None: ...

if sys.version_info >= (3, 8):
    class UID:
        data: int
        def __init__(self, data: int) -> None: ...
        def __index__(self) -> int: ...
        def __reduce__(self: Self) -> tuple[type[Self], tuple[int]]: ...
        def __hash__(self) -> int: ...
        def __eq__(self, other: object) -> bool: ...

class InvalidFileException(ValueError):
    def __init__(self, message: str = ...) -> None: ...
