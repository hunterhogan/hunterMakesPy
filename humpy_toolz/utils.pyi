from collections.abc import Callable
from typing import Protocol, TypeVar

def raises(err: type[Exception], lamda: Callable[[], None]) -> bool: ...

no_default = "__no__default__"

_KT_contra = TypeVar("_KT_contra", contravariant=True)
_VT_co = TypeVar("_VT_co", covariant=True)

class SupportsGetItem(Protocol[_KT_contra, _VT_co]):
	def __getitem__(self, key: _KT_contra, /) -> _VT_co: ...

