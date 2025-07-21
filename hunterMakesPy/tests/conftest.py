# pyright: standard
from collections.abc import Callable
from typing import Any
import io
import pathlib
import pytest

# SSOT for test data paths and filenames
pathDataSamples = pathlib.Path("hunterMakesPy/tests/dataSamples")

# Fixture to provide a temporary directory for filesystem tests
@pytest.fixture
def pathTmpTesting(tmp_path: pathlib.Path) -> pathlib.Path:
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
	"""Format assertion message for any test comparison."""
	listArgumentComponents: list[str] = [str(parameter) for parameter in arguments]
	listKeywordComponents: list[str] = [f"{key}={value}" for key, value in keywordArguments.items()]
	joinedArguments: str = ', '.join(listArgumentComponents + listKeywordComponents)

	return (f"\nTesting: `{functionName}({joinedArguments})`\n"
			f"Expected: {expected}\n"
			f"Got: {actual}")

def standardizedEqualTo(expected: Any, functionTarget: Callable[..., Any], *arguments: Any, **keywordArguments: Any) -> None:
	"""Template for most tests to compare the actual outcome with the expected outcome, including expected errors."""
	if type(expected) == type[Exception]:  # noqa: E721
		messageExpected: str = expected.__name__
	else:
		messageExpected = expected

	try:
		messageActual = actual = functionTarget(*arguments, **keywordArguments)
	except Exception as actualError:
		messageActual: str = type(actualError).__name__
		actual = type(actualError)

	assert actual == expected, uniformTestFailureMessage(messageExpected, messageActual, functionTarget.__name__, *arguments, **keywordArguments)
