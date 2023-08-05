from typing import Mapping, Sequence

_Cap = dict[str, str | int]

__all__ = ["getcaps", "findmatch"]

def findmatch(
    caps: Mapping[str, list[_Cap]], MIMEtype: str, key: str = ..., filename: str = ..., plist: Sequence[str] = ...
) -> tuple[str | None, _Cap | None]: ...
def getcaps() -> dict[str, list[_Cap]]: ...
