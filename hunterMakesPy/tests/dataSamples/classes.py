"""Classes whose instances exhibit one unusual behavior, named by that behavior."""
from __future__ import annotations

from collections import UserList
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from collections.abc import Iterator

class ListGrowsWhenIterated(UserList[int]):
	"""Append 89 each time iteration begins, so the length changes during iteration.

	An instance in a shared parameter grows with every consumer; every length still changes during iteration.
	"""

	def __iter__(self) -> Iterator[int]:
		self.append(89)
		return super().__iter__()

class StrReturnsNone:
	"""Return `None` from `__str__`, so `str(instance)` raises `TypeError`."""

	def __str__(self) -> str:
		return None  # pyright: ignore[reportReturnType] # ruff: ignore[invalid-str-return-type] # ty: ignore[invalid-return-type]

class StrReturnsNoneText:

	def __str__(self) -> str:
		return 'None'


class StrDividesByZero:
	"""Divide by zero in `__str__`, so `str(instance)` raises `ZeroDivisionError`."""

	def __str__(self) -> str:
		return str(13 // 0)
