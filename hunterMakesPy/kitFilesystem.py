"""Import Python identifiers and write or append text to files.

(AI generated docstring)

You can use this module to import `identifier` values from logical module paths or Python files,
create parent directories for output paths, append text to files, and write text or formatted Python
source to files and text streams. The function `writePython` removes unused imports with `autoflake`
and sorts imports with `isort` before the destination receives the final text.

Contents
--------
Functions
	appendStringToHere
		Append `this` to `pathFilename` without changing existing text.
	importLogicalPath2Identifier
		Import `identifier` from the module named by `logicalPathModule`.
	importPathFilename2Identifier
		Import `identifier` from the Python file at `pathFilename`.
	makeDirectorySafely
		Create parent directories for `pathFilename` when `pathFilename` is a filesystem path.
	writePython
		Format `pythonSource` and write `pythonSource` to `pathFilename`.
	writeStringToHere
		Write `this` to `pathFilename`.

Variables
	settings_autoflakeDEFAULT
		Default settings dictionary for Python source cleanup.
	settings_isortDEFAULT
		Default settings dictionary for Python import sorting.
"""
from __future__ import annotations

from autoflake import fix_code as autoflake_fix_code
from io import IOBase, TextIOBase
from isort import code as isort_code
from pathlib import Path, PurePath
from typing import overload, TYPE_CHECKING
import contextlib
import importlib
import importlib.util

if TYPE_CHECKING:
	from hunterMakesPy import identifierDotAttribute
	from importlib.machinery import ModuleSpec
	from os import PathLike
	from types import ModuleType
	from typing import Any

def appendStringToHere(this: str, pathFilename: PathLike[Any] | PurePath) -> Path:
	"""Append `this` to the UTF-8 file at `pathFilename`.

	(AI generated docstring)

	You can use this function to add text to the end of a file while preserving existing text. This
	function creates missing parent directories when possible and creates the file when needed.
	This function returns the destination path after writing and closing the file.

	Parameters
	----------
	this : str
		The text to append. This function does not add a separator or trailing newline.
	pathFilename : PathLike[Any] | PurePath
		The destination file path. This function accepts a filesystem path rather than an open stream.

	Returns
	-------
	destinationAppended : Path
		The destination path as a `Path`, without resolving the path to an absolute path.

	See Also
	--------
	`writeStringToHere`
		Replace a file's contents or write to an open text stream.

	File Appending
	--------------
	The file receives `this` as UTF-8 text at the end of the existing text. Newline characters in
	`this` are written without translation, so a line feed remains a line feed on every operating
	system.
	A failure to create a parent directory is silent, but a failure to open or write the file
	raises the corresponding `OSError`.
	"""
	pathFilename = Path(pathFilename)
	makeDirectorySafely(pathFilename)
	with pathFilename.open(encoding='utf-8', mode='a', newline='') as streamAppend:
		writeStringToHere(this, streamAppend)
	return pathFilename

def importLogicalPath2Identifier(logicalPathModule: identifierDotAttribute, identifier: str, packageIdentifierIfRelative: str | None = None) -> Any:
	"""Import `identifier` from the module named by `logicalPathModule`.

	You can use this function to resolve a function, class, or other attribute from a module path
	string. This function imports `logicalPathModule` with `importlib.import_module` [1] and returns
	the attribute selected by `identifier`.

	Parameters
	----------
	logicalPathModule : identifierDotAttribute
		The logical module path in dot notation.
	identifier : str
		The attribute name to retrieve from the imported module.
	packageIdentifierIfRelative : str | None = None
		The package name that anchors a relative `logicalPathModule`, such as `'.kitFilesystem'`.
		`None` means that `logicalPathModule` is interpreted as an absolute import.

	Returns
	-------
	identifierImported : Any
		The attribute retrieved from the imported module.

	Raises
	------
	ModuleNotFoundError
		Raised when Python cannot find the module named by `logicalPathModule`.
	AttributeError
		Raised when the imported module does not define `identifier`.

	See Also
	--------
	`importPathFilename2Identifier`
		Import `identifier` from a Python file instead of from a logical module path.

	Examples
	--------
	The `mapFolding` package retrieves a dataclass from a logical module path.

		```python
		from hunterMakesPy.kitFilesystem import importLogicalPath2Identifier

		dataclass: type = importLogicalPath2Identifier(logicalPathDataclass, identifierDataclass)
		```

	References
	----------
	[1] importlib.import_module - Python documentation
		https://docs.python.org/3/library/importlib.html#importlib.import_module
	"""
	moduleImported: ModuleType = importlib.import_module(logicalPathModule, packageIdentifierIfRelative)
	return getattr(moduleImported, identifier)

def importPathFilename2Identifier(pathFilename: PathLike[Any] | PurePath, identifier: str, moduleIdentifier: str | None = None) -> Any:
	#ruff: ignore[docstring-extraneous-exception]
	"""Import `identifier` from the Python file at `pathFilename`.

	(AI generated docstring)

	You can use this function to load a Python source file as a module and retrieve a named attribute
	from that module. The file does not need to be part of an installed package.

	Parameters
	----------
	pathFilename : PathLike[Any] | PurePath
		The filesystem path of the Python source file.
	identifier : str
		The attribute name to retrieve from the loaded module.
	moduleIdentifier : str = pathFilename.stem
		The module name to assign during loading. `None` and empty text use the filename of
		`pathFilename` without the suffix.

	Returns
	-------
	identifierImported : Any
		The attribute retrieved from the loaded module.

	Raises
	------
	ImportError
		Raised when Python cannot create a module loader for `pathFilename`, such as when the
		filename suffix is not a Python source suffix like `.py`.
	FileNotFoundError
		Raised when the loader cannot read `pathFilename`.
	AttributeError
		Raised when the loaded module does not define `identifier`.

	See Also
	--------
	`importLogicalPath2Identifier`
		Import `identifier` from a logical module path instead of from a Python file.

	Module Execution
	----------------
	Each call executes the top-level code in `pathFilename` again and creates a new module object.
	This function does not add the module to `sys.modules`, so a later Python keyword `import` with
	the same module name does not find the loaded module. Exceptions raised by the top-level code in
	`pathFilename` propagate to the caller.

	Examples
	--------
	The `astToolFactory` package retrieves a parsing function from a Python file in the CPython
	source tree.

		```python
		from hunterMakesPy.kitFilesystem import importPathFilename2Identifier

		asdl_parse: Callable[[str], asdlParsedProtocol] = importPathFilename2Identifier(
			path_asdl / filename_asdlDOTpy, 'parse')
		```
	"""
	pathFilename = Path(pathFilename)

	importlibSpecification: ModuleSpec | None = importlib.util.spec_from_file_location(moduleIdentifier or pathFilename.stem, pathFilename)
	if importlibSpecification is None or importlibSpecification.loader is None:
		message: str = f"I received\n\t`{pathFilename = }`,\n\t`{identifier = }`, and\n\t`{moduleIdentifier = }`.\n\tAfter loading, \n\t`importlibSpecification` {'is `None`' if importlibSpecification is None else 'has a value'} and\n\t`importlibSpecification.loader` is unknown."
		raise ImportError(message)

	moduleImported_jk_hahaha: ModuleType = importlib.util.module_from_spec(importlibSpecification)
	importlibSpecification.loader.exec_module(moduleImported_jk_hahaha)
	return getattr(moduleImported_jk_hahaha, identifier)

def makeDirectorySafely(pathFilename: Any) -> None:
	"""Create parent directories for `pathFilename` when `pathFilename` is a filesystem path.

	(AI generated docstring)

	You can use this function to prepare an output location before a later write operation. You can
	pass a path or an open stream; an open stream does not need a directory, so nothing happens. A
	failure to create a directory is silent: the later write operation reports any problem with the
	output location.

	Parameters
	----------
	pathFilename : Any
		The target path or open stream. When `pathFilename` is not an `IOBase` instance, the
		function creates the parent directory of `pathFilename` and every missing ancestor
		directory. The function does not create `pathFilename` itself.

	Examples
	--------
	The `hunterHearsPy` package prepares the directory for a WAV file before writing audio data.

		```python
		from hunterMakesPy.kitFilesystem import makeDirectorySafely

		makeDirectorySafely(pathFilename)
		soundfile.write(file=pathFilename, data=audioData, samplerate=sampleRate, subtype=subtype
			, format='WAV')
		```
	"""
	if not isinstance(pathFilename, IOBase):
		with contextlib.suppress(OSError):
			Path(pathFilename).parent.mkdir(parents=True, exist_ok=True)

settings_autoflakeDEFAULT: dict[str, list[str] | bool] = {
	'additional_imports': []
	, 'expand_star_imports': True
	, 'remove_all_unused_imports': True
	, 'remove_duplicate_keys': False
	, 'remove_unused_variables': False
}
"""Default settings dictionary for Python source cleanup.

You can read this dictionary to see the keyword arguments that `writePython` passes to `autoflake`
when `settings` has no `'autoflake'` key. Changes to this dictionary affect every later call to
`writePython` in the same process that uses the default `autoflake` settings.
"""

settings_isortDEFAULT: dict[str, bool | int | str | list[str]] = {
	"combine_as_imports": True
	, "force_alphabetical_sort_within_sections": True
	, "from_first": True
	, "honor_noqa": True
	, "indent": "\t"
	, "line_length": 140
	, "lines_after_imports": 1
	, "lines_between_types": 0
	, "multi_line_output": 4
	, "no_sections": True
	, "use_parentheses": True
}
"""Default settings dictionary for Python import sorting.

You can read this dictionary to see the keyword arguments that `writePython` passes to `isort`
when `settings` has no `'isort'` key. Changes to this dictionary affect every later call to
`writePython` in the same process that uses the default `isort` settings.
"""

@overload
def writePython(pythonSource: str, pathFilename: PathLike[Any] | PurePath, settings: dict[str, dict[str, Any]] | None = None) -> Path: ...
@overload
def writePython(pythonSource: str, pathFilename: TextIOBase, settings: dict[str, dict[str, Any]] | None = None) ->  TextIOBase: ...
def writePython(pythonSource: str, pathFilename: PathLike[Any] | PurePath | TextIOBase, settings: dict[str, dict[str, Any]] | None = None) -> Path | TextIOBase:
	"""Format and write Python source code to a file or text stream.

	(AI generated docstring)

	You can use this function to normalize Python imports and then send the resulting source code to a
	file path or open text stream. `autoflake` [1] removes unused imports, `isort` [2] sorts the
	remaining imports, and `pathFilename` receives the formatted source code followed by a newline.
	When the formatted source code already ends with a newline, the written text ends with a blank
	line.

	Parameters
	----------
	pythonSource : str
		The Python source code to format and write.
	pathFilename : PathLike[Any] | PurePath | TextIOBase
		The target destination. `pathFilename` can be a filesystem path or an open text stream.
	settings : dict[str, dict[str, Any]] | None = None
		Formatter configuration. The `'autoflake'` value replaces `settings_autoflakeDEFAULT`
		entirely, and the `'isort'` value replaces `settings_isortDEFAULT` entirely; this function
		does not merge a supplied value with the default dictionary. A missing key, `None`, and an
		empty dictionary use the default settings for the corresponding formatter.

	Returns
	-------
	destinationWritten : Path | TextIOBase
		The file path, as a `Path`, or the text stream that received the formatted source code.

	See Also
	--------
	`writeStringToHere`
		Write text to the same destination types without Python-source formatting.

	File Replacement
	----------------
	A path destination receives the same treatment as in `writeStringToHere`: this function
	creates missing parent directories and replaces any existing file.

	Examples
	--------
	The `astToolkit` package writes the source code of an `ast.Module` with optional formatter
	settings.

		```python
		from hunterMakesPy.kitFilesystem import writePython

		pythonSource: str = ast.unparse(astModule)
		writePython(pythonSource, pathFilename, settings)
		```

	References
	----------
	[1] autoflake - keyword arguments of `fix_code`
		https://github.com/PyCQA/autoflake
	[2] isort - configuration options
		https://pycqa.github.io/isort/docs/configuration/options.html
	"""
	if settings is None:
		settings = {}
# TODO The formatting system needs a complete rethink.
	settings_autoflake: dict[str, Any] = settings.get('autoflake', settings_autoflakeDEFAULT)
	pythonSource = autoflake_fix_code(pythonSource, **settings_autoflake)

	settings_isort: dict[str, Any] = settings.get('isort', settings_isortDEFAULT)
	pythonSource = isort_code(pythonSource, **settings_isort)
	return writeStringToHere(pythonSource + '\n', pathFilename)

@overload
def writeStringToHere(this: str, pathFilename: PathLike[Any] | PurePath) -> Path: ...
@overload
def writeStringToHere(this: str, pathFilename: TextIOBase) -> TextIOBase: ...
def writeStringToHere(this: str, pathFilename: PathLike[Any] | PurePath | TextIOBase) -> Path | TextIOBase:
	"""Write `this` to `pathFilename`.

	(AI generated docstring)

	You can use this function to send text to a filesystem path or an open text stream. When
	`pathFilename` is a path, this function creates missing parent directories and writes `this` as
	UTF-8 text. When `pathFilename` is an open text stream, this function writes `this` at the current
	position of the stream and flushes the stream; the stream remains open.

	Parameters
	----------
	this : str
		The string content to write.
	pathFilename : PathLike[Any] | PurePath | TextIOBase
		The target destination. `pathFilename` can be a filesystem path or an open text stream.

	Returns
	-------
	destinationWritten : Path | TextIOBase
		The file path, as a `Path`, or the text stream that received `this`.

	See Also
	--------
	`appendStringToHere`
		Add text to the end of a file instead of replacing the file.
	`writePython`
		Format Python source before writing to the destination.

	File Replacement
	----------------
	A path destination replaces any existing file. Each line feed in `this` becomes the newline
	sequence of the operating system, so a file written on Windows contains a carriage return and a
	line feed at the end of each line. A text stream receives `this` without this change by this
	function. A failure to create a parent
	directory is silent, but a failure to write the file raises the corresponding `OSError`.

	Examples
	--------
	The `mapFolding` package writes a computed count to a file.

		```python
		from hunterMakesPy.kitFilesystem import writeStringToHere

		writeStringToHere(str(countTotal), pathFilename)
		```
	"""
	if isinstance(pathFilename, TextIOBase):
		pathFilename.write(str(this))
		pathFilename.flush()
	else:
		pathFilename = Path(pathFilename)
		makeDirectorySafely(pathFilename)
		pathFilename.write_text(str(this), encoding='utf-8')
	return pathFilename
