"""Provide immutable, functional-style operations on `Mapping`[1] objects.

(AI generated docstring)

You can use this module to transform, filter, retrieve from, and merge `Mapping`[1] objects
without modifying the source mapping. Each function returns a new mapping created by a
`factory` argument that defaults to `dict`. Functions that navigate nested structures accept
a `Sequence`[1] of keys to specify the path.

Contents
--------
Classes
    SupportsGetItem
        Structural type constraint for objects that support item retrieval via `__getitem__`.

Functions
    assoc
        Create a new `Mapping` with `key` associated with `value`.
    assoc_in
        Create a new `MutableMapping` from `d` with `value` at the path specified by `keys`.
    dissoc
        Create a new `MutableMapping` from `d` with the specified `keys` removed.
    get_in
        Retrieve a value from a potentially nested collection using a sequence of keys.
    itemfilter
        Retain only items from `d` whose key-value pairs satisfy `predicate` and return a new `Mapping`.
    itemmap
        Apply `func` to all items of `d` and return a new `Mapping` with the transformed items.
    keyfilter
        Retain only items from `d` whose keys satisfy `predicate` and return a new `Mapping`.
    keymap
        Apply `func` to all keys of `d` and return a new `Mapping` with the transformed keys.
    merge
        Merge a collection of `Mapping` objects and return a new `Mapping`.
    merge_with
        Merge `Mapping` objects and apply a `Callable` to combined values.
    update_in
        Apply a `Callable` to a value at a nested path in a `Mapping`.
    valfilter
        Retain only items from `d` whose values satisfy `predicate` and return a new `Mapping`.
    valmap
        Apply `func` to all values of `d` and return a new `Mapping` with the transformed values.

References
----------
[1] Python `collections.abc` module
    https://docs.python.org/3/library/collections.abc.html
"""
from collections import defaultdict, deque
from collections.abc import Callable, Mapping, MutableMapping, Sequence
from functools import reduce
from typing import Any, Literal, overload, Protocol
import copy
import operator

__all__ = ('assoc', 'assoc_in', 'dissoc', 'get_in', 'itemfilter', 'itemmap', 'keyfilter', 'keymap', 'merge', 'merge_with', 'update_in', 'valfilter', 'valmap')

class SupportsGetItem[K, V](Protocol):
	def __getitem__(self, key: K, /) -> V: ...

@overload
def assoc[K, V](d: Mapping[K, V], key: K, value: V) -> dict[K, V]: ...
@overload
def assoc[K, V](d: Mapping[K, V], key: K, value: V, factory: Callable[[], MutableMapping[K, V]]) -> MutableMapping[K, V]: ...
def assoc[K, V](d: Mapping[K, V], key: K, value: V, factory: Callable[[], MutableMapping[K, V]] = dict) -> MutableMapping[K, V]:
	"""Create a new `Mapping`[1] with `key` associated with `value`.

	You can use `assoc` (***assoc***iate) to copy `d` (***d***ictionary) to a new `Mapping` created by
	`factory` and assign `value` to `key`. `assoc` does not change `d`.

	Parameters
	----------
	d : Mapping[K, V]
		Source `Mapping`.
	key : K
		`key` that `assoc` inserts or replaces.
	value : V
		`value` that `assoc` assigns to `key`.
	factory : Callable[[], MutableMapping[K, V]] = dict
		`Callable` that creates the `MutableMapping`[1] to `return`.

	Returns
	-------
	mappingUpdated : MutableMapping[K, V]
		New `Mapping` with `key` associated to `value`.

	Examples
	--------
	>>> assoc({}, 'a', 1)
	{'a': 1}
	>>> assoc({'a': 1}, 'a', 3)
	{'a': 3}
	>>> assoc({'a': 1}, 'b', 3)
	{'a': 1, 'b': 3}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	d2: MutableMapping[K, V] = factory()
	d2.update(d)
	d2[key] = value
	return d2

@overload
def assoc_in[K, V](d: Mapping[K, V], keys: Sequence[K], value: V) -> dict[K, V]: ...
@overload
def assoc_in[K, V](d: Mapping[K, V], keys: Sequence[K], value: V, factory: Callable[[], MutableMapping[K, V]]) -> MutableMapping[K, V]: ...
def assoc_in[K, V](d: Mapping[K, V], keys: Sequence[K], value: V, factory: Callable[[], MutableMapping[K, V]] = dict) -> MutableMapping[K, V]:
	"""Create a new `MutableMapping` from `d` with `value` at the path specified by `keys`.

	(AI generated docstring)

	You can use `assoc_in` to produce a copy of `d` with `value` placed at the nested
	location given by `keys`. `assoc_in` creates intermediate `MutableMapping` instances
	as needed when a key in `keys` is absent from `d`. `assoc_in` does not mutate `d` or
	any nested `Mapping` within `d`.

	Parameters
	----------
	d : Mapping[K, V]
		Source `Mapping`.
	keys : Iterable[K]
		Non-empty sequence of keys specifying the nested path to the target location in `d`.
	value : V
		The value to place at the location specified by `keys`.
	factory : Callable[[], MutableMapping[K, V]] = dict
		`Callable` that creates each new `MutableMapping`[1] in the result.

	Returns
	-------
	mappingUpdated : MutableMapping[K, V]
		New `MutableMapping` based on `d` with `value` at the path specified by `keys`.

	See Also
	--------
	update_in : Apply a `Callable` to a value at a nested path in a `Mapping`.
	get_in : Retrieve a value at a nested path in a `Mapping`.
	assoc : Create a new `Mapping` from `d` with one key associated to a value.

	Examples
	--------
	>>> assoc_in({'a': 1}, ['a'], 2)
	{'a': 2}
	>>> assoc_in({'a': {'b': 1}}, ['a', 'b'], 2)
	{'a': {'b': 2}}
	>>> assoc_in({}, ['a', 'b'], 1)
	{'a': {'b': 1}}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	return update_in(d, keys, lambda _x: value, value, factory)

@overload
def dissoc[K, V](d: Mapping[K, V], *keys: K) -> dict[K, V]: ...
@overload
def dissoc[K, V](d: Mapping[K, V], *keys: K, factory: Callable[[], MutableMapping[K, V]]) -> MutableMapping[K, V]: ...
def dissoc[K, V](d: Mapping[K, V], *keys: K, factory: Callable[[], MutableMapping[K, V]] = dict) -> MutableMapping[K, V]:
	"""Create a new `MutableMapping`[1] from `d` with the specified `keys` removed.

	(AI generated docstring)

	You can use `dissoc` (***dissoc***iate) to copy `d` (***d***ictionary) to a new `MutableMapping`
	created by `factory`, then remove each key in `keys` from the result. `dissoc` does not change
	`d`. Keys in `keys` that are absent from `d` are silently ignored.

	Parameters
	----------
	d : Mapping[K, V]
		Source `Mapping`.
	*keys : K
		Keys to remove from `d` in the returned `MutableMapping`.
	factory : Callable[[], MutableMapping[K, V]] = dict
		`Callable` that creates the `MutableMapping`[1] to `return`.

	Returns
	-------
	mappingReduced : MutableMapping[K, V]
		New `MutableMapping` containing all items from `d` except those whose keys are in `keys`.

	Algorithm Details
	-----------------
	`dissoc` selects between two strategies based on the ratio of removed keys to total keys.

	When fewer than 60% of keys are removed, `dissoc` copies all items from `d` and then
	deletes the specified keys one by one.

	When 60% or more of keys are removed, `dissoc` computes the set of remaining keys and
	copies only those items to the result, avoiding unnecessary copy-and-delete operations.

	See Also
	--------
	assoc : Create a new `MutableMapping` from `d` with one key associated to a value.

	Examples
	--------
	>>> dissoc({'x': 1, 'y': 2}, 'y')
	{'x': 1}
	>>> dissoc({'x': 1, 'y': 2}, 'y', 'x')
	{}
	>>> dissoc({'x': 1}, 'y') # Ignores missing keys
	{'x': 1}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	d2: MutableMapping[K, V] = factory()
	if len(keys) < len(d) * 0.6:
		d2.update(d)
		for key in keys:
			if key in d2:
				del d2[key]
	else:
		remaining: set[K] = set(d)
		remaining.difference_update(keys)
		for k in remaining:
			d2[k] = d[k]
	return d2

@overload
def get_in[K, V](keys: Sequence[K], coll: SupportsGetItem[K, V], default: None = None, *, no_default: Literal[True]) -> V: ...
@overload
def get_in[K, V](keys: Sequence[K], coll: SupportsGetItem[K, V], default: None = None, no_default: bool = False) -> V | None: ...  # noqa: FBT001, FBT002
@overload
def get_in[K, V](keys: Sequence[K], coll: SupportsGetItem[K, V], default: V, no_default: bool = False) -> V: ...  # noqa: FBT001, FBT002
def get_in[K, V](keys: Sequence[K], coll: SupportsGetItem[K, V], default: V | None = None, no_default: bool = False) -> V | None:  # noqa: FBT001, FBT002
	"""Retrieve a value from a potentially nested `coll` (***coll***ection) using a `Sequence` of `keys`.

	(AI generated docstring)

	You can use `get_in` to navigate into a nested `coll` (***coll***ection) by following a
	sequence of `keys`. `get_in` applies each key in `keys` sequentially using
	`operator.getitem`[1]. If the path does not exist, `get_in` returns `default`. If
	`no_default` is `True`, `get_in` re-raises the original exception instead of returning
	`default`.

	Parameters
	----------
	keys : Sequence[K]
		Sequence of keys that describes the path to traverse in `coll`.
	coll : SupportsGetItem[K, V]
		Collection to traverse. `get_in` applies each key in `keys` to the current `coll`
		using `operator.getitem`[1], so `coll` can be any nested structure such as a `dict`
		or `list`.
	default : V | None = None
		Value to return when the path in `keys` does not exist in `coll`.
	no_default : bool = False
		When `True`, re-raise the original `KeyError`, `IndexError`, or `TypeError`
		instead of returning `default`.

	Returns
	-------
	value : V | None
		The value at the nested path in `coll`, or `default` if the path does not exist.

	Raises
	------
	KeyError
		When `no_default` is `True` and a key is missing from a mapping.
	IndexError
		When `no_default` is `True` and an index is out of range.
	TypeError
		When `no_default` is `True` and a key type is incompatible with `coll`.

	See Also
	--------
	itertoolz.get : Retrieve a value or values from a collection.
	operator.getitem : Return the value at a given key in a collection.
	assoc_in : Create a new `Mapping` from `d` with a value at a nested path.
	update_in : Apply a `Callable` to a value at a nested path in a `Mapping`.

	Examples
	--------
	>>> transaction = {'name': 'Alice',
	...                'purchase': {'items': ['Apple', 'Orange'],
	...                             'costs': [0.50, 1.25]},
	...                'credit card': '5555-1234-1234-1234'}
	>>> get_in(['purchase', 'items', 0], transaction)
	'Apple'
	>>> get_in(['name'], transaction)
	'Alice'
	>>> get_in(['purchase', 'total'], transaction)
	>>> get_in(['purchase', 'items', 'apple'], transaction)
	>>> get_in(['purchase', 'items', 10], transaction)
	>>> get_in(['purchase', 'total'], transaction, 0)
	0
	>>> get_in(['y'], {}, no_default=True)
	Traceback (most recent call last):
		...
	KeyError: 'y'

	References
	----------
	[1] Python `operator` module
		https://docs.python.org/3/library/operator.html#operator.getitem
	"""
	try:
		return reduce(operator.getitem, keys, coll) # pyright: ignore[reportReturnType, reportArgumentType]
	except (KeyError, IndexError, TypeError):
		if no_default:
			raise
		return default

@overload
def itemfilter[K, V](predicate: Callable[[tuple[K, V]], bool], d: Mapping[K, V]) -> dict[K, V]: ...
@overload
def itemfilter[K, V](predicate: Callable[[tuple[K, V]], bool], d: Mapping[K, V], factory: Callable[[], MutableMapping[K, V]]) -> MutableMapping[K, V]: ...
def itemfilter[K, V](predicate: Callable[[tuple[K, V]], bool], d: Mapping[K, V], factory: Callable[[], MutableMapping[K, V]] = dict) -> MutableMapping[K, V]:
	"""Retain only items from `d` whose key-value pairs satisfy `predicate` and return a new `Mapping`.

	(AI generated docstring)

	You can use `itemfilter` to select items from `d` (***d***ictionary) by both key and value
	simultaneously. `itemfilter` calls `predicate` with each item yielded by `d.items()`. Each
	item is passed to `predicate` as a `tuple[K, V]`. `itemfilter` inserts each item for which
	`predicate` returns `True` into a new `MutableMapping`[1] created by `factory`. `itemfilter`
	does not change `d`.

	Parameters
	----------
	predicate : Callable[[tuple[K, V]], bool]
		`Callable` applied to each item of `d`. Each item is passed to `predicate` as a
		`tuple[K, V]`, and `predicate` must return `True` for the item to be retained.
	d : Mapping[K, V]
		Source `Mapping`[1]. `itemfilter` reads all items from `d` and does not change `d`.
	factory : Callable[[], MutableMapping[K, V]] = dict
		`Callable` that creates the `MutableMapping`[1] to `return`.

	Returns
	-------
	mappingFiltered : MutableMapping[K, V]
		New `MutableMapping` created by `factory` containing only items from `d` for which
		`predicate` returns `True`.

	See Also
	--------
	keyfilter : Retain only items from `d` whose keys satisfy `predicate` and return a new `Mapping`.
	valfilter : Retain only items from `d` whose values satisfy `predicate` and return a new `Mapping`.
	itemmap : Apply a `Callable` to all items of a `Mapping` and return a new `Mapping`.

	Examples
	--------
	>>> def isvalid(item):
	...     k, v = item
	...     return k % 2 == 0 and v < 4

	>>> d = {1: 2, 2: 3, 3: 4, 4: 5}
	>>> itemfilter(isvalid, d)
	{2: 3}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	rv: MutableMapping[K, V] = factory()
	for item in d.items():
		if predicate(item):
			k, v = item
			rv[k] = v
	return rv

@overload
def itemmap[K, V, L, W](func: Callable[[tuple[K, V]], tuple[L, W]], d: Mapping[K, V]) -> dict[L, W]: ...
@overload
def itemmap[K, V, L, W](func: Callable[[tuple[K, V]], tuple[L, W]], d: Mapping[K, V], factory: Callable[[], MutableMapping[L, W]]) -> MutableMapping[L, W]: ...
def itemmap[K, V, L, W](func: Callable[[tuple[K, V]], tuple[L, W]], d: Mapping[K, V], factory: Callable[[], MutableMapping[L, W]] = dict) -> MutableMapping[L, W]:
	"""Apply `func` to all items of `d` and return a new `Mapping` with the transformed items.

	(AI generated docstring)

	You can use `itemmap` to transform all keys and values in `d` simultaneously without
	changing `d`. `itemmap` applies `func` to each item yielded by `d.items()`. Each item
	is passed to `func` as a `tuple[K, V]`, and `func` must return a `tuple[L, W]`. `itemmap`
	inserts each returned `tuple` as a new key-value pair in a `MutableMapping`[1] created
	by `factory`.

	Parameters
	----------
	func : Callable[[tuple[K, V]], tuple[L, W]]
		`Callable` applied to each item of `d`. Each item of `d` is passed to `func` as a
		`tuple[K, V]`, and `func` must return a `tuple[L, W]` containing the new key and value.
	d : Mapping[K, V]
		Source `Mapping`[1]. `itemmap` reads all items from `d` and does not change `d`.
	factory : Callable[[], MutableMapping[L, W]] = dict
		`Callable` that creates the `MutableMapping`[1] to `return`.

	Returns
	-------
	mappingTransformed : MutableMapping[L, W]
		New `MutableMapping` created by `factory` populated with each `tuple[L, W]` returned
		by `func`.

	See Also
	--------
	keymap : Apply a `Callable` to all keys of a `Mapping` and return a new `Mapping`.
	valmap : Apply a `Callable` to all values of a `Mapping` and return a new `Mapping`.

	Examples
	--------
	>>> accountids = {'Alice': 10, 'Bob': 20}
	>>> itemmap(reversed, accountids)  # doctest: +SKIP
	{10: 'Alice', 20: 'Bob'}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	rv: MutableMapping[L, W] = factory()
	rv.update(map(func, d.items()))
	return rv

@overload
def keyfilter[K, V](predicate: Callable[[K], bool], d: Mapping[K, V]) -> dict[K, V]: ...
@overload
def keyfilter[K, V](predicate: Callable[[K], bool], d: Mapping[K, V], factory: Callable[[], MutableMapping[K, V]]) -> MutableMapping[K, V]: ...
def keyfilter[K, V](predicate: Callable[[K], bool], d: Mapping[K, V], factory: Callable[[], MutableMapping[K, V]] = dict) -> MutableMapping[K, V]:
	"""Retain only items from `d` whose keys satisfy `predicate` and return a new `Mapping`.

	(AI generated docstring)

	You can use `keyfilter` to select items from `d` (***d***ictionary) by their keys. `keyfilter`
	calls `predicate` with each key yielded by `d.keys()`. `keyfilter` inserts each item whose
	key causes `predicate` to return `True` into a new `MutableMapping`[1] created by `factory`.
	`keyfilter` does not change `d`.

	Parameters
	----------
	predicate : Callable[[K], bool]
		`Callable` applied to each key of `d`. `keyfilter` keeps each item for which `predicate`
		returns `True`.
	d : Mapping[K, V]
		Source `Mapping`[1]. `keyfilter` reads all items from `d` and does not change `d`.
	factory : Callable[[], MutableMapping[K, V]] = dict
		`Callable` that creates the `MutableMapping`[1] to `return`.

	Returns
	-------
	mappingFiltered : MutableMapping[K, V]
		New `MutableMapping` created by `factory` containing only items from `d` whose keys
		cause `predicate` to return `True`.

	See Also
	--------
	valfilter : Retain only items from `d` whose values satisfy `predicate` and return a new `Mapping`.
	itemfilter : Retain only items from `d` whose key-value pairs satisfy `predicate` and return a new `Mapping`.
	keymap : Apply a `Callable` to all keys of a `Mapping` and return a new `Mapping`.

	Examples
	--------
	>>> iseven = lambda x: x % 2 == 0
	>>> d = {1: 2, 2: 3, 3: 4, 4: 5}
	>>> keyfilter(iseven, d)
	{2: 3, 4: 5}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	rv: MutableMapping[K, V] = factory()
	for k, v in d.items():
		if predicate(k):
			rv[k] = v
	return rv

@overload
def keymap[K, V, L](func: Callable[[K], L], d: Mapping[K, V]) -> dict[L, V]: ...
@overload
def keymap[K, V, L](func: Callable[[K], L], d: Mapping[K, V], factory: Callable[[], MutableMapping[L, V]]) -> MutableMapping[L, V]: ...
def keymap[K, V, L](func: Callable[[K], L], d: Mapping[K, V], factory: Callable[[], MutableMapping[L, V]] = dict) -> MutableMapping[L, V]:
	"""Apply `func` to all keys of `d` and return a new `Mapping` with the transformed keys.

	(AI generated docstring)

	You can use `keymap` to transform all keys in `d` without changing `d`. `keymap` applies
	`func` to each key yielded by `d.keys()` and builds a new `MutableMapping`[1] created by
	`factory`, associating each transformed key with the corresponding original value of `d`.

	Parameters
	----------
	func : Callable[[K], L]
		`Callable` applied to each key of `d`. Each key of `d` is passed to `func`
		individually, and `func` returns the corresponding transformed key.
	d : Mapping[K, V]
		Source `Mapping`[1]. `keymap` reads all keys from `d` and does not change `d`.
	factory : Callable[[], MutableMapping[L, V]] = dict
		`Callable` that creates the `MutableMapping`[1] to `return`.

	Returns
	-------
	mappingTransformed : MutableMapping[L, V]
		New `MutableMapping` created by `factory` in which each key from `d` is replaced by
		the result of applying `func` to that key, associated with the original value of `d`.

	See Also
	--------
	valmap : Apply a `Callable` to all values of a `Mapping` and return a new `Mapping`.
	itemmap : Apply a `Callable` to all items of a `Mapping` and return a new `Mapping`.

	Examples
	--------
	>>> bills = {'Alice': [20, 15, 30], 'Bob': [10, 35]}
	>>> keymap(str.lower, bills)  # doctest: +SKIP
	{'alice': [20, 15, 30], 'bob': [10, 35]}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	rv: MutableMapping[L, V] = factory()
	rv.update(zip(map(func, d.keys()), d.values(), strict=True))
	return rv

@overload
def merge[K, V](*dicts: Mapping[K, V]) -> dict[K, V]: ...
@overload
def merge[K, V](*dicts: Mapping[K, V], factory: Callable[[], MutableMapping[K, V]]) -> MutableMapping[K, V]: ...
def merge[K, V](*dicts: Mapping[K, V], factory: Callable[[], MutableMapping[K, V]] = dict) -> MutableMapping[K, V]:
	"""Merge a collection of dictionaries and return a new `Mapping`.

	(AI generated docstring)

	You can use `merge` to combine two or more `Mapping`[1] objects into a single new `Mapping`.
	`merge` calls `factory` to create the result, then updates it in order with each `Mapping` in
	`dicts`. When the same key appears in more than one element, the value from the later element
	takes precedence. You can also pass a single `Iterable[Mapping[K, V]]` as the sole positional
	argument instead of multiple `Mapping` arguments.

	Parameters
	----------
	*dicts : Mapping[K, V]
		`Mapping` objects to merge. Alternatively, pass a single `Iterable[Mapping[K, V]]` as the
		sole positional argument.
	factory : Callable[[], MutableMapping[K, V]] = dict
		`Callable` that creates the `MutableMapping`[1] to `return`.

	Returns
	-------
	mappingMerged : MutableMapping[K, V]
		New `MutableMapping` created by `factory` containing all key-value pairs from `dicts`. For
		duplicate keys, the value from the last `Mapping` in `dicts` that contains the key takes
		precedence.

	See Also
	--------
	merge_with : Merge dictionaries and apply a `Callable` to combined values.

	Examples
	--------
	>>> merge({1: 'one'}, {2: 'two'})
	{1: 'one', 2: 'two'}

	Later dictionaries have precedence

	>>> merge({1: 2, 3: 4}, {3: 3, 4: 4})
	{1: 2, 3: 3, 4: 4}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	if len(dicts) == 1 and not isinstance(dicts[0], Mapping):
		dicts = dicts[0]
	rv: MutableMapping[K, V] = factory()
	for d in dicts:
		rv.update(d)
	return rv

@overload
def merge_with[K, V](func: Callable[[list[V]], V], *dicts: Mapping[K, V]) -> dict[K, V]: ...
@overload
def merge_with[K, V](func: Callable[[list[V]], V], *dicts: Mapping[K, V], factory: Callable[[], MutableMapping[K, V]]) -> MutableMapping[K, V]: ...
def merge_with[K, V](func: Callable[[list[V]], V], *dicts: Mapping[K, V], factory: Callable[[], MutableMapping[K, V]] = dict) -> MutableMapping[K, V]:
	"""Merge dictionaries and apply a `Callable` to combined values.

	(AI generated docstring)

	You can use `merge_with` to combine two or more `Mapping`[1] objects and resolve key conflicts
	by applying `func` to a `list` of all values associated with each key. For each key that
	appears in one or more elements of `dicts`, `merge_with` collects all associated values into a
	`list` in the order they appear across `dicts`, then calls `func` with that `list` to produce
	the value in the result. You can also pass a single `Iterable[Mapping[K, V]]` as the sole
	positional argument after `func`.

	Parameters
	----------
	func : Callable[[list[V]], V]
		`Callable` applied to the `list` of values associated with each key across all `Mapping`
		objects in `dicts`. `func` receives a non-empty `list` and must return the merged value for
		that key.
	*dicts : Mapping[K, V]
		`Mapping` objects to merge. Alternatively, pass a single `Iterable[Mapping[K, V]]` as the
		sole positional argument after `func`.
	factory : Callable[[], MutableMapping[K, V]] = dict
		`Callable` that creates the `MutableMapping`[1] to `return`.

	Returns
	-------
	mappingMerged : MutableMapping[K, V]
		New `MutableMapping` created by `factory` where each key maps to the result of calling
		`func` with all values associated with that key across `dicts`.

	See Also
	--------
	merge : Merge a collection of `Mapping` objects into a new `Mapping`.

	Examples
	--------
	>>> merge_with(sum, {1: 1, 2: 2}, {1: 10, 2: 20})
	{1: 11, 2: 22}

	>>> merge_with(first, {1: 1, 2: 2}, {2: 20, 3: 30})  # doctest: +SKIP
	{1: 1, 2: 2, 3: 30}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	if len(dicts) == 1 and not isinstance(dicts[0], Mapping):
		dicts = dicts[0]
	groupedValues: defaultdict[K, list[V]] = defaultdict(list)
	for d in dicts:
		for k, v in d.items():
			groupedValues[k].append(v)
	rv: MutableMapping[K, V] = factory()
	for k, valueList in groupedValues.items():
		rv[k] = func(valueList)
	return rv

# TODO Given `d: dict[str, int | str]`. It does not follow that `func: Callable[[int | str], int | str]`
@overload
def update_in[K, V](d: Mapping[K, V], keys: Sequence[K], func: Callable[[V | None], V], default: None = None, *, factory: Callable[[], MutableMapping[K, V]] = dict) -> dict[K, V]: ...
@overload
def update_in[K, V](d: Mapping[K, V], keys: Sequence[K], func: Callable[[V], V], default: V, factory: Callable[[], MutableMapping[K, V]] = dict) -> dict[K, V]: ...
@overload
def update_in[K, V](d: Mapping[K, V], keys: Sequence[K], func: Callable[[V | None], V], default: None = None, *, factory: Callable[[], MutableMapping[K, V]]) -> MutableMapping[K, V]: ...
@overload
def update_in[K, V](d: Mapping[K, V], keys: Sequence[K], func: Callable[[V], V], default: V, factory: Callable[[], MutableMapping[K, V]]) -> MutableMapping[K, V]: ...
def update_in[K, V](d: Mapping[K, V], keys: Sequence[K], func: Callable[[V], V], default: V | None = None, factory: Callable[[], MutableMapping[K, V]] = dict) -> MutableMapping[K, V]:
	"""Apply a `Callable` to a value at a nested path in a `Mapping`.

	(AI generated docstring)

	You can use `update_in` to produce a copy of `d` with the value at the nested path
	specified by `keys` replaced by the result of calling `func` on the current value.
	`update_in` creates intermediate `MutableMapping` instances as needed when a key in
	`keys` is absent from `d`. If the innermost key is absent, `func` receives `default`
	instead of an existing value. `update_in` does not mutate `d` or any nested `Mapping`
	within `d`.

	Parameters
	----------
	d : Mapping[K, V]
		Source `Mapping`.
	keys : Sequence[K]
		Non-empty sequence of keys specifying the nested path to the value to update in `d`.
	func : Callable[[V], V]
		`Callable` applied to the current value at the path in `keys`. If the innermost
		key is absent from `d`, `func` receives `default`.
	default : V | None = None
		Value passed to `func` when the innermost key is absent from `d`.
	factory : Callable[[], MutableMapping[K, V]] = dict
		`Callable` that creates each new `MutableMapping`[1] in the result.

	Returns
	-------
	mappingUpdated : MutableMapping[K, V]
		New `MutableMapping` based on `d` with the value at the path specified by `keys`
		replaced by the result of `func`.

	See Also
	--------
	assoc_in : Create a new `Mapping` from `d` with a value at a nested path.
	get_in : Retrieve a value at a nested path in a `Mapping`.
	assoc : Create a new `Mapping` from `d` with one key associated to a value.

	Examples
	--------
	>>> inc = lambda x: x + 1
	>>> update_in({'a': 0}, ['a'], inc)
	{'a': 1}

	>>> update_in({}, ['z'], inc, 0)
	{'z': 1}

	>>> update_in({}, [1, 2, 3], str, default="bar")
	{1: {2: {3: 'bar'}}}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	# DEVELOPMENT Deconstruction of `update_in` to understand it better and to see if it can be improved.
	# Is deepcopy slow or is there a fundamental reason they chose factory() then update? YES.  # noqa: ERA001
	# 	In their tests, their `CustomMapping` does not have basic `Mapping` methods.

	updateInMeWith_funcOfValueOr_funcOf_default = pointerTo_item_in_updateInMe = factory()
	updateInMeWith_funcOfValueOr_funcOf_default.update(d)

	dequeKeys: deque[K] = deque(keys)

	keyDelDia: K = dequeKeys.popleft()

	# DEVELOPMENT I added a new identifier `mappingDelDia` because I don't like what used to be `d = d[k]` and `d = factory()` in the original code.  # noqa: ERA001
	# Perhaps I lack the knowledge to understand that it is safe. But, I feel it is dangerous to play with the object that you told the user would not change.
	mappingDelDia = factory()
	mappingDelDia.update(d)

	while dequeKeys:
		keyInTheWings: K = dequeKeys.popleft()					# NOTE potentially duplicate code
		if keyDelDia in mappingDelDia: # pyright: ignore[reportOperatorIssue]
			mappingDelDia = mappingDelDia[keyDelDia] # pyright: ignore[reportIndexIssue, reportUnknownVariableType]
			mappingDelDiaCOPY = factory()
			mappingDelDiaCOPY.update(mappingDelDia) # pyright: ignore[reportArgumentType, reportCallIssue]
		else:
			# reinitialize mappingDelDia and mappingDelDiaCOPY to empty Mapping
			mappingDelDia = mappingDelDiaCOPY = factory()

		pointerTo_item_in_updateInMe[keyDelDia] = pointerTo_item_in_updateInMe = mappingDelDiaCOPY # pyright: ignore[reportArgumentType]
		keyDelDia = keyInTheWings

	if keyDelDia in mappingDelDia:								# pyright: ignore[reportOperatorIssue] # NOTE duplicate code
		# This branch is only possible if `keyDelDia in mappingDelDia` has always been `True`
		pointerTo_item_in_updateInMe[keyDelDia] = func(mappingDelDia[keyDelDia]) # pyright: ignore[reportUnknownArgumentType, reportIndexIssue]
	else:
		pointerTo_item_in_updateInMe[keyDelDia] = func(default) # pyright: ignore[reportArgumentType] # TODO `raiseIfNone` might be causing pytest to hang in humpy_toolz\sandbox\tests\test_parallel.py
		"""# DEVELOPMENT list of Mappings
		d											no change
		updateInMeWith_funcOfValueOr_funcOf_default	d
		mappingDelDia								d[0][1]
			else									empty
		mappingDelDiaCOPY							d[0][1]
			else									empty
		pointerTo_item_in_updateInMe				pointerTo_item_in_updateInMe[1] = d[0][1]	pointing at EXISTING item updateInMeWith_funcOfValueOr_funcOf_default[0][1]
			else									pointerTo_item_in_updateInMe[1] = empty		pointing at NEW 	 item updateInMeWith_funcOfValueOr_funcOf_default[0][1]
		"""
		"""# DEVELOPMENT list of keys
		dequeKeys									popped 3
		keyDelDia									[2]
		keyInTheWings								[2]
		"""
	"""# DEVELOPMENT If `d` were a `Mapping` and `factory` were a `MutableMapping`, and the tests would need to change, this would work:
	rv = dATk = factory(d)
	rv.update(d)
	dequeKeys: deque[K] = deque(keys)
	keyFinal: K = dequeKeys.pop()
	sherpa = factory(d)
	while dequeKeys:
		k: K = dequeKeys.popleft()
		sherpa = sherpa.get(k, factory())
		dATk[k] = dATk = sherpa.copy()
	dATk[keyFinal] = func(sherpa.get(keyFinal, default))
	return rv
	"""
	return updateInMeWith_funcOfValueOr_funcOf_default

@overload
def valfilter[K, V](predicate: Callable[[V], bool], d: Mapping[K, V]) -> dict[K, V]: ...
@overload
def valfilter[K, V](predicate: Callable[[V], bool], d: Mapping[K, V], factory: Callable[[], MutableMapping[K, V]]) -> MutableMapping[K, V]: ...
def valfilter[K, V](predicate: Callable[[V], bool], d: Mapping[K, V], factory: Callable[[], MutableMapping[K, V]] = dict) -> MutableMapping[K, V]:
	"""Retain only items from `d` whose values satisfy `predicate` and return a new `Mapping`.

	(AI generated docstring)

	You can use `valfilter` to select items from `d` (***d***ictionary) by their values. `valfilter`
	calls `predicate` with each value yielded by `d.values()`. `valfilter` inserts each item whose
	value causes `predicate` to return `True` into a new `MutableMapping`[1] created by `factory`.
	`valfilter` does not change `d`.

	Parameters
	----------
	predicate : Callable[[V], bool]
		`Callable` applied to each value of `d`. `valfilter` keeps each item for which `predicate`
		returns `True`.
	d : Mapping[K, V]
		Source `Mapping`[1]. `valfilter` reads all items from `d` and does not change `d`.
	factory : Callable[[], MutableMapping[K, V]] = dict
		`Callable` that creates the `MutableMapping`[1] to `return`.

	Returns
	-------
	mappingFiltered : MutableMapping[K, V]
		New `MutableMapping` created by `factory` containing only items from `d` whose values
		cause `predicate` to return `True`.

	See Also
	--------
	keyfilter : Retain only items from `d` whose keys satisfy `predicate` and return a new `Mapping`.
	itemfilter : Retain only items from `d` whose key-value pairs satisfy `predicate` and return a new `Mapping`.
	valmap : Apply a `Callable` to all values of a `Mapping` and return a new `Mapping`.

	Examples
	--------
	>>> iseven = lambda x: x % 2 == 0
	>>> d = {1: 2, 2: 3, 3: 4, 4: 5}
	>>> valfilter(iseven, d)
	{1: 2, 3: 4}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	rv: MutableMapping[K, V] = factory()
	for k, v in d.items():
		if predicate(v):
			rv[k] = v
	return rv

@overload
def valmap[K, V, W](func: Callable[[V], W], d: Mapping[K, V]) -> dict[K, W]: ...
@overload
def valmap[K, V, W](func: Callable[[V], W], d: Mapping[K, V], factory: Callable[[], MutableMapping[K, W]]) -> MutableMapping[K, W]: ...
def valmap[K, V, W](func: Callable[[V], W], d: Mapping[K, V], factory: Callable[[], MutableMapping[K, W]] = dict) -> MutableMapping[K, W]:
	"""Apply `func` to all values of `d` and return a new `Mapping` with the transformed values.

	(AI generated docstring)

	You can use `valmap` to transform all values in `d` without changing `d`. `valmap` applies
	`func` to each value yielded by `d.values()` and builds a new `MutableMapping`[1] created
	by `factory`, preserving each original key associated with its transformed value.

	Parameters
	----------
	func : Callable[[V], W]
		`Callable` applied to each value of `d`. Each value of `d` is passed to `func`
		individually, and `func` returns the corresponding transformed value.
	d : Mapping[K, V]
		Source `Mapping`[1]. `valmap` reads all values from `d` and does not change `d`.
	factory : Callable[[], MutableMapping[K, W]] = dict
		`Callable` that creates the `MutableMapping`[1] to `return`.

	Returns
	-------
	mappingTransformed : MutableMapping[K, W]
		New `MutableMapping` created by `factory` in which each key from `d` is associated
		with the result of applying `func` to the corresponding value of `d`.

	See Also
	--------
	keymap : Apply a `Callable` to all keys of a `Mapping` and return a new `Mapping`.
	itemmap : Apply a `Callable` to all items of a `Mapping` and return a new `Mapping`.

	Examples
	--------
	>>> bills = {'Alice': [20, 15, 30], 'Bob': [10, 35]}
	>>> valmap(sum, bills)  # doctest: +SKIP
	{'Alice': 65, 'Bob': 45}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	rv: MutableMapping[K, W] = factory()
	rv.update(zip(d.keys(), map(func, d.values()), strict=True))
	return rv

