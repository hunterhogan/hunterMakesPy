"""recipes.

========

- countby : Count elements of a collection by a key function
- partitionby : Partition a sequence according to a function
"""

from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from typing import Any, overload

__all__ = ("countby", "partitionby")

@overload
def countby[T, K](key: Callable[[T], K], seq: Iterable[T]) -> dict[K, int]: ...
@overload
def countby[V](key: Any, seq: Iterable[Sequence[V] | Mapping[Any, V]]) -> dict[V, int]: ...
def countby[T, K, V]( key: Callable[[T], K] | Any, seq: Iterable[T] | Iterable[Sequence[V] | Mapping[Any, V]] ) -> dict[K, int] | dict[V, int]:
	"""Count elements of a collection by a key function

	>>> countby(len, ['cat', 'mouse', 'dog'])
	{3: 2, 5: 1}

	>>> def iseven(x): return x % 2 == 0
	>>> countby(iseven, [1, 2, 3])  # doctest:+SKIP
	{True: 1, False: 2}

	Non-callable keys imply counting on a member.

	>>> countby(0, ('ab', 'ac', 'bc'))
	{'a': 2, 'b': 1}

	See Also
	--------
		groupby
	"""

class partitionby[T](Iterator[tuple[T, ...]]):
	"""Partition a sequence according to a function

	Partition `s` into a sequence of lists such that, when traversing
	`s`, every time the output of `func` changes a new list is started
	and that and subsequent items are collected into that list.

	>>> is_space = lambda c: c == " "
	>>> list(partitionby(is_space, "I have space"))
	[('I',), (' ',), ('h', 'a', 'v', 'e'), (' ',), ('s', 'p', 'a', 'c', 'e')]

	>>> is_large = lambda x: x > 10
	>>> list(partitionby(is_large, [1, 2, 1, 99, 88, 33, 99, -1, 5]))
	[(1, 2, 1), (99, 88, 33, 99), (-1, 5)]

	See Also
	--------
		partition
		groupby
		itertools.groupby
	"""
	def __init__(self, func: Callable[[T], Any], seq: Iterable[T]) -> None: ...
	def __iter__(self) -> partitionby[T]: ...
	def __next__(self) -> tuple[T, ...]: ...
