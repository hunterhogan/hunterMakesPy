"""Access dynamic import utilities and text-writing utilities.

(AI generated docstring)

You can use this module to import `identifier` values from logical module paths or Python files,
create parent directories for output paths, and write text or formatted Python source to files and
text streams. The writing functions can normalize Python imports with `autoflake` [1] and `isort` [2]
before the destination receives the final text.

Contents
--------
Functions
    importLogicalPath2Identifier
        Import `identifier` from the module named by `logicalPathModule`.
    importPathFilename2Identifier
        Import `identifier` from the Python file at `pathFilename`.
    makeDirectorySafely
        Create parent directories for `pathFilename` when `pathFilename` is a filesystem path.
    makeDirsSafely
        Temporary alias for `makeDirectorySafely`.
    writePython
        Format `pythonSource` and write `pythonSource` to `pathFilename`.
    writeStringToHere
        Write `this` to `pathFilename`.

Variables
---------
    settings_autoflakeDEFAULT
        Default settings dictionary for Python source cleanup.
    settings_isortDEFAULT
        Default settings dictionary for Python import sorting.

References
----------
[1] autoflake
    https://github.com/PyCQA/autoflake
[2] isort
    https://pycqa.github.io/isort/
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
		The package name that anchors a relative `logicalPathModule`. `None` means that
		`logicalPathModule` is interpreted as an absolute import.

	Returns
	-------
	identifierImported : Any
		The attribute retrieved from the imported module.

	"""
	moduleImported: ModuleType = importlib.import_module(logicalPathModule, packageIdentifierIfRelative)
	return getattr(moduleImported, identifier)

def importPathFilename2Identifier(pathFilename: PathLike[Any] | PurePath, identifier: str, moduleIdentifier: str | None = None) -> Any:
	"""Import `identifier` from the Python file at `pathFilename`.

	You can use this function to load a Python source file as a module and retrieve a named attribute
	from that module. This function builds a module specification with
	`importlib.util.spec_from_file_location` [1], executes the loaded module with
	`importlib.util.module_from_spec` [2], and returns the attribute selected by `identifier`.

	Parameters
	----------
	pathFilename : PathLike[Any] | PurePath
		The filesystem path of the Python source file.
	identifier : str
		The attribute name to retrieve from the loaded module.
	moduleIdentifier : str | None = None
		The module name to assign during loading. `None` uses `pathFilename.stem`.

	Returns
	-------
	identifierImported : Any
		The attribute retrieved from the loaded module.

	Raises
	------
	ImportError
		Raised when Python creates a module specification without a usable loader.
	FileNotFoundError
		Raised when the loader cannot read `pathFilename`.
	AttributeError
		Raised when the loaded module does not define `identifier`.

	References
	----------
	[1] `importlib.util.spec_from_file_location`
		https://docs.python.org/3/library/importlib.html#importlib.util.spec_from_file_location
	[2] `importlib.util.module_from_spec`
		https://docs.python.org/3/library/importlib.html#importlib.util.module_from_spec
	"""  # noqa: DOC502
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

	You can use this function to prepare an output location before a later write operation. This
	function ignores `OSError` from `Path.mkdir` [1] and does nothing when `pathFilename` is an
	`IOBase` [2] stream.

	Parameters
	----------
	pathFilename : Any
		The target path or open stream. When `pathFilename` is not an `IOBase` instance, the
		function creates the parent directory of `pathFilename`.

	References
	----------
	[1] `pathlib.Path.mkdir`
		https://docs.python.org/3/library/pathlib.html#pathlib.Path.mkdir
	[2] `IOBase`
		https://docs.python.org/3/library/io.html#io.IOBase
	"""
	if not isinstance(pathFilename, IOBase):
		with contextlib.suppress(OSError):
			Path(pathFilename).parent.mkdir(parents=True, exist_ok=True)
makeDirsSafely = makeDirectorySafely
"""Alias for `makeDirectorySafely`."""

settings_autoflakeDEFAULT: dict[str, list[str] | bool] = {
	'additional_imports': []
	, 'expand_star_imports': True
	, 'remove_all_unused_imports': True
	, 'remove_duplicate_keys': False
	, 'remove_unused_variables': False
}
"""Default settings dictionary for Python source cleanup."""

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
"""Default settings dictionary for Python import sorting."""

@overload
def writePython(pythonSource: str, pathFilename: PathLike[Any] | PurePath, settings: dict[str, dict[str, Any]] | None = None) -> Path: ...
@overload
def writePython(pythonSource: str, pathFilename: TextIOBase, settings: dict[str, dict[str, Any]] | None = None) ->  TextIOBase: ...
def writePython(pythonSource: str, pathFilename: PathLike[Any] | PurePath | TextIOBase, settings: dict[str, dict[str, Any]] | None = None) -> Path | TextIOBase:
	"""Format and write Python source code to a file or text stream.

	(AI generated docstring)

	You can use this function to normalize Python imports and then send the resulting source code to a
	file path or open text stream. This function applies `autoflake` [1] first, applies `isort` [2]
	second, appends a trailing newline, and writes the final text to `pathFilename`.

	Parameters
	----------
	pythonSource : str
		The Python source code to format and write.
	pathFilename : PathLike[Any] | PurePath | TextIOBase
		The target destination. `pathFilename` can be a filesystem path or an open text stream.
	settings : dict[str, dict[str, Any]] | None = None
		Formatter configuration. The `'autoflake'` key overrides `settings_autoflakeDEFAULT`. The
		`'isort'` key overrides `settings_isortDEFAULT`. `None` uses the default settings for each
		formatter.

	Returns
	-------
	destinationWritten : Path | TextIOBase
		The file path or text stream that received the formatted source code.

	See Also
	--------
	`writeStringToHere`
		Write text to the same destination types without Python-source formatting.

	References
	----------
	[1] autoflake
		https://github.com/PyCQA/autoflake
	[2] isort
		https://pycqa.github.io/isort/

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

	You can use this function to send text to a filesystem path or an open text stream. This function
	creates the parent directory when `pathFilename` is path-like, writes UTF-8 text with
	`Path.write_text` [1], or writes and flushes a `TextIOBase` [2] stream.

	Parameters
	----------
	this : str
		The string content to write.
	pathFilename : PathLike[Any] | PurePath | TextIOBase
		The target destination. `pathFilename` can be a filesystem path or an open text stream.

	Returns
	-------
	destinationWritten : Path | TextIOBase
		The file path or text stream that received `this`.

	See Also
	--------
	`writePython`
		Format Python source before writing to the destination.

	Examples
	--------
	The package-assimilation code writes transformed source text to a destination package path.

	```python from hunterMakesPy.filesystemToolkit import writeStringToHere

	writeStringToHere(
		regexChangeImports(pathFilename.read_text()), settingsFor[humpyPackage].pathPackage /
		pathFilename.relative_to(pathTransformee)
	)
	```

	References
	----------
	[1] `pathlib.Path.write_text`
		https://docs.python.org/3/library/pathlib.html#pathlib.Path.write_text
	[2] `TextIOBase`
		https://docs.python.org/3/library/io.html#io.TextIOBase
	"""
	if isinstance(pathFilename, TextIOBase):
		pathFilename.write(str(this))
		pathFilename.flush()
	else:
		pathFilename = Path(pathFilename)
		makeDirectorySafely(pathFilename)
		pathFilename.write_text(str(this), encoding='utf-8')
	return pathFilename
