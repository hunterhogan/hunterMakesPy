"""Configuration and fixtures for pytest.

(AI generated docstring)

This module provides shared fixtures and utility functions for the test suite,
including data paths, source code samples, and standardized assertion functions.

"""
# pyright: standard
from collections.abc import Callable
from typing import Any
import io
import pathlib
import pytest

# SSOT for test data paths and filenames
pathDataSamples: pathlib.Path = pathlib.Path("hunterMakesPy/tests/dataSamples")

# Fixture to provide a temporary directory for filesystem tests
@pytest.fixture
def pathTmpTesting(tmp_path: pathlib.Path) -> pathlib.Path:
	"""Provide a temporary directory for filesystem tests.

	(AI generated docstring)

	Parameters
	----------
	tmp_path : pathlib.Path
		The pytest built-in temporary path fixture.

	Returns
	-------
	pathTmpTesting : pathlib.Path
		The path to the temporary directory.

	"""
	return tmp_path

# Fixture for predictable Python source code samples
@pytest.fixture
def dictionaryPythonSourceSamples() -> dict[str, str]:
	"""Provide predictable Python source code samples for testing."""
	return {
		'functionFibonacci': "def fibonacciNumber():\n    return 13\n",
		'functionPrime': "def primeNumber():\n    return 17\n",
		'variablePrime': "prime = 19\n",
		'variableFibonacci': "fibonacci = 21\n",
		'classCardinal': "class CardinalDirection:\n    north = 'N'\n    south = 'S'\n",
	}

# Fixture for IO stream objects
@pytest.fixture
def streamMemoryString() -> io.StringIO:
	"""Provide a StringIO object for testing stream operations."""
	return io.StringIO()

# Fixture for predictable directory names using cardinal directions
@pytest.fixture
def listDirectoryNamesCardinal() -> list[str]:
	"""Provide predictable directory names using cardinal directions."""
	return ['north', 'south', 'east', 'west']

# Fixture for predictable file content using Fibonacci numbers
@pytest.fixture
def listFileContentsFibonacci() -> list[str]:
	"""Provide predictable file contents using Fibonacci sequence."""
	return ['fibonacci8', 'fibonacci13', 'fibonacci21', 'fibonacci34']

def uniformTestFailureMessage(expected: Any, actual: Any, functionName: str, *arguments: Any, **keywordArguments: Any) -> str:
	"""Format assertion message for any test comparison.

	Parameters
	----------
	expected : Any
		The expected value or outcome.
	actual : Any
		The actual value or outcome received.
	functionName : str
		The name of the function or test case being executed.
	*arguments : Any
		Positional arguments passed to the function having its return value checked.
	**keywordArguments : Any
		Keyword arguments passed to the function having its return value checked.

	Returns
	-------
	message : str
		A formatted failure message detailing the expectation vs reality.

	"""
	listArgumentComponents: list[str] = [str(parameter) for parameter in arguments]
	listKeywordComponents: list[str] = [f"{key}={value}" for key, value in keywordArguments.items()]
	joinedArguments: str = ', '.join(listArgumentComponents + listKeywordComponents)

	return (f"\nTesting: `{functionName}({joinedArguments})`\n"
			f"Expected: {expected}\n"
			f"Got: {actual}")

def standardizedEqualTo(expected: Any, functionTarget: Callable[..., Any], *arguments: Any, **keywordArguments: Any) -> None:
	"""Template for most tests to compare actual outcome with expected outcome.

	Includes handling for expected errors/exceptions.

	Parameters
	----------
	expected : Any
		The expected return value, or an Exception type if an error is expected.
	functionTarget : Callable[..., Any]
		The function to call and test.
	*arguments : Any
		Positional arguments to pass to `functionTarget`.
	**keywordArguments : Any
		Keyword arguments to pass to `functionTarget`.

	"""
	if type(expected) == type[Exception]:  # noqa: E721
		messageExpected: str = expected.__name__
	else:
		messageExpected = expected

	try:
		messageActual = actual = functionTarget(*arguments, **keywordArguments)
	except Exception as actualError:
		messageActual = type(actualError).__name__
		actual = type(actualError)

	functionName: str = getattr(functionTarget, "__name__", functionTarget.__class__.__name__)
	assert actual == expected, uniformTestFailureMessage(messageExpected, messageActual, functionName, *arguments, **keywordArguments)

# Why I wish I could figure out how to implement standardized* test functions.
# ruff: noqa: ERA001
	# standardizedEqualTo(expected, updateExtendPolishDictionaryLists, *value_dictionaryLists, **keywordArguments)
# NOTE one line of code with `standardizedEqualTo` (above) replaced the following ten lines of code. Use `standardizedEqualTo`.
	# if isinstance(expected, type) and issubclass(expected, Exception):
	#	 with pytest.raises(expected):
	#		 updateExtendPolishDictionaryLists(*value_dictionaryLists, **keywordArguments)
	# else:
	#	 result = updateExtendPolishDictionaryLists(*value_dictionaryLists, **keywordArguments)
	#	 if description == "Set values":  # Special handling for unordered sets
	#		 for key in result:
	#			 assert sorted(result[key]) == sorted(expected[key])
	#	 else:
	#		 assert result == expected
