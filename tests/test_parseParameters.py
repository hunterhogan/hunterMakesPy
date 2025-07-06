from collections.abc import Callable
from hunterMakesPy.pytestForYourUse import (
	PytestFor_defineConcurrencyLimit, PytestFor_intInnit, PytestFor_oopsieKwargsie)
from typing import ParamSpec, TypeVar
import pytest

parameters = ParamSpec('parameters')
returnType = TypeVar('returnType')

@pytest.mark.parametrize("nameOfTest,aPytest", PytestFor_defineConcurrencyLimit())
def testConcurrencyLimit(nameOfTest: str, aPytest: Callable[parameters, returnType], *arguments: parameters.args, **keywordArguments: parameters.kwargs) -> None:
	aPytest(*arguments, **keywordArguments)

@pytest.mark.parametrize("nameOfTest,aPytest", PytestFor_intInnit())
def testIntInnit(nameOfTest: str, aPytest: Callable[parameters, returnType], *arguments: parameters.args, **keywordArguments: parameters.kwargs) -> None:
	aPytest(*arguments, **keywordArguments)

@pytest.mark.parametrize("nameOfTest,aPytest", PytestFor_oopsieKwargsie())
def testOopsieKwargsie(nameOfTest: str, aPytest: Callable[parameters, returnType], *arguments: parameters.args, **keywordArguments: parameters.kwargs) -> None:
	aPytest(*arguments, **keywordArguments)
