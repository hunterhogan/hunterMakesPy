# See #166: https://github.com/pytoolz/toolz/issues/166
# See #173: https://github.com/pytoolz/toolz/pull/173
from collections.abc import Callable, Hashable, Iterable, Iterator
from typing import overload, override

class EqualityHashKey:
    """Create a hash key that uses equality comparisons between items.

    This may be used to create hash keys for otherwise unhashable types:

    >>> from toolz import curry
    >>> EqualityHashDefault = curry(EqualityHashKey, None)
    >>> set(map(EqualityHashDefault, [[], (), [1], [1]]))  # doctest: +SKIP
    {=[]=, =()=, =[1]=}

    **Caution:** adding N ``EqualityHashKey`` items to a hash container
    may require O(N**2) operations, not O(N) as for typical hashable types.
    Therefore, a suitable key function such as ``tuple`` or ``frozenset``
    is usually preferred over using ``EqualityHashKey`` if possible.

    The ``key`` argument to ``EqualityHashKey`` should be a function or
    index that returns a hashable object that effectively distinguishes
    unequal items.  This helps avoid the poor scaling that occurs when
    using the default key.  For example, the above example can be improved
    by using a key function that distinguishes items by length or type:

    >>> EqualityHashLen = curry(EqualityHashKey, len)
    >>> EqualityHashType = curry(EqualityHashKey, type)  # this works too
    >>> set(map(EqualityHashLen, [[], (), [1], [1]]))  # doctest: +SKIP
    {=[]=, =()=, =[1]=}

    ``EqualityHashKey`` is convenient to use when a suitable key function
    is complicated or unavailable.  For example, the following returns all
    unique values based on equality:

    >>> from toolz import unique
    >>> vals = [[], [], (), [1], [1], [2], {}, {}, {}]
    >>> list(unique(vals, key=EqualityHashDefault))
    [[], (), [1], [2], {}]

    **Warning:** don't change the equality value of an item already in a hash
    container.  Unhashable types are unhashable for a reason.  For example:

    >>> L1 = [1] ; L2 = [2]
    >>> s = set(map(EqualityHashDefault, [L1, L2]))
    >>> s  # doctest: +SKIP
    {=[1]=, =[2]=}

    >>> L1[0] = 2  # Don't do this!  ``s`` now has duplicate items!
    >>> s  # doctest: +SKIP
    {=[2]=, =[2]=}

    Although this may appear problematic, immutable data types is a common
    idiom in functional programming, and``EqualityHashKey`` easily allows
    the same idiom to be used by convention rather than strict requirement.

    See Also
    --------
        identity
    """

    def __init__[T](
        self, key: Callable[[T], Hashable] | int | None, item: T
    ) -> None: ...
    @override
    def __hash__(self) -> int: ...
    @override
    def __eq__(self, other: object) -> bool: ...
    @override
    def __ne__(self, other: object) -> bool: ...

# See issue #293: https://github.com/pytoolz/toolz/issues/239
@overload
def unzip(seq: Iterable[tuple[()]]) -> tuple[()]: ...
@overload
def unzip[T1](
    seq: Iterable[tuple[T1]],
) -> tuple[Iterator[T1]]: ...
@overload
def unzip[T1, T2](
    seq: Iterable[tuple[T1, T2]],
) -> tuple[Iterator[T1], Iterator[T2]]: ...
@overload
def unzip[T1, T2, T3](
    seq: Iterable[tuple[T1, T2, T3]],
) -> tuple[
    Iterator[T1],
    Iterator[T2],
    Iterator[T3],
]: ...
@overload
def unzip[T1, T2, T3, T4](
    seq: Iterable[tuple[T1, T2, T3, T4]],
) -> tuple[
    Iterator[T1],
    Iterator[T2],
    Iterator[T3],
    Iterator[T4],
]: ...
@overload
def unzip[T](
    seq: Iterable[tuple[T, ...]],
) -> tuple[Iterator[T], ...]: ...

# Implementation signature
def unzip[T](
    seq: Iterable[tuple[T, ...]],
) -> tuple[Iterator[T], ...]:
    """Inverse of ``zip``

    >>> a, b = unzip([('a', 1), ('b', 2)])
    >>> list(a)
    ['a', 'b']
    >>> list(b)
    [1, 2]

    Unlike the naive implementation ``def unzip(seq): zip(*seq)`` this
    implementation can handle an infinite sequence ``seq``.

    Caveats:

    * The implementation uses ``tee``, and so can use a significant amount
      of auxiliary storage if the resulting iterators are consumed at
      different times.

    * The inner sequence cannot be infinite. In Python 3 ``zip(*seq)`` can be
      used if ``seq`` is a finite sequence of infinite sequences.

    """
