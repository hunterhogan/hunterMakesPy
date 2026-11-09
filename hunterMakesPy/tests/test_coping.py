from __future__ import annotations

from hunterMakesPy import PackageSettings, raiseIfNone
from hunterMakesPy.coping import getIdentifierPackagePACKAGING, getPathPackageINSTALLING
from hunterMakesPy.tests import assertEqualTo
from hunterMakesPy.tests.dataSamples.coping import (
	boxOfErrorMessages, boxOfIdentifiersAbsent, boxOfIdentifiersInstalled, boxOfIdentifiersPackage, boxOfPathsPackage, boxOfPyprojects,
	boxOfValuesNotNone, parametersPyprojectNamed, parametersPyprojectUnnamed, parametersRaiseIfNoneError)
from typing import TYPE_CHECKING
import importlib.resources
import pytest
import re as regex

if TYPE_CHECKING:
	from pathlib import Path

@pytest.mark.parametrize('identifierPackageFALLBACK', boxOfIdentifiersPackage)
@pytest.mark.parametrize('pathWorkingDirectory, expected', parametersPyprojectNamed, indirect=['pathWorkingDirectory'])
def test_getIdentifierPackagePACKAGING(pathWorkingDirectory: Path, identifierPackageFALLBACK: str, expected: str) -> None:
	assertEqualTo(getIdentifierPackagePACKAGING(identifierPackageFALLBACK), expected, getIdentifierPackagePACKAGING.__name__, identifierPackageFALLBACK, pathWorkingDirectory=pathWorkingDirectory)

@pytest.mark.parametrize('identifierPackageFALLBACK', boxOfIdentifiersPackage)
@pytest.mark.parametrize('pathWorkingDirectory', parametersPyprojectUnnamed, indirect=True)
def test_getIdentifierPackagePACKAGINGFallback(pathWorkingDirectory: Path, identifierPackageFALLBACK: str) -> None:
	assertEqualTo(getIdentifierPackagePACKAGING(identifierPackageFALLBACK), identifierPackageFALLBACK, getIdentifierPackagePACKAGING.__name__, identifierPackageFALLBACK, pathWorkingDirectory=pathWorkingDirectory)

@pytest.mark.parametrize('identifierPackage', boxOfIdentifiersInstalled)
def test_getPathPackageINSTALLING(identifierPackage: str) -> None:
	assertEqualTo(getPathPackageINSTALLING(identifierPackage), importlib.resources.files(identifierPackage), getPathPackageINSTALLING.__name__, identifierPackage)

@pytest.mark.parametrize('identifierPackage', boxOfIdentifiersAbsent)
@pytest.mark.parametrize('pathWorkingDirectory', [None], indirect=True, ids=['pyprojectAbsent'])
def test_getPathPackageINSTALLINGWorkingDirectory(pathWorkingDirectory: Path, identifierPackage: str) -> None:
	assertEqualTo(getPathPackageINSTALLING(identifierPackage), pathWorkingDirectory, getPathPackageINSTALLING.__name__, identifierPackage)

@pytest.mark.parametrize('pathPackage', boxOfPathsPackage)
@pytest.mark.parametrize('identifierPackage', boxOfIdentifiersPackage)
@pytest.mark.parametrize('identifierPackageFALLBACK', boxOfIdentifiersPackage)
@pytest.mark.parametrize('pathWorkingDirectory', boxOfPyprojects, indirect=True)
def test_PackageSettings(pathWorkingDirectory: Path, identifierPackageFALLBACK: str, pathPackage: Path, identifierPackage: str) -> None:
	packageSettings: PackageSettings = PackageSettings(identifierPackageFALLBACK, pathPackage=pathPackage, identifierPackage=identifierPackage)
	assertEqualTo((packageSettings.identifierPackage, packageSettings.pathPackage), (identifierPackage, pathPackage), PackageSettings.__name__, identifierPackageFALLBACK, pathPackage=pathPackage, identifierPackage=identifierPackage)

@pytest.mark.parametrize('errorMessage', boxOfErrorMessages)
@pytest.mark.parametrize('expression', boxOfValuesNotNone)
def test_raiseIfNone(expression: object, errorMessage: str | None) -> None:
	assert raiseIfNone(expression, errorMessage) is expression, f'{raiseIfNone.__name__}({expression!r}, {errorMessage!r}) did not return {expression!r}.'

@pytest.mark.parametrize('errorMessage, expected', parametersRaiseIfNoneError)
def test_raiseIfNoneError(errorMessage: str | None, expected: str) -> None:
	with pytest.raises(ValueError, match=f'^{regex.escape(expected)}$'):
		raiseIfNone(None, errorMessage)
