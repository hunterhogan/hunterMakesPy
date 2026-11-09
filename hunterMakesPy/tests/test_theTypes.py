from __future__ import annotations

from hunterMakesPy import CallableFunction
from hunterMakesPy.tests import assertEqualTo
from hunterMakesPy.tests.dataSamples.theTypes import parametersCallableFunction, parametersCallableFunctionArguments
import pytest
import typing

@pytest.mark.parametrize('value, expected', parametersCallableFunction)
def test_CallableFunction(value: object, expected: bool) -> None:
	assertEqualTo(isinstance(value, CallableFunction), expected, isinstance.__name__, value, CallableFunction)

@pytest.mark.parametrize('parameters, returnType, expected', parametersCallableFunctionArguments)
def test_CallableFunctionArguments(parameters: list[type], returnType: type, expected: tuple[tuple[type, ...], type]) -> None:
	assertEqualTo(typing.get_args(CallableFunction[parameters, returnType]), expected, typing.get_args.__name__, parameters, returnType)  # pyright: ignore[reportInvalidTypeArguments] # ty: ignore[invalid-type-form]
