import pathlib

class PlaysoundException(Exception): ...

def playsound(sound: str | pathlib.Path, block: bool = ...) -> None: ...
