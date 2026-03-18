import collections.abc
import typing

__all__ = ["merge", "merge_with"]

@typing.overload
def merge_with[K, V]() -> typing.Callable[
    ..., dict[K, V] | collections.abc.MutableMapping[K, V]
]: ...
@typing.overload
def merge_with[K, V](
    func: typing.Callable[[list[V]], V], /
) -> typing.Callable[..., dict[K, V] | collections.abc.MutableMapping[K, V]]: ...
@typing.overload
def merge_with[K, V](
    func: typing.Callable[[list[V]], V],
    d: collections.abc.Mapping[K, V],
    /,
) -> dict[K, V]: ...
@typing.overload
def merge_with[K, V](
    func: typing.Callable[[list[V]], V],
    d: collections.abc.Mapping[K, V],
    d2: collections.abc.Mapping[K, V],
    /,
    *dicts: collections.abc.Mapping[K, V],
) -> dict[K, V]: ...
@typing.overload
def merge_with[K, V](
    func: typing.Callable[[list[V]], V],
    d: collections.abc.Mapping[K, V],
    d2: collections.abc.Mapping[K, V],
    /,
    *dicts: collections.abc.Mapping[K, V],
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V]],
) -> collections.abc.MutableMapping[K, V]: ...
@typing.overload
def merge_with[K, V](
    func: typing.Callable[[list[V]], V],
    /,
    *,
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V]],
) -> typing.Callable[..., collections.abc.MutableMapping[K, V]]: ...
def merge_with[K, V](
    func: typing.Callable[[list[V]], V] = ...,
    d: collections.abc.Mapping[K, V] = ...,
    *dicts: collections.abc.Mapping[K, V],
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V]] = ...,
) -> (
    dict[K, V]
    | collections.abc.MutableMapping[K, V]
    | typing.Callable[..., dict[K, V] | collections.abc.MutableMapping[K, V]]
):
    """Merge dictionaries and apply function to combined values

    A key may occur in more than one dict, and all values mapped from the key
    will be passed to the function as a list, such as func([val1, val2, ...]).

    >>> merge_with(sum, {1: 1, 2: 2}, {1: 10, 2: 20})
    {1: 11, 2: 22}

    >>> merge_with(first, {1: 1, 2: 2}, {2: 20, 3: 30})  # doctest: +SKIP
    {1: 1, 2: 2, 3: 30}

    See Also:
        merge
    """
    ...

@typing.overload
def merge[K, V]() -> typing.Callable[
    ..., dict[K, V] | collections.abc.MutableMapping[K, V]
]: ...
@typing.overload
def merge[K, V](d: collections.abc.Mapping[K, V], /) -> dict[K, V]: ...
@typing.overload
def merge[K, V](
    d: collections.abc.Mapping[K, V],
    d2: collections.abc.Mapping[K, V],
    /,
    *dicts: collections.abc.Mapping[K, V],
) -> dict[K, V]: ...
@typing.overload
def merge[K, V](
    d: collections.abc.Mapping[K, V],
    d2: collections.abc.Mapping[K, V],
    /,
    *dicts: collections.abc.Mapping[K, V],
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V]],
) -> collections.abc.MutableMapping[K, V]: ...
@typing.overload
def merge[K, V](
    *,
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V]],
) -> typing.Callable[..., collections.abc.MutableMapping[K, V]]: ...
def merge[K, V](
    d: collections.abc.Mapping[K, V] = ...,
    *dicts: collections.abc.Mapping[K, V],
    factory: typing.Callable[[], collections.abc.MutableMapping[K, V]] = ...,
) -> (
    dict[K, V]
    | collections.abc.MutableMapping[K, V]
    | typing.Callable[..., dict[K, V] | collections.abc.MutableMapping[K, V]]
):
    """Merge a collection of dictionaries

    >>> merge({1: 'one'}, {2: 'two'})
    {1: 'one', 2: 'two'}

    Later dictionaries have precedence

    >>> merge({1: 2, 3: 4}, {3: 3, 4: 4})
    {1: 2, 3: 3, 4: 4}

    See Also:
        merge_with
    """
    ...
