import sys

def find_library(name: str) -> str | None: ...

if sys.platform == "win32":
    def find_msvcrt() -> str | None: ...
