from __future__ import annotations

from collections import Counter
from hunterMakesPy.dataStructures import autoDecodingRLE, removeExtraWhitespace, stringItUp, updateExtendPolishDictionaryLists
from hunterMakesPy.tests import assert_array_equal, assertEqualTo
from hunterMakesPy.tests.dataSamples.arrays import boxOfArraysInteger
from hunterMakesPy.tests.dataSamples.dataStructures import (
	parametersAutoDecodingRLE, parametersRemoveExtraWhitespace, parametersStringItUp, parametersStringItUpError,
	parametersUpdateExtendPolishDictionaryLists, parametersUpdateExtendPolishDictionaryListsError)
from hypothesis import given, strategies
from hypothesis.extra.numpy import array_shapes, arrays
from typing import TYPE_CHECKING
import copy
import numpy
import pytest

if TYPE_CHECKING:
	from collections.abc import Iterable, Mapping
	from numpy.typing import NDArray
	from typing import Any

@pytest.mark.parametrize('arrayTarget, assumeAddSpaces, expected', parametersAutoDecodingRLE)
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

@pytest.mark.parametrize('string, expected', parametersRemoveExtraWhitespace)
def test_removeExtraWhitespace(string: str, expected: str) -> None:
	assertEqualTo(removeExtraWhitespace(string), expected, removeExtraWhitespace.__name__, string)

@pytest.mark.parametrize('scrapPile, expected', parametersStringItUp)
def test_stringItUp(scrapPile: tuple[Any, ...], expected: list[str]) -> None:
	assertEqualTo(Counter(stringItUp(*scrapPile)), Counter(expected), stringItUp.__name__, *scrapPile)

@pytest.mark.parametrize('scrapPile, expected', parametersStringItUpError)
def test_stringItUpError(scrapPile: tuple[Any, ...], expected: type[Exception]) -> None:
	with pytest.raises(expected):
		stringItUp(*scrapPile)

@pytest.mark.parametrize('dictionaryLists, destroyDuplicates, reorderLists, killErroneousDataTypes, expected', parametersUpdateExtendPolishDictionaryLists)
def test_updateExtendPolishDictionaryLists(dictionaryLists: tuple[Mapping[str, Iterable[Any]], ...], destroyDuplicates: bool, reorderLists: bool, killErroneousDataTypes: bool, expected: dict[str, list[Any]]) -> None:
	dictionaryListsBefore: tuple[Mapping[str, Iterable[Any]], ...] = copy.deepcopy(dictionaryLists)
	assertEqualTo(
		updateExtendPolishDictionaryLists(*dictionaryLists, destroyDuplicates=destroyDuplicates, reorderLists=reorderLists, killErroneousDataTypes=killErroneousDataTypes)
		, expected, updateExtendPolishDictionaryLists.__name__, *dictionaryLists
		, destroyDuplicates=destroyDuplicates, reorderLists=reorderLists, killErroneousDataTypes=killErroneousDataTypes
	)
	assert dictionaryLists == dictionaryListsBefore, f'{updateExtendPolishDictionaryLists.__name__} modified its input mappings: {dictionaryLists!r}.'

@pytest.mark.parametrize('dictionaryLists, destroyDuplicates, reorderLists, killErroneousDataTypes, expected', parametersUpdateExtendPolishDictionaryListsError)
def test_updateExtendPolishDictionaryListsError(dictionaryLists: tuple[Mapping[str, Iterable[Any]], ...], destroyDuplicates: bool, reorderLists: bool, killErroneousDataTypes: bool, expected: type[Exception]) -> None:
	with pytest.raises(expected):
		updateExtendPolishDictionaryLists(*dictionaryLists, destroyDuplicates=destroyDuplicates, reorderLists=reorderLists, killErroneousDataTypes=killErroneousDataTypes)
