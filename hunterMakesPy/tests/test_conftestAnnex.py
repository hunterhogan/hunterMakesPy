"""Expected values and exceptions come from the docstrings of `hunterMakesPy.tests.conftestAnnex` unless a comment names another basis."""
from __future__ import annotations

from hunterMakesPy.tests import assert_allclose, assert_array_equal, assertEqualTo, messageTestFailure, messageTestFailure_ndarray
from hunterMakesPy.tests.dataSamples.arrays import array2x3Primes, arrayRange, arrayRepeat, boxOfArraysInteger
from typing import Any, TYPE_CHECKING
import numpy
import pytest

if TYPE_CHECKING:
	from numpy.typing import NDArray

# Accepted recording: the message format, which reads as the call that produced `actual`.
@pytest.mark.parametrize('actual, expected, function, arguments, keywordArguments, messageExpected', (
	pytest.param([13], [21], 'intInnit', (['NW'],), {}, "intInnit(['NW']) = [13], but expected = [21].", id='intInnit-positional'),
	pytest.param(
		13, 21, 'defineConcurrencyLimit', (), {'limit': 0.5, 'cpuTotal': 13}
		, 'defineConcurrencyLimit(limit=0.5, cpuTotal=13) = 13, but expected = 21.', id='defineConcurrencyLimit-keyword'
	),
	pytest.param('NE', 'SW', 'oopsieKwargsie', (), {}, "oopsieKwargsie() = 'NE', but expected = 'SW'.", id='oopsieKwargsie-none'),
))
def test_messageTestFailure(actual: Any, expected: Any, function: str, arguments: tuple[Any, ...], keywordArguments: dict[str, Any], messageExpected: str) -> None:
	assertEqualTo(
		messageTestFailure(actual, expected, function, *arguments, **keywordArguments)
		, messageExpected, messageTestFailure.__name__, actual, expected, function, *arguments, **keywordArguments
	)

# Accepted recording: the message format, which reports shapes and dtypes and never the arrays.
@pytest.mark.parametrize('actual, expected, messageExpected', (
	pytest.param(
		arrayRange, arrayRange.astype(numpy.float64)
		, "autoDecodingRLE() = actual.shape=(10,), actual.dtype=dtype('int64'), but expected.shape=(10,), expected.dtype=dtype('float64')."
		, id='arrayRange-float64'
	),
))
def test_messageTestFailure_ndarray(actual: NDArray[Any], expected: NDArray[Any], messageExpected: str) -> None:
	assertEqualTo(messageTestFailure_ndarray(actual, expected, 'autoDecodingRLE'), messageExpected, messageTestFailure_ndarray.__name__, actual.shape, expected.shape)

# Relation: an array equals its copy.
@pytest.mark.parametrize('arrayTarget', boxOfArraysInteger)
def test_assert_array_equal(arrayTarget: NDArray[numpy.integer[Any]]) -> None:
	assert_array_equal(arrayTarget, arrayTarget.copy(), assert_array_equal.__name__)

# `numpy.testing` without `strict=True` accepts the first two pairs: equal values in another dtype, and a zero-dimensional
# array against an array of its value.
@pytest.mark.parametrize('actual, expected', (
	pytest.param(array2x3Primes, array2x3Primes.astype(numpy.float64), id='array2x3Primes-float64'),
	pytest.param(arrayRepeat, numpy.array(191), id='arrayRepeat-scalar191'),
	pytest.param(arrayRange, arrayRange + 1, id='arrayRange-arrayRangePlus1'),
))
def test_assert_array_equalError(actual: NDArray[Any], expected: NDArray[Any]) -> None:
	with pytest.raises(AssertionError):
		assert_array_equal(actual, expected, assert_array_equal.__name__)

@pytest.mark.parametrize('actual, expected, rtol, atol', (
	pytest.param(numpy.array([numpy.nan, 1.0]), numpy.array([numpy.nan, 1.0]), 1e-7, 0, id='NaN'),
	pytest.param(numpy.array([1.0]), numpy.array([1.0 + 1e-9]), 1e-7, 0, id='withinRelativeTolerance'),
))
def test_assert_allclose(actual: NDArray[Any], expected: NDArray[Any], rtol: float, atol: float) -> None:
	assert_allclose(actual, expected, rtol, atol, assert_allclose.__name__)

# `numpy.testing` without `strict=True` accepts the first two pairs: equal values in another dtype, and a zero-dimensional
# array against an array of its value.
@pytest.mark.parametrize('actual, expected, rtol, atol', (
	pytest.param(numpy.arange(3.0, dtype=numpy.float32), numpy.arange(3.0), 1e-7, 0, id='float32-float64'),
	pytest.param(numpy.full(3, 0.5), numpy.array(0.5), 1e-7, 0, id='full3Half-scalarHalf'),
	pytest.param(numpy.array([1.0]), numpy.array([1.001]), 1e-7, 0, id='beyondRelativeTolerance'),
))
def test_assert_allcloseError(actual: NDArray[Any], expected: NDArray[Any], rtol: float, atol: float) -> None:
	with pytest.raises(AssertionError):
		assert_allclose(actual, expected, rtol, atol, assert_allclose.__name__)
