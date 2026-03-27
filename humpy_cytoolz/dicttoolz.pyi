from _typeshed import SupportsGetItem
from collections.abc import Callable, Iterable, Mapping, MutableMapping, Sequence
from typing import Literal, overload, TypeGuard
from typing_extensions import TypeIs

__all__ = (
	"assoc",
	"assoc_in",
	"dissoc",
	"get_in",
	"itemfilter",
	"itemmap",
	"keyfilter",
	"keymap",
	"merge",
	"merge_with",
	"update_in",
	"valfilter",
	"valmap",
)

@overload
def assoc[K, V](d: Mapping[K, V], key: K, value: V) -> dict[K, V]: ...
@overload
def assoc[K, V](d: Mapping[K, V], key: K, value: V, factory: Callable[[], MutableMapping[K, V]]) -> MutableMapping[K, V]: ...

@overload
def assoc_in[K, V](d: Mapping[K, V], keys: Sequence[K], value: V) -> dict[K, V]: ...
@overload
def assoc_in[K, V](d: Mapping[K, V], keys: Sequence[K], value: V, factory: Callable[[], MutableMapping[K, V]]) -> MutableMapping[K, V]: ...

@overload
def dissoc[K, V](d: Mapping[K, V], *keys: K) -> dict[K, V]: ...
@overload
def dissoc[K, V](d: Mapping[K, V], *keys: K, factory: Callable[[], MutableMapping[K, V]]) -> MutableMapping[K, V]: ...

@overload
def get_in[K, V](keys: Sequence[K], coll: SupportsGetItem[K, V], default: None = None, *, no_default: Literal[True]) -> V: ...
@overload
def get_in[K, V](keys: Sequence[K], coll: SupportsGetItem[K, V], default: None = None, no_default: bool = False) -> V | None: ...
@overload
def get_in[K, V](keys: Sequence[K], coll: SupportsGetItem[K, V], default: V, no_default: bool = False) -> V: ...

@overload
def itemfilter[K, V, K1, V1](
	predicate: Callable[[tuple[K, V]], TypeIs[tuple[K1, V1]]],
	d: Mapping[K, V],
) -> dict[K1, V1]: ...
@overload
def itemfilter[K, V, K1, V1](
	predicate: Callable[[tuple[K, V]], TypeGuard[tuple[K1, V1]]],
	d: Mapping[K, V],
) -> dict[K1, V1]: ...
@overload
def itemfilter[K, V](
	predicate: Callable[[tuple[K, V]], bool],
	d: Mapping[K, V],
) -> dict[K, V]: ...
@overload
def itemfilter[K, V, K1, V1](
	predicate: Callable[[tuple[K, V]], TypeIs[tuple[K1, V1]]],
	d: Mapping[K, V],
	*,
	factory: Callable[[], MutableMapping[K1, V1]],
) -> MutableMapping[K1, V1]: ...
@overload
def itemfilter[K, V, K1, V1](
	predicate: Callable[[tuple[K, V]], TypeGuard[tuple[K1, V1]]],
	d: Mapping[K, V],
	*,
	factory: Callable[[], MutableMapping[K1, V1]],
) -> MutableMapping[K1, V1]: ...
@overload
def itemfilter[K, V](
	predicate: Callable[[tuple[K, V]], bool],
	d: Mapping[K, V],
	*,
	factory: Callable[[], MutableMapping[K, V]],
) -> MutableMapping[K, V]: ...
def itemfilter[K, V, K1, V1](
	predicate: Callable[[tuple[K, V]], bool]
	| Callable[[tuple[K, V]], TypeGuard[tuple[K1, V1]]],
	d: Mapping[K, V],
	*,
	factory: Callable[[], MutableMapping[K, V]] = dict,
) -> MutableMapping[K, V]:
	...

@overload
def itemmap[K0, V0, K1, V1](
	func: Callable[[tuple[K0, V0]], tuple[K1, V1]],
	d: Mapping[K0, V0],
) -> dict[K1, V1]: ...
@overload
def itemmap[K0, V0, K1, V1](
	func: Callable[[tuple[K0, V0]], tuple[K1, V1]],
	d: Mapping[K0, V0],
	*,
	factory: Callable[[], MutableMapping[K1, V1]],
) -> MutableMapping[K1, V1]: ...
@overload
def itemmap[K0, V0, K1, V1](
	func: Callable[[tuple[K0, V0]], Iterable[K1 | V1]],
	d: Mapping[K0, V0],
) -> dict[K1, V1]: ...
@overload
def itemmap[K0, V0, K1, V1](
	func: Callable[[tuple[K0, V0]], Iterable[K1 | V1]],
	d: Mapping[K0, V0],
	*,
	factory: Callable[[], MutableMapping[K1, V1]],
) -> MutableMapping[K1, V1]: ...
def itemmap[K0, V0, K1, V1](
	func: Callable[[tuple[K0, V0]], tuple[K1, V1]]
	| Callable[[tuple[K0, V0]], Iterable[K1 | V1]],
	d: Mapping[K0, V0],
	*,
	factory: Callable[[], MutableMapping[K1, V1]] = dict,
) -> MutableMapping[K1, V1]:
	...

@overload
def keyfilter[K, V, R](
	predicate: Callable[[K], TypeIs[R]],
	d: Mapping[K, V],
) -> dict[R, V]: ...
@overload
def keyfilter[K, V, R](
	predicate: Callable[[K], TypeGuard[R]],
	d: Mapping[K, V],
) -> dict[R, V]: ...
@overload
def keyfilter[K, V](
	predicate: Callable[[K], bool],
	d: Mapping[K, V],
) -> dict[K, V]: ...
@overload
def keyfilter[K, V, R](
	predicate: Callable[[K], TypeIs[R]],
	d: Mapping[K, V],
	*,
	factory: Callable[[], MutableMapping[R, V]],
) -> MutableMapping[R, V]: ...
@overload
def keyfilter[K, V, R](
	predicate: Callable[[K], TypeGuard[R]],
	d: Mapping[K, V],
	*,
	factory: Callable[[], MutableMapping[R, V]],
) -> MutableMapping[R, V]: ...
@overload
def keyfilter[K, V](
	predicate: Callable[[K], bool],
	d: Mapping[K, V],
	*,
	factory: Callable[[], MutableMapping[K, V]],
) -> MutableMapping[K, V]: ...
def keyfilter[K, V, R](
	predicate: Callable[[K], bool] | Callable[[K], TypeGuard[R]],
	d: Mapping[K, V],
	*,
	factory: Callable[[], MutableMapping[K, V]] = dict,
) -> MutableMapping[K, V]:
	...

@overload
def keymap[K0, K1, V](
	func: Callable[[K0], K1],
	d: Mapping[K0, V],
) -> dict[K1, V]: ...
@overload
def keymap[K0, K1, V](
	func: Callable[[K0], K1],
	d: Mapping[K0, V],
	*,
	factory: Callable[[], MutableMapping[K1, V]],
) -> MutableMapping[K1, V]: ...
def keymap[K0, K1, V](
	func: Callable[[K0], K1],
	d: Mapping[K0, V],
	*,
	factory: Callable[[], MutableMapping[K1, V]] = dict,
) -> MutableMapping[K1, V]:
	...

@overload
def merge[K, V](dicts: Iterable[Mapping[K, V]]) -> dict[K, V]: ...
@overload
def merge[K, V](
	dicts: Iterable[Mapping[K, V]],
	*,
	factory: Callable[[], MutableMapping[K, V]],
) -> MutableMapping[K, V]: ...
@overload
def merge[K, V](*dicts: Mapping[K, V]) -> dict[K, V]: ...
@overload
def merge[K, V](
	*dicts: Mapping[K, V],
	factory: Callable[[], MutableMapping[K, V]],
) -> MutableMapping[K, V]: ...
def merge[K, V](
	*dicts: Mapping[K, V] | Iterable[Mapping[K, V]],
	factory: Callable[[], MutableMapping[K, V]] = dict,
) -> MutableMapping[K, V]:
	...

@overload
def merge_with[K, V](
	func: Callable[[list[V]], V],
	dicts: Iterable[Mapping[K, V]],
) -> dict[K, V]: ...
@overload
def merge_with[K, V](
	func: Callable[[list[V]], V],
	dicts: Iterable[Mapping[K, V]],
	*,
	factory: Callable[[], MutableMapping[K, V]],
) -> MutableMapping[K, V]: ...
@overload
def merge_with[K, V](
	func: Callable[[list[V]], V],
	*dicts: Mapping[K, V],
) -> dict[K, V]: ...
@overload
def merge_with[K, V](
	func: Callable[[list[V]], V],
	*dicts: Mapping[K, V],
	factory: Callable[[], MutableMapping[K, V]],
) -> MutableMapping[K, V]: ...
def merge_with[K, V](
	func: Callable[[list[V]], V],
	*dicts: Mapping[K, V] | Iterable[Mapping[K, V]],
	factory: Callable[[], MutableMapping[K, V]] = dict,
) -> MutableMapping[K, V]:
	...

@overload
def update_in[K, V](
	d: Mapping[K, V],
	keys: Sequence[K],
	func: Callable[[V | None], V],
	default: None = None,
) -> dict[K, V]: ...
@overload
def update_in[K, V](
	d: Mapping[K, V],
	keys: Sequence[K],
	func: Callable[[V], V],
	default: V,
) -> dict[K, V]: ...
@overload
def update_in[K, V](
	d: Mapping[K, V],
	keys: Sequence[K],
	func: Callable[[V | None], V],
	default: None,
	factory: Callable[[], MutableMapping[K, V]],
) -> MutableMapping[K, V]: ...
@overload
def update_in[K, V](
	d: Mapping[K, V],
	keys: Sequence[K],
	func: Callable[[V], V],
	default: V,
	factory: Callable[[], MutableMapping[K, V]],
) -> MutableMapping[K, V]: ...
def update_in[K, V](
	d: Mapping[K, V],
	keys: Sequence[K],
	func: Callable[[V], V],
	default: V | None = None,
	factory: Callable[[], MutableMapping[K, V]] = dict,
) -> MutableMapping[K, V]:
	...

@overload
def valfilter[K, V, R](
	predicate: Callable[[V], TypeIs[R]],
	d: Mapping[K, V],
) -> dict[K, R]: ...
@overload
def valfilter[K, V, R](
	predicate: Callable[[V], TypeGuard[R]],
	d: Mapping[K, V],
) -> dict[K, R]: ...
@overload
def valfilter[K, V](
	predicate: Callable[[V], bool],
	d: Mapping[K, V],
) -> dict[K, V]: ...
@overload
def valfilter[K, V, R](
	predicate: Callable[[V], TypeIs[R]],
	d: Mapping[K, V],
	*,
	factory: Callable[[], MutableMapping[K, R]],
) -> MutableMapping[K, R]: ...
@overload
def valfilter[K, V, R](
	predicate: Callable[[V], TypeGuard[R]],
	d: Mapping[K, V],
	*,
	factory: Callable[[], MutableMapping[K, R]],
) -> MutableMapping[K, R]: ...
@overload
def valfilter[K, V](
	predicate: Callable[[V], bool],
	d: Mapping[K, V],
	*,
	factory: Callable[[], MutableMapping[K, V]],
) -> MutableMapping[K, V]: ...
def valfilter[K, V, R](
	predicate: Callable[[V], bool] | Callable[[V], TypeGuard[R]],
	d: Mapping[K, V],
	*,
	factory: Callable[[], MutableMapping[K, V]] = dict,
) -> MutableMapping[K, V]:
	...

@overload
def valmap[K, V0, V1](
	func: Callable[[V0], V1],
	d: Mapping[K, V0],
) -> dict[K, V1]: ...
@overload
def valmap[K, V0, V1](
	func: Callable[[V0], V1],
	d: Mapping[K, V0],
	*,
	factory: Callable[[], MutableMapping[K, V1]],
) -> MutableMapping[K, V1]: ...
def valmap[K, V0, V1](
	func: Callable[[V0], V1],
	d: Mapping[K, V0],
	*,
	factory: Callable[[], MutableMapping[K, V1]] = dict,
) -> MutableMapping[K, V1]:
	...

