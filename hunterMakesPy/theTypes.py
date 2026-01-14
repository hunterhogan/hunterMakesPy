"""I type, you type, we all `type` for `theTypes`."""
from typing import Protocol, Self, TypeAlias

identifierDotAttribute: TypeAlias = str
"""`str` (***str***ing) representing a dotted attribute identifier.

`TypeAlias` for a `str` `object` using dot notation to access an attribute, such as 'scipy.signal.windows'.

"""


class Ordinals(Protocol):
	"""Any Python `object` `type` that may be ordered before or after a comparable `object` `type` using a less-than-or-equal-to comparison."""

	def __le__(self, not_self_selfButSelfSelf_youKnow: Self, /) -> bool:
		"""Comparison by "***l***ess than or ***e***qual to"."""
		...
