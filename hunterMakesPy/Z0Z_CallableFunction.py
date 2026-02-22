"""Protocols for callable functions with full type safety."""
from collections.abc import Callable
from types import CellType, CodeType, MethodType
from typing import Any, overload, ParamSpec, Protocol, runtime_checkable, Self, TypeVar, TypeVarTuple
import sys

#======== Stolen, uh, I mean copied from typeshed:stdlib\_typeshed\__init__.pyi ========
type AnnotationForm = Any

if (3, 14) <= sys.version_info:
	from annotationlib import Format

# NOTE These return annotations, which can be arbitrary objects
	type AnnotateFunc = Callable[[Format], dict[str, AnnotationForm]]
	type EvaluateFunc = Callable[[Format], AnnotationForm]
#======== End stolen, uh, I mean copied from typeshed:stdlib\_typeshed\__init__.pyi ========

@runtime_checkable
class CallableFunction[**P, R](Protocol):
	"""A Protocol representing callable functions with descriptor support.

	Mimics types.FunctionType while being a drop-in replacement for `collections.abc.Callable`. Includes all standard function
	attributes and the descriptor protocol for proper method binding.

	Note: @runtime_checkable only validates attribute presence, not signatures.
	"""

# NOTE: The eehhhh, IDK... section
	__doc__: str | None
	__wrapped__: Any  # Allegedly, for functools.wraps support
# NOTE: End eehhhh, IDK... section

	@property
	def __closure__(self) -> tuple[CellType, ...] | None:
		"""Tuple of cells that contain bindings for the function's free variables."""
		...
	__code__: CodeType
	__defaults__: tuple[Any, ...] | None
	__dict__: dict[str, Any]
	@property
	def __globals__(self) -> dict[str, Any]:
		"""The global namespace in which the function was defined."""
		...
	__name__: str
	__qualname__: str
	__annotations__: dict[str, AnnotationForm]
	if (3, 14) <= sys.version_info:
		__annotate__: AnnotateFunc | None
	__kwdefaults__: dict[str, Any] | None
	@property
	def __builtins__(self) -> dict[str, Any]:
		"""The built-in namespace in which the function was defined."""
		...
	__type_params__: tuple[TypeVar | ParamSpec | TypeVarTuple, ...]
	__module__: str

	def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
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
