"""File system and module import utilities.

This module provides basic file I/O utilities such as importing callables from modules, safely creating directories, and writing to files or streams (pipes).

"""
from autoflake import fix_code as autoflake_fix_code
from hunterMakesPy import identifierDotAttribute
from isort import code as isort_code
from os import PathLike
from pathlib import Path, PurePath
from typing import Any, TYPE_CHECKING, TypeVar
import contextlib
import importlib
import importlib.util
import io

if TYPE_CHECKING:
	from importlib.machinery import ModuleSpec
	from types import ModuleType

归个 = TypeVar('归个')

def importLogicalPath2Identifier(logicalPathModule: identifierDotAttribute, identifier: str, packageIdentifierIfRelative: str | None = None) -> 归个:
	"""Import an `identifier`, such as a function or `class`, from a module using its logical path.

	This function imports a module and retrieves a specific attribute (function, class, or other object) from that module.

	Parameters
	----------
	logicalPathModule : identifierDotAttribute
		The logical path to the module, using dot notation (e.g., 'scipy.signal.windows').
	identifier : str
		The identifier of the object to retrieve from the module.
	packageIdentifierIfRelative : str | None = None
		The package name to use as the anchor point if `logicalPathModule` is a relative import. `None` means an absolute import.

	Returns
	-------
	identifierImported : 归个
		The identifier (function, class, or object) retrieved from the module.

	"""
	moduleImported: ModuleType = importlib.import_module(logicalPathModule, packageIdentifierIfRelative)
	return getattr(moduleImported, identifier)

def importPathFilename2Identifier(pathFilename: PathLike[Any] | PurePath, identifier: str, moduleIdentifier: str | None = None) -> 归个:
	"""Load an identifier from a Python file.

	This function imports a specified Python file as a module, extracts an identifier from it by name, and returns that
	identifier.

	Parameters
	----------
	pathFilename : PathLike[Any] | PurePath
		Path to the Python file to import.
	identifier : str
		Name of the identifier to extract from the imported module.
	moduleIdentifier : str | None = None
		Name to use for the imported module. If `None`, the filename stem is used.

	Returns
	-------
	identifierImported : 归个
		The identifier extracted from the imported module.

	Raises
	------
	ImportError
		If the file cannot be imported or the importlib specification is invalid.
	AttributeError
		If the identifier does not exist in the imported module.

	"""
	pathFilename = Path(pathFilename)

	importlibSpecification: ModuleSpec | None = importlib.util.spec_from_file_location(moduleIdentifier or pathFilename.stem, pathFilename)
	if importlibSpecification is None or importlibSpecification.loader is None:
		message: str = f"I received\n\t`{pathFilename = }`,\n\t`{identifier = }`, and\n\t`{moduleIdentifier = }`.\n\tAfter loading, \n\t`importlibSpecification` {'is `None`' if importlibSpecification is None else 'has a value'} and\n\t`importlibSpecification.loader` is unknown."
		raise ImportError(message)

	moduleImported_jk_hahaha: ModuleType = importlib.util.module_from_spec(importlibSpecification)
	importlibSpecification.loader.exec_module(moduleImported_jk_hahaha)
	return getattr(moduleImported_jk_hahaha, identifier)

def makeDirsSafely(pathFilename: Any) -> None:
	"""Create parent directories for a given path safely.

	This function attempts to create all necessary parent directories for a given path. If the directory already exists or if
	there's an `OSError` during creation, it will silently continue without raising an exception.

	Parameters
	----------
	pathFilename : Any
		A path-like object or file object representing the path for which to create parent directories. If it's an IO stream
		object, no directories will be created.

	"""
	if not isinstance(pathFilename, io.IOBase):
		with contextlib.suppress(OSError):
			Path(pathFilename).parent.mkdir(parents=True, exist_ok=True)

settings_autoflakeDEFAULT: dict[str, list[str] | bool] = {
	'additional_imports': [],
	'expand_star_imports': True,
	'remove_all_unused_imports': True,
	'remove_duplicate_keys': False,
	'remove_unused_variables': False,
}

settings_isortDEFAULT: dict[str, bool | int | str | list[str]] = {
	"combine_as_imports": True,
	"force_alphabetical_sort_within_sections": True,
	"from_first": True,
	"honor_noqa": True,
	"indent": "\t",
	"line_length": 120,
	"lines_after_imports": 1,
	"lines_between_types": 0,
	"multi_line_output": 4,
	"no_sections": True,
	"use_parentheses": True,
}

def writePython(pythonSource: str, pathFilename: PathLike[Any] | PurePath | io.TextIOBase, settings: dict[str, dict[str, Any]] | None = None) -> None:
	"""Format and write Python source code to a file or text stream.

	(AI generated docstring)

	This function processes Python source code through autoflake and isort formatters before writing to the specified destination.
	The formatters remove unused imports, sort imports, and apply consistent code style according to the provided or default
	settings.

	Parameters
	----------
	pythonSource : str
		The Python source code to format and write.
	pathFilename : PathLike[Any] | PurePath | io.TextIOBase
		The target destination: either a file path or an open text stream.
	settings : dict[str, dict[str, Any]] | None = None
		Configuration for the formatters. Keys are `'autoflake'` and `'isort'`, each mapping to a dictionary of formatter-specific
		settings. If `None`, default settings are used for both formatters.

	"""
	if settings is None:
		settings = {}

	settings_autoflake: dict[str, Any] = settings.get('autoflake', settings_autoflakeDEFAULT)
	pythonSource = autoflake_fix_code(pythonSource, **settings_autoflake)

	settings_isort: dict[str, Any] = settings.get('isort', settings_isortDEFAULT)
	pythonSource = isort_code(pythonSource, **settings_isort)
	writeStringToHere(pythonSource + '\n', pathFilename)

def writeStringToHere(this: str, pathFilename: PathLike[Any] | PurePath | io.TextIOBase) -> None:
	"""Write a string to a file or text stream.

	This function writes a string to either a file path or an open text stream. For file paths, it creates parent directories as
	needed and writes with UTF-8 encoding. For text streams, it writes directly to the stream and flushes the buffer.

	Parameters
	----------
	this : str
		The string content to write.
	pathFilename : PathLike[Any] | PurePath | io.TextIOBase
		The target destination: either a file path or an open text stream.

	"""
	if isinstance(pathFilename, io.TextIOBase):
		pathFilename.write(str(this))
		pathFilename.flush()
	else:
		pathFilename = Path(pathFilename)
		makeDirsSafely(pathFilename)
		pathFilename.write_text(str(this), encoding='utf-8')

