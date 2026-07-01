"""Prototype for callable functions with full type safety."""
from __future__ import annotations

from collections.abc import Callable
from typing import Any, overload, ParamSpec, Protocol, runtime_checkable, TYPE_CHECKING, TypeVar
import sys

if TYPE_CHECKING:
	from types import CodeType, MethodType
	from typing import TypeAlias
	from typing_extensions import Self, TypeVarTuple

# TODO explore the following
"""
I've added new test cases using a lambda function and a standard user-defined imported function
(stringItUp itself). Built-in functions like len don't trigger the FunctionType check because their
type is technically a builtin_function_or_method in CPython, whereas functions defined via def or
lambda correspond exactly to types.FunctionType. Your coverage should now reflect this branch as
expected reflect activation of that branch.
"""

#======== Copied from typeshed:stdlib\_typeshed\__init__.pyi ========
AnnotationForm: TypeAlias = Any

if (3, 14) <= sys.version_info:
	from annotationlib import Format

# NOTE These return annotations, which can be arbitrary objects
	AnnotateFunc: TypeAlias = Callable[[Format], dict[str, AnnotationForm]]
	EvaluateFunc: TypeAlias = Callable[[Format], AnnotationForm]
#======== End Copied from typeshed:stdlib\_typeshed\__init__.pyi ========

_P = ParamSpec("_P")
_R_co = TypeVar("_R_co", covariant=True)

@runtime_checkable
class CallableFunction(Protocol[_P, _R_co]):
	"""A Protocol representing callable functions with descriptor support.

	Mimics types.FunctionType while being a drop-in replacement for `collections.abc.Callable`. Includes all standard function
	attributes and the descriptor protocol for proper method binding.

	Note: @runtime_checkable only validates attribute presence, not signatures.
	"""

	__code__: CodeType
	__defaults__: tuple[Any, ...] | None
	__dict__: dict[str, Any]

	__name__: str
	__qualname__: str
	__annotations__: dict[str, AnnotationForm]
	if (3, 14) <= sys.version_info:
		__annotate__: AnnotateFunc | None
	__kwdefaults__: dict[str, Any] | None

	__type_params__: tuple[TypeVar | ParamSpec | TypeVarTuple, ...]
	__module__: str

	def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> _R_co:
		"""Execute the callable with the given arguments."""
		...

	@overload
	def __get__(self, instance: None, owner: type, /) -> Self: ...
	@overload
	def __get__(self, instance: object, owner: type | None = None, /) -> MethodType: ...
	def __get__(self, instance: object | None, owner: type | None = None) -> Self | MethodType:
		"""Descriptor protocol for method binding.

		Returns self when accessed on the class, or a bound MethodType when accessed on an instance.
		"""
		...
