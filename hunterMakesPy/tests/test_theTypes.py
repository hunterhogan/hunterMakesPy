"""Expected values come from the `CallableFunction` docstring."""
from __future__ import annotations

from hunterMakesPy import CallableFunction
from hunterMakesPy.tests import assertEqualTo
from hunterMakesPy.tests.dataSamples.callables import (
	callableItemGetter, callablePartial, functionBuiltin, functionCached, functionPurePython, methodBoundPython)
import pytest
import typing

@pytest.mark.parametrize('value, expected', (
	pytest.param(functionPurePython, True, id='functionPurePython'),
	pytest.param(functionBuiltin, True, id='functionBuiltin'),
	pytest.param(functionCached, True, id='functionCached'),
	pytest.param(methodBoundPython, False, id='methodBoundPython'),
	pytest.param(callablePartial, False, id='callablePartial'),
	pytest.param(callableItemGetter, False, id='callableItemGetter'),
))
def test_CallableFunction(value: object, expected: bool) -> None:
	assertEqualTo(isinstance(value, CallableFunction), expected, isinstance.__name__, value, CallableFunction)

@pytest.mark.parametrize('parameters, returnType, expected', (
	pytest.param([int], str, ((int,), str), id='intToStr'),
	pytest.param([int, float], bool, ((int, float), bool), id='intFloatToBool'),
))
def test_CallableFunctionArguments(parameters: list[type], returnType: type, expected: tuple[tuple[type, ...], type]) -> None:
	assertEqualTo(typing.get_args(CallableFunction[parameters, returnType]), expected, typing.get_args.__name__, parameters, returnType)  # pyright: ignore[reportInvalidTypeArguments] # ty: ignore[invalid-type-form]
