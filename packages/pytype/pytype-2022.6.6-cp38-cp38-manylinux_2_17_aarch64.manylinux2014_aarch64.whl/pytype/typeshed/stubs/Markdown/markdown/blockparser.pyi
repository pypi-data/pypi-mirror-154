from typing import Any, Iterable, TypeVar
from xml.etree.ElementTree import Element, ElementTree

from . import Markdown
from .util import Registry

_T = TypeVar("_T")

class State(list[_T]):
    def set(self, state: _T) -> None: ...
    def reset(self) -> None: ...
    def isstate(self, state: _T) -> bool: ...

class BlockParser:
    blockprocessors: Registry
    state: State[Any]  # TODO: possible to get rid of Any?
    md: Markdown
    def __init__(self, md: Markdown) -> None: ...
    @property
    def markdown(self): ...  # deprecated
    root: Element
    def parseDocument(self, lines: Iterable[str]) -> ElementTree: ...
    def parseChunk(self, parent: Element, text: str) -> None: ...
    def parseBlocks(self, parent: Element, blocks: list[str]) -> None: ...
