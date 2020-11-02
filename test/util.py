from typing import Callable, Optional, TypeVar


T = TypeVar('T')


def check_equality(a, aa, aaa, b, func=None):
    # type: (T, T, T, T, Optional[Callable[[T, T], bool]]) -> None
    def f(l, r):
        # type: (T, T) -> bool
        if not func:
            return l == r
        return func(l, r)

    def nf(l, r):
        # type: (T, T) -> bool
        return l != r

    assert f(a, a)
    assert f(a, aa)
    assert f(aa, a)
    assert f(a, aa) and f(aa, aaa) == f(a, aaa)
    assert not f(a, b)
    assert f(a, b) == f(b, a)
    assert f(a, b) == f(aa, b) == f(aaa, b)
    if func:
        assert not nf(a, a)
        assert not nf(a, aa)
        assert not nf(aa, a)
        assert not nf(a, aa) and nf(aa, aaa) == nf(a, aaa)
        assert nf(a, b)
        assert nf(a, b) == nf(b, a)
        assert nf(a, b) == nf(aa, b) == nf(aaa, b)


