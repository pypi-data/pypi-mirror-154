from typing import Iterable, NoReturn, Sequence

from ..collection import Collection
from ..parser import ParserContext, ParseResult

def complete(names: Iterable[str], core: ParseResult, initial_context: ParserContext, collection: Collection) -> NoReturn: ...
def print_task_names(collection: Collection) -> None: ...
def print_completion_script(shell: str, names: Sequence[str]) -> None: ...
