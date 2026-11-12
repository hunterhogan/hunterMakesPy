"""Expected values and exceptions come from the targets' docstrings unless a comment names another basis."""
from __future__ import annotations

from collections import deque
from decimal import Decimal
from fractions import Fraction
from hunterMakesPy.dataStructures import autoDecodingRLE, removeExtraWhitespace, stringItUp, updateExtendPolishDictionaryLists
from hunterMakesPy.tests import assert_array_equal, assertEqualTo
from hunterMakesPy.tests.dataSamples.arrays import (
	array2x2x2Primes, array2x3Primes, array2x3x5Range, array3x20RangeRun, array8x8Checkerboard, array10x12Stripes, array13x9Saddle,
	array60x1025MelMask, array100x100Modular, arrayEmpty, arrayRange, arrayRangeNegative, arrayRangeRange, arrayRangeRepeat, arrayRangeRun,
	arrayRangeValue, arrayRepeat, arrayRepeatRange, arrayRepeatRangeValue, arrayRepeatRepeatValue, arrayRunsFibonacci, arrayScalarFibonacci,
	arrayValueRange, arrayValueRangeRepeat, arrayValueRangeRunValue, arrayValueRangeValue, arrayValueRepeat, arrayValueRepeatNegative,
	boxOfArraysInteger)
from hunterMakesPy.tests.dataSamples.arraysRLE import (
	rleArray8x8Checkerboard, rleArray13x9Saddle, rleArray60x1025MelMask, rleArray100x100Modular)
from hunterMakesPy.tests.dataSamples.callables import (
	callableItemGetter, callablePartial, functionBuiltin, functionCached, functionPurePython)
from hunterMakesPy.tests.dataSamples.classes import (
	StrDividesByZero, StrFormatsBadSpecification, StrReadsAbsentAttribute, StrReturnsNone, StrReturnsNoneText)
from hypothesis import given, strategies
from hypothesis.extra.numpy import array_shapes, arrays
from typing import TYPE_CHECKING
import copy
import datetime
import numpy
import pytest

if TYPE_CHECKING:
	from collections.abc import Iterable, Mapping
	from numpy.typing import NDArray
	from typing import Any

# Accepted recording: outputs of `autoDecodingRLE` accepted before this suite was reorganized. The round-trip relation in
# `test_autoDecodingRLERoundTrip` independently establishes that each output decodes to its array.
@pytest.mark.parametrize('arrayTarget, assumeAddSpaces, expected', (
	pytest.param(arrayRange, False, '[*range(50,60)]', id='arrayRange-False'),
	pytest.param(arrayRange, True, '[*range(50,60)]', id='arrayRange-True'),
	pytest.param(arrayValueRange, False, '[123,*range(71,81)]', id='arrayValueRange-False'),
	pytest.param(arrayValueRange, True, '[123,*range(71,81)]', id='arrayValueRange-True'),
	pytest.param(arrayRangeValue, False, '[*range(91,97),101]', id='arrayRangeValue-False'),
	pytest.param(arrayRangeValue, True, '[*range(91,97),101]', id='arrayRangeValue-True'),
	pytest.param(arrayValueRangeValue, False, '[151,*range(163,171),181]', id='arrayValueRangeValue-False'),
	pytest.param(arrayValueRangeValue, True, '[151,*range(163,171),181]', id='arrayValueRangeValue-True'),
	pytest.param(arrayRepeat, False, '[191]*3', id='arrayRepeat-False'),
	pytest.param(arrayRepeat, True, '[191]*3', id='arrayRepeat-True'),
	pytest.param(arrayValueRepeat, False, '[211]+[223]*3', id='arrayValueRepeat-False'),
	pytest.param(arrayValueRepeat, True, '[211]+[223]*3', id='arrayValueRepeat-True'),
	pytest.param(arrayValueRepeatNegative, False, '[5]+[-3]*3', id='arrayValueRepeatNegative-False'),
	pytest.param(arrayValueRepeatNegative, True, '[5]+[-3]*3', id='arrayValueRepeatNegative-True'),
	pytest.param(arrayRangeRepeat, False, '[*range(251,257)]+[271]*3', id='arrayRangeRepeat-False'),
	pytest.param(arrayRangeRepeat, True, '[*range(251,257)]+[271]*3', id='arrayRangeRepeat-True'),
	pytest.param(arrayRepeatRepeatValue, False, '[313]*3+[331]*2+[349]', id='arrayRepeatRepeatValue-False'),
	pytest.param(arrayRepeatRepeatValue, True, '[313]*3+[331]*2+[349]', id='arrayRepeatRepeatValue-True'),
	pytest.param(arrayRepeatRange, False, '[373]*3+[*range(383,389)]', id='arrayRepeatRange-False'),
	pytest.param(arrayRepeatRange, True, '[373]*3+[*range(383,389)]', id='arrayRepeatRange-True'),
	pytest.param(arrayRangeNegative, False, '[*range(-34,35)]', id='arrayRangeNegative-False'),
	pytest.param(arrayRangeNegative, True, '[*range(-34,35)]', id='arrayRangeNegative-True'),
	pytest.param(arrayValueRangeRepeat, False, '[281,*range(291,297)]+[307]*2', id='arrayValueRangeRepeat-False'),
	pytest.param(arrayValueRangeRepeat, True, '[281,*range(291,297)]+[307]*2', id='arrayValueRangeRepeat-True'),
	pytest.param(arrayRepeatRangeValue, False, '[401]*7+[*range(409,415),421]', id='arrayRepeatRangeValue-False'),
	pytest.param(arrayRepeatRangeValue, True, '[401]*7+[*range(409,415),421]', id='arrayRepeatRangeValue-True'),
	pytest.param(arrayRangeRange, False, '[*range(461,471),*range(479,487)]', id='arrayRangeRange-False'),
	pytest.param(arrayRangeRange, True, '[*range(461,471),*range(479,487)]', id='arrayRangeRange-True'),
	pytest.param(array2x3Primes, False, '[[491,499,503],[509,521,523]]', id='array2x3Primes-False'),
	pytest.param(array2x3Primes, True, '[[491,499,503],[509,521,523]]', id='array2x3Primes-True'),
	pytest.param(array2x2x2Primes, False, '[[[541,547],[557,563]],[[569,571],[577,587]]]', id='array2x2x2Primes-False'),
	pytest.param(array2x2x2Primes, True, '[[[541,547],[557,563]],[[569,571],[577,587]]]', id='array2x2x2Primes-True'),
	pytest.param(arrayRunsFibonacci, False, '[3]*4+[8,8]+[13]*5+[21]', id='arrayRunsFibonacci-False'),
	pytest.param(arrayRunsFibonacci, True, '[3]*4+[8,8]+[13]*5+[21]', id='arrayRunsFibonacci-True'),
	pytest.param(array8x8Checkerboard, False, rleArray8x8Checkerboard, id='array8x8Checkerboard-False'),
	pytest.param(array8x8Checkerboard, True, rleArray8x8Checkerboard, id='array8x8Checkerboard-True'),
	pytest.param(array10x12Stripes, False, '[[0]*12,[0]*12,[1]*12,[1]*12,[2]*12,[2]*12,[3]*12,[3]*12,[4]*12,[4]*12]', id='array10x12Stripes-False'),
	pytest.param(array10x12Stripes, True, '[[0]*12,[0]*12,[1]*12,[1]*12,[2]*12,[2]*12,[3]*12,[3]*12,[4]*12,[4]*12]', id='array10x12Stripes-True'),
	pytest.param(array13x9Saddle, False, rleArray13x9Saddle, id='array13x9Saddle-False'),
	pytest.param(array13x9Saddle, True, rleArray13x9Saddle, id='array13x9Saddle-True'),
	pytest.param(array2x3x5Range, False, '[[[0,1,2,3,4],[5,6,7,8,9],[*range(10,15)]],[[*range(15,20)],[*range(20,25)],[*range(25,30)]]]', id='array2x3x5Range-False'),
	pytest.param(array2x3x5Range, True, '[[[*range(5)],[5,6,7,8,9],[*range(10,15)]],[[*range(15,20)],[*range(20,25)],[*range(25,30)]]]', id='array2x3x5Range-True'),
	pytest.param(array100x100Modular, False, rleArray100x100Modular, id='array100x100Modular-False'),
	pytest.param(array100x100Modular, True, rleArray100x100Modular, id='array100x100Modular-True'),
	pytest.param(array60x1025MelMask, False, rleArray60x1025MelMask, id='array60x1025MelMask-False'),
	pytest.param(array60x1025MelMask, True, rleArray60x1025MelMask, id='array60x1025MelMask-True'),
	# Reference: hand-derived from the docstring's two strategies. A run of a range is multiplication syntax around range syntax.
	pytest.param(arrayRangeRun, False, '[*range(-5,5)]*3', id='arrayRangeRun-False'),
	pytest.param(arrayRangeRun, True, '[*range(-5,5)]*3', id='arrayRangeRun-True'),
	pytest.param(arrayValueRangeRunValue, False, '[97]+[*range(-5,5)]*3+[97]', id='arrayValueRangeRunValue-False'),
	pytest.param(arrayValueRangeRunValue, True, '[97]+[*range(-5,5)]*3+[97]', id='arrayValueRangeRunValue-True'),
	pytest.param(array3x20RangeRun, False, '[[*range(10)]*2,[*range(10)]*2,[*range(10)]*2]', id='array3x20RangeRun-False'),
	pytest.param(array3x20RangeRun, True, '[[*range(10)]*2,[*range(10)]*2,[*range(10)]*2]', id='array3x20RangeRun-True'),
	# Reference: the docstring's scalar expression for a zero-dimensional array, and `arrayEmpty.tolist()`.
	pytest.param(arrayScalarFibonacci, False, '233', id='arrayScalarFibonacci-False'),
	pytest.param(arrayScalarFibonacci, True, '233', id='arrayScalarFibonacci-True'),
	pytest.param(arrayEmpty, False, '[]', id='arrayEmpty-False'),
	pytest.param(arrayEmpty, True, '[]', id='arrayEmpty-True'),
))
def test_autoDecodingRLE(arrayTarget: NDArray[numpy.integer[Any]], assumeAddSpaces: bool, expected: str) -> None:
	assertEqualTo(autoDecodingRLE(arrayTarget, assumeAddSpaces=assumeAddSpaces), expected, autoDecodingRLE.__name__, arrayTarget.shape, assumeAddSpaces=assumeAddSpaces)

@pytest.mark.parametrize('assumeAddSpaces', [False, True])
@pytest.mark.parametrize('arrayTarget', boxOfArraysInteger)
def test_autoDecodingRLERoundTrip(arrayTarget: NDArray[numpy.integer[Any]], assumeAddSpaces: bool) -> None:
	encoded: str = autoDecodingRLE(arrayTarget, assumeAddSpaces=assumeAddSpaces)
	assert_array_equal(numpy.array(eval(encoded), dtype=arrayTarget.dtype), arrayTarget, autoDecodingRLE.__name__, encoded)  # ruff: ignore[suspicious-eval-usage]
	assert len(encoded) <= len(str(arrayTarget.tolist())), f'{autoDecodingRLE.__name__} is longer than `str(arrayTarget.tolist())`: {encoded!r}.'

# Cumulative steps of 1 and 0 form the consecutive ranges and runs that the encoding compresses; steps from -21 to 21 break them,
# including toward negative values. `numpy.tile` repeats each row 1 to 3 times, which forms runs of ranges.
@given(
	arrayTarget=strategies.builds(
		numpy.tile
		, strategies.builds(
			numpy.cumsum
			, arrays(numpy.int64, array_shapes(min_dims=1, max_dims=3, min_side=1, max_side=13)
				, elements=strategies.one_of(strategies.just(1), strategies.just(0), strategies.integers(-21, 21)))
			, axis=strategies.just(-1)
		)
		, strategies.integers(1, 3)
	)
	, assumeAddSpaces=strategies.booleans()
)
def test_autoDecodingRLERoundTripGenerated(arrayTarget: NDArray[numpy.int64], assumeAddSpaces: bool) -> None:
	encoded: str = autoDecodingRLE(arrayTarget, assumeAddSpaces=assumeAddSpaces)
	assert_array_equal(numpy.array(eval(encoded), dtype=arrayTarget.dtype), arrayTarget, autoDecodingRLE.__name__, encoded)  # ruff: ignore[suspicious-eval-usage]
	assert len(encoded) <= len(str(arrayTarget.tolist())), f'{autoDecodingRLE.__name__} is longer than `str(arrayTarget.tolist())`: {encoded!r}.'

@pytest.mark.parametrize('string, expected', (
	pytest.param('[13, 21,  34]', '[13,21,34]', id='listSpaces'),
	pytest.param('( 3, 5 )', '(3,5)', id='tupleSpaces'),
	pytest.param('[\n\t8,\n\t13\n]', '[8,13]', id='listNewlinesTabs'),
	pytest.param("{'NE': 37, 'SW': 41}", "{'NE': 37,'SW': 41}", id='dictionaryKeepsColonSpace'),
	pytest.param('[*range(50,60)]', '[*range(50,60)]', id='alreadyCompact'),
))
def test_removeExtraWhitespace(string: str, expected: str) -> None:
	assertEqualTo(removeExtraWhitespace(string), expected, removeExtraWhitespace.__name__, string)

listContainsItself: list[Any] = []
listContainsItself.append(listContainsItself)

setPrimes: set[int] = {37, 41}
frozensetPrimes: frozenset[int] = frozenset((43, 47))

@pytest.mark.parametrize('scrapPile, expected', (
	pytest.param((), [], id='nothing'),
	pytest.param((11, 13, 17), ['11', '13', '17'], id='int'),
	pytest.param(('NE', 'SW'), ['NE', 'SW'], id='str'),
	pytest.param(('None',), ['None'], id='strNone'),
	pytest.param((True, None), ['True', 'None'], id='boolNone'),
	pytest.param((2.584, complex(13, 0)), ['2.584', '(13+0j)'], id='floatComplex'),
	pytest.param((float('nan'), float('inf')), ['nan', 'inf'], id='floatNonFinite'),
	pytest.param((Decimal('3.141'), Fraction(89, 55)), ['3.141', '89/55'], id='DecimalFraction'),
	pytest.param((10**19 + 33,), ['10000000000000000033'], id='intLarge'),
	pytest.param((datetime.date(1789, 7, 14),), ['1789-07-14'], id='date'),
	pytest.param((b'\x0b', bytearray(b'DEADBEEF')), ["b'\\x0b'", "bytearray(b'DEADBEEF')"], id='bytesBytearray'),
	pytest.param((memoryview(b'DEADBEEF'),), ['DEADBEEF'], id='memoryviewDecoded'),
	pytest.param(({'phi': 1.618},), ['phi', '1.618'], id='dictionary'),
	pytest.param(([{'NE': 37}, {'SW': 41}],), ['NE', '37', 'SW', '41'], id='listOfDictionaries'),
	pytest.param(((13, 17), [19, 23], range(3, 5)), ['13', '17', '19', '23', '3', '4'], id='tupleListRange'),
	pytest.param((setPrimes, frozensetPrimes), [*map(str, setPrimes), *map(str, frozensetPrimes)], id='setFrozenset'),
	pytest.param((deque((3, 5, 8)),), ['3', '5', '8'], id='iterableDeque'),
	pytest.param((numpy.array([11, 13, 17]),), ['11', '13', '17'], id='arrayNumpy'),
	pytest.param((functionPurePython, functionBuiltin, functionCached, int), ['dedent', 'len', 'factorial', 'int'], id='callablesNamed'),
	pytest.param((callableItemGetter, callablePartial), ['itemgetter', 'partial'], id='callablesUnnamed'),
	pytest.param((StrReturnsNone(),), [], id='objectStrReturnsNone'),
	pytest.param((StrReturnsNoneText(),), ['None'], id='objectStrReturnsNoneText'),
	pytest.param((StrReadsAbsentAttribute(),), [], id='objectStrReadsAbsentAttribute'),
	pytest.param((StrFormatsBadSpecification(),), [], id='objectStrFormatsBadSpecification'),
	pytest.param(('NE', listContainsItself, 'SW'), ['NE', '[[...]]'], id='listContainsItself'),
	# Accepted recording: `charset_normalizer` finds no encoding for the 256 byte values in order, so nothing is contributed.
	pytest.param((memoryview(bytes(range(256))),), [], id='memoryviewUndecodable'),
))
def test_stringItUp(scrapPile: tuple[Any, ...], expected: list[str]) -> None:
	assertEqualTo(stringItUp(*scrapPile), expected, stringItUp.__name__, *scrapPile)

@pytest.mark.parametrize('scrapPile, expected', (
	pytest.param((StrDividesByZero(),), ZeroDivisionError, id='objectStrDividesByZero'),
))
def test_stringItUpError(capsys: pytest.CaptureFixture[str], scrapPile: tuple[Any, ...], expected: type[Exception]) -> None:
	with pytest.raises(expected):
		stringItUp(*scrapPile)
	assert capsys.readouterr().err, f'{stringItUp.__name__}(*{scrapPile!r}) wrote no diagnostic to `sys.stderr`.'

lookupPrimesFewer: dict[str, list[int]] = {'NE': [11, 13], 'SW': [17]}
lookupPrimesMore: dict[str, list[int]] = {'NE': [19, 23, 13, 29, 11], 'SW': [31, 17, 37]}

@pytest.mark.parametrize('dictionaryLists, destroyDuplicates, reorderLists, killErroneousDataTypes, expected', (
	pytest.param(
		({'servers': ['chicago']}, {'servers': ['tokyo', 'chicago']}), True, False, False, {'servers': ['chicago', 'tokyo']}
		, id='READMEServers'
	),
	pytest.param(
		(lookupPrimesFewer, lookupPrimesMore), False, False, False, {'NE': [11, 13, 19, 23, 13, 29, 11], 'SW': [17, 31, 17, 37]}
		, id='primes'
	),
	pytest.param(
		(lookupPrimesFewer, lookupPrimesMore), True, False, False, {'NE': [11, 13, 19, 23, 29], 'SW': [17, 31, 37]}
		, id='primes-destroyDuplicates'
	),
	pytest.param(
		(lookupPrimesFewer, lookupPrimesMore), False, True, False, {'NE': [11, 11, 13, 13, 19, 23, 29], 'SW': [17, 17, 31, 37]}
		, id='primes-reorderLists'
	),
	pytest.param(
		(lookupPrimesFewer, lookupPrimesMore), True, True, False, {'NE': [11, 13, 19, 23, 29], 'SW': [17, 31, 37]}
		, id='primes-destroyDuplicates-reorderLists'
	),
	pytest.param(
		(lookupPrimesFewer, lookupPrimesMore), False, False, True, {'NE': [11, 13, 19, 23, 13, 29, 11], 'SW': [17, 31, 17, 37]}
		, id='primes-killErroneousDataTypes'
	),
	pytest.param(
		(lookupPrimesFewer, {'NE': 23, 'NW': 29}), False, False, True, {'NE': [11, 13], 'SW': [17]}
		, id='valuesNotIterable-killErroneousDataTypes'
	),
	pytest.param(({'NE': (11, 13)}, {'NE': range(17, 20)}), False, False, False, {'NE': [11, 13, 17, 18, 19]}, id='tupleRange'),
	pytest.param(({'NE': {13, 11}}, {'NE': {17, 11}}), True, True, False, {'NE': [11, 13, 17]}, id='sets-destroyDuplicates-reorderLists'),
	pytest.param(({'NE': 'NE'}, {'NE': {'SW': 37}}), False, False, False, {'NE': ['N', 'E', 'SW']}, id='stringMapping'),
	pytest.param((lookupPrimesFewer,), False, False, False, {'NE': [11, 13], 'SW': [17]}, id='oneMapping'),
	pytest.param((), False, False, False, {}, id='noMappings'),
))
def test_updateExtendPolishDictionaryLists(dictionaryLists: tuple[Mapping[str, Iterable[Any]], ...], destroyDuplicates: bool, reorderLists: bool, killErroneousDataTypes: bool, expected: dict[str, list[Any]]) -> None:
	dictionaryListsBefore: tuple[Mapping[str, Iterable[Any]], ...] = copy.deepcopy(dictionaryLists)
	assertEqualTo(
		updateExtendPolishDictionaryLists(*dictionaryLists, destroyDuplicates=destroyDuplicates, reorderLists=reorderLists, killErroneousDataTypes=killErroneousDataTypes)
		, expected, updateExtendPolishDictionaryLists.__name__, *dictionaryLists
		, destroyDuplicates=destroyDuplicates, reorderLists=reorderLists, killErroneousDataTypes=killErroneousDataTypes
	)
	assert dictionaryLists == dictionaryListsBefore, f'{updateExtendPolishDictionaryLists.__name__} modified its input mappings: {dictionaryLists!r}.'

@pytest.mark.parametrize('dictionaryLists, destroyDuplicates, reorderLists, killErroneousDataTypes, expected', (
	pytest.param(({'NE': 13},), False, False, False, TypeError, id='valueNotIterable'),
	pytest.param(({'NE': [[11], [13]]},), True, False, False, TypeError, id='unhashable-destroyDuplicates'),
	pytest.param(({'NE': [[11], [13]]},), True, False, True, TypeError, id='unhashable-destroyDuplicates-killErroneousDataTypes'),
	pytest.param(({'NE': [11, 'NE']},), False, True, False, TypeError, id='incomparable-reorderLists'),
	pytest.param(({'NE': [11, 'NE']},), False, True, True, TypeError, id='incomparable-reorderLists-killErroneousDataTypes'),
))
def test_updateExtendPolishDictionaryListsError(dictionaryLists: tuple[Mapping[str, Iterable[Any]], ...], destroyDuplicates: bool, reorderLists: bool, killErroneousDataTypes: bool, expected: type[Exception]) -> None:
	with pytest.raises(expected):
		updateExtendPolishDictionaryLists(*dictionaryLists, destroyDuplicates=destroyDuplicates, reorderLists=reorderLists, killErroneousDataTypes=killErroneousDataTypes)
