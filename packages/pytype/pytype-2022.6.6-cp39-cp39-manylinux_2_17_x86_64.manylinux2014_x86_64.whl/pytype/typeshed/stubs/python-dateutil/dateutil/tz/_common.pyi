from datetime import datetime, timedelta, tzinfo
from typing import Any

def tzname_in_python2(namefunc): ...
def enfold(dt: datetime, fold: int = ...): ...

class _DatetimeWithFold(datetime):
    @property
    def fold(self): ...

class _tzinfo(tzinfo):
    def is_ambiguous(self, dt: datetime) -> bool: ...
    def fromutc(self, dt: datetime) -> datetime: ...

class tzrangebase(_tzinfo):
    def __init__(self) -> None: ...
    def utcoffset(self, dt: datetime | None) -> timedelta | None: ...
    def dst(self, dt: datetime | None) -> timedelta | None: ...
    def tzname(self, dt: datetime | None) -> str: ...
    def fromutc(self, dt: datetime) -> datetime: ...
    def is_ambiguous(self, dt: datetime) -> bool: ...
    __hash__: Any
    def __ne__(self, other): ...
    __reduce__: Any
