"""Samples and expected results for `hunterMakesPy.theTypes`."""
from __future__ import annotations

from hunterMakesPy.tests.dataSamples.callables import (
	callableItemGetter, callablePartial, functionBuiltin, functionCached, functionPurePython, methodBoundPython)
from typing import TYPE_CHECKING
import pytest

if TYPE_CHECKING:
	from _pytest.mark.structures import ParameterSet

# Reference: the "Runtime Checking", "Accepted Functions", and "Selected Attributes" sections of the `CallableFunction` docstring.
parametersCallableFunction: tuple[ParameterSet, ...] = (
	pytest.param(functionPurePython, True, id='functionPurePython'),
	pytest.param(functionBuiltin, True, id='functionBuiltin'),
	pytest.param(functionCached, True, id='functionCached'),
	pytest.param(methodBoundPython, False, id='methodBoundPython'),
	pytest.param(callablePartial, False, id='callablePartial'),
	pytest.param(callableItemGetter, False, id='callableItemGetter'),
)

# Reference: the "Differences From `Callable`" section of the `CallableFunction` docstring.
parametersCallableFunctionArguments: tuple[ParameterSet, ...] = (
	pytest.param([int], str, ((int,), str), id='intToStr'),
	pytest.param([int, float], bool, ((int, float), bool), id='intFloatToBool'),
)
