"""Expected values and exceptions come from the targets' docstrings unless a test's docstring names another basis."""
from __future__ import annotations

from collections import deque
from decimal import Decimal
from fractions import Fraction
from hunterMakesPy.dataStructures import autoDecodingRLE, removeExtraWhitespace, stringItUp, updateExtendPolishDictionaryLists
from hunterMakesPy.tests import assert_array_equal, assertEqualTo
from hunterMakesPy.tests.dataSamples.arrays import lookupArraysInteger
from hunterMakesPy.tests.dataSamples.arraysRLE import (
	rleArray8x8Checkerboard, rleArray13x9Saddle, rleArray60x1025MelMask, rleArray100x100Modular)
from hunterMakesPy.tests.dataSamples.callables import (
	callableItemGetter, callablePartial, functionBuiltin, functionCached, functionPurePython)
from hunterMakesPy.tests.dataSamples.classes import (
	StrDividesByZero, StrFormatsBadSpecification, StrReadsAbsentAttribute, StrReturnsNone, StrReturnsNoneText)
from hunterMakesPy.tests.dataSamples.containers import (
	boxOfLookupsIntText, boxOfLookupsIntValues, boxOfLookupsNested, boxOfLookupsPrimes, boxOfLookupsServers, boxOfLookupsSets,
	boxOfLookupsText, boxOfLookupsTupleRange, listContainsItself, lookupPrimesFewer)
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

@pytest.mark.parametrize('assumeAddSpaces', (False, True))
@pytest.mark.parametrize('arrayTarget, expected', tuple(zip(lookupArraysInteger.values(), map({
	'arrayRange': ('[*range(50,60)]', '[*range(50,60)]'),
	'arrayValueRange': ('[123,*range(71,81)]', '[123,*range(71,81)]'),
	'arrayRangeValue': ('[*range(91,97),101]', '[*range(91,97),101]'),
	'arrayValueRangeValue': ('[151,*range(163,171),181]', '[151,*range(163,171),181]'),
	'arrayRepeat': ('[191]*3', '[191]*3'),
	'arrayValueRepeat': ('[211]+[223]*3', '[211]+[223]*3'),
	'arrayValueRepeatNegative': ('[5]+[-3]*3', '[5]+[-3]*3'),
	'arrayRangeRepeat': ('[*range(251,257)]+[271]*3', '[*range(251,257)]+[271]*3'),
	'arrayRepeatRepeatValue': ('[313]*3+[331]*2+[349]', '[313]*3+[331]*2+[349]'),
	'arrayRepeatRange': ('[373]*3+[*range(383,389)]', '[373]*3+[*range(383,389)]'),
	'arrayRangeNegative': ('[*range(-34,35)]', '[*range(-34,35)]'),
	'arrayValueRangeRepeat': ('[281,*range(291,297)]+[307]*2', '[281,*range(291,297)]+[307]*2'),
	'arrayRepeatRangeValue': ('[401]*7+[*range(409,415),421]', '[401]*7+[*range(409,415),421]'),
	'arrayRangeRange': ('[*range(461,471),*range(479,487)]', '[*range(461,471),*range(479,487)]'),
	'array2x3Primes': ('[[491,499,503],[509,521,523]]', '[[491,499,503],[509,521,523]]'),
	'array2x2x2Primes': ('[[[541,547],[557,563]],[[569,571],[577,587]]]', '[[[541,547],[557,563]],[[569,571],[577,587]]]'),
	'arrayRunsFibonacci': ('[3]*4+[8,8]+[13]*5+[21]', '[3]*4+[8,8]+[13]*5+[21]'),
	'array8x8Checkerboard': (rleArray8x8Checkerboard, rleArray8x8Checkerboard),
	'array10x12Stripes': ('[[0]*12,[0]*12,[1]*12,[1]*12,[2]*12,[2]*12,[3]*12,[3]*12,[4]*12,[4]*12]', '[[0]*12,[0]*12,[1]*12,[1]*12,[2]*12,[2]*12,[3]*12,[3]*12,[4]*12,[4]*12]'),
	'array13x9Saddle': (rleArray13x9Saddle, rleArray13x9Saddle),
	'array2x3x5Range': (
		'[[[0,1,2,3,4],[5,6,7,8,9],[*range(10,15)]],[[*range(15,20)],[*range(20,25)],[*range(25,30)]]]',
		'[[[*range(5)],[5,6,7,8,9],[*range(10,15)]],[[*range(15,20)],[*range(20,25)],[*range(25,30)]]]',
	),
	'array100x100Modular': (rleArray100x100Modular, rleArray100x100Modular),
	'array60x1025MelMask': (rleArray60x1025MelMask, rleArray60x1025MelMask),
	'arrayRangeRun': ('[*range(-5,5)]*3', '[*range(-5,5)]*3'),
	'arrayValueRangeRunValue': ('[97]+[*range(-5,5)]*3+[97]', '[97]+[*range(-5,5)]*3+[97]'),
	'array3x20RangeRun': ('[[*range(10)]*2,[*range(10)]*2,[*range(10)]*2]', '[[*range(10)]*2,[*range(10)]*2,[*range(10)]*2]'),
	'arrayScalarFibonacci': ('233', '233'),
	'arrayEmpty': ('[]', '[]'),
}.__getitem__, lookupArraysInteger), strict=True)), ids=lookupArraysInteger.keys())
def test_autoDecodingRLE(arrayTarget: NDArray[numpy.integer[Any]], assumeAddSpaces: bool, expected: tuple[str, str]) -> None:
	"""Accepted recording: outputs of `autoDecodingRLE` accepted before this suite was reorganized.

	`test_autoDecodingRLERoundTrip` independently establishes that each output decodes to its array. Five expressions are
	references instead. `arrayRangeRun`, `arrayValueRangeRunValue`, and `array3x20RangeRun` are hand-derived from the
	docstring's two strategies: a run of a range is multiplication syntax around range syntax. `arrayScalarFibonacci` is the
	docstring's scalar expression for a zero-dimensional array, and `arrayEmpty` is `arrayEmpty.tolist()`.
	"""
	assertEqualTo(autoDecodingRLE(arrayTarget, assumeAddSpaces=assumeAddSpaces), expected[assumeAddSpaces], autoDecodingRLE.__name__, arrayTarget.shape, assumeAddSpaces=assumeAddSpaces)

@pytest.mark.parametrize('assumeAddSpaces', [False, True])
@pytest.mark.parametrize('arrayTarget', lookupArraysInteger.values(), ids=lookupArraysInteger.keys())
def test_autoDecodingRLERoundTrip(arrayTarget: NDArray[numpy.integer[Any]], assumeAddSpaces: bool) -> None:
	encoded: str = autoDecodingRLE(arrayTarget, assumeAddSpaces=assumeAddSpaces)
	assert_array_equal(numpy.array(eval(encoded), dtype=arrayTarget.dtype), arrayTarget, autoDecodingRLE.__name__, encoded)  # ruff: ignore[suspicious-eval-usage]
	assert len(encoded) <= len(str(arrayTarget.tolist())), f'{autoDecodingRLE.__name__} is longer than `str(arrayTarget.tolist())`: {encoded!r}.'

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
	"""Cumulative steps of 1 and 0 form the consecutive ranges and runs that the encoding compresses; steps from -21 to 21 break
	them, including toward negative values. `numpy.tile` repeats each row 1 to 3 times, which forms runs of ranges.
	"""
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
	pytest.param(((setPrimes := {37, 41}), (frozensetPrimes := frozenset((43, 47)))), [*map(str, setPrimes), *map(str, frozensetPrimes)], id='setFrozenset'),
	pytest.param((deque((3, 5, 8)),), ['3', '5', '8'], id='iterableDeque'),
	pytest.param((numpy.array([11, 13, 17]),), ['11', '13', '17'], id='arrayNumpy'),
	pytest.param((functionPurePython, functionBuiltin, functionCached, int), ['dedent', 'len', 'factorial', 'int'], id='callablesNamed'),
	pytest.param((callableItemGetter, callablePartial), ['itemgetter', 'partial'], id='callablesUnnamed'),
	pytest.param((StrReturnsNone(),), [], id='objectStrReturnsNone'),
	pytest.param((StrReturnsNoneText(),), ['None'], id='objectStrReturnsNoneText'),
	pytest.param((StrReadsAbsentAttribute(),), [], id='objectStrReadsAbsentAttribute'),
	pytest.param((StrFormatsBadSpecification(),), [], id='objectStrFormatsBadSpecification'),
	pytest.param(('NE', listContainsItself, 'SW'), ['NE', '[[...]]'], id='listContainsItself'),
	pytest.param((memoryview(bytes(range(256))),), [], id='memoryviewUndecodable'),
))
def test_stringItUp(scrapPile: tuple[Any, ...], expected: list[str]) -> None:
	"""`memoryviewUndecodable` is an accepted recording: `charset_normalizer` finds no encoding for the 256 byte values in order, so nothing is contributed."""
	assertEqualTo(stringItUp(*scrapPile), expected, stringItUp.__name__, *scrapPile)

@pytest.mark.parametrize('scrapPile, expected', (
	pytest.param((StrDividesByZero(),), ZeroDivisionError, id='objectStrDividesByZero'),
))
def test_stringItUpError(capsys: pytest.CaptureFixture[str], scrapPile: tuple[Any, ...], expected: type[Exception]) -> None:
	with pytest.raises(expected, match=r'division (?:or modulo )?by zero'):
		stringItUp(*scrapPile)
	assert capsys.readouterr().err, f'{stringItUp.__name__}(*{scrapPile!r}) wrote no diagnostic to `sys.stderr`.'

@pytest.mark.parametrize('dictionaryLists, destroyDuplicates, reorderLists, killErroneousDataTypes, expected', (
	pytest.param(boxOfLookupsServers, False, False, False, {'servers': ['chicago', 'tokyo', 'chicago']}, id='boxOfLookupsServers-False-False-False'),
	pytest.param(boxOfLookupsServers, False, False, True, {'servers': ['chicago', 'tokyo', 'chicago']}, id='boxOfLookupsServers-False-False-True'),
	pytest.param(boxOfLookupsServers, False, True, False, {'servers': ['chicago', 'chicago', 'tokyo']}, id='boxOfLookupsServers-False-True-False'),
	pytest.param(boxOfLookupsServers, False, True, True, {'servers': ['chicago', 'chicago', 'tokyo']}, id='boxOfLookupsServers-False-True-True'),
	pytest.param(boxOfLookupsServers, True, False, False, {'servers': ['chicago', 'tokyo']}, id='boxOfLookupsServers-True-False-False'),
	pytest.param(boxOfLookupsServers, True, False, True, {'servers': ['chicago', 'tokyo']}, id='boxOfLookupsServers-True-False-True'),
	pytest.param(boxOfLookupsServers, True, True, False, {'servers': ['chicago', 'tokyo']}, id='boxOfLookupsServers-True-True-False'),
	pytest.param(boxOfLookupsServers, True, True, True, {'servers': ['chicago', 'tokyo']}, id='boxOfLookupsServers-True-True-True'),
	pytest.param(boxOfLookupsPrimes, False, False, False, (expectedPrimes := {'NE': [11, 13, 19, 23, 13, 29, 11], 'SW': [17, 31, 17, 37]}), id='boxOfLookupsPrimes-False-False-False'),
	pytest.param(boxOfLookupsPrimes, False, False, True, expectedPrimes, id='boxOfLookupsPrimes-False-False-True'),
	pytest.param(boxOfLookupsPrimes, False, True, False, (expectedPrimesSorted := {'NE': [11, 11, 13, 13, 19, 23, 29], 'SW': [17, 17, 31, 37]}), id='boxOfLookupsPrimes-False-True-False'),
	pytest.param(boxOfLookupsPrimes, False, True, True, expectedPrimesSorted, id='boxOfLookupsPrimes-False-True-True'),
	pytest.param(boxOfLookupsPrimes, True, False, False, (expectedPrimesUnique := {'NE': [11, 13, 19, 23, 29], 'SW': [17, 31, 37]}), id='boxOfLookupsPrimes-True-False-False'),
	pytest.param(boxOfLookupsPrimes, True, False, True, expectedPrimesUnique, id='boxOfLookupsPrimes-True-False-True'),
	pytest.param(boxOfLookupsPrimes, True, True, False, expectedPrimesUnique, id='boxOfLookupsPrimes-True-True-False'),
	pytest.param(boxOfLookupsPrimes, True, True, True, expectedPrimesUnique, id='boxOfLookupsPrimes-True-True-True'),
	pytest.param(boxOfLookupsTupleRange, False, False, False, {'NE': [11, 13, 17, 18, 19]}, id='boxOfLookupsTupleRange-False-False-False'),
	pytest.param(boxOfLookupsTupleRange, False, False, True, {'NE': [11, 13, 17, 18, 19]}, id='boxOfLookupsTupleRange-False-False-True'),
	pytest.param(boxOfLookupsTupleRange, False, True, False, {'NE': [11, 13, 17, 18, 19]}, id='boxOfLookupsTupleRange-False-True-False'),
	pytest.param(boxOfLookupsTupleRange, False, True, True, {'NE': [11, 13, 17, 18, 19]}, id='boxOfLookupsTupleRange-False-True-True'),
	pytest.param(boxOfLookupsTupleRange, True, False, False, {'NE': [11, 13, 17, 18, 19]}, id='boxOfLookupsTupleRange-True-False-False'),
	pytest.param(boxOfLookupsTupleRange, True, False, True, {'NE': [11, 13, 17, 18, 19]}, id='boxOfLookupsTupleRange-True-False-True'),
	pytest.param(boxOfLookupsTupleRange, True, True, False, {'NE': [11, 13, 17, 18, 19]}, id='boxOfLookupsTupleRange-True-True-False'),
	pytest.param(boxOfLookupsTupleRange, True, True, True, {'NE': [11, 13, 17, 18, 19]}, id='boxOfLookupsTupleRange-True-True-True'),
	pytest.param(boxOfLookupsSets, False, False, False, (expectedSets := {'NE': [*boxOfLookupsSets[0]['NE'], *boxOfLookupsSets[1]['NE']]}), id='boxOfLookupsSets-False-False-False'),
	pytest.param(boxOfLookupsSets, False, False, True, expectedSets, id='boxOfLookupsSets-False-False-True'),
	pytest.param(boxOfLookupsSets, False, True, False, {'NE': [11, 11, 13, 17]}, id='boxOfLookupsSets-False-True-False'),
	pytest.param(boxOfLookupsSets, False, True, True, {'NE': [11, 11, 13, 17]}, id='boxOfLookupsSets-False-True-True'),
	pytest.param(boxOfLookupsSets, True, False, False, {'NE': [*boxOfLookupsSets[0]['NE'], 17]}, id='boxOfLookupsSets-True-False-False'),
	pytest.param(boxOfLookupsSets, True, False, True, {'NE': [*boxOfLookupsSets[0]['NE'], 17]}, id='boxOfLookupsSets-True-False-True'),
	pytest.param(boxOfLookupsSets, True, True, False, {'NE': [11, 13, 17]}, id='boxOfLookupsSets-True-True-False'),
	pytest.param(boxOfLookupsSets, True, True, True, {'NE': [11, 13, 17]}, id='boxOfLookupsSets-True-True-True'),
	pytest.param(boxOfLookupsText, False, False, False, {'NE': ['N', 'E', 'SW']}, id='boxOfLookupsText-False-False-False'),
	pytest.param(boxOfLookupsText, False, False, True, {'NE': ['N', 'E', 'SW']}, id='boxOfLookupsText-False-False-True'),
	pytest.param(boxOfLookupsText, False, True, False, {'NE': ['E', 'N', 'SW']}, id='boxOfLookupsText-False-True-False'),
	pytest.param(boxOfLookupsText, False, True, True, {'NE': ['E', 'N', 'SW']}, id='boxOfLookupsText-False-True-True'),
	pytest.param(boxOfLookupsText, True, False, False, {'NE': ['N', 'E', 'SW']}, id='boxOfLookupsText-True-False-False'),
	pytest.param(boxOfLookupsText, True, False, True, {'NE': ['N', 'E', 'SW']}, id='boxOfLookupsText-True-False-True'),
	pytest.param(boxOfLookupsText, True, True, False, {'NE': ['E', 'N', 'SW']}, id='boxOfLookupsText-True-True-False'),
	pytest.param(boxOfLookupsText, True, True, True, {'NE': ['E', 'N', 'SW']}, id='boxOfLookupsText-True-True-True'),
	pytest.param((lookupPrimesFewer,), False, False, False, {'NE': [11, 13], 'SW': [17]}, id='oneMapping-False-False-False'),
	pytest.param((lookupPrimesFewer,), False, False, True, {'NE': [11, 13], 'SW': [17]}, id='oneMapping-False-False-True'),
	pytest.param((lookupPrimesFewer,), False, True, False, {'NE': [11, 13], 'SW': [17]}, id='oneMapping-False-True-False'),
	pytest.param((lookupPrimesFewer,), False, True, True, {'NE': [11, 13], 'SW': [17]}, id='oneMapping-False-True-True'),
	pytest.param((lookupPrimesFewer,), True, False, False, {'NE': [11, 13], 'SW': [17]}, id='oneMapping-True-False-False'),
	pytest.param((lookupPrimesFewer,), True, False, True, {'NE': [11, 13], 'SW': [17]}, id='oneMapping-True-False-True'),
	pytest.param((lookupPrimesFewer,), True, True, False, {'NE': [11, 13], 'SW': [17]}, id='oneMapping-True-True-False'),
	pytest.param((lookupPrimesFewer,), True, True, True, {'NE': [11, 13], 'SW': [17]}, id='oneMapping-True-True-True'),
	pytest.param((), False, False, False, {}, id='noMappings-False-False-False'),
	pytest.param((), False, False, True, {}, id='noMappings-False-False-True'),
	pytest.param((), False, True, False, {}, id='noMappings-False-True-False'),
	pytest.param((), False, True, True, {}, id='noMappings-False-True-True'),
	pytest.param((), True, False, False, {}, id='noMappings-True-False-False'),
	pytest.param((), True, False, True, {}, id='noMappings-True-False-True'),
	pytest.param((), True, True, False, {}, id='noMappings-True-True-False'),
	pytest.param((), True, True, True, {}, id='noMappings-True-True-True'),
	pytest.param(boxOfLookupsIntValues, False, False, True, {'NE': [11, 13], 'SW': [17]}, id='boxOfLookupsIntValues-False-False-True'),
	pytest.param(boxOfLookupsIntValues, False, True, True, {'NE': [11, 13], 'SW': [17]}, id='boxOfLookupsIntValues-False-True-True'),
	pytest.param(boxOfLookupsIntValues, True, False, True, {'NE': [11, 13], 'SW': [17]}, id='boxOfLookupsIntValues-True-False-True'),
	pytest.param(boxOfLookupsIntValues, True, True, True, {'NE': [11, 13], 'SW': [17]}, id='boxOfLookupsIntValues-True-True-True'),
	pytest.param(({'NE': 13},), False, False, True, {}, id='valueNotIterable-False-False-True'),
	pytest.param(({'NE': 13},), False, True, True, {}, id='valueNotIterable-False-True-True'),
	pytest.param(({'NE': 13},), True, False, True, {}, id='valueNotIterable-True-False-True'),
	pytest.param(({'NE': 13},), True, True, True, {}, id='valueNotIterable-True-True-True'),
	pytest.param(boxOfLookupsNested, False, False, False, {'NE': [[11], [13]]}, id='boxOfLookupsNested-False-False-False'),
	pytest.param(boxOfLookupsNested, False, False, True, {'NE': [[11], [13]]}, id='boxOfLookupsNested-False-False-True'),
	pytest.param(boxOfLookupsNested, False, True, False, {'NE': [[11], [13]]}, id='boxOfLookupsNested-False-True-False'),
	pytest.param(boxOfLookupsNested, False, True, True, {'NE': [[11], [13]]}, id='boxOfLookupsNested-False-True-True'),
	pytest.param(boxOfLookupsIntText, False, False, False, {'NE': [11, 'NE']}, id='boxOfLookupsIntText-False-False-False'),
	pytest.param(boxOfLookupsIntText, False, False, True, {'NE': [11, 'NE']}, id='boxOfLookupsIntText-False-False-True'),
	pytest.param(boxOfLookupsIntText, True, False, False, {'NE': [11, 'NE']}, id='boxOfLookupsIntText-True-False-False'),
	pytest.param(boxOfLookupsIntText, True, False, True, {'NE': [11, 'NE']}, id='boxOfLookupsIntText-True-False-True'),
))
def test_updateExtendPolishDictionaryLists(dictionaryLists: tuple[Mapping[str, Iterable[Any]], ...], destroyDuplicates: bool, reorderLists: bool, killErroneousDataTypes: bool, expected: dict[str, list[Any]]) -> None:
	dictionaryListsBefore: tuple[Mapping[str, Iterable[Any]], ...] = copy.deepcopy(dictionaryLists)
	assertEqualTo(
		updateExtendPolishDictionaryLists(*dictionaryLists, destroyDuplicates=destroyDuplicates, reorderLists=reorderLists, killErroneousDataTypes=killErroneousDataTypes)
		, expected, updateExtendPolishDictionaryLists.__name__, *dictionaryLists
		, destroyDuplicates=destroyDuplicates, reorderLists=reorderLists, killErroneousDataTypes=killErroneousDataTypes
	)
	assert dictionaryLists == dictionaryListsBefore, f'{updateExtendPolishDictionaryLists.__name__} modified its input mappings: {dictionaryLists!r}.'

@pytest.mark.parametrize('dictionaryLists, destroyDuplicates, reorderLists, killErroneousDataTypes, expected, match', (
	pytest.param(boxOfLookupsIntValues, False, False, False, TypeError, "'int' object is not iterable", id='boxOfLookupsIntValues-False-False-False'),
	pytest.param(boxOfLookupsIntValues, False, True, False, TypeError, "'int' object is not iterable", id='boxOfLookupsIntValues-False-True-False'),
	pytest.param(boxOfLookupsIntValues, True, False, False, TypeError, "'int' object is not iterable", id='boxOfLookupsIntValues-True-False-False'),
	pytest.param(boxOfLookupsIntValues, True, True, False, TypeError, "'int' object is not iterable", id='boxOfLookupsIntValues-True-True-False'),
	pytest.param(({'NE': 13},), False, False, False, TypeError, "'int' object is not iterable", id='valueNotIterable-False-False-False'),
	pytest.param(({'NE': 13},), False, True, False, TypeError, "'int' object is not iterable", id='valueNotIterable-False-True-False'),
	pytest.param(({'NE': 13},), True, False, False, TypeError, "'int' object is not iterable", id='valueNotIterable-True-False-False'),
	pytest.param(({'NE': 13},), True, True, False, TypeError, "'int' object is not iterable", id='valueNotIterable-True-True-False'),
	pytest.param(boxOfLookupsNested, True, False, False, TypeError, "unhashable type: 'list'", id='boxOfLookupsNested-True-False-False'),
	pytest.param(boxOfLookupsNested, True, False, True, TypeError, "unhashable type: 'list'", id='boxOfLookupsNested-True-False-True'),
	pytest.param(boxOfLookupsNested, True, True, False, TypeError, "unhashable type: 'list'", id='boxOfLookupsNested-True-True-False'),
	pytest.param(boxOfLookupsNested, True, True, True, TypeError, "unhashable type: 'list'", id='boxOfLookupsNested-True-True-True'),
	pytest.param(boxOfLookupsIntText, False, True, False, TypeError, "'<' not supported", id='boxOfLookupsIntText-False-True-False'),
	pytest.param(boxOfLookupsIntText, False, True, True, TypeError, "'<' not supported", id='boxOfLookupsIntText-False-True-True'),
	pytest.param(boxOfLookupsIntText, True, True, False, TypeError, "'<' not supported", id='boxOfLookupsIntText-True-True-False'),
	pytest.param(boxOfLookupsIntText, True, True, True, TypeError, "'<' not supported", id='boxOfLookupsIntText-True-True-True'),
))
def test_updateExtendPolishDictionaryListsError(dictionaryLists: tuple[Mapping[str, Iterable[Any]], ...], destroyDuplicates: bool, reorderLists: bool, killErroneousDataTypes: bool, expected: type[Exception], match: str) -> None:
	with pytest.raises(expected) as failure:
		updateExtendPolishDictionaryLists(*dictionaryLists, destroyDuplicates=destroyDuplicates, reorderLists=reorderLists, killErroneousDataTypes=killErroneousDataTypes)
	exceptionExpected = pytest.RaisesExc(expected, match=match)
	assert exceptionExpected.matches(failure.value.__cause__ or failure.value), exceptionExpected.fail_reason
