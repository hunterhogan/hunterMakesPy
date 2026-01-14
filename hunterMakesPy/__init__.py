"""A modular toolkit for defensive programming, parameter validation, file system utilities, and data structure manipulation.

This package provides:
- Defensive programming helpers for handling `None` values and error propagation.
- Parameter and input validation, integer parsing, and concurrency limit utilities.
- File system and import utilities for safe directory creation and dynamic module/attribute loading.
- Utilities for string extraction from nested data structures and merging dictionaries of lists.

"""

from hunterMakesPy.theTypes import identifierDotAttribute as identifierDotAttribute, Ordinals as Ordinals

from hunterMakesPy.coping import PackageSettings as PackageSettings, raiseIfNone as raiseIfNone

from hunterMakesPy.parseParameters import defineConcurrencyLimit, intInnit, oopsieKwargsie

from hunterMakesPy.filesystemToolkit import (
	importLogicalPath2Identifier, importPathFilename2Identifier, makeDirsSafely, writePython, writeStringToHere)

from hunterMakesPy.dataStructures import autoDecodingRLE, stringItUp, updateExtendPolishDictionaryLists

from hunterMakesPy._theSSOT import settingsPackage  # pyright: ignore[reportUnusedImport]
