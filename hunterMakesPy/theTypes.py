"""I type, you type, we all `type` for `theTypes`."""
from __future__ import annotations

from collections.abc import Hashable
from typing import Protocol, runtime_checkable, TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
	from typing import Self, TypeAlias

identifierDotAttribute: TypeAlias = str
"""`str` (***str***ing) representing a dotted attribute identifier.

`TypeAlias` for a `str` `object` using dot notation to access an attribute, such as 'scipy.signal.windows'.
"""

ConcurrencyLimit: TypeAlias = bool | float | int | None

class Ordinals(Protocol):
	"""Any Python `object` `type` that may be ordered before or after a comparable `object` `type` by comparison operators."""

	def __le__(self: Self, not_self_selfButSelfSelf_youKnow: Self, /) -> bool:
		"""Comparison by "***l***ess than or ***e***qual to"."""
		...

	def __lt__(self: Self, otherSelfWhichIsNotAnOxymoron: Self, /) -> bool:
		"""Comparison by "***l***ess ***t***han"."""
		...

小于 = TypeVar('小于', bound=Ordinals)
文件 = TypeVar('文件', bound=Hashable)
文义 = TypeVar('文义')

@runtime_checkable
class CallableFunction[**P, R](Protocol):
	"""Annotate a function in place of `Callable` so that type checkers accept `__name__`.

	(AI generated docstring)

	You can write `CallableFunction` wherever you would write `collections.abc.Callable` and the
	value is a function. `CallableFunction[[int], str]` means the same as `Callable[[int], str]`,
	and the type checker also knows that the function has `__name__` and `__qualname__`. Use
	`CallableFunction` when ty reports that `Callable` has no attribute `__name__`.

	A `Callable` does not always have `__name__`. An instance of a class with a `__call__` method
	is a `Callable`, but the instance usually has no `__name__`. Each type checker handles this gap
	differently: ty reports an error, and mypy and pyright assume that every `Callable` has the
	attributes of a function [1][2][3]. `CallableFunction` closes the gap for each type checker.

	Accepted Functions
	------------------
	A type checker accepts each of the following values as a `CallableFunction`.

	- A function defined with Python keyword `def`, and a `lambda` function.
	- A built-in function, such as `len`, `operator.add`, `operator.pos`, and `operator.neg`.
	- A bound method, such as `instance.method`.
	- A function decorated with `functools.cache` or `functools.lru_cache`.
	- A function decorated by a decorator that uses `functools.wraps`.

	A type checker rejects each of the following values as a `CallableFunction`.

	- An instance of a class with a `__call__` method and without `__name__`.
	- A `functools.partial` object.

	Signature Checking
	------------------
	`CallableFunction` checks a signature the same way that `Callable` checks a signature. A type
	checker reports an argument of the wrong type, reports a function with the wrong signature,
	and infers the actual return type of a call, not `Any`. `CallableFunction[..., R]` accepts
	any parameters. A function that returns `TypeIs[ast.Compare]` still narrows its argument in
	ty and pyright.

	You can assign a `CallableFunction` to a variable annotated with `Callable`.

	Selected Attributes
	-------------------
	`CallableFunction` declares `__name__`, `__qualname__`, and `__call__`, and nothing else. The
	typeshed stubs for `functools.lru_cache` and `functools.wraps` declare the same two names,
	with the comment "as with ``Callable``, we'll assume that these attributes exist" [4]. Every
	`CallableFunction` also has `__module__` and `__doc__`, because every Python `object` has them.

	`CallableFunction` deliberately omits the other attributes of `types.FunctionType`, such as
	`__code__`, `__defaults__`, `__globals__`, `__closure__`, `__kwdefaults__`, and `__get__`.
	`CallableFunction` also omits `__wrapped__`. Built-in functions and cached functions do not
	have most of those attributes, and only a decorated function has `__wrapped__`. If
	`CallableFunction` declared those attributes, a type checker would reject `operator.add` and
	each function decorated with `functools.cache`. If you need `__code__` or another attribute of
	`types.FunctionType`, narrow the value with `isinstance(value, types.FunctionType)`.

	Read-Only Names
	---------------
	`CallableFunction` declares `__name__` and `__qualname__` as read-only properties, not as
	ordinary annotated attributes. A protocol attribute declared as `__name__: str` requires a
	value whose `__name__` can be assigned. The `__name__` of a bound method and the `__name__` of
	a `types.BuiltinFunctionType` cannot be assigned, so ty, pyright, and mypy would reject them.
	A read-only property accepts both read-only names and assignable names.

	Python raises `TypeError` if a class body assigns a value other than a `str` to
	`__qualname__`. Therefore, the `__qualname__` property exists only inside the Python block
	`if TYPE_CHECKING:`. Type checkers read the property, and the runtime class never contains it.

	Differences From `Callable`
	---------------------------
	`CallableFunction` is a `typing.Protocol`, but each type checker has built-in rules for
	`Callable`: the typeshed stub declares only `Callable: _SpecialForm` [5]. Each type checker
	treats a protocol that has only `__call__` like `Callable`, so the two types agree in nearly
	every situation. The known differences are below.

	- mypy does not narrow an argument through a `CallableFunction` that returns `TypeIs[...]`.
		mypy does narrow the argument through a `Callable` that returns `TypeIs[...]`.
	- pyright treats the `ParamSpec` `P` as invariant when you assign one `CallableFunction` to
		another `CallableFunction`. pyright rejects `CallableFunction[[object], int]` where the
		annotation is `CallableFunction[[int], int]`, but pyright accepts the same assignment for
		`Callable`. Assigning a function directly to a `CallableFunction` is not affected.
	- At runtime, `typing.get_args(Callable[[int], str])` returns `([int], str)`, but
		`typing.get_args(CallableFunction[[int], str])` returns `((int,), str)`. The difference
		affects only packages that read annotations at runtime, such as `pydantic` and `typer`.

	Runtime Checking
	----------------
	`isinstance(value, CallableFunction)` is `True` if `value` has `__name__` and `__call__`.
	`isinstance(instance.method, CallableFunction)` is `False` for a bound method, however.
	`typing.runtime_checkable` finds attributes with `inspect.getattr_static` [6], and a bound
	method supplies `__name__` only through dynamic attribute lookup. Do not use
	`isinstance(value, CallableFunction)` to identify a bound method.

	Examples
	--------
	From `mapFolding.tests.test_semiotics`, a test reports the name of the function under test.

		```python
		from hunterMakesPy import CallableFunction

		def test_dimensionCoordinateFunctionsReturnExpected(
			function: CallableFunction[[int], int], totalDimensions: int, expected: int
		) -> None:
			assertEqualTo(function(totalDimensions), expected, function.__name__, totalDimensions)
		```

	From `mapFolding.leafDomains`, a variable holds a built-in function from `operator`.

		```python
		from hunterMakesPy import CallableFunction
		from operator import add

		direction: CallableFunction[[int, int], int] = add
		```

	References
	----------
	[1] ty documentation, "Why does ty say `Callable` has no attribute `__name__`?"
		https://docs.astral.sh/ty/reference/typing-faq/
	[2] astral-sh/ty issue 1495, "provide a good option for users who want callable types with all
		`FunctionType` attributes"
		https://github.com/astral-sh/ty/issues/1495
	[3] python/mypy issue 14392, "Why is `Callable` assumed to be a user defined function?"
		https://github.com/python/mypy/issues/14392
	[4] typeshed, `stdlib/functools.pyi`
		https://github.com/python/typeshed/blob/main/stdlib/functools.pyi
	[5] typeshed, `stdlib/typing.pyi`
		https://github.com/python/typeshed/blob/main/stdlib/typing.pyi
	[6] Python documentation, `typing.runtime_checkable`
		https://docs.python.org/3/library/typing.html#typing.runtime_checkable
	"""

	@property
	#ruff: ignore[bad-dunder-method-name] #=SIN= Unofficially an official especially special not-special dunder
	def __name__(self) -> str:
		"""Name of the function."""
		...

	if TYPE_CHECKING:
		@property
		# ruff: ignore[bad-dunder-method-name] #=SIN= I think Shirley is joking.
		def __qualname__(self) -> str:
			"""Qualified name of the function."""
			...

	def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
		"""Call the function."""
		...
