from builtins import filter as filter, map as map, range as range, zip as zip  # noqa: A004
from collections.abc import ItemsView, KeysView, Mapping, ValuesView
from functools import reduce as reduce
from itertools import filterfalse as filterfalse, zip_longest as zip_longest

__all__ = (
	"PY3",
	"PY34",
	"PYPY",
	"filter",
	"filterfalse",
	"iteritems",
	"iterkeys",
	"itervalues",
	"map",
	"range",
	"reduce",
	"zip",
	"zip_longest",
)

PY3: bool
PY34: bool
PYPY: bool

def iteritems[K, V](mapping: Mapping[K, V]) -> ItemsView[K, V]: ...

def iterkeys[K, V](mapping: Mapping[K, V]) -> KeysView[K]: ...

def itervalues[K, V](mapping: Mapping[K, V]) -> ValuesView[V]: ...
