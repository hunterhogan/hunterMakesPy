from collections.abc import Callable, Mapping, MutableMapping
from typing import overload

__all__ = ["merge", "merge_with"]

@overload
def merge_with[K, V]() -> Callable[
    ..., dict[K, V] | MutableMapping[K, V]
]: ...
@overload
def merge_with[K, V](
    func: Callable[[list[V]], V], /
) -> Callable[..., dict[K, V] | MutableMapping[K, V]]: ...
@overload
def merge_with[K, V](
    func: Callable[[list[V]], V],
    d: Mapping[K, V],
    /,
) -> dict[K, V]: ...
@overload
def merge_with[K, V](
    func: Callable[[list[V]], V],
    d: Mapping[K, V],
    d2: Mapping[K, V],
    /,
    *dicts: Mapping[K, V],
) -> dict[K, V]: ...
@overload
def merge_with[K, V](
    func: Callable[[list[V]], V],
    d: Mapping[K, V],
    d2: Mapping[K, V],
    /,
    *dicts: Mapping[K, V],
    factory: Callable[[], MutableMapping[K, V]],
) -> MutableMapping[K, V]: ...
@overload
def merge_with[K, V](
    func: Callable[[list[V]], V],
    /,
    *,
    factory: Callable[[], MutableMapping[K, V]],
) -> Callable[..., MutableMapping[K, V]]: ...
def merge_with[K, V](
    func: Callable[[list[V]], V] = ...,
    d: Mapping[K, V] = ...,
    *dicts: Mapping[K, V],
    factory: Callable[[], MutableMapping[K, V]] = ...,
) -> (
    dict[K, V]
    | MutableMapping[K, V]
    | Callable[..., dict[K, V] | MutableMapping[K, V]]
):
    """Merge dictionaries and apply function to combined values

    A key may occur in more than one dict, and all values mapped from the key
    will be passed to the function as a list, such as func([val1, val2, ...]).

    >>> merge_with(sum, {1: 1, 2: 2}, {1: 10, 2: 20})
    {1: 11, 2: 22}

    >>> merge_with(first, {1: 1, 2: 2}, {2: 20, 3: 30})  # doctest: +SKIP
    {1: 1, 2: 2, 3: 30}

    See Also
    --------
        merge
    """

@overload
def merge[K, V]() -> Callable[
    ..., dict[K, V] | MutableMapping[K, V]
]: ...
@overload
def merge[K, V](d: Mapping[K, V], /) -> dict[K, V]: ...
@overload
def merge[K, V](
    d: Mapping[K, V],
    d2: Mapping[K, V],
    /,
    *dicts: Mapping[K, V],
) -> dict[K, V]: ...
@overload
def merge[K, V](
    d: Mapping[K, V],
    d2: Mapping[K, V],
    /,
    *dicts: Mapping[K, V],
    factory: Callable[[], MutableMapping[K, V]],
) -> MutableMapping[K, V]: ...
@overload
def merge[K, V](
    *,
    factory: Callable[[], MutableMapping[K, V]],
) -> Callable[..., MutableMapping[K, V]]: ...
def merge[K, V](
    d: Mapping[K, V] = ...,
    *dicts: Mapping[K, V],
    factory: Callable[[], MutableMapping[K, V]] = ...,
) -> (
    dict[K, V]
    | MutableMapping[K, V]
    | Callable[..., dict[K, V] | MutableMapping[K, V]]
):
    """Merge a collection of dictionaries

    >>> merge({1: 'one'}, {2: 'two'})
    {1: 'one', 2: 'two'}

    Later dictionaries have precedence

    >>> merge({1: 2, 3: 4}, {3: 3, 4: 4})
    {1: 2, 3: 3, 4: 4}

    See Also
    --------
        merge_with
    """
