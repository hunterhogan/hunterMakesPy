"""Execute defensive programming, parameter validation, file operations, and data manipulation.

(AI generated docstring)

You can use this package to implement defensive programming patterns, validate and parse
input parameters, perform file system operations with safe error handling, and manipulate
data structures with specialized encoding and merging utilities. The package provides a
curated collection of functions for common programming tasks with emphasis on fail-early
validation and explicit semantic intent.

The package re-exports core semantic constants (`decreasing`, `errorL33T`, `inclusive`,
`zeroIndexed`) and type definitions (`identifierDotAttribute`, `Ordinals`) for direct
access. The package exposes configuration utilities (`PackageSettings`) and defensive
programming functions (`raiseIfNone`) as primary interfaces. Public modules provide
specialized functionality for parameter parsing, file operations, and data structure
manipulation.

Re-exported Identifiers
-----------------------
Semantic Constants
	decreasing
		Express descending iteration or a reverse direction.
	errorL33T
		Signal an error state with a visually distinctive numeric value.
	inclusive
		Express inclusion or exclusion of a boundary value.
	zeroIndexed
		Express that the adjustment to a value is due to zero-based indexing.

Type Definitions
	identifierDotAttribute
		String representing a dotted attribute identifier.
	Ordinals
		Protocol for types supporting comparison operators.

Configuration and Defensive Programming
	PackageSettings
		Configuration container for Python package metadata and runtime settings.
	raiseIfNone
		Convert return annotation from 'Type | None' to 'Type' with runtime validation.

Public Modules
--------------
coping
	Package configuration and defensive programming utilities.
dataStructures
	Data structure manipulation with encoding, extraction, and merging utilities.
filesystemToolkit
	File system operations and dynamic module imports.
parseParameters
	Parameter validation, integer parsing, and concurrency limit computation.
pytestForYourUse
	Backward compatibility module redirecting to test_parseParameters.
semiotics
	Semantic constants and ANSI color codes for terminal output.
theTypes
	Type aliases and protocols for type annotations.
tests
	Comprehensive test suites for all package modules.

References
----------
[1] hunterMakesPy - Context7
	https://context7.com/hunterhogan/huntermakespy

"""

# isort: split
from hunterMakesPy.semiotics import (
	decreasing as decreasing, errorL33T as errorL33T, inclusive as inclusive, zeroIndexed as zeroIndexed)

# isort: split
from hunterMakesPy.theTypes import (
	CallableFunction as CallableFunction, identifierDotAttribute as identifierDotAttribute, Ordinals as Ordinals)

# isort: split
from hunterMakesPy.coping import PackageSettings as PackageSettings, raiseIfNone as raiseIfNone

# isort: split
from hunterMakesPy.parseParameters import defineConcurrencyLimit, intInnit, oopsieKwargsie

# isort: split
from hunterMakesPy.filesystemToolkit import (
	importLogicalPath2Identifier, importPathFilename2Identifier, makeDirsSafely, writePython, writeStringToHere)

# isort: split
from hunterMakesPy.dataStructures import autoDecodingRLE, stringItUp, updateExtendPolishDictionaryLists

# isort: split
from hunterMakesPy._theSSOT import settingsPackage  # pyright: ignore[reportUnusedImport]
