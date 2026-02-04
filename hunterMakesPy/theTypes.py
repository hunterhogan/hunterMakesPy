"""I type, you type, we all `type` for `theTypes`."""
from hunterMakesPy.Z0Z_CallableFunction import CallableFunction as CallableFunction
from typing import Protocol, Self

type identifierDotAttribute = str
"""`str` (***str***ing) representing a dotted attribute identifier.

`TypeAlias` for a `str` `object` using dot notation to access an attribute, such as 'scipy.signal.windows'.
"""

class Ordinals(Protocol):
	"""Any Python `object` `type` that may be ordered before or after a comparable `object` `type` by comparison operators."""

	def __le__(self: Self, not_self_selfButSelfSelf_youKnow: Self, /) -> bool:
		"""Comparison by "***l***ess than or ***e***qual to"."""
		...

	def __lt__(self: Self, otherSelfWhichIsNotAnOxymoron: Self, /) -> bool:
		"""Comparison by "***l***ess ***t***han"."""
		...
