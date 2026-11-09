"""Assert test contracts and report the call that broke them.

Other packages import these objects from `hunterMakesPy.tests`. Each assertion reports the target function and the
arguments that produced `actual`, then delegates the comparison to `==`, `pytest.approx`, or `numpy.testing`.
"""
from __future__ import annotations

from itertools import starmap
from typing import TYPE_CHECKING
import numpy.testing
import pytest

if TYPE_CHECKING:
	from numpy import dtype, ndarray
	from typing import Any

#================== Assert scalar and built-in containers ========================================================================

def assertEqualTo[个](actual: 个, expected: 个, function: str, *arguments: Any, **keywordArguments: Any) -> None:
	"""Assert that two objects are equal, and if not, raise an AssertionError with a detailed message."""
	assert actual == expected, messageTestFailure(actual, expected, function, *arguments, **keywordArguments)

def assert_approx[个](actual: 个, expected: 个, pytest_rel: float, pytest_abs: float, function: str, *arguments: Any, **keywordArguments: Any) -> None:
	"""Assert that two numbers or numeric containers are equal within `pytest.approx` tolerances; NaN equals NaN."""
	assert actual == pytest.approx(expected, pytest_rel, pytest_abs, nan_ok=True), messageTestFailure(actual, expected, function, *arguments, **keywordArguments)

def messageTestFailure(actual: Any, expected: Any, function: str, *arguments: Any, **keywordArguments: Any) -> str:
	"""Format assertion message for any test comparison."""
	parameters: list[str] = [*map(repr, arguments), *starmap('{}={!r}'.format, keywordArguments.items())]
	return f'{function}({", ".join(parameters)}) = {actual!r}, but {expected = }.'

#================== Assert NumPy arrays ==========================================================================================

def assert_array_equal[形ndarray: ndarray[tuple[Any, ...], dtype[Any]]](actual: 形ndarray, expected: 形ndarray, function: str, *arguments: Any, **keywordArguments: Any) -> None:
	"""Assert that two arrays have equal values, equal shapes, and equal dtypes."""
	numpy.testing.assert_array_equal(actual, expected, err_msg=messageTestFailure_ndarray(actual, expected, function, *arguments, **keywordArguments), strict=True)

def assert_allclose[形ndarray: ndarray[tuple[Any, ...], dtype[Any]]](actual: 形ndarray, expected: 形ndarray, rtol: float, atol: float, function: str, *arguments: Any, **keywordArguments: Any) -> None:
	"""Assert that two arrays have values equal within `rtol` and `atol`, equal shapes, and equal dtypes; NaN equals NaN."""
	numpy.testing.assert_allclose(actual, expected, rtol, atol, err_msg=messageTestFailure_ndarray(actual, expected, function, *arguments, **keywordArguments), strict=True)

def messageTestFailure_ndarray[形ndarray: ndarray[tuple[Any, ...], dtype[Any]]](actual: 形ndarray, expected: 形ndarray, function: str, *arguments: Any, **keywordArguments: Any) -> str:
	"""Format assertion message for an array comparison without printing the arrays."""
	parameters: list[str] = [*map(repr, arguments), *starmap('{}={!r}'.format, keywordArguments.items())]
	return f'{function}({", ".join(parameters)}) = {actual.shape=}, {actual.dtype=}, but {expected.shape=}, {expected.dtype=}.'
