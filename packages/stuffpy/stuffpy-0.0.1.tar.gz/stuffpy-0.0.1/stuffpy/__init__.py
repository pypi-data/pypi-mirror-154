"""All sorts of cool stuff"""
import sys
from collections.abc import Callable, Sequence, Iterator
from typing import TypeAlias
import traceback

Write: TypeAlias = Callable[[str], int]
Flush: TypeAlias = Callable[[], None]
WriteFlush: TypeAlias = tuple[Write, Flush]


class Disable:
    """A context manager to temporarily disable stdout
     and specified exceptions"""
    def __init__(self, errors: tuple[BaseException]) -> None:
        self.errors = errors

    def __enter__(self) -> WriteFlush:
        self.writer, self.flusher = sys.stdout.write, sys.stdout.flush
        sys.stdout.write = lambda text: None
        sys.stdout.flush = lambda: None
        return self.writer, self.flusher

    def __exit__(self, exc_type: type, exc_val: BaseException,
                 exc_tb: traceback.StackSummary) -> bool | None:
        sys.stdout.write, sys.stdout.flush = self.writer, self.flusher
        if exc_type:
            if exc_type in self.errors:
                return True
            else:
                for error in self.errors:
                    if issubclass(exc_type, error):  # type: ignore
                        return True
                return False


def parallel(iterable: Sequence | Sequence[Sequence],
             *iterables: Sequence, func: Callable = lambda a, b: (a, b),
             strict: bool = True) -> Iterator:
    """Parallelize an iterable or many arguments"""
    if not iterables:
        if strict:
            length = len(iterable[0])
            for i, it in enumerate(iterable, 1):
                if len(it) > length:
                    msg = f'parallel() argument {i} is longer than argument 1'
                    raise ValueError(msg)
                elif len(it) < length:
                    msg = f'parallel() argument {i} is shorter than argument 1'
                    raise ValueError(msg)
        return map(func, *iterable)
    else:
        if strict:
            length = len(iterable)
            for i, it in enumerate(iterables, 1):
                if len(it) > length:
                    msg = f'parallel() argument {i} is longer than argument 1'
                    raise ValueError(msg)
                elif len(it) < length:
                    msg = f'parallel() argument {i} is shorter than argument 1'
                    raise ValueError(msg)
        return map(func, iterable, *iterables)
