"""Expected values and exceptions come from the targets' docstrings unless a test's docstring names another basis."""
from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from hunterMakesPy.parseParameters import defineConcurrencyLimit, intInnit, oopsieKwargsie
from hunterMakesPy.tests import assertEqualTo
from hunterMakesPy.tests.dataSamples.classes import ListGrowsWhenIterated, StrReturnsNone
from hypothesis import given, strategies
from typing import Any, TYPE_CHECKING
import numpy
import pytest
import re as regex
import sys

if TYPE_CHECKING:
	from collections.abc import Collection
	from hunterMakesPy import ConcurrencyLimit

@pytest.mark.parametrize('limit, cpuTotal, expected', (
	pytest.param(None, 13, 13, id='None'),
	pytest.param(False, 13, 13, id='False'),
	pytest.param(0, 13, 13, id='zero'),
	pytest.param(0.0, 13, 13, id='zeroFloat'),
	pytest.param(True, 13, 1, id='True'),
	pytest.param(5, 13, 5, id='count5'),
	pytest.param(21, 13, 21, id='count21ExceedsCPUs'),
	pytest.param(1.5, 13, 2, id='count3HalvesRoundsUp'),
	pytest.param(2.5, 13, 2, id='count5HalvesRoundsToEven'),
	pytest.param(0.01, 13, 1, id='fraction1HundredthMinimum'),
	pytest.param(0.25, 13, 3, id='fraction1Quarter'),
	pytest.param(0.5, 13, 6, id='fraction1HalfRoundsToEven'),
	pytest.param(0.75, 13, 10, id='fraction3Quarters'),
	pytest.param(-0.25, 13, 10, id='reserveFraction1Quarter'),
	pytest.param(-0.5, 13, 7, id='reserveFraction1HalfRoundsToEven'),
	pytest.param(-0.99, 13, 1, id='reserveFraction99HundredthsMinimum'),
	pytest.param(-2.5, 13, 11, id='reserveCount5HalvesRoundsToEven'),
	pytest.param(-3, 13, 10, id='reserveCount3'),
	pytest.param(-21, 13, 1, id='reserveCount21Minimum'),
	pytest.param(' TRUE ', 13, 1, id='stringTRUE'),
	pytest.param('False', 13, 13, id='stringFalse'),
	pytest.param('none', 13, 13, id='stringNone'),
	pytest.param('4', 13, 4, id='string4'),
	pytest.param('1.51', 13, 2, id='string151Hundredths'),
	pytest.param('0.5', 13, 6, id='string1Half'),
	pytest.param('-3', 13, 10, id='stringReserve3'),
	pytest.param('-2.51', 13, 10, id='stringReserve251Hundredths'),
	pytest.param(89, 13, 61, id='count89Windows', marks=(markWindows := pytest.mark.skipif(sys.platform != 'win32', reason='Windows caps the worker count at 61.'))),
	pytest.param(89, 13, 89, id='count89', marks=(markNotWindows := pytest.mark.skipif(sys.platform == 'win32', reason='Only Windows caps the worker count at 61.'))),
	pytest.param(None, 144, 61, id='cpuTotal144Windows', marks=markWindows),
	pytest.param(None, 144, 144, id='cpuTotal144', marks=markNotWindows),
))
def test_defineConcurrencyLimit(limit: ConcurrencyLimit | str, cpuTotal: int, expected: int) -> None:
	concurrencyLimit = defineConcurrencyLimit(limit=limit, cpuTotal=cpuTotal)  # pyrefly: ignore[bad-argument-type] # ty: ignore[invalid-argument-type]
	assertEqualTo((concurrencyLimit, type(concurrencyLimit)), (expected, int), defineConcurrencyLimit.__name__, limit=limit, cpuTotal=cpuTotal)

@given(
	limit=strategies.one_of(strategies.none(), strategies.booleans(), strategies.integers(-233, 233), strategies.floats(-233, 233))
	, cpuTotal=strategies.integers(1, 1597)
)
def test_defineConcurrencyLimitBounds(limit: ConcurrencyLimit, cpuTotal: int) -> None:
	"""Limits span every documented rule: fractions and counts on both sides of zero, and counts beyond `cpuTotal`. `cpuTotal`
	reaches beyond the Windows cap of 61.
	"""
	concurrencyLimit: int = defineConcurrencyLimit(limit=limit, cpuTotal=cpuTotal)
	assert 1 <= concurrencyLimit, f'{defineConcurrencyLimit.__name__}({limit=}, {cpuTotal=}) = {concurrencyLimit}, but the minimum is 1.'
	assert sys.platform != 'win32' or concurrencyLimit <= 61, f'{defineConcurrencyLimit.__name__}({limit=}, {cpuTotal=}) = {concurrencyLimit}, but the Windows maximum is 61.'

@pytest.mark.parametrize('limit, cpuTotal, expected', (
	pytest.param('', 13, ValueError, id='stringEmpty'),
	pytest.param('NE', 13, ValueError, id='stringNE'),
	pytest.param('None of the above', 13, ValueError, id='stringNoneOfTheAbove'),
	pytest.param('True but not quite', 13, ValueError, id='stringTrueButNotQuite'),
))
def test_defineConcurrencyLimitError(limit: str, cpuTotal: int, expected: type[Exception]) -> None:
	with pytest.raises(expected, match='must be a number, `True`, `False`, or `None`'):
		defineConcurrencyLimit(limit=limit, cpuTotal=cpuTotal)  # pyrefly: ignore[bad-argument-type] # ty: ignore[invalid-argument-type]

@pytest.mark.parametrize('parameterType', (None, tuple))
@pytest.mark.parametrize('parameterName', (None, pytest.param('', id='stringEmpty'), 'ports'))
@pytest.mark.parametrize('listInt_Allegedly, expected', (
	pytest.param([2, 3, 5, 8], [2, 3, 5, 8], id='listInt'),
	pytest.param((3, 5, 7), [3, 5, 7], id='tupleInt'),
	pytest.param(range(3, 7), [3, 4, 5, 6], id='range'),
	pytest.param([13.0, 21.0, 34.0], [13, 21, 34], id='listFloatWhole'),
	pytest.param(['55', '89', '144'], [55, 89, 144], id='listString'),
	pytest.param([' 233 ', '377', '-610'], [233, 377, -610], id='listStringWhitespaceNegative'),
	pytest.param([13, '21', 34.0], [13, 21, 34], id='listMixed'),
	pytest.param([13 + 0j, 21 + 0j], [13, 21], id='listComplexReal'),
	pytest.param([b'123'], [123], id='listBytes'),
	pytest.param([bytearray(b'21')], [21], id='listBytearray'),
	pytest.param([memoryview(b'9999999999')], [9999999999], id='listMemoryview'),
	pytest.param([numpy.int64(89), numpy.int32(144)], [89, 144], id='listNumpyIntegers'),
	pytest.param([Decimal('233.0'), Fraction(754, 2)], [233, 377], id='listDecimalFractionWhole'),
	pytest.param(['9007199254740993'], [9007199254740993], id='listStringAbove2上53'),
	pytest.param(numpy.array([89, 144]), [89, 144], id='arrayNumpy'),
))
def test_intInnit(listInt_Allegedly: Collection[Any], parameterName: str | None, parameterType: type | None, expected: list[int]) -> None:
	listInt: list[int] = intInnit(listInt_Allegedly, parameterName, parameterType)
	assertEqualTo((listInt, [*map(type, listInt)]), (expected, [*map(type, expected)]), intInnit.__name__, listInt_Allegedly, parameterName, parameterType)

@given(strategies.lists(strategies.integers(), min_size=1))
def test_intInnitGenerated(listInt: list[int]) -> None:
	assertEqualTo(intInnit(listInt), listInt, intInnit.__name__, listInt)
	assertEqualTo(intInnit([*map(str, listInt)]), listInt, intInnit.__name__, [*map(str, listInt)])

@pytest.mark.parametrize('parameterType', (None, tuple))
@pytest.mark.parametrize('parameterName', (None, pytest.param('', id='stringEmpty'), 'ports'))
@pytest.mark.parametrize('listInt_Allegedly, expected, message', (
	pytest.param([], ValueError, 'I did not receive a value for `{parameterName}`', id='listEmpty'),
	pytest.param(None, ValueError, 'I did not receive a value for `{parameterName}`', id='None'),
	pytest.param(13, TypeError, "object of type 'int' has no len()", id='intNotCollection'),
	pytest.param([True], TypeError, (messageElement := '{parameterName}` must have integers in type(s) `{parameterType}`'), id='listBool'),
	pytest.param([13.7], ValueError, messageElement, id='listFloatFractional'),
	pytest.param([float('inf')], ValueError, messageElement, id='listInfinity'),
	pytest.param([float('nan')], ValueError, messageElement, id='listNaN'),
	pytest.param(['NW'], ValueError, messageElement, id='listStringNW'),
	pytest.param([''], ValueError, messageElement, id='listStringEmpty'),
	pytest.param(['SE.SW'], ValueError, messageElement, id='listStringDotted'),
	pytest.param([13 + 1j], ValueError, messageElement, id='listComplexImaginary'),
	pytest.param([34.5 + 0j], ValueError, messageElement, id='listComplexFractional'),
	pytest.param([b'\x00'], ValueError, messageElement, id='listBytesNull'),
	pytest.param([memoryview(b'\x00')], ValueError, messageElement, id='listMemoryviewNull'),
	pytest.param([None], TypeError, messageElement, id='listNone'),
	pytest.param([[17, 39]], TypeError, messageElement, id='listNested'),
	pytest.param(ListGrowsWhenIterated([13, 21, 34]), RuntimeError, 'length of `{parameterName}` change from `3` to `4`', id='listGrowsWhenIterated'),
	pytest.param([Decimal('13.5')], ValueError, messageElement, id='listDecimalFractional'),
	pytest.param([Fraction(27, 2)], ValueError, messageElement, id='listFractionFractional'),
), indirect=['listInt_Allegedly'])
def test_intInnitError(listInt_Allegedly: Collection[Any] | int | None, parameterName: str | None, parameterType: type | None, expected: type[Exception], message: str) -> None:
	with pytest.raises(expected, match=regex.escape(message.format(parameterName=parameterName or 'the parameter', parameterType=parameterType or list))):
		intInnit(listInt_Allegedly, parameterName, parameterType)  # pyrefly: ignore[bad-argument-type] # ty: ignore[invalid-argument-type]

@pytest.mark.parametrize('huh, expected', (
	pytest.param('True', True, id='True'),
	pytest.param('TRUE', True, id='TRUE'),
	pytest.param(' true ', True, id='trueWhitespace'),
	pytest.param('TrUe', True, id='TrUe'),
	pytest.param('False', False, id='False'),
	pytest.param('FALSE', False, id='FALSE'),
	pytest.param('\tfalse\n', False, id='falseWhitespace'),
	pytest.param('None', None, id='None'),
	pytest.param('NONE', None, id='NONE'),
	pytest.param(' none ', None, id='noneWhitespace'),
	pytest.param('NE', 'NE', id='stringNE'),
	pytest.param('123', '123', id='stringDigits'),
	pytest.param('True story', 'True story', id='stringTrueStory'),
	pytest.param('', '', id='stringEmpty'),
	pytest.param(123, '123', id='int'),
	pytest.param(True, True, id='boolTrue'),
	pytest.param(None, None, id='objectNone'),
	pytest.param((objectStrReturnsNone := StrReturnsNone()), objectStrReturnsNone, id='objectStrReturnsNone'),
))
def test_oopsieKwargsie(huh: Any, expected: object) -> None:
	interpretation: bool | str | None = oopsieKwargsie(huh)
	assertEqualTo((interpretation, type(interpretation)), (expected, type(expected)), oopsieKwargsie.__name__, huh)
