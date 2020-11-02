from typing import Sequence, TypeVar

T = TypeVar('T')


def unordered_equals(xs, ys):
    # type: (Sequence[T], Sequence[T]) -> bool
    ys = list(ys)
    try:
        for x in xs:
            ys.remove(x)
    except ValueError:
        return False
    return len(ys) == 0
