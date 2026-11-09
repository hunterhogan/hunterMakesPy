"""Callables named by kind: functions, a bound method, and callable instances without `__name__`."""
from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING
import functools
import math
import operator
import textwrap

if TYPE_CHECKING:
	from collections.abc import Callable
	from typing import Any

callableItemGetter: operator.itemgetter[Any] = operator.itemgetter(2)
callablePartial: Callable[[int], int] = functools.partial(operator.add, 13)
functionBuiltin: Callable[..., int] = len
functionCached: Callable[[int], int] = functools.cache(math.factorial)
functionPurePython: Callable[[str], str] = textwrap.dedent
methodBoundPython: Callable[..., Fraction] = Fraction(3, 5).limit_denominator
