"""A modular toolkit for defensive programming, parameter validation, file system utilities, and data structure manipulation.

(AI generated docstring)

This package provides:
- Defensive programming helpers for handling `None` values and error propagation.
- Parameter and input validation, integer parsing, and concurrency limit utilities.
- File system and import utilities for safe directory creation and dynamic module/attribute loading.
- Utilities for string extraction from nested data structures and merging dictionaries of lists.

"""
from hunterMakesPy.theTypes import identifierDotAttribute as identifierDotAttribute

from hunterMakesPy.coping import raiseIfNone as raiseIfNone

from hunterMakesPy.parseParameters import (defineConcurrencyLimit as defineConcurrencyLimit, intInnit as intInnit,
	oopsieKwargsie as oopsieKwargsie)

from hunterMakesPy.filesystemToolkit import (importLogicalPath2Identifier as importLogicalPath2Identifier,
	importPathFilename2Identifier as importPathFilename2Identifier, makeDirsSafely as makeDirsSafely,
	writeStringToHere as writeStringToHere)

from hunterMakesPy.dataStructures import (autoDecodingRLE as autoDecodingRLE, stringItUp as stringItUp,
	updateExtendPolishDictionaryLists as updateExtendPolishDictionaryLists)

from hunterMakesPy._theSSOT import settingsPackage
