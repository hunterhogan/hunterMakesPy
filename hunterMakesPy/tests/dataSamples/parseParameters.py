"""Samples and expected results for `hunterMakesPy.parseParameters`."""
from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from hunterMakesPy.tests.dataSamples.classes import ListGrowsWhenIterated, StrReturnsNone
from typing import TYPE_CHECKING
import numpy
import pytest
import sys

if TYPE_CHECKING:
	from _pytest.mark.structures import ParameterSet

#================== defineConcurrencyLimit =======================================================================================

markWindows: pytest.MarkDecorator = pytest.mark.skipif(sys.platform != 'win32', reason='Windows caps the worker count at 61.')
markNotWindows: pytest.MarkDecorator = pytest.mark.skipif(sys.platform == 'win32', reason='Only Windows caps the worker count at 61.')

# Reference: hand-derived from the rules in the `defineConcurrencyLimit` docstring. Python `round` rounds ties to even.
parametersDefineConcurrencyLimit: tuple[ParameterSet, ...] = (
	pytest.param(None, 13, 13, id='None'),
	pytest.param(False, 13, 13, id='False'),
	pytest.param(0, 13, 13, id='zero'),
	pytest.param(0.0, 13, 13, id='zeroFloat'),
	pytest.param(True, 13, 1, id='True'),
	pytest.param(5, 13, 5, id='count5'),
	pytest.param(21, 13, 21, id='count21ExceedsCPUs'),
	pytest.param(1.5, 13, 2, id='count1.5RoundsUp'),
	pytest.param(2.5, 13, 2, id='count2.5RoundsToEven'),
	pytest.param(0.01, 13, 1, id='fraction0.01Minimum'),
	pytest.param(0.25, 13, 3, id='fraction0.25'),
	pytest.param(0.5, 13, 6, id='fraction0.5RoundsToEven'),
	pytest.param(0.75, 13, 10, id='fraction0.75'),
	pytest.param(-0.25, 13, 10, id='reserveFraction0.25'),
	pytest.param(-0.5, 13, 7, id='reserveFraction0.5RoundsToEven'),
	pytest.param(-0.99, 13, 1, id='reserveFraction0.99Minimum'),
	pytest.param(-2.5, 13, 11, id='reserveCount2.5RoundsToEven'),
	pytest.param(-3, 13, 10, id='reserveCount3'),
	pytest.param(-21, 13, 1, id='reserveCount21Minimum'),
	pytest.param(' TRUE ', 13, 1, id='stringTRUE'),
	pytest.param('False', 13, 13, id='stringFalse'),
	pytest.param('none', 13, 13, id='stringNone'),
	pytest.param('4', 13, 4, id='string4'),
	pytest.param('1.51', 13, 2, id='string1.51'),
	pytest.param('0.5', 13, 6, id='string0.5'),
	pytest.param('-3', 13, 10, id='stringReserve3'),
	pytest.param('-2.51', 13, 10, id='stringReserve2.51'),
	pytest.param(89, 13, 61, id='count89Windows', marks=markWindows),
	pytest.param(89, 13, 89, id='count89', marks=markNotWindows),
	pytest.param(None, 144, 61, id='cpuTotal144Windows', marks=markWindows),
	pytest.param(None, 144, 144, id='cpuTotal144', marks=markNotWindows),
)

# Reference: the docstring states that a string must represent a number, `True`, `False`, or `None`.
parametersDefineConcurrencyLimitError: tuple[ParameterSet, ...] = (
	pytest.param('', 13, ValueError, id='stringEmpty'),
	pytest.param('NE', 13, ValueError, id='stringNE'),
	pytest.param('None of the above', 13, ValueError, id='stringNoneOfTheAbove'),
	pytest.param('True but not quite', 13, ValueError, id='stringTrueButNotQuite'),
)

#================== intInnit =====================================================================================================

# Reference: the docstring lists integers, NumPy integers, strings, floats, `Decimal`, `Fraction`, complex numbers, and binary
# data as integer-compatible, and states that conversion keeps every digit.
parametersIntInnit: tuple[ParameterSet, ...] = (
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
	pytest.param(['9007199254740993'], [9007199254740993], id='listStringAbove2**53'),
	pytest.param(numpy.array([89, 144]), [89, 144], id='arrayNumpy'),
)

# Reference: the docstring states that `intInnit` raises `ValueError` for `None`, empty input, and non-integer values, and
# `TypeError` for input without a length, booleans, and incompatible element types.
parametersIntInnitError: tuple[ParameterSet, ...] = (
	pytest.param([], ValueError, id='listEmpty'),
	pytest.param(None, ValueError, id='None'),
	pytest.param(13, TypeError, id='intNotCollection'),
	pytest.param([True], TypeError, id='listBool'),
	pytest.param([13.7], ValueError, id='listFloatFractional'),
	pytest.param([float('inf')], ValueError, id='listInfinity'),
	pytest.param([float('nan')], ValueError, id='listNaN'),
	pytest.param(['NW'], ValueError, id='listStringNW'),
	pytest.param([''], ValueError, id='listStringEmpty'),
	pytest.param(['SE.SW'], ValueError, id='listStringDotted'),
	pytest.param([13 + 1j], ValueError, id='listComplexImaginary'),
	pytest.param([34.5 + 0j], ValueError, id='listComplexFractional'),
	pytest.param([b'\x00'], ValueError, id='listBytesNull'),
	pytest.param([memoryview(b'\x00')], ValueError, id='listMemoryviewNull'),
	pytest.param([None], TypeError, id='listNone'),
	pytest.param([[17, 39]], TypeError, id='listNested'),
	pytest.param(ListGrowsWhenIterated([13, 21, 34]), RuntimeError, id='listGrowsWhenIterated'),
	pytest.param([Decimal('13.5')], ValueError, id='listDecimalFractional'),
	pytest.param([Fraction(27, 2)], ValueError, id='listFractionFractional'),
)

#================== oopsieKwargsie ===============================================================================================

objectStrReturnsNone: StrReturnsNone = StrReturnsNone()

# Reference: the docstring states that `oopsieKwargsie` returns `True`, `False`, `None`, or the original string. Accepted
# recording: a non-string becomes `str(huh)` before interpretation, and an object that `str` rejects returns unchanged.
parametersOopsieKwargsie: tuple[ParameterSet, ...] = (
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
	pytest.param(objectStrReturnsNone, objectStrReturnsNone, id='objectStrReturnsNone'),
)
