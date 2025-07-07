# pyright: standard
from hunterMakesPy import importLogicalPath2Identifier, importPathFilename2Identifier, makeDirsSafely, writeStringToHere
from tests.conftest import uniformTestFailureMessage
import io
import math
import os
import pathlib
import pytest

def testMakeDirsSafelyCreatesParentDirectories(pathTmpTesting: pathlib.Path) -> None:
	nestedDirectory = pathTmpTesting / "sub1" / "sub2"
	filePath = nestedDirectory / "dummy.txt"
	makeDirsSafely(filePath)
	assert nestedDirectory.exists() and nestedDirectory.is_dir(), uniformTestFailureMessage(True, nestedDirectory.exists() and nestedDirectory.is_dir(), "testMakeDirsSafelyCreatesParentDirectories", filePath)

def testMakeDirsSafelyWithIOBaseDoesNotRaise() -> None:
	memoryStream = io.StringIO()
	makeDirsSafely(memoryStream)

def testWriteStringToHereCreatesFileAndWritesContent(pathTmpTesting: pathlib.Path) -> None:
	nestedDirectory = pathTmpTesting / "a" / "b"
	filePath = nestedDirectory / "test.txt"
	writeStringToHere("hello world", filePath)
	assert filePath.exists(), uniformTestFailureMessage(True, filePath.exists(), "testWriteStringToHereCreatesFileAndWritesContent", filePath)
	assert filePath.read_text(encoding="utf-8") == "hello world", uniformTestFailureMessage("hello world", filePath.read_text(encoding="utf-8"), "testWriteStringToHereCreatesFileAndWritesContent", filePath)

@pytest.mark.parametrize(
	"moduleName, identifier, expectedType",
	[("math", "gcd", type(math.gcd)),("os.path", "join", type(os.path.join))])
def testImportLogicalPath2Identifier(moduleName: str, identifier: str, expectedType: type) -> None:
	imported = importLogicalPath2Identifier(moduleName, identifier)
	assert isinstance(imported, expectedType), uniformTestFailureMessage(expectedType, type(imported), "testImportLogicalPath2Identifier", (moduleName, identifier))

@pytest.mark.parametrize( "source, identifier, expected", [ ("def fibonacciNumber():\n    return 13\n", "fibonacciNumber", 13), ("prime = 17\n", "prime", 17), ] )
def testImportPathFilename2Identifier(tmp_path: pathlib.Path, source: str, identifier: str, expected: object) -> None:
	filePath = tmp_path / "moduleTest.py"
	filePath.write_text(source)
	imported = importPathFilename2Identifier(filePath, identifier)
	if callable(imported):
		actual = imported()
	else:
		actual = imported
	assert actual == expected, uniformTestFailureMessage(expected, actual, "testImportPathFilename2Identifier", (filePath, identifier))
