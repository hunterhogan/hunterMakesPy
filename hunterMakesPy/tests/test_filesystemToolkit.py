# pyright: standard
from hunterMakesPy import importLogicalPath2Identifier, importPathFilename2Identifier, makeDirsSafely, writeStringToHere
from hunterMakesPy.tests.conftest import standardizedEqualTo
import io
import math
import os
import pathlib
import pytest
import sys

@pytest.mark.parametrize(
	"logicalPathModuleTarget, identifierTarget, packageIdentifierIfRelativeTarget, expectedType",
	[
		('math', 'gcd', None, type(math.gcd)),
		('os.path', 'join', None, type(os.path.join)),
		('pathlib', 'Path', None, type(pathlib.Path)),
		('sys', 'version', None, type(sys.version)),
	]
)
def testImportLogicalPath2IdentifierWithAbsolutePaths(
	logicalPathModuleTarget: str,
	identifierTarget: str,
	packageIdentifierIfRelativeTarget: str | None,
	expectedType: type
) -> None:
	"""Test importing identifiers from modules using absolute logical paths."""
	identifierImported = importLogicalPath2Identifier(logicalPathModuleTarget, identifierTarget, packageIdentifierIfRelativeTarget)

	assert isinstance(identifierImported, expectedType), (
		f"\nTesting: `importLogicalPath2Identifier({logicalPathModuleTarget}, {identifierTarget}, {packageIdentifierIfRelativeTarget})`\n"
		f"Expected type: {expectedType}\n"
		f"Got type: {type(identifierImported)}"
	)


@pytest.mark.parametrize(
	"pythonSourceTarget, identifierTarget, moduleIdentifierTarget, expectedValueWhenCalled",
	[
		("def fibonacciNumber():\n    return 13\n", "fibonacciNumber", None, 13),
		("def primeNumber():\n    return 17\n", "primeNumber", "moduleNorth", 17),
		("def cardinalDirection():\n    return 'N'\n", "cardinalDirection", "moduleSouth", 'N'),
		("def fibonacciSequence():\n    return 21\n", "fibonacciSequence", "moduleEast", 21),
	]
)
def testImportPathFilename2IdentifierWithCallables(
	pathTmpTesting: pathlib.Path,
	pythonSourceTarget: str,
	identifierTarget: str,
	moduleIdentifierTarget: str | None,
	expectedValueWhenCalled: object
) -> None:
	"""Test importing callable identifiers from Python files."""
	pathFilenameModule = pathTmpTesting / f"moduleTest{hash(pythonSourceTarget) % 89}.py"  # Use prime number 89
	pathFilenameModule.write_text(pythonSourceTarget)

	standardizedEqualTo(
		expectedValueWhenCalled,
		lambda: importPathFilename2Identifier(pathFilenameModule, identifierTarget, moduleIdentifierTarget)(),
	)


@pytest.mark.parametrize(
	"pythonSourceTarget, identifierTarget, moduleIdentifierTarget, expectedValue",
	[
		("prime = 23\n", "prime", None, 23),
		("fibonacci = 34\n", "fibonacci", "moduleWest", 34),
		("cardinalDirection = 'S'\n", "cardinalDirection", "moduleNorthEast", 'S'),
		("sequenceValue = 55\n", "sequenceValue", "moduleSouthWest", 55),
	]
)
def testImportPathFilename2IdentifierWithVariables(
	pathTmpTesting: pathlib.Path,
	pythonSourceTarget: str,
	identifierTarget: str,
	moduleIdentifierTarget: str | None,
	expectedValue: object
) -> None:
	"""Test importing variable identifiers from Python files."""
	pathFilenameModule = pathTmpTesting / f"moduleTest{hash(pythonSourceTarget) % 97}.py"  # Use prime number 97
	pathFilenameModule.write_text(pythonSourceTarget)

	standardizedEqualTo(
		expectedValue,
		importPathFilename2Identifier,
		pathFilenameModule,
		identifierTarget,
		moduleIdentifierTarget
	)


@pytest.mark.parametrize(
	"listDirectoryComponents, filenameTarget",
	[
		(['north', 'south'], 'fibonacci13.txt'),
		(['east', 'west', 'northeast'], 'prime17.txt'),
		(['southwest', 'northwest'], 'fibonacci21.txt'),
		(['cardinal', 'directions', 'multiple'], 'prime23.txt'),
	]
)
def testMakeDirsSafelyCreatesNestedDirectories(
	pathTmpTesting: pathlib.Path,
	listDirectoryComponents: list[str],
	filenameTarget: str
) -> None:
	"""Test that makeDirsSafely creates nested parent directories."""
	pathDirectoryNested = pathTmpTesting
	for directoryComponent in listDirectoryComponents:
		pathDirectoryNested = pathDirectoryNested / directoryComponent

	pathFilenameTarget = pathDirectoryNested / filenameTarget
	makeDirsSafely(pathFilenameTarget)

	assert pathDirectoryNested.exists() and pathDirectoryNested.is_dir(), (
		f"\nTesting: `makeDirsSafely({pathFilenameTarget})`\n"
		f"Expected: Directory {pathDirectoryNested} to exist and be a directory\n"
		f"Got: exists={pathDirectoryNested.exists()}, is_dir={pathDirectoryNested.is_dir() if pathDirectoryNested.exists() else False}"
	)


@pytest.mark.parametrize(
	"streamTypeTarget",
	[
		io.StringIO(),
		io.StringIO("initialContent"),
	]
)
def testMakeDirsSafelyWithIOStreamDoesNotRaise(streamTypeTarget: io.IOBase) -> None:
	"""Test that makeDirsSafely handles IO streams without raising exceptions."""
	# This test verifies that no exception is raised
	makeDirsSafely(streamTypeTarget)

	# If we reach this point, no exception was raised
	assert True


@pytest.mark.parametrize(
	"listDirectoryComponents, filenameTarget, contentTarget",
	[
		(['north', 'fibonacci'], 'test13.txt', 'fibonacci content 13'),
		(['south', 'prime'], 'test17.txt', 'prime content 17'),
		(['east', 'cardinal'], 'test21.txt', 'cardinal direction east'),
		(['west', 'sequence'], 'test23.txt', 'sequence value 23'),
	]
)
def testWriteStringToHereCreatesFileAndDirectories(
	pathTmpTesting: pathlib.Path,
	listDirectoryComponents: list[str],
	filenameTarget: str,
	contentTarget: str
) -> None:
	"""Test that writeStringToHere creates directories and writes content to files."""
	pathDirectoryNested = pathTmpTesting
	for directoryComponent in listDirectoryComponents:
		pathDirectoryNested = pathDirectoryNested / directoryComponent

	pathFilenameTarget = pathDirectoryNested / filenameTarget
	writeStringToHere(contentTarget, pathFilenameTarget)

	assert pathFilenameTarget.exists(), (
		f"\nTesting: `writeStringToHere({contentTarget}, {pathFilenameTarget})`\n"
		f"Expected: File {pathFilenameTarget} to exist\n"
		f"Got: exists={pathFilenameTarget.exists()}"
	)

	contentActual = pathFilenameTarget.read_text(encoding="utf-8")
	assert contentActual == contentTarget, (
		f"\nTesting: `writeStringToHere({contentTarget}, {pathFilenameTarget})`\n"
		f"Expected content: {contentTarget}\n"
		f"Got content: {contentActual}"
	)


@pytest.mark.parametrize(
	"contentTarget",
	[
		'fibonacci content 34',
		'prime content 29',
		'cardinal direction NE',
		'sequence value 55',
	]
)
def testWriteStringToHereWithIOStream(contentTarget: str) -> None:
	"""Test that writeStringToHere writes content to IO streams."""
	streamMemory = io.StringIO()
	writeStringToHere(contentTarget, streamMemory)

	contentActual = streamMemory.getvalue()
	assert contentActual == contentTarget, (
		f"\nTesting: `writeStringToHere({contentTarget}, StringIO)`\n"
		f"Expected content: {contentTarget}\n"
		f"Got content: {contentActual}"
	)


@pytest.mark.parametrize(
	"logicalPathModuleTarget, identifierTarget, expectedExceptionType",
	[
		('nonexistent.module', 'anyIdentifier', ModuleNotFoundError),
		('math', 'nonexistentFunction', AttributeError),
		('os.path', 'nonexistentAttribute', AttributeError),
	]
)
def testImportLogicalPath2IdentifierWithInvalidInputs(
	logicalPathModuleTarget: str,
	identifierTarget: str,
	expectedExceptionType: type[Exception]
) -> None:
	"""Test that importLogicalPath2Identifier raises appropriate exceptions for invalid inputs."""
	standardizedEqualTo(
		expectedExceptionType,
		importLogicalPath2Identifier,
		logicalPathModuleTarget,
		identifierTarget
	)


@pytest.mark.parametrize(
	"pathFilenameTarget, identifierTarget, expectedExceptionType",
	[
		('nonexistent.py', 'anyIdentifier', FileNotFoundError),
	]
)
def testImportPathFilename2IdentifierWithInvalidInputs(
	pathTmpTesting: pathlib.Path,
	pathFilenameTarget: str,
	identifierTarget: str,
	expectedExceptionType: type[Exception]
) -> None:
	"""Test that importPathFilename2Identifier raises appropriate exceptions for invalid inputs."""
	pathFilenameNonexistent = pathTmpTesting / pathFilenameTarget

	standardizedEqualTo(
		expectedExceptionType,
		importPathFilename2Identifier,
		pathFilenameNonexistent,
		identifierTarget
	)


@pytest.mark.parametrize(
	"pythonSourceTarget, identifierTarget, expectedExceptionType",
	[
		("def validFunction():\n    return 89\n", "nonexistentIdentifier", AttributeError),
		("validVariable = 97\n", "nonexistentVariable", AttributeError),
	]
)
def testImportPathFilename2IdentifierWithValidFileInvalidIdentifier(
	pathTmpTesting: pathlib.Path,
	pythonSourceTarget: str,
	identifierTarget: str,
	expectedExceptionType: type[Exception]
) -> None:
	"""Test that importPathFilename2Identifier raises AttributeError for nonexistent identifiers in valid files."""
	pathFilenameModule = pathTmpTesting / f"moduleTest{hash(pythonSourceTarget) % 101}.py"  # Use prime number 101
	pathFilenameModule.write_text(pythonSourceTarget)

	standardizedEqualTo(
		expectedExceptionType,
		importPathFilename2Identifier,
		pathFilenameModule,
		identifierTarget
	)

