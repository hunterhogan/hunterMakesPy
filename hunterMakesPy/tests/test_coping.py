"""Expected values and exceptions come from the targets' docstrings unless a test's docstring names another basis."""
from __future__ import annotations

from hunterMakesPy import PackageSettings, raiseIfNone
from hunterMakesPy.coping import _getIdentifierPackagePACKAGING, _getPathPackageINSTALLING
from hunterMakesPy.tests import assertEqualTo
from hunterMakesPy.tests.dataSamples.arrays import arrayRange
from hunterMakesPy.tests.dataSamples.messages import messageHostMissing
from hunterMakesPy.tests.dataSamples.packages import boxOfIdentifiersPackageAbsent, lookupIdentifiersPackageInstalled
from hunterMakesPy.tests.dataSamples.pyprojects import tomlProjectMalformed, tomlProjectNamed, tomlProjectNameEmpty, tomlProjectNameless
from pathlib import Path
import importlib.resources
import pytest
import re as regex

@pytest.mark.parametrize('identifierPackageFALLBACK', boxOfIdentifiersPackageAbsent)
@pytest.mark.parametrize('pathWorkingDirectory, expected', (
	pytest.param(tomlProjectNamed, 'cobraPy', id='tomlProjectNamed'),
), indirect=['pathWorkingDirectory'])
def test_getIdentifierPackagePACKAGING(pathWorkingDirectory: Path, identifierPackageFALLBACK: str, expected: str) -> None:
	"""Reference: the `project.name` that `tomlProjectNamed` states."""
	assertEqualTo(_getIdentifierPackagePACKAGING(identifierPackageFALLBACK), expected, _getIdentifierPackagePACKAGING.__name__, identifierPackageFALLBACK, pathWorkingDirectory=pathWorkingDirectory)

@pytest.mark.parametrize('identifierPackageFALLBACK', boxOfIdentifiersPackageAbsent)
@pytest.mark.parametrize('pathWorkingDirectory', (
	pytest.param(None, id='pyprojectAbsent'),
	pytest.param(tomlProjectMalformed, id='tomlProjectMalformed'),
	pytest.param(tomlProjectNameEmpty, id='tomlProjectNameEmpty'),
	pytest.param(tomlProjectNameless, id='tomlProjectNameless'),
), indirect=True)
def test_getIdentifierPackagePACKAGINGFallback(pathWorkingDirectory: Path, identifierPackageFALLBACK: str) -> None:
	assertEqualTo(_getIdentifierPackagePACKAGING(identifierPackageFALLBACK), identifierPackageFALLBACK, _getIdentifierPackagePACKAGING.__name__, identifierPackageFALLBACK, pathWorkingDirectory=pathWorkingDirectory)

@pytest.mark.parametrize('identifierPackage', lookupIdentifiersPackageInstalled.values(), ids=lookupIdentifiersPackageInstalled.keys())
def test_getPathPackageINSTALLING(identifierPackage: str) -> None:
	assertEqualTo(_getPathPackageINSTALLING(identifierPackage), importlib.resources.files(identifierPackage), _getPathPackageINSTALLING.__name__, identifierPackage)

@pytest.mark.parametrize('identifierPackage', (
	pytest.param('hunterMakesPy.noSuchModule', id='hunterMakesPyNoSuchModule'),
	'noSuchPackage13',
	pytest.param('noSuchParent.child', id='noSuchParentChild'),
))
@pytest.mark.parametrize('pathWorkingDirectory', [None], indirect=True, ids=['pyprojectAbsent'])
def test_getPathPackageINSTALLINGWorkingDirectory(pathWorkingDirectory: Path, identifierPackage: str) -> None:
	"""Reference: `importlib.util.find_spec` finds no module, so the location is the working directory."""
	assertEqualTo(_getPathPackageINSTALLING(identifierPackage), pathWorkingDirectory, _getPathPackageINSTALLING.__name__, identifierPackage)

@pytest.mark.parametrize('pathPackage', (
	pytest.param(Path('C:/fibonacci/path'), id='pathWindowsAbsolute'),
	pytest.param(Path('relative/north'), id='pathRelative'),
	pytest.param(Path('/usr/local/lib/prime'), id='pathRootAbsolute'),
))
@pytest.mark.parametrize('identifierPackage', boxOfIdentifiersPackageAbsent)
@pytest.mark.parametrize('identifierPackageFALLBACK', boxOfIdentifiersPackageAbsent)
@pytest.mark.parametrize('pathWorkingDirectory', (
	pytest.param(None, id='pyprojectAbsent'),
	pytest.param(tomlProjectMalformed, id='tomlProjectMalformed'),
	pytest.param(tomlProjectNameEmpty, id='tomlProjectNameEmpty'),
	pytest.param(tomlProjectNamed, id='tomlProjectNamed'),
	pytest.param(tomlProjectNameless, id='tomlProjectNameless'),
), indirect=True)
def test_PackageSettings(pathWorkingDirectory: Path, identifierPackageFALLBACK: str, pathPackage: Path, identifierPackage: str) -> None:
	packageSettings: PackageSettings = PackageSettings(identifierPackageFALLBACK, pathPackage=pathPackage, identifierPackage=identifierPackage)
	assertEqualTo((packageSettings.identifierPackage, packageSettings.pathPackage), (identifierPackage, pathPackage), PackageSettings.__name__, identifierPackageFALLBACK, pathPackage=pathPackage, identifierPackage=identifierPackage)

@pytest.mark.parametrize('identifierPackageFALLBACK', lookupIdentifiersPackageInstalled.values(), ids=lookupIdentifiersPackageInstalled.keys())
@pytest.mark.parametrize('pathWorkingDirectory', [None], indirect=True, ids=['pyprojectAbsent'])
def test_PackageSettingsDiscovery(pathWorkingDirectory: Path, identifierPackageFALLBACK: str) -> None:
	packageSettings: PackageSettings = PackageSettings(identifierPackageFALLBACK)
	assertEqualTo(
		(packageSettings.identifierPackage, packageSettings.pathPackage)
		, (identifierPackageFALLBACK, importlib.resources.files(identifierPackageFALLBACK))
		, PackageSettings.__name__, identifierPackageFALLBACK, pathWorkingDirectory=pathWorkingDirectory
	)

@pytest.mark.parametrize('errorMessage', (
	pytest.param(None, id='errorMessageNone'),
	pytest.param(messageHostMissing, id='messageHostMissing'),
))
@pytest.mark.parametrize('expression', (
	pytest.param(0, id='zero'),
	pytest.param(13, id='prime13'),
	pytest.param('', id='stringEmpty'),
	pytest.param('NE', id='stringNE'),
	pytest.param(False, id='false'),
	pytest.param([], id='listEmpty'),
	pytest.param(arrayRange, id='arrayRange'),
))
def test_raiseIfNone(expression: object, errorMessage: str | None) -> None:
	assert raiseIfNone(expression, errorMessage) is expression, f'{raiseIfNone.__name__}({expression!r}, {errorMessage!r}) did not return {expression!r}.'

@pytest.mark.parametrize('errorMessage, expected', (
	pytest.param(None, (messageRaiseIfNoneDEFAULT := 'A function unexpectedly returned `None`. Hint: look at the traceback immediately before `raiseIfNone`.'), id='errorMessageNone'),
	pytest.param('', messageRaiseIfNoneDEFAULT, id='errorMessageEmpty'),
	pytest.param(messageHostMissing, messageHostMissing, id='messageHostMissing'),
))
def test_raiseIfNoneError(errorMessage: str | None, expected: str) -> None:
	"""`errorMessageEmpty` is an accepted recording: an empty `errorMessage` selects the default message."""
	with pytest.raises(ValueError, match=f'^{regex.escape(expected)}$'):
		raiseIfNone(None, errorMessage)
