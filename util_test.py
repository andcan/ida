from hypothesis import given
from hypothesis.strategies import lists, integers
from typing import Sequence
from .test.util import check_equality
from .util import unordered_equals


@given(xs=lists(integers()), x=integers()) # type: ignore
def test_unordered_equals(xs, x):
    # type: (Sequence[int], int) -> None
    ys = list(xs)
    zs = list(reversed(xs))
    ws = list(xs)
    ws.append(x)

    check_equality(xs, ys, zs, ws, unordered_equals)
