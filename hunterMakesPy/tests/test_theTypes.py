"""Tests for `Ordinals` ordering behaviors.

(AI generated docstring)

This module validates comparison semantics and sorting consistency across built-in and custom comparables using `pytest`.

"""
from dataclasses import dataclass
from hunterMakesPy import CallableFunction, Ordinals
from hunterMakesPy.tests.conftest import uniformTestFailureMessage
from typing import Self, TYPE_CHECKING, TypeVar
import functools
import inspect
import pytest

if TYPE_CHECKING:
	from collections.abc import Callable

小于 = TypeVar('小于', bound=Ordinals)
"""Type variable bound to `Ordinals`.

(AI generated docstring)

"""

def between(floor: 小于, ceiling: 小于, comparand: 小于) -> bool:
	"""Return whether `comparand` lies between `floor` and `ceiling` inclusive.

	Parameters
	----------
	floor : 小于
		Lower bound for `comparand`.
	ceiling : 小于
		Upper bound for `comparand`.
	comparand : 小于
		Value compared against `floor` and `ceiling`.

	Returns
	-------
	isBetween : bool
		Whether `comparand` is within the inclusive bounds.

	"""
	return floor <= comparand <= ceiling

@dataclass(frozen=True, slots=True)
class ComparableCardinal:
	"""Comparable wrapper for an `int` value.

	(AI generated docstring)

	Attributes
	----------
	value : int
		Integer used for ordering comparisons.

	"""

	value: int
	"""Integer used for ordering comparisons.

	(AI generated docstring)

	"""

	def __le__(self: Self, other: Self, /) -> bool:
		"""Return whether `self` is less than or equal to `other`.

		(AI generated docstring)

		Parameters
		----------
		self : Self
			Instance compared against `other`.
		other : Self
			Instance compared against `self`.

		Returns
		-------
		isLessThanOrEqual : bool
			Whether `self` is ordered before or equal to `other`.

		"""
		return self.value <= other.value

	def __lt__(self: Self, other: Self, /) -> bool:
		"""Return whether `self` is strictly less than `other`.

		(AI generated docstring)

		Parameters
		----------
		self : Self
			Instance compared against `other`.
		other : Self
			Instance compared against `self`.

		Returns
		-------
		isLessThan : bool
			Whether `self` is ordered before `other`.

		"""
		return self.value < other.value

@pytest.mark.parametrize(
	'floor, ceiling, comparand, expected'
	, [ (13, 34, 21, True) , (227, 695, 88, False) ]
)
def testOrdinalsBetweenWorksForInt(floor: int, ceiling: int, comparand: int, expected: bool) -> None:
	"""Verify `between` handles `int` operands.

	(AI generated docstring)

	Parameters
	----------
	floor : int
		Lower bound for `comparand`.
	ceiling : int
		Upper bound for `comparand`.
	comparand : int
		Value of `comparand` compared against the bounds.
	expected : bool
		Expected outcome from `between`.

	Returns
	-------
	unusedReturnValue : None
		Returns `None`.

	"""
	actual: bool = between(floor, ceiling, comparand)
	assert actual == expected, uniformTestFailureMessage( expected , actual , 'between' , floor , ceiling , comparand )

@pytest.mark.parametrize(
	'values, expected'
	, [ ([21, 13, 34, 8], [8, 13, 21, 34]) ]
)
def testOrdinalsSortingWorksForInt(values: list[int], expected: list[int]) -> None:
	"""Verify sorting uses ordinal ordering for `int` values.

	(AI generated docstring)

	Parameters
	----------
	values : list[int]
		Input `values` to sort.
	expected : list[int]
		Expected sorted output for `values`.

	Returns
	-------
	unusedReturnValue : None
		Returns `None`.

	"""
	actual: list[int] = sorted(values)
	assert actual == expected, uniformTestFailureMessage( expected , actual , 'sorted' , values )

@pytest.mark.parametrize(
	'floor, ceiling, comparand, expected'
	, [ ('fibonacci', 'prime', 'omega', True) , ('fibonacci', 'prime', 'tango', False) ]
)
def testOrdinalsBetweenWorksForStr(floor: str, ceiling: str, comparand: str, expected: bool) -> None:
	"""Verify `between` handles `str` operands.

	(AI generated docstring)

	Parameters
	----------
	floor : str
		Lower bound for `comparand`.
	ceiling : str
		Upper bound for `comparand`.
	comparand : str
		Value of `comparand` compared against the bounds.
	expected : bool
		Expected outcome from `between`.

	Returns
	-------
	unusedReturnValue : None
		Returns `None`.

	"""
	actual: bool = between(floor, ceiling, comparand)
	assert actual == expected, uniformTestFailureMessage( expected , actual , 'between' , floor , ceiling , comparand )

@pytest.mark.parametrize(
	'values, expected'
	, [ (['prime', 'fibonacci', 'omega'], ['fibonacci', 'omega', 'prime']) ]
)
def testOrdinalsSortingWorksForStr(values: list[str], expected: list[str]) -> None:
	"""Verify sorting uses ordinal ordering for `str` values.

	(AI generated docstring)

	Parameters
	----------
	values : list[str]
		Input `values` to sort.
	expected : list[str]
		Expected sorted output for `values`.

	Returns
	-------
	unusedReturnValue : None
		Returns `None`.

	"""
	actual: list[str] = sorted(values)
	assert actual == expected, uniformTestFailureMessage( expected , actual , 'sorted' , values )

@pytest.mark.parametrize(
	'floor, ceiling, comparand, expected'
	, [ ((13, 17), (21, 2), (13, 19), True) , ((13, 17), (21, 2), (8, 34), False) ]
)
def testOrdinalsBetweenWorksForTuple(floor: tuple[int, int], ceiling: tuple[int, int], comparand: tuple[int, int], expected: bool) -> None:
	"""Verify `between` handles `tuple[int, int]` operands.

	(AI generated docstring)

	Parameters
	----------
	floor : tuple[int, int]
		Lower bound for `comparand`.
	ceiling : tuple[int, int]
		Upper bound for `comparand`.
	comparand : tuple[int, int]
		Value of `comparand` compared against the bounds.
	expected : bool
		Expected outcome from `between`.

	Returns
	-------
	unusedReturnValue : None
		Returns `None`.

	"""
	actual: bool = between(floor, ceiling, comparand)
	assert actual == expected, uniformTestFailureMessage( expected , actual , 'between' , floor , ceiling , comparand )

@pytest.mark.parametrize( 'values, expected' , [ ( [(21, 2), (13, 19), (13, 17), (8, 34)] , [(8, 34), (13, 17), (13, 19), (21, 2)] ) ] )
def testOrdinalsSortingWorksForTuple(values: list[tuple[int, int]], expected: list[tuple[int, int]]) -> None:
	"""Verify sorting uses ordinal ordering for `tuple[int, int]` values.

	(AI generated docstring)

	Parameters
	----------
	values : list[tuple[int, int]]
		Input `values` to sort.
	expected : list[tuple[int, int]]
		Expected sorted output for `values`.

	Returns
	-------
	unusedReturnValue : None
		Returns `None`.

	"""
	actual: list[tuple[int, int]] = sorted(values)
	assert actual == expected, uniformTestFailureMessage( expected , actual , 'sorted' , values )

@pytest.mark.parametrize(
	'floor, ceiling, comparand, expected'
	, [
		(ComparableCardinal(13), ComparableCardinal(34), ComparableCardinal(21), True)
		, (ComparableCardinal(13), ComparableCardinal(34), ComparableCardinal(8), False)
	]
)
def testOrdinalsBetweenWorksForCustomComparable( floor: ComparableCardinal, ceiling: ComparableCardinal, comparand: ComparableCardinal, expected: bool ) -> None:
	"""Verify `between` handles `ComparableCardinal` operands.

	(AI generated docstring)

	Parameters
	----------
	floor : ComparableCardinal
		Lower `ComparableCardinal` bound for `comparand`.
	ceiling : ComparableCardinal
		Upper `ComparableCardinal` bound for `comparand`.
	comparand : ComparableCardinal
		Value of `comparand` compared against the bounds.
	expected : bool
		Expected outcome from `between`.

	Returns
	-------
	unusedReturnValue : None
		Returns `None`.

	"""
	actual: bool = between(floor, ceiling, comparand)
	assert actual == expected, uniformTestFailureMessage( expected , actual , 'between' , floor , ceiling , comparand )

@pytest.mark.parametrize( 'comparisonMethodName' , [ '__le__' , '__lt__' ] )
def testOrdinalsComparisonMethodsAcceptOtherOperand(comparisonMethodName: str) -> None:
	"""Validate `Ordinals` comparison method signatures.

	(AI generated docstring)

	Parameters
	----------
	comparisonMethodName : str
		Name of the `Ordinals` comparison method to inspect.

	Returns
	-------
	unusedReturnValue : None
		Returns `None`.

	"""
	comparisonMethod: Callable[[Ordinals, Ordinals], bool] = getattr(Ordinals, comparisonMethodName)
	signature: inspect.Signature = inspect.signature(comparisonMethod)
	listParameters: list[inspect.Parameter] = list(signature.parameters.values())

	assert len(listParameters) == 2, uniformTestFailureMessage(
		2 , len(listParameters) , 'Ordinals comparison parameter count' , comparisonMethodName , signature )

	listKinds: list[inspect._ParameterKind] = [parameter.kind for parameter in listParameters]
	expectedKinds: list[inspect._ParameterKind] = [inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_ONLY]
	assert listKinds == expectedKinds, uniformTestFailureMessage(
		expectedKinds , listKinds , 'Ordinals comparison parameter kinds' , comparisonMethodName , signature )

	actualReturnAnnotation: object = signature.return_annotation
	assert actualReturnAnnotation is bool, uniformTestFailureMessage(
		bool , actualReturnAnnotation , 'Ordinals comparison return annotation' , comparisonMethodName , signature )

def _plainFunction() -> None:
	"""A plain function for testing."""

@functools.wraps(_plainFunction)
def _wrappedFunction() -> None:
	"""A wrapped function for testing."""

_lambdaFunction = lambda: None  # noqa: E731

@pytest.mark.parametrize( 'candidate, expected' , [ (_wrappedFunction, True), (_plainFunction, False), (_lambdaFunction, False)] )
def testCallableFunctionIdentifiesCompatibleObjects(candidate: object, expected: bool) -> None:
	"""Verify `CallableFunction` protocol matching.

	(AI generated docstring)

	Parameters
	----------
	candidate : object
		The object to check against `CallableFunction`.
	expected : bool
		Expected result of `isinstance(candidate, CallableFunction)`.

	Return
	------
	unusedReturnValue : None
		Returns `None`.

	"""
	actual: bool = isinstance(candidate, CallableFunction)
	assert actual == expected, uniformTestFailureMessage(expected, actual, 'isinstance', candidate)
