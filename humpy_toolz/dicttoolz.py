from collections.abc import Callable, Mapping, MutableMapping
from functools import reduce
from typing import overload
import collections
import operator

__all__ = ('assoc', 'assoc_in', 'dissoc', 'get_in', 'itemfilter', 'itemmap', 'keyfilter', 'keymap', 'merge', 'merge_with', 'update_in', 'valfilter', 'valmap')

def _get_factory(f, kwargs):
	factory = kwargs.pop('factory', dict)
	if kwargs:
		raise TypeError(f"{f.__name__}() got an unexpected keyword argument '{kwargs.popitem()[0]}'")
	return factory

def merge(*dicts, **kwargs):
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
	if len(dicts) == 1 and (not isinstance(dicts[0], Mapping)):
		dicts = dicts[0]
	factory = _get_factory(merge, kwargs)
	rv = factory()
	for d in dicts:
		rv.update(d)
	return rv

def merge_with(func, *dicts, **kwargs):
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
	if len(dicts) == 1 and (not isinstance(dicts[0], Mapping)):
		dicts = dicts[0]
	factory = _get_factory(merge_with, kwargs)
	values = collections.defaultdict(lambda: [].append)
	for d in dicts:
		for k, v in d.items():
			values[k](v)
	result = factory()
	for k, v in values.items():
		result[k] = func(v.__self__)
	return result

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
	>>> bills = {"Alice": [20, 15, 30], "Bob": [10, 35]}
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
	>>> bills = {"Alice": [20, 15, 30], "Bob": [10, 35]}
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
	>>> accountids = {"Alice": 10, "Bob": 20}
	>>> itemmap(reversed, accountids)  # doctest: +SKIP
	{10: "Alice", 20: "Bob"}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	rv: MutableMapping[L, W] = factory()
	rv.update(map(func, d.items()))
	return rv

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

def assoc_in(d, keys, value, factory=dict):
	"""Return a new dict with new, potentially nested, key value pair

	>>> purchase = {'name': 'Alice',
	...             'order': {'items': ['Apple', 'Orange'],
	...                       'costs': [0.50, 1.25]},
	...             'credit card': '5555-1234-1234-1234'}
	>>> assoc_in(purchase, ['order', 'costs'], [0.25, 1.00]) # doctest: +SKIP
	{'credit card': '5555-1234-1234-1234',
	'name': 'Alice',
	'order': {'costs': [0.25, 1.00], 'items': ['Apple', 'Orange']}}
	"""
	return update_in(d, keys, lambda x: value, value, factory)

def update_in(d, keys, func, default=None, factory=dict):
	"""Update value in a (potentially) nested dictionary

	inputs:
	d - dictionary on which to operate
	keys - list or tuple giving the location of the value to be changed in d
	func - function to operate on that value

	If keys == [k0,..,kX] and d[k0]..[kX] == v, update_in returns a copy of the
	original dictionary with v replaced by func(v), but does not mutate the
	original dictionary.

	If k0 is not a key in d, update_in creates nested dictionaries to the depth
	specified by the keys, with the innermost value set to func(default).

	>>> inc = lambda x: x + 1
	>>> update_in({'a': 0}, ['a'], inc)
	{'a': 1}

	>>> transaction = {'name': 'Alice',
	...                'purchase': {'items': ['Apple', 'Orange'],
	...                             'costs': [0.50, 1.25]},
	...                'credit card': '5555-1234-1234-1234'}
	>>> update_in(transaction, ['purchase', 'costs'], sum) # doctest: +SKIP
	{'credit card': '5555-1234-1234-1234',
	 'name': 'Alice',
	 'purchase': {'costs': 1.75, 'items': ['Apple', 'Orange']}}

	>>> # updating a value when k0 is not in d
	>>> update_in({}, [1, 2, 3], str, default="bar")
	{1: {2: {3: 'bar'}}}
	>>> update_in({1: 'foo'}, [2, 3, 4], inc, 0)
	{1: 'foo', 2: {3: {4: 1}}}
	"""
	ks = iter(keys)
	k = next(ks)
	rv = inner = factory()
	rv.update(d)
	for key in ks:
		if k in d:
			d = d[k]
			dtemp = factory()
			dtemp.update(d)
		else:
			d = dtemp = factory()
		inner[k] = inner = dtemp
		k = key
	if k in d:
		inner[k] = func(d[k])
	else:
		inner[k] = func(default)
	return rv

def get_in(keys, coll, default=None, no_default=False):
	"""Returns coll[i0][i1]...[iX] where [i0, i1, ..., iX]==keys.

	If coll[i0][i1]...[iX] cannot be found, returns ``default``, unless
	``no_default`` is specified, then it raises KeyError or IndexError.

	``get_in`` is a generalization of ``operator.getitem`` for nested data
	structures such as dictionaries and lists.

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

	See Also
	--------
		itertoolz.get
		operator.getitem
	"""
	try:
		return reduce(operator.getitem, keys, coll)
	except (KeyError, IndexError, TypeError):
		if no_default:
			raise
		return default
