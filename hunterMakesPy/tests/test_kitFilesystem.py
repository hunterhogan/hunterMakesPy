from __future__ import annotations

from hunterMakesPy.kitFilesystem import (
	appendStringToHere, importLogicalPath2Identifier, importPathFilename2Identifier, makeDirectorySafely, writePython, writeStringToHere)
from hunterMakesPy.tests import assertEqualTo
from hunterMakesPy.tests.dataSamples.kitFilesystem import (
	boxOfModuleIdentifiers, boxOfPathFilenamesNotPython, parametersImportLogicalPath2Identifier, parametersImportLogicalPath2IdentifierError,
	parametersImportPathFilename2Identifier, parametersImportPathFilename2IdentifierError, parametersMakeDirectorySafelyStream,
	parametersWritePython)
from hunterMakesPy.tests.dataSamples.text import boxOfTexts
from typing import Any, TYPE_CHECKING
import io
import pytest

if TYPE_CHECKING:
	from pathlib import Path, PurePath

@pytest.mark.parametrize('this', boxOfTexts)
def test_appendStringToHere(tmp_path: Path, this: str) -> None:
	pathFilename: Path = tmp_path / 'north' / 'east' / 'appended.txt'
	assertEqualTo(appendStringToHere(this, pathFilename), pathFilename, appendStringToHere.__name__, this, pathFilename)
	appendStringToHere(this, pathFilename)
	assertEqualTo(pathFilename.read_bytes(), (this + this).encode('utf-8'), appendStringToHere.__name__, this, pathFilename)

@pytest.mark.parametrize('logicalPathModule, identifier, packageIdentifierIfRelative, expected', parametersImportLogicalPath2Identifier)
def test_importLogicalPath2Identifier(logicalPathModule: str, identifier: str, packageIdentifierIfRelative: str | None, expected: object) -> None:
	assert importLogicalPath2Identifier(logicalPathModule, identifier, packageIdentifierIfRelative) is expected, (
		f'{importLogicalPath2Identifier.__name__}({logicalPathModule!r}, {identifier!r}, {packageIdentifierIfRelative!r}) is not {expected!r}.')

@pytest.mark.parametrize('logicalPathModule, identifier, packageIdentifierIfRelative, expected', parametersImportLogicalPath2IdentifierError)
def test_importLogicalPath2IdentifierError(logicalPathModule: str, identifier: str, packageIdentifierIfRelative: str | None, expected: type[Exception]) -> None:
	with pytest.raises(expected):
		importLogicalPath2Identifier(logicalPathModule, identifier, packageIdentifierIfRelative)

@pytest.mark.parametrize('moduleIdentifier', boxOfModuleIdentifiers)
@pytest.mark.parametrize('pathFilename, identifier, expected', parametersImportPathFilename2Identifier, indirect=['pathFilename'])
def test_importPathFilename2Identifier(pathFilename: Path, identifier: str, moduleIdentifier: str | None, expected: object) -> None:
	assertEqualTo(importPathFilename2Identifier(pathFilename, identifier, moduleIdentifier), expected, importPathFilename2Identifier.__name__, pathFilename, identifier, moduleIdentifier)

@pytest.mark.parametrize('pathFilename, identifier, expected', parametersImportPathFilename2IdentifierError, indirect=['pathFilename'])
def test_importPathFilename2IdentifierError(pathFilename: Path, identifier: str, expected: type[Exception]) -> None:
	with pytest.raises(expected):
		importPathFilename2Identifier(pathFilename, identifier)

@pytest.mark.parametrize('pathFilename', boxOfPathFilenamesNotPython)
def test_importPathFilename2IdentifierSuffixError(pathFilename: PurePath) -> None:
	with pytest.raises(ImportError):
		importPathFilename2Identifier(pathFilename, 'primeGCD')

def test_makeDirectorySafely(tmp_path: Path) -> None:
	pathFilename: Path = tmp_path / 'north' / 'east' / 'south.txt'
	makeDirectorySafely(pathFilename)
	assertEqualTo((pathFilename.parent.is_dir(), pathFilename.exists()), (True, False), makeDirectorySafely.__name__, pathFilename)

def test_makeDirectorySafelyOSError(tmp_path: Path) -> None:
	pathFilenameOccupied: Path = tmp_path / 'north'
	pathFilenameOccupied.write_text('NE', encoding='utf-8')
	makeDirectorySafely(pathFilenameOccupied / 'east' / 'south.txt')
	assertEqualTo(pathFilenameOccupied.read_text(encoding='utf-8'), 'NE', makeDirectorySafely.__name__, pathFilenameOccupied / 'east' / 'south.txt')

@pytest.mark.parametrize('pathFilename, expected', parametersMakeDirectorySafelyStream)
def test_makeDirectorySafelyStream(pathFilename: io.BytesIO | io.StringIO, expected: bytes | str) -> None:
	makeDirectorySafely(pathFilename)
	assertEqualTo(pathFilename.getvalue(), expected, makeDirectorySafely.__name__, pathFilename)

@pytest.mark.parametrize('pythonSource, settings, expected', parametersWritePython)
def test_writePython(tmp_path: Path, pythonSource: str, settings: dict[str, dict[str, Any]] | None, expected: str) -> None:
	pathFilename: Path = tmp_path / 'north' / 'moduleWritten.py'
	assertEqualTo(writePython(pythonSource, pathFilename, settings), pathFilename, writePython.__name__, pythonSource, pathFilename, settings)
	assertEqualTo(pathFilename.read_text(encoding='utf-8'), expected, writePython.__name__, pythonSource, pathFilename, settings)

@pytest.mark.parametrize('pythonSource, settings, expected', parametersWritePython)
def test_writePythonStream(pythonSource: str, settings: dict[str, dict[str, Any]] | None, expected: str) -> None:
	streamText: io.StringIO = io.StringIO()
	assert writePython(pythonSource, streamText, settings) is streamText, f'{writePython.__name__} did not return the stream it received.'
	assertEqualTo(streamText.getvalue(), expected, writePython.__name__, pythonSource, streamText, settings)

@pytest.mark.parametrize('this', boxOfTexts)
def test_writeStringToHere(tmp_path: Path, this: str) -> None:
	pathFilename: Path = tmp_path / 'north' / 'east' / 'written.txt'
	assertEqualTo(writeStringToHere(this, pathFilename), pathFilename, writeStringToHere.__name__, this, pathFilename)
	assertEqualTo(pathFilename.read_text(encoding='utf-8'), this, writeStringToHere.__name__, this, pathFilename)

@pytest.mark.parametrize('this', boxOfTexts)
def test_writeStringToHereStream(this: str) -> None:
	streamText: io.StringIO = io.StringIO()
	assert writeStringToHere(this, streamText) is streamText, f'{writeStringToHere.__name__} did not return the stream it received.'
	assertEqualTo(streamText.getvalue(), this, writeStringToHere.__name__, this, streamText)
