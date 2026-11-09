"""Execute defensive programming, parameter validation, file operations, and data manipulation.

(AI generated docstring)

You can use this package to implement defensive programming patterns, validate and parse
input parameters, perform file system operations with safe error handling, and manipulate
data structures with specialized encoding and merging utilities. The package provides a
curated collection of functions for common programming tasks with emphasis on fail-early
validation and explicit semantic intent.

The package re-exports semantic constants, ANSI color codes, and type definitions for direct
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
	oneIndexed
		Express that the adjustment to a value is due to one-based indexing.
	zeroIndexed
		Express that the adjustment to a value is due to zero-based indexing.

Terminal Colors
	ansiColor
		Look up ANSI escape codes for terminal text and background colors.
	ansiColorReset
		Reset terminal text color and background to default settings.

Type Definitions
	CallableFunction
		Annotate a function in place of `Callable` so that type checkers accept `__name__`.
	ConcurrencyLimit
		Type alias for the values that specify a number of concurrent workers.
	identifierDotAttribute
		String representing a dotted attribute identifier.
	Ordinals
		Protocol for types supporting comparison operators.
	小于
		Type variable bound to `Ordinals`.
	文义
		Unbounded type variable.
	文件
		Type variable bound to `Hashable`.

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
kitFilesystem
	File system operations and dynamic module imports.
parseParameters
	Parameter validation, integer parsing, and concurrency limit computation.
semiotics
	Semantic constants and ANSI color codes for terminal output.
tests
	Test suites for the package modules, and assertion functions that other packages can import.
theTypes
	Type aliases and protocols for type annotations.

References
----------
[1] hunterMakesPy - Context7
	https://context7.com/hunterhogan/huntermakespy

"""

# isort: split
from __future__ import annotations

from hunterMakesPy.semiotics import (
	ansiColor as ansiColor, ansiColorReset as ansiColorReset, decreasing as decreasing, errorL33T as errorL33T, inclusive as inclusive,
	oneIndexed as oneIndexed, zeroIndexed as zeroIndexed)

# isort: split
from hunterMakesPy.theTypes import (
	CallableFunction as CallableFunction, ConcurrencyLimit as ConcurrencyLimit, identifierDotAttribute as identifierDotAttribute,
	Ordinals as Ordinals, 小于 as 小于, 文义 as 文义, 文件 as 文件)

# isort: split
from hunterMakesPy.coping import PackageSettings as PackageSettings, raiseIfNone as raiseIfNone
