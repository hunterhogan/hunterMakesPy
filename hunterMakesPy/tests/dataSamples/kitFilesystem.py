"""Samples and expected results for `hunterMakesPy.kitFilesystem`."""
from __future__ import annotations

from collections import Counter
from hunterMakesPy import raiseIfNone
from hunterMakesPy.kitFilesystem import settings_isortDEFAULT
from hunterMakesPy.tests.dataSamples.pythonSource import (
	sourceImportsUnsorted, sourceImportsUnused, sourceImportsUnusedThirdParty, sourceImportsUsed)
from pathlib import PurePosixPath
from typing import TYPE_CHECKING
import io
import math
import os
import pytest

if TYPE_CHECKING:
	from _pytest.mark.structures import ParameterSet

#================== Import identifiers ===========================================================================================

# Relation: the imported object is the object that an ordinary import statement binds.
parametersImportLogicalPath2Identifier: tuple[ParameterSet, ...] = (
	pytest.param('math', 'gcd', None, math.gcd, id='math.gcd'),
	pytest.param('os.path', 'join', None, os.path.join, id='os.path.join'),
	pytest.param('hunterMakesPy.coping', 'raiseIfNone', None, raiseIfNone, id='hunterMakesPy.coping.raiseIfNone'),
	pytest.param('.coping', 'raiseIfNone', 'hunterMakesPy', raiseIfNone, id='relative.coping.raiseIfNone'),
	pytest.param('.kitFilesystem', 'settings_isortDEFAULT', 'hunterMakesPy', settings_isortDEFAULT, id='relative.settings_isortDEFAULT'),
)

# Reference: `importlib.import_module` raises `ModuleNotFoundError` for an absent module, and `getattr` raises `AttributeError`.
parametersImportLogicalPath2IdentifierError: tuple[ParameterSet, ...] = (
	pytest.param('hunterMakesPy.noSuchModule', 'raiseIfNone', None, ModuleNotFoundError, id='moduleAbsent'),
	pytest.param('math', 'noSuchFunction', None, AttributeError, id='identifierAbsent'),
	pytest.param('.noSuchModule', 'raiseIfNone', 'hunterMakesPy', ModuleNotFoundError, id='relativeModuleAbsent'),
)

# Reference: the value that each source binds to the identifier.
parametersImportPathFilename2Identifier: tuple[ParameterSet, ...] = (
	pytest.param(sourceImportsUnsorted, 'primes', Counter({2: 1, 3: 2, 5: 1}), id='sourceImportsUnsorted.primes'),
	pytest.param(sourceImportsUnsorted, 'north', PurePosixPath('north'), id='sourceImportsUnsorted.north'),
	pytest.param(sourceImportsUnsorted, 'tau', math.tau, id='sourceImportsUnsorted.tau'),
	pytest.param(sourceImportsUnused, 'fibonacci', 13, id='sourceImportsUnused.fibonacci'),
	pytest.param(sourceImportsUnusedThirdParty, 'fibonacci', 21, id='sourceImportsUnusedThirdParty.fibonacci'),
	pytest.param(sourceImportsUsed, 'primeGCD', 17, id='sourceImportsUsed.primeGCD'),
)

# Reference: the docstring lists the exceptions. `None` means no file exists at the path.
parametersImportPathFilename2IdentifierError: tuple[ParameterSet, ...] = (
	pytest.param(sourceImportsUsed, 'noSuchIdentifier', AttributeError, id='identifierAbsent'),
	pytest.param(None, 'primeGCD', FileNotFoundError, id='fileAbsent'),
)

boxOfModuleIdentifiers: tuple[ParameterSet, ...] = (
	pytest.param(None, id='moduleIdentifierNone'),
	pytest.param('moduleNorthEast', id='moduleNorthEast'),
)

#================== makeDirectorySafely ==========================================================================================

# Reference: the docstring states that `makeDirectorySafely` does nothing when `pathFilename` is an `IOBase` stream.
parametersMakeDirectorySafelyStream: tuple[ParameterSet, ...] = (
	pytest.param(io.BytesIO(b'NE'), b'NE', id='BytesIO'),
	pytest.param(io.StringIO('NE'), 'NE', id='StringIO'),
)

#================== writePython ==================================================================================================

settingsAutoflakeKeepImports: dict[str, dict[str, bool]] = {'autoflake': {'remove_all_unused_imports': False}}
settingsIsortDefaultProfile: dict[str, dict[str, bool]] = {'isort': {}}

# Reference: hand-derived from `settings_autoflakeDEFAULT`, `settings_isortDEFAULT`, the isort defaults, and the trailing newline
# that `writePython` appends. Removing an import leaves the blank line that followed the imports.
parametersWritePython: tuple[ParameterSet, ...] = (
	pytest.param(sourceImportsUnused, None, '\nfibonacci = 13\n\n', id='sourceImportsUnused'),
	pytest.param(sourceImportsUsed, None, 'import math\n\nprimeGCD = math.gcd(221, 323)\n\n', id='sourceImportsUsed'),
	pytest.param(
		sourceImportsUnsorted, None
		, "from pathlib import PurePosixPath\nimport collections\nimport math\n\n"
		"primes = collections.Counter([2, 3, 3, 5])\nnorth = PurePosixPath('north')\ntau = math.tau\n\n"
		, id='sourceImportsUnsorted'
	),
	pytest.param(sourceImportsUnusedThirdParty, None, '\nfibonacci = 21\n\n', id='sourceImportsUnusedThirdParty'),
	# autoflake removes an unused standard-library import even when `remove_all_unused_imports` is `False`.
	pytest.param(
		sourceImportsUnusedThirdParty, settingsAutoflakeKeepImports, 'import numpy\n\nfibonacci = 21\n\n'
		, id='sourceImportsUnusedThirdParty-settingsAutoflakeKeepImports'
	),
	pytest.param(
		sourceImportsUnsorted, settingsIsortDefaultProfile
		, "import collections\nimport math\nfrom pathlib import PurePosixPath\n\n"
		"primes = collections.Counter([2, 3, 3, 5])\nnorth = PurePosixPath('north')\ntau = math.tau\n\n"
		, id='sourceImportsUnsorted-settingsIsortDefaultProfile'
	),
)
