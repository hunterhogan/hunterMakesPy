from __future__ import annotations

from hunterMakesPy.parseParameters import defineConcurrencyLimit, intInnit, oopsieKwargsie
from hunterMakesPy.tests import assertEqualTo
from hunterMakesPy.tests.dataSamples.parseParameters import (
	parametersDefineConcurrencyLimit, parametersDefineConcurrencyLimitError, parametersIntInnit, parametersIntInnitError,
	parametersOopsieKwargsie)
from hypothesis import given, strategies
from typing import Any, TYPE_CHECKING
import pytest
import sys

if TYPE_CHECKING:
	from collections.abc import Collection
	from hunterMakesPy import ConcurrencyLimit

@pytest.mark.parametrize('limit, cpuTotal, expected', parametersDefineConcurrencyLimit)
def test_defineConcurrencyLimit(limit: ConcurrencyLimit | str, cpuTotal: int, expected: int) -> None:
	assertEqualTo(defineConcurrencyLimit(limit=limit, cpuTotal=cpuTotal), expected, defineConcurrencyLimit.__name__, limit=limit, cpuTotal=cpuTotal)  # pyright: ignore[reportArgumentType] # ty: ignore[invalid-argument-type]

# Limits span every documented rule: fractions and counts on both sides of zero, and counts beyond `cpuTotal`. `cpuTotal`
# reaches beyond the Windows cap of 61.
@given(
	limit=strategies.one_of(strategies.none(), strategies.booleans(), strategies.integers(-233, 233), strategies.floats(-233, 233))
	, cpuTotal=strategies.integers(1, 1597)
)
def test_defineConcurrencyLimitBounds(limit: ConcurrencyLimit, cpuTotal: int) -> None:
	concurrencyLimit: int = defineConcurrencyLimit(limit=limit, cpuTotal=cpuTotal)
	assert 1 <= concurrencyLimit, f'{defineConcurrencyLimit.__name__}({limit=}, {cpuTotal=}) = {concurrencyLimit}, but the minimum is 1.'
	assert sys.platform != 'win32' or concurrencyLimit <= 61, f'{defineConcurrencyLimit.__name__}({limit=}, {cpuTotal=}) = {concurrencyLimit}, but the Windows maximum is 61.'

@pytest.mark.parametrize('limit, cpuTotal, expected', parametersDefineConcurrencyLimitError)
def test_defineConcurrencyLimitError(limit: str, cpuTotal: int, expected: type[Exception]) -> None:
	with pytest.raises(expected, match='must be a number, `True`, `False`, or `None`'):
		defineConcurrencyLimit(limit=limit, cpuTotal=cpuTotal)  # pyright: ignore[reportArgumentType] # ty: ignore[invalid-argument-type]

@pytest.mark.parametrize('listInt_Allegedly, expected', parametersIntInnit)
def test_intInnit(listInt_Allegedly: Collection[Any], expected: list[int]) -> None:
	assertEqualTo(intInnit(listInt_Allegedly), expected, intInnit.__name__, listInt_Allegedly)

@given(strategies.lists(strategies.integers(), min_size=1))
def test_intInnitGenerated(listInt: list[int]) -> None:
	assertEqualTo(intInnit(listInt), listInt, intInnit.__name__, listInt)
	assertEqualTo(intInnit([*map(str, listInt)]), listInt, intInnit.__name__, [*map(str, listInt)])

@pytest.mark.parametrize('listInt_Allegedly, expected', parametersIntInnitError)
def test_intInnitError(listInt_Allegedly: Collection[Any], expected: type[Exception]) -> None:
	with pytest.raises(expected):
		intInnit(listInt_Allegedly)

@pytest.mark.parametrize('huh, expected', parametersOopsieKwargsie)
def test_oopsieKwargsie(huh: Any, expected: bool | str | None) -> None:
	assertEqualTo(oopsieKwargsie(huh), expected, oopsieKwargsie.__name__, huh)
