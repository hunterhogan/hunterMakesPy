# pyright: standard
"""Tests for data structure utilities.

(AI generated docstring)

This module validates the behavior of data structure manipulation functions,
string conversion utilities, and Run-Length Encoding (RLE) tools.

"""
from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from hunterMakesPy.dataStructures import autoDecodingRLE, stringItUp, updateExtendPolishDictionaryLists
from hunterMakesPy.tests.conftest import standardizedEqualTo
from hunterMakesPy.tests.dataSamples.rle import AUTO_DECODING_RLE_CASES
from typing import Any, TYPE_CHECKING
import datetime
import librosa.filters
import numpy
import pytest

if TYPE_CHECKING:
	from collections.abc import Iterable, Iterator
	from numpy.typing import NDArray

class CustomIterable:
	"""A simple custom iterable for testing purposes.

	(AI generated docstring)

	Attributes
	----------
	items : Iterable[Any]
		The items to iterate over.

	"""
	def __init__(self, items: Iterable[Any]) -> None: self.items: Iterable[Any] = items
	def __iter__(self) -> Iterator[Any]: return iter(self.items)

@pytest.mark.parametrize("description,value_scrapPile,expected", [
	# Basic types and structures
	("Empty input", [], []),
	("Prime numbers", [11, 13, 17], ['11', '13', '17']),
	("Cardinal directions", ["NE", "SW", "SE"], ["NE", "SW", "SE"]),
	("Country codes", ["FR", "JP", "BR"], ["FR", "JP", "BR"]),
	("Boolean values", [True, False], ['True', 'False']),
	("None value", [None], ['None']),
	# Numbers and numeric types
	("Fibonacci floats", [2.584, -4.236, 6.854], ['2.584', '-4.236', '6.854']),
	("Complex with primes", [complex(11,0), complex(13,0)], ['(11+0j)', '(13+0j)']),
	("Decimal and Fraction", [Decimal('3.141'), Fraction(89, 55)], ['3.141', '89/55']),
	("NumPy primes", numpy.array([11, 13, 17]), ['11', '13', '17']),
	# Temporal types with meaningful dates
	("Historical date", [datetime.date(1789, 7, 14)], ['1789-07-14']),  # Bastille Day
	("Time zones", [datetime.time(23, 11, 37)], ['23:11:37']),  # Non-standard time
	("Moon landing", [datetime.datetime(1969, 7, 20, 20, 17, 40)], ['1969-07-20 20:17:40']),
	# Binary data - accepting either representation
	("Prime bytes", [b'\x0B', b'\x0D', b'\x11'], [repr(b'\x0b'), repr(b'\x0d'), repr(b'\x11')]),  # Let Python choose representation
	("Custom bytearray", [bytearray(b"DEADBEEF")], ["bytearray(b'DEADBEEF')"]),
	("Memory view decoded", memoryview(b"DEADBEEF"), ["DEADBEEF"]),
	# Nested structures with unique values
	("Nested dictionary", {'phi': 1.618, 'euler': 2.718}, ['phi', '1.618', 'euler', '2.718']),
	("Mixed nesting", [{'NE': 37}, {'SW': 41}], ['NE', '37', 'SW', '41']),
	("Tuples and lists", [(13, 17), [19, 23]], ['13', '17', '19', '23']),
	("Sets and frozensets", [{37, 41}, frozenset([43, 47])], ['41', '37', '43', '47']),
	# Special cases and error handling
	("NaN and Infinities", [float('nan'), float('inf'), -float('inf')], ['nan', 'inf', '-inf']),
	("Large prime", [10**19 + 33], ['10000000000000000033']),
	("Simple recursive", [[[...]]], ['Ellipsis']),  # Recursive list
	("Complex recursive", {'self': {'self': None}}, ['self', 'self', 'None']),
	# Generators and custom iterables
	("Generator from primes", (x for x in [11, 13, 17]), ['11', '13', '17']),
	("Iterator from Fibonacci", iter([3, 5, 8, 13]), ['3', '5', '8', '13']),
	("Custom iterable cardinal", CustomIterable(["NW", "SE", "NE"]), ["NW", "SE", "NE"]),
	("Custom iterable empty", CustomIterable([]), []),
	# Callable objects
	("User-defined function", [stringItUp], ['stringItUp']),
	("Lambda function", [lambda: None], ['<lambda>']),
	("Built-in function", [len], ['len']),
	("Class type", [int], ['int']),
	("Callable instance", [type('CallableClass', (), {'__call__': lambda self: None})()], ['CallableClass']),
	# Weird stuff
	("Bad __str__", type('BadStr', (), {'__str__': lambda x: None})(), [None]),
	# Error cases
	("Raising __str__", type('RaisingStr', (), {'__str__': lambda x: 1/0})(), ZeroDivisionError),
], ids=lambda x: x if isinstance(x, str) else "")
def test_stringItUp(description: str, value_scrapPile: list[Any], expected: list[str] | type[Exception]) -> None:
	"""Test stringItUp with various inputs.

	Parameters
	----------
	description : str
		Description of the test case.
	value_scrapPile : list[Any]
		List of values to convert to strings.
	expected : list[str] | type[Exception]
		Expected list of string representations or an Exception type.

	"""
	standardizedEqualTo(expected, stringItUp, value_scrapPile)

@pytest.mark.parametrize("description,value_dictionaryLists,keywordArguments,expected", [
	("Mixed value types", ({'ne': [11, 'prime'], 'sw': [True, None]}, {'ne': [3.141, 'golden'], 'sw': [False, 'void']}), {'destroyDuplicates': False, 'reorderLists': False}, {'ne': [11, 'prime', 3.141, 'golden'], 'sw': [True, None, False, 'void']}),
	("Empty dictionaries", (dict[str, list[Any]](), dict[str, list[Any]]()), dict[str, Any](), dict[str, list[Any]]()),
	("Tuple values", ({'ne': (11, 13), 'sw': (17,)}, {'ne': (19, 23, 13, 29, 11), 'sw': (31, 17, 37)}), {'destroyDuplicates': False, 'reorderLists': False}, {'ne': [11, 13, 19, 23, 13, 29, 11], 'sw': [17, 31, 17, 37]}),
	("Set values", ({'ne': {11, 13}, 'sw': {17}}, {'ne': {19, 23, 13, 29, 11}, 'sw': {31, 17, 37}}), {'destroyDuplicates': True, 'reorderLists': True}, {'ne': [11, 13, 19, 23, 29], 'sw': [17, 31, 37]}),
	("NumPy arrays", ({'ne': numpy.array([11, 13]), 'sw': numpy.array([17])}, {'ne': numpy.array([19, 23, 13, 29, 11]), 'sw': numpy.array([31, 17, 37])}), {'destroyDuplicates': False, 'reorderLists': False}, {'ne': [11, 13, 19, 23, 13, 29, 11], 'sw': [17, 31, 17, 37]}),
	("Destroy duplicates", ({'fr': [11, 13], 'jp': [17]}, {'fr': [19, 23, 13, 29, 11], 'jp': [31, 17, 37]}), {'destroyDuplicates': True, 'reorderLists': False}, {'fr': [11, 13, 19, 23, 29], 'jp': [17, 31, 37]}),
	("Non-string keys", ({None: [13], True: [17]}, {19: [23], (29, 31): [37]}), {'destroyDuplicates': False, 'reorderLists': False}, {'None': [13], 'True': [17], '19': [23], '(29, 31)': [37]}),
	("Reorder lists", ({'fr': [11, 13], 'jp': [17]}, {'fr': [19, 23, 13, 29, 11], 'jp': [31, 17, 37]}), {'destroyDuplicates': False, 'reorderLists': True}, {'fr': [11, 11, 13, 13, 19, 23, 29], 'jp': [17, 17, 31, 37]}),
	("Non-iterable values", ({'ne': 13, 'sw': 17}, {'ne': 19, 'nw': 23}), {'destroyDuplicates': False, 'reorderLists': False}, TypeError),
	("Skip erroneous types", ({'ne': [11, 13], 'sw': [17, 19]}, {'ne': 23, 'nw': 29}), {'killErroneousDataTypes': True}, {'ne': [11, 13], 'sw': [17, 19]}),
], ids=lambda x: x if isinstance(x, str) else "")
def test_updateExtendPolishDictionaryLists(description: str, value_dictionaryLists: tuple[dict[str, Any], ...], keywordArguments: dict[str, Any], expected: dict[str, Any] | type[TypeError]) -> None:
	"""Test dictionary list updating and extension logic.

	(AI generated docstring)

	Parameters
	----------
	description : str
		Description of the test case.
	value_dictionaryLists : tuple[dict[str, Any], ...]
		Tuple of dictionaries to merge/update.
	keywordArguments : dict[str, Any]
		Keyword arguments controlling the behavior (e.g., destroyDuplicates).
	expected : dict[str, Any] | type[TypeError]
		The expected result dictionary or an exception type.

	"""
	standardizedEqualTo(expected, updateExtendPolishDictionaryLists, *value_dictionaryLists, **keywordArguments)

@pytest.mark.parametrize(
	"assumeAddSpaces",
	[
		pytest.param(False, id="without-spaces"),
		pytest.param(True, id="with-spaces"),
	],
)
@pytest.mark.parametrize(
	"description,arrayExpression,expectedWithoutSpaces,expectedWithSpaces",
	[
		pytest.param(description, arrayExpression, expectedWithoutSpaces, expectedWithSpaces, id=description)
		for description, arrayExpression, expectedWithoutSpaces, expectedWithSpaces in AUTO_DECODING_RLE_CASES
	],
)
def test_autoDecodingRLE(
	description: str,
	arrayExpression: str,
	expectedWithoutSpaces: str,
	expectedWithSpaces: str,
	assumeAddSpaces: bool,
) -> None:
	"""Verify exact output, structural properties, and roundtrip decoding for all RLE cases."""
	expected: str = expectedWithSpaces if assumeAddSpaces else expectedWithoutSpaces

	evaluationContext: dict[str, Any] = {
		"numpy": numpy,
		"librosa": librosa,
		"range": range,
		"list": list,
	}
	value_arrayTarget: NDArray[numpy.integer[Any]] = eval(arrayExpression, evaluationContext)  # noqa: S307

	resultRLE: str = autoDecodingRLE(value_arrayTarget, assumeAddSpaces=assumeAddSpaces)

	assert isinstance(resultRLE, str), (
		f"autoDecodingRLE returned {type(resultRLE).__name__}, expected str for {description=} and {assumeAddSpaces=}."
	)
	assert "[" in resultRLE, (
		f"autoDecodingRLE returned {resultRLE!r}, expected '[' in output for {description=} and {assumeAddSpaces=}."
	)
	assert "]" in resultRLE, (
		f"autoDecodingRLE returned {resultRLE!r}, expected ']' in output for {description=} and {assumeAddSpaces=}."
	)

	rawStrLength: int = len(str(value_arrayTarget.tolist()))
	encodedLength: int = len(resultRLE)
	assert encodedLength <= rawStrLength, (
		f"autoDecodingRLE produced length {encodedLength}, expected <= {rawStrLength} for {description=} and {assumeAddSpaces=}."
	)

	assert resultRLE == expected, (
		f"autoDecodingRLE returned {resultRLE!r}, expected {expected!r} for {description=} and {assumeAddSpaces=}."
	)

	decodedData = eval(resultRLE)  # noqa: S307
	reconstructedArray: NDArray[numpy.integer[Any]] = numpy.array(decodedData)
	numpy.testing.assert_array_equal(
		reconstructedArray,
		value_arrayTarget,
		err_msg=(
			f"autoDecodingRLE roundtrip produced {reconstructedArray.tolist()}, "
			f"expected {value_arrayTarget.tolist()} for {description=} and {assumeAddSpaces=}."
		),
	)
