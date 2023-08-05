from typing import Any

from .base import Bool, Convertible, Descriptor, Float, Integer, MinMax, NoneSet, Set, String

class Nested(Descriptor):
    nested: bool
    attribute: str
    def __set__(self, instance, value) -> None: ...
    def from_tree(self, node): ...
    def to_tree(self, tagname: Any | None = ..., value: Any | None = ..., namespace: Any | None = ...): ...

class NestedValue(Nested, Convertible): ...

class NestedText(NestedValue):
    def from_tree(self, node): ...
    def to_tree(self, tagname: Any | None = ..., value: Any | None = ..., namespace: Any | None = ...): ...

class NestedFloat(NestedValue, Float): ...
class NestedInteger(NestedValue, Integer): ...
class NestedString(NestedValue, String): ...

class NestedBool(NestedValue, Bool):
    def from_tree(self, node): ...

class NestedNoneSet(Nested, NoneSet): ...
class NestedSet(Nested, Set): ...
class NestedMinMax(Nested, MinMax): ...

class EmptyTag(Nested, Bool):
    def from_tree(self, node): ...
    def to_tree(self, tagname: Any | None = ..., value: Any | None = ..., namespace: Any | None = ...): ...
