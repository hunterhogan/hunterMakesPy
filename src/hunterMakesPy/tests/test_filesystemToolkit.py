# pyright: standard
"""Tests for filesystem toolkit utilities.

(AI generated docstring)

This module validates the behavior of file and directory operations,
including safe directory creation, file writing, and dynamic importing.

"""
from hunterMakesPy import (
	importLogicalPath2Identifier, importPathFilename2Identifier, makeDirsSafely, writePython, writeStringToHere)
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
def testImportLogicalPath2IdentifierWithAbsolutePaths(logicalPathModuleTarget: str, identifierTarget: str, packageIdentifierIfRelativeTarget: str | None, expectedType: type) -> None:
	"""Test importing identifiers from modules using absolute logical paths.

	Parameters
	----------
	logicalPathModuleTarget : str
		The logical path of the module (e.g., 'os.path').
	identifierTarget : str
		The identifier (function/class) to import.
	packageIdentifierIfRelativeTarget : str | None
		Expected to be None for absolute paths.
	expectedType : type
		The expected type of the imported object.

	"""
	identifierImported: object = importLogicalPath2Identifier(logicalPathModuleTarget, identifierTarget, packageIdentifierIfRelativeTarget)

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
def testImportPathFilename2IdentifierWithCallables(pathTmpTesting: pathlib.Path, pythonSourceTarget: str, identifierTarget: str, moduleIdentifierTarget: str | None, expectedValueWhenCalled: object) -> None:
	"""Test importing callable identifiers from Python files.

	Parameters
	----------
	pathTmpTesting : pathlib.Path
		Temporary directory fixture.
	pythonSourceTarget : str
		Source code to write to the temporary file.
	identifierTarget : str
		The callable identifier to import.
	moduleIdentifierTarget : str | None
		Optional module name hint.
	expectedValueWhenCalled : object
		The expected return value when calling the imported object.

	"""
	pathFilenameModule: pathlib.Path = pathTmpTesting / f"moduleTest{hash(pythonSourceTarget) % 89}.py"  # Use prime number 89
	pathFilenameModule.write_text(pythonSourceTarget)

	def callImportedIdentifier() -> object:
		return importPathFilename2Identifier(pathFilenameModule, identifierTarget, moduleIdentifierTarget)()

	standardizedEqualTo(
		expectedValueWhenCalled,
		callImportedIdentifier,
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
def testImportPathFilename2IdentifierWithVariables(pathTmpTesting: pathlib.Path, pythonSourceTarget: str, identifierTarget: str, moduleIdentifierTarget: str | None, expectedValue: object) -> None:
	"""Test importing variable identifiers from Python files.

	Parameters
	----------
	pathTmpTesting : pathlib.Path
		Temporary directory fixture.
	pythonSourceTarget : str
		Source code to write to the temporary file.
	identifierTarget : str
		The variable identifier to import.
	moduleIdentifierTarget : str | None
		Optional module name hint.
	expectedValue : object
		The expected value of the imported variable.

	"""
	pathFilenameModule: pathlib.Path = pathTmpTesting / f"moduleTest{hash(pythonSourceTarget) % 97}.py"  # Use prime number 97
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
def testMakeDirsSafelyCreatesNestedDirectories(pathTmpTesting: pathlib.Path, listDirectoryComponents: list[str], filenameTarget: str) -> None:
	"""Test that makeDirsSafely creates nested parent directories.

	Parameters
	----------
	pathTmpTesting : pathlib.Path
		Temporary directory fixture.
	listDirectoryComponents : list[str]
		List of nested directory names.
	filenameTarget : str
		Name of the target file inside the nested directories.

	"""
	pathDirectoryNested: pathlib.Path = pathTmpTesting
	for directoryComponent in listDirectoryComponents:
		pathDirectoryNested = pathDirectoryNested / directoryComponent

	pathFilenameTarget: pathlib.Path = pathDirectoryNested / filenameTarget
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
	"""Test that makeDirsSafely handles IO streams without raising exceptions.

	Parameters
	----------
	streamTypeTarget : io.IOBase
		The IO stream object to test.

	"""
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
def testWriteStringToHereCreatesFileAndDirectories(pathTmpTesting: pathlib.Path, listDirectoryComponents: list[str], filenameTarget: str, contentTarget: str) -> None:
	"""Test that writeStringToHere creates directories and writes content to files.

	Parameters
	----------
	pathTmpTesting : pathlib.Path
		Temporary directory fixture.
	listDirectoryComponents : list[str]
		Nested directory names.
	filenameTarget : str
		Target filename.
	contentTarget : str
		Content to write to the file.

	"""
	pathDirectoryNested: pathlib.Path = pathTmpTesting
	for directoryComponent in listDirectoryComponents:
		pathDirectoryNested = pathDirectoryNested / directoryComponent

	pathFilenameTarget: pathlib.Path = pathDirectoryNested / filenameTarget
	writeStringToHere(contentTarget, pathFilenameTarget)

	assert pathFilenameTarget.exists(), (
		f"\nTesting: `writeStringToHere({contentTarget}, {pathFilenameTarget})`\n"
		f"Expected: File {pathFilenameTarget} to exist\n"
		f"Got: exists={pathFilenameTarget.exists()}"
	)

	contentActual: str = pathFilenameTarget.read_text(encoding="utf-8")
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
	"""Test that writeStringToHere writes content to IO streams.

	Parameters
	----------
	contentTarget : str
		Content to write to the stream.

	"""
	streamMemory: io.StringIO = io.StringIO()
	writeStringToHere(contentTarget, streamMemory)

	contentActual: str = streamMemory.getvalue()
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
	"""Test that importLogicalPath2Identifier raises appropriate exceptions for invalid inputs.

	Parameters
	----------
	logicalPathModuleTarget : str
		Invalid module path.
	identifierTarget : str
		Identifier to import.
	expectedExceptionType : type[Exception]
		The expected exception type.

	"""
	standardizedEqualTo( expectedExceptionType, importLogicalPath2Identifier, logicalPathModuleTarget, identifierTarget )

@pytest.mark.parametrize(
	"pathFilenameTarget, identifierTarget, expectedExceptionType",
	[
		('nonexistent.py', 'anyIdentifier', FileNotFoundError),
	]
)
def testImportPathFilename2IdentifierWithInvalidInputs(pathTmpTesting: pathlib.Path, pathFilenameTarget: str, identifierTarget: str, expectedExceptionType: type[Exception]) -> None:
	"""Test that importPathFilename2Identifier raises appropriate exceptions for invalid inputs.

	Parameters
	----------
	pathTmpTesting : pathlib.Path
		Temporary directory fixture.
	pathFilenameTarget : str
		Invalid or nonexistent filename.
	identifierTarget : str
		Identifier to import.
	expectedExceptionType : type[Exception]
		The expected exception type.

	"""
	pathFilenameNonexistent: pathlib.Path = pathTmpTesting / pathFilenameTarget

	standardizedEqualTo( expectedExceptionType, importPathFilename2Identifier, pathFilenameNonexistent, identifierTarget )

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
	"""Test that importPathFilename2Identifier raises AttributeError for nonexistent identifiers.

	Parameters
	----------
	pathTmpTesting : pathlib.Path
		Temporary directory fixture.
	pythonSourceTarget : str
		Valid python source code.
	identifierTarget : str
		Identifier that does not exist in the source.
	expectedExceptionType : type[Exception]
		Expected exception (usually AttributeError).

	"""
	pathFilenameModule: pathlib.Path = pathTmpTesting / f"moduleTest{hash(pythonSourceTarget) % 101}.py"  # Use prime number 101
	pathFilenameModule.write_text(pythonSourceTarget)

	standardizedEqualTo( expectedExceptionType, importPathFilename2Identifier, pathFilenameModule, identifierTarget )

@pytest.mark.parametrize(
	"pythonSourceTarget, expectedFormattedContent",
	[
		(
			"import sys\nimport os\nimport math\n\ndef fibonacciFunction():\n    return 13\n",
			"\ndef fibonacciFunction():\n    return 13\n\n"
		),
		(
			"from pathlib import Path\nimport sys\nimport os\n\ndef primeFunction():\n    return 17\n",
			"\ndef primeFunction():\n    return 17\n\n"
		),
		(
			"import unused\nimport sys\n\nvalueCardinal = sys.version\n",
			"import sys\n\nvalueCardinal = sys.version\n\n"
		),
		(
			"import math\n\nvalueFibonacci = math.sqrt(21)\n",
			"import math\n\nvalueFibonacci = math.sqrt(21)\n\n"
		),
	]
)
def testWritePythonFormatsAndWritesToFile(pathTmpTesting: pathlib.Path, pythonSourceTarget: str, expectedFormattedContent: str) -> None:
	"""Test that writePython formats Python source code and writes it to files.

	Parameters
	----------
	pathTmpTesting : pathlib.Path
		Temporary directory fixture.
	pythonSourceTarget : str
		Unformatted python source.
	expectedFormattedContent : str
		Expected formatted content.

	"""
	pathFilenameTarget: pathlib.Path = pathTmpTesting / "formattedModule.py"
	writePython(pythonSourceTarget, pathFilenameTarget)

	assert pathFilenameTarget.exists(), (
		f"\nTesting: `writePython(..., {pathFilenameTarget})`\n"
		f"Expected: File {pathFilenameTarget} to exist\n"
		f"Got: exists={pathFilenameTarget.exists()}"
	)

	contentActual: str = pathFilenameTarget.read_text(encoding="utf-8")
	assert contentActual == expectedFormattedContent, (
		f"\nTesting: `writePython(...)`\n"
		f"Expected content:\n{repr(expectedFormattedContent)}\n"
		f"Got content:\n{repr(contentActual)}"
	)

@pytest.mark.parametrize(
	"pythonSourceTarget, expectedFormattedContent",
	[
		(
			"import sys\nimport unused\n\ndef cardinalFunction():\n    return sys.version\n",
			"import sys\n\ndef cardinalFunction():\n    return sys.version\n\n"
		),
		(
			"from pathlib import Path\nfrom os import getcwd\nimport math\n\nvalueSequence = getcwd()\n",
			"from os import getcwd\n\nvalueSequence = getcwd()\n\n"
		),
	]
)
def testWritePythonFormatsAndWritesToStream(pythonSourceTarget: str, expectedFormattedContent: str) -> None:
	"""Test that writePython formats Python source code and writes it to IO streams.

	Parameters
	----------
	pythonSourceTarget : str
		Unformatted python source.
	expectedFormattedContent : str
		Expected formatted content.

	"""
	streamMemory: io.StringIO = io.StringIO()
	writePython(pythonSourceTarget, streamMemory)

	contentActual: str = streamMemory.getvalue()
	assert contentActual == expectedFormattedContent, (
		f"\nTesting: `writePython(..., StringIO)`\n"
		f"Expected content:\n{repr(expectedFormattedContent)}\n"
		f"Got content:\n{repr(contentActual)}"
	)

@pytest.mark.parametrize(
	"pythonSourceTarget, settingsCustom, expectedFormattedContent",
	[
		(
			"import math\nimport unused\n\nvalueFibonacci = 34\n\ndef fibonacciFunction():\n    return math.sqrt(13)\n",
			{'autoflake': {'remove_all_unused_imports': True, 'remove_unused_variables': False}},
			"import math\n\nvalueFibonacci = 34\n\ndef fibonacciFunction():\n    return math.sqrt(13)\n\n"
		),
		(
			"from pathlib import Path\nimport sys\n\nvaluePrime = Path.cwd()\n",
			{'isort': {'force_alphabetical_sort_within_sections': False, 'from_first': False}},
			"from pathlib import Path\n\nvaluePrime = Path.cwd()\n\n"
		),
	]
)
def testWritePythonWithCustomSettings(
	pathTmpTesting: pathlib.Path,
	pythonSourceTarget: str,
	settingsCustom: dict[str, dict[str, object]],
	expectedFormattedContent: str
) -> None:
	"""Test that writePython respects custom formatter settings.

	Parameters
	----------
	pathTmpTesting : pathlib.Path
		Temporary directory fixture.
	pythonSourceTarget : str
		Unformatted python source.
	settingsCustom : dict[str, dict[str, object]]
		Dictionary of formatter settings.
	expectedFormattedContent : str
		Expected formatted content.

	"""
	pathFilenameTarget: pathlib.Path = pathTmpTesting / "customFormattedModule.py"
	writePython(pythonSourceTarget, pathFilenameTarget, settingsCustom)

	contentActual: str = pathFilenameTarget.read_text(encoding="utf-8")
	assert contentActual == expectedFormattedContent, (
		f"\nTesting: `writePython(..., custom settings)`\n"
		f"Expected content:\n{repr(expectedFormattedContent)}\n"
		f"Got content:\n{repr(contentActual)}"
	)

@pytest.mark.parametrize(
	"pythonSourceTarget",
	[
		"import math\nimport sys\n\nvalueFibonacci = 34\n",
		"from pathlib import Path\n\nvalueCardinal = 'SW'\n",
		"def primeFunction():\n    return 37\n",
	]
)
def testWritePythonCreatesNestedDirectories(pathTmpTesting: pathlib.Path, pythonSourceTarget: str) -> None:
	"""Test that writePython creates nested directories when writing to files.

	Parameters
	----------
	pathTmpTesting : pathlib.Path
		Temporary directory fixture.
	pythonSourceTarget : str
		Python source code.

	"""
	pathFilenameTarget: pathlib.Path = pathTmpTesting / "nested" / "directories" / "module.py"
	writePython(pythonSourceTarget, pathFilenameTarget)

	assert pathFilenameTarget.exists(), (
		f"\nTesting: `writePython(..., {pathFilenameTarget})`\n"
		f"Expected: File {pathFilenameTarget} to exist\n"
		f"Got: exists={pathFilenameTarget.exists()}"
	)

	assert pathFilenameTarget.parent.exists(), (
		f"\nTesting: `writePython(..., {pathFilenameTarget})`\n"
		f"Expected: Parent directory {pathFilenameTarget.parent} to exist\n"
		f"Got: exists={pathFilenameTarget.parent.exists()}"
	)

@pytest.mark.parametrize(
	"pythonSourceTarget, expectedContainsImport",
	[
		("import math\n\nvaluePrime = math.sqrt(41)\n", "import math"),
		("from os import getcwd\n\nvalueSequence = getcwd()\n", "from os import getcwd"),
		("import sys\n\nvalueFibonacci = sys.version\n", "import sys"),
	]
)
def testWritePythonPreservesUsedImports(pathTmpTesting: pathlib.Path, pythonSourceTarget: str, expectedContainsImport: str) -> None:
	"""Test that writePython preserves imports that are actually used in the code.

	Parameters
	----------
	pathTmpTesting : pathlib.Path
		Temporary directory fixture.
	pythonSourceTarget : str
		Python source with used imports.
	expectedContainsImport : str
		Import string that should remain.

	"""
	pathFilenameTarget: pathlib.Path = pathTmpTesting / "preservedImports.py"
	writePython(pythonSourceTarget, pathFilenameTarget)

	contentActual: str = pathFilenameTarget.read_text(encoding="utf-8")
	assert expectedContainsImport in contentActual, (
		f"\nTesting: `writePython(...)` preserves used imports\n"
		f"Expected content to contain: {expectedContainsImport}\n"
		f"Got content:\n{contentActual}"
	)

@pytest.mark.parametrize(
	"pythonSourceTarget, expectedNotContainsImport",
	[
		("import math\nimport unused\n\nvaluePrime = 43\n", "import unused"),
		("from os import getcwd, unused\n\nvalueSequence = getcwd()\n", "unused"),
		("import sys\nimport collections\n\nvalueFibonacci = sys.version\n", "import collections"),
	]
)
def testWritePythonRemovesUnusedImports(pathTmpTesting: pathlib.Path, pythonSourceTarget: str, expectedNotContainsImport: str) -> None:
	"""Test that writePython removes imports that are not used in the code.

	Parameters
	----------
	pathTmpTesting : pathlib.Path
		Temporary directory fixture.
	pythonSourceTarget : str
		Python source with unused imports.
	expectedNotContainsImport : str
		Import string that should be removed.

	"""
	pathFilenameTarget: pathlib.Path = pathTmpTesting / "removedImports.py"
	writePython(pythonSourceTarget, pathFilenameTarget)

	contentActual: str = pathFilenameTarget.read_text(encoding="utf-8")
	assert expectedNotContainsImport not in contentActual, (
		f"\nTesting: `writePython(...)` removes unused imports\n"
		f"Expected content to NOT contain: {expectedNotContainsImport}\n"
		f"Got content:\n{contentActual}"
	)

