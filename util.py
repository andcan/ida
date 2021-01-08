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


def format_query(q) -> str:
    s = repr(q)
    formatted = ''
    ident = 0
    for i in range(len(s)):
        if s[i] == '[':
            ident += 1
            formatted += '[\n' + ('  ' * ident)
        elif s[i] == ']':
            ident -= 1
            formatted += '\n' + ('  ' * ident) + ']'
        else:
            formatted += s[i]
    return formatted
