"""I type, you type, we all `type` for `theTypes`."""
from __future__ import annotations

from collections.abc import Hashable
from hunterMakesPy.theTypesCallableFunction import CallableFunction as CallableFunction
from typing import Protocol, Self, TypeAlias, TypeVar

identifierDotAttribute: TypeAlias = str
"""`str` (***str***ing) representing a dotted attribute identifier.

`TypeAlias` for a `str` `object` using dot notation to access an attribute, such as 'scipy.signal.windows'.
"""

ConcurrencyLimit: TypeAlias = bool | float | int | None

class Ordinals(Protocol):
	"""Any Python `object` `type` that may be ordered before or after a comparable `object` `type` by comparison operators."""

	def __le__(self: Self, not_self_selfButSelfSelf_youKnow: Self, /) -> bool:
		"""Comparison by "***l***ess than or ***e***qual to"."""
		...

	def __lt__(self: Self, otherSelfWhichIsNotAnOxymoron: Self, /) -> bool:
		"""Comparison by "***l***ess ***t***han"."""
		...

小于 = TypeVar('小于', bound=Ordinals)
文件 = TypeVar('文件', bound=Hashable)
文义 = TypeVar('文义')
