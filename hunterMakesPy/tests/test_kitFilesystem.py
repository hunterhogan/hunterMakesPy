"""Expected values and exceptions come from the targets' docstrings unless a test's docstring names another basis."""
from __future__ import annotations

from collections import Counter
from hunterMakesPy import raiseIfNone
from hunterMakesPy.kitFilesystem import (
	appendStringToHere, importLogicalPath2Identifier, importPathFilename2Identifier, makeDirectorySafely, settings_isortDEFAULT, writePython,
	writeStringToHere)
from hunterMakesPy.tests import assertEqualTo
from hunterMakesPy.tests.dataSamples.pythonSource import (
	sourceImportsUnsorted, sourceImportsUnused, sourceImportsUnusedThirdParty, sourceImportsUsed)
from hunterMakesPy.tests.dataSamples.text import textASCIIPrimes, textEastAsianCities, textGreekCities
from pathlib import PurePosixPath
from typing import Any, TYPE_CHECKING
import io
import math
import os
import pytest

if TYPE_CHECKING:
	from hunterMakesPy import identifierDotAttribute
	from pathlib import Path, PurePath

markParametrizeTexts: pytest.MarkDecorator = pytest.mark.parametrize('this', (
	pytest.param(textASCIIPrimes, id='textASCIIPrimes'),
	pytest.param(textEastAsianCities, id='textEastAsianCities'),
	pytest.param(textGreekCities, id='textGreekCities'),
))

markParametrizeWritePython: pytest.MarkDecorator = pytest.mark.parametrize('pythonSource, settings, expected', (
	pytest.param(sourceImportsUnused, None, '\nfibonacci = 13\n\n', id='sourceImportsUnused-None'),
	pytest.param(sourceImportsUnused, {}, '\nfibonacci = 13\n\n', id='sourceImportsUnused-settingsEmpty'),
	pytest.param(sourceImportsUnused, (settingsAutoflakeKeepImports := {'autoflake': {'remove_all_unused_imports': False}}), '\nfibonacci = 13\n\n', id='sourceImportsUnused-settingsAutoflakeKeepImports'),
	pytest.param(sourceImportsUnused, (settingsIsortDefaultProfile := {'isort': dict[str, Any]()}), '\nfibonacci = 13\n\n', id='sourceImportsUnused-settingsIsortDefaultProfile'),
	pytest.param(sourceImportsUnused, (settingsFormatters := settingsAutoflakeKeepImports | settingsIsortDefaultProfile), '\nfibonacci = 13\n\n', id='sourceImportsUnused-settingsFormatters'),
	pytest.param(sourceImportsUsed, None, sourceImportsUsed + '\n', id='sourceImportsUsed-None'),
	pytest.param(sourceImportsUsed, {}, sourceImportsUsed + '\n', id='sourceImportsUsed-settingsEmpty'),
	pytest.param(sourceImportsUsed, settingsAutoflakeKeepImports, sourceImportsUsed + '\n', id='sourceImportsUsed-settingsAutoflakeKeepImports'),
	pytest.param(sourceImportsUsed, settingsIsortDefaultProfile, sourceImportsUsed + '\n', id='sourceImportsUsed-settingsIsortDefaultProfile'),
	pytest.param(sourceImportsUsed, settingsFormatters, sourceImportsUsed + '\n', id='sourceImportsUsed-settingsFormatters'),
	pytest.param(sourceImportsUnusedThirdParty, None, '\nfibonacci = 21\n\n', id='sourceImportsUnusedThirdParty-None'),
	pytest.param(sourceImportsUnusedThirdParty, {}, '\nfibonacci = 21\n\n', id='sourceImportsUnusedThirdParty-settingsEmpty'),
	pytest.param(sourceImportsUnusedThirdParty, settingsAutoflakeKeepImports, 'import numpy\n\nfibonacci = 21\n\n', id='sourceImportsUnusedThirdParty-settingsAutoflakeKeepImports'),
	pytest.param(sourceImportsUnusedThirdParty, settingsIsortDefaultProfile, '\nfibonacci = 21\n\n', id='sourceImportsUnusedThirdParty-settingsIsortDefaultProfile'),
	pytest.param(sourceImportsUnusedThirdParty, settingsFormatters, 'import numpy\n\nfibonacci = 21\n\n', id='sourceImportsUnusedThirdParty-settingsFormatters'),
	pytest.param(sourceImportsUnsorted, None, (sourceIsortProject := (
		"from pathlib import PurePosixPath\nimport collections\nimport math\n\n"
		"primes = collections.Counter([2, 3, 3, 5])\nnorth = PurePosixPath('north')\ntau = math.tau\n\n"
	)), id='sourceImportsUnsorted-None'),
	pytest.param(sourceImportsUnsorted, {}, sourceIsortProject, id='sourceImportsUnsorted-settingsEmpty'),
	pytest.param(sourceImportsUnsorted, settingsAutoflakeKeepImports, sourceIsortProject, id='sourceImportsUnsorted-settingsAutoflakeKeepImports'),
	pytest.param(sourceImportsUnsorted, settingsIsortDefaultProfile, (sourceIsortDefault := (
		"import collections\nimport math\nfrom pathlib import PurePosixPath\n\n"
		"primes = collections.Counter([2, 3, 3, 5])\nnorth = PurePosixPath('north')\ntau = math.tau\n\n"
	)), id='sourceImportsUnsorted-settingsIsortDefaultProfile'),
	pytest.param(sourceImportsUnsorted, settingsFormatters, sourceIsortDefault, id='sourceImportsUnsorted-settingsFormatters'),
))
"""Reference: the docstring of `writePython`, and the documentation of autoflake and isort.

autoflake removes an unused standard-library import even when `remove_all_unused_imports` is `False`. Each formatter reads
only its own settings, and `writePython` appends a newline to the formatted source.
"""

@markParametrizeTexts
def test_appendStringToHere(tmp_path: Path, this: str) -> None:
	pathFilename: Path = tmp_path / 'north' / 'east' / 'appended.txt'
	assertEqualTo(appendStringToHere(this, pathFilename), pathFilename, appendStringToHere.__name__, this, pathFilename)
	appendStringToHere(this, pathFilename)
	assertEqualTo(pathFilename.read_bytes(), (this + this).encode('utf-8'), appendStringToHere.__name__, this, pathFilename)

@pytest.mark.parametrize('logicalPathModule, identifier, packageIdentifierIfRelative, expected', (
	pytest.param('math', 'gcd', None, math.gcd, id='math-gcd-None'),
	pytest.param('os.path', 'join', None, os.path.join, id='osPath-join-None'),
	pytest.param('hunterMakesPy.coping', 'raiseIfNone', None, raiseIfNone, id='hunterMakesPyCoping-raiseIfNone-None'),
	pytest.param('.coping', 'raiseIfNone', 'hunterMakesPy', raiseIfNone, id='relativeCoping-raiseIfNone-hunterMakesPy'),
	pytest.param(
		'.kitFilesystem', 'settings_isortDEFAULT', 'hunterMakesPy', settings_isortDEFAULT
		, id='relativeKitFilesystem-settings_isortDEFAULT-hunterMakesPy'
	),
))
def test_importLogicalPath2Identifier(logicalPathModule: identifierDotAttribute, identifier: str, packageIdentifierIfRelative: str | None, expected: object) -> None:
	assert importLogicalPath2Identifier(logicalPathModule, identifier, packageIdentifierIfRelative) is expected, (
		f'{importLogicalPath2Identifier.__name__}({logicalPathModule!r}, {identifier!r}, {packageIdentifierIfRelative!r}) is not {expected!r}.')

@pytest.mark.parametrize('logicalPathModule, identifier, packageIdentifierIfRelative, expected, match', (
	pytest.param('hunterMakesPy.noSuchModule', 'raiseIfNone', None, ModuleNotFoundError, "No module named 'hunterMakesPy[.]noSuchModule'", id='moduleAbsent'),
	pytest.param('math', 'noSuchFunction', None, AttributeError, "has no attribute 'noSuchFunction'", id='identifierAbsent'),
	pytest.param('.noSuchModule', 'raiseIfNone', 'hunterMakesPy', ModuleNotFoundError, "No module named 'hunterMakesPy[.]noSuchModule'", id='relativeModuleAbsent'),
))
def test_importLogicalPath2IdentifierError(logicalPathModule: identifierDotAttribute, identifier: str, packageIdentifierIfRelative: str | None, expected: type[Exception], match: str) -> None:
	with pytest.raises(expected, match=match):
		importLogicalPath2Identifier(logicalPathModule, identifier, packageIdentifierIfRelative)

@pytest.mark.parametrize('moduleIdentifier', (
	pytest.param(None, id='moduleIdentifierNone'),
	pytest.param('moduleNorthEast', id='moduleNorthEast'),
))
@pytest.mark.parametrize('pathFilename, identifier, expected', (
	pytest.param(sourceImportsUnsorted, 'primes', Counter({2: 1, 3: 2, 5: 1}), id='sourceImportsUnsorted-primes'),
	pytest.param(sourceImportsUnsorted, 'north', PurePosixPath('north'), id='sourceImportsUnsorted-north'),
	pytest.param(sourceImportsUnsorted, 'tau', math.tau, id='sourceImportsUnsorted-tau'),
	pytest.param(sourceImportsUnused, 'fibonacci', 13, id='sourceImportsUnused-fibonacci'),
	pytest.param(sourceImportsUnusedThirdParty, 'fibonacci', 21, id='sourceImportsUnusedThirdParty-fibonacci'),
	pytest.param(sourceImportsUsed, 'primeGCD', 17, id='sourceImportsUsed-primeGCD'),
), indirect=['pathFilename'])
def test_importPathFilename2Identifier(pathFilename: Path, identifier: str, moduleIdentifier: str | None, expected: object) -> None:
	"""Reference: the value that each source binds to the identifier."""
	assertEqualTo(importPathFilename2Identifier(pathFilename, identifier, moduleIdentifier), expected, importPathFilename2Identifier.__name__, pathFilename, identifier, moduleIdentifier)

@pytest.mark.parametrize('pathFilename, identifier, expected, match', (
	pytest.param(sourceImportsUsed, 'noSuchIdentifier', AttributeError, "has no attribute 'noSuchIdentifier'", id='identifierAbsent'),
	pytest.param(None, 'primeGCD', FileNotFoundError, 'moduleSample[.]py', id='fileAbsent'),
), indirect=['pathFilename'])
def test_importPathFilename2IdentifierError(pathFilename: Path, identifier: str, expected: type[Exception], match: str) -> None:
	with pytest.raises(expected, match=match):
		importPathFilename2Identifier(pathFilename, identifier)

@pytest.mark.parametrize('pathFilename', (
	pytest.param(PurePosixPath('north/moduleSample.txt'), id='suffixTxt'),
	pytest.param(PurePosixPath('north/moduleSample'), id='suffixAbsent'),
))
def test_importPathFilename2IdentifierSuffixError(pathFilename: PurePath) -> None:
	with pytest.raises(ImportError, match='`importlibSpecification` is `None`'):
		importPathFilename2Identifier(pathFilename, 'primeGCD')

def test_makeDirectorySafely(tmp_path: Path) -> None:
	pathFilename: Path = tmp_path / 'north' / 'east' / 'south.txt'
	makeDirectorySafely(pathFilename)
	assertEqualTo((pathFilename.parent.is_dir(), pathFilename.exists()), (True, False), makeDirectorySafely.__name__, pathFilename)

def test_makeDirectorySafelyFailureSilent(tmp_path: Path) -> None:
	pathFilenameOccupied: Path = tmp_path / 'north'
	pathFilenameOccupied.write_text('NE', encoding='utf-8')
	makeDirectorySafely(pathFilenameOccupied / 'east' / 'south.txt')
	assertEqualTo(pathFilenameOccupied.read_text(encoding='utf-8'), 'NE', makeDirectorySafely.__name__, pathFilenameOccupied / 'east' / 'south.txt')

@pytest.mark.parametrize('pathFilename, expected', (
	pytest.param(io.BytesIO(b'NE'), b'NE', id='BytesIO'),
	pytest.param(io.StringIO('NE'), 'NE', id='StringIO'),
))
def test_makeDirectorySafelyStream(pathFilename: io.BytesIO | io.StringIO, expected: bytes | str) -> None:
	makeDirectorySafely(pathFilename)
	assertEqualTo(pathFilename.getvalue(), expected, makeDirectorySafely.__name__, pathFilename)

@markParametrizeWritePython
def test_writePython(tmp_path: Path, pythonSource: str, settings: dict[str, dict[str, Any]] | None, expected: str) -> None:
	pathFilename: Path = tmp_path / 'north' / 'moduleWritten.py'
	assertEqualTo(writePython(pythonSource, pathFilename, settings), pathFilename, writePython.__name__, pythonSource, pathFilename, settings)
	assertEqualTo(pathFilename.read_text(encoding='utf-8'), expected, writePython.__name__, pythonSource, pathFilename, settings)

@markParametrizeWritePython
def test_writePythonStream(pythonSource: str, settings: dict[str, dict[str, Any]] | None, expected: str) -> None:
	streamText: io.StringIO = io.StringIO()
	assert writePython(pythonSource, streamText, settings) is streamText, f'{writePython.__name__} did not return the stream it received.'
	assertEqualTo(streamText.getvalue(), expected, writePython.__name__, pythonSource, streamText, settings)

@markParametrizeTexts
def test_writeStringToHere(tmp_path: Path, this: str) -> None:
	pathFilename: Path = tmp_path / 'north' / 'east' / 'written.txt'
	assertEqualTo(writeStringToHere(this, pathFilename), pathFilename, writeStringToHere.__name__, this, pathFilename)
	assertEqualTo(pathFilename.read_text(encoding='utf-8'), this, writeStringToHere.__name__, this, pathFilename)

@markParametrizeTexts
def test_writeStringToHereStream(this: str) -> None:
	streamText: io.StringIO = io.StringIO()
	assert writeStringToHere(this, streamText) is streamText, f'{writeStringToHere.__name__} did not return the stream it received.'
	assertEqualTo(streamText.getvalue(), this, writeStringToHere.__name__, this, streamText)
