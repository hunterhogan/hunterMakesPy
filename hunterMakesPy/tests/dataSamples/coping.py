"""Samples and expected results for `hunterMakesPy.coping`."""
from __future__ import annotations

from hunterMakesPy.tests.dataSamples.arrays import arrayRange
from pathlib import Path
from typing import TYPE_CHECKING
import pytest

if TYPE_CHECKING:
	from _pytest.mark.structures import ParameterSet

#================== pyproject.toml ===============================================================================================

tomlProjectMalformed: str = "[project\nname = 'cobraPy'\n"
tomlProjectNameEmpty: str = "[project]\nname = ''\n"
tomlProjectNamed: str = "[project]\nname = 'cobraPy'\nversion = '2.3.5'\n"
tomlProjectNameless: str = "[project]\nversion = '13.21.34'\n"

# `None` means the working directory has no `pyproject.toml`.
boxOfPyprojects: tuple[ParameterSet, ...] = (
	pytest.param(None, id='pyprojectAbsent'),
	pytest.param(tomlProjectMalformed, id='tomlProjectMalformed'),
	pytest.param(tomlProjectNameEmpty, id='tomlProjectNameEmpty'),
	pytest.param(tomlProjectNamed, id='tomlProjectNamed'),
	pytest.param(tomlProjectNameless, id='tomlProjectNameless'),
)
"""Every `pyproject.toml` state of a working directory."""

# Reference: the TOML text states `project.name`.
parametersPyprojectNamed: tuple[ParameterSet, ...] = (
	pytest.param(tomlProjectNamed, 'cobraPy', id='tomlProjectNamed'),
)

# Reference: none of these states has a usable `project.name`, so the fallback identifier applies.
parametersPyprojectUnnamed: tuple[ParameterSet, ...] = (
	pytest.param(None, id='pyprojectAbsent'),
	pytest.param(tomlProjectMalformed, id='tomlProjectMalformed'),
	pytest.param(tomlProjectNameEmpty, id='tomlProjectNameEmpty'),
	pytest.param(tomlProjectNameless, id='tomlProjectNameless'),
)

#================== Package identity and location ================================================================================

boxOfIdentifiersPackage: tuple[str, ...] = ('astToolkit', 'mapFolding')
"""Package identifiers that are neither this package nor installed in its environment."""

# Relation: an explicit `identifierPackage` and an explicit `pathPackage` survive `__post_init__` unchanged.
boxOfPathsPackage: tuple[ParameterSet, ...] = (
	pytest.param(Path('C:/fibonacci/path'), id='pathWindowsAbsolute'),
	pytest.param(Path('relative/north'), id='pathRelative'),
	pytest.param(Path('/usr/local/lib/prime'), id='pathRootAbsolute'),
)

# Reference for each installed identifier: `importlib.resources.files(identifierPackage)`.
boxOfIdentifiersInstalled: tuple[str, ...] = ('fractions', 'hunterMakesPy', 'hunterMakesPy.tests', 'json')

# Reference: `find_spec` finds no module, so the location is the working directory.
boxOfIdentifiersAbsent: tuple[str, ...] = ('hunterMakesPy.noSuchModule', 'noSuchPackage13', 'noSuchParent.child')

#================== raiseIfNone ==================================================================================================

# Relation: `raiseIfNone` returns the object it received, including every falsy object.
boxOfValuesNotNone: tuple[ParameterSet, ...] = (
	pytest.param(0, id='zero'),
	pytest.param(13, id='prime13'),
	pytest.param('', id='stringEmpty'),
	pytest.param('NE', id='stringNE'),
	pytest.param(False, id='false'),
	pytest.param([], id='listEmpty'),
	pytest.param(arrayRange, id='arrayRange'),
)

messageRaiseIfNoneDEFAULT: str = 'A function unexpectedly returned `None`. Hint: look at the traceback immediately before `raiseIfNone`.'
messageHostMissing: str = "Configuration must include 'host' setting"

boxOfErrorMessages: tuple[ParameterSet, ...] = (
	pytest.param(None, id='errorMessageNone'),
	pytest.param(messageHostMissing, id='messageHostMissing'),
)

# Reference: the docstring states the default message. Accepted recording: an empty `errorMessage` selects the default.
parametersRaiseIfNoneError: tuple[ParameterSet, ...] = (
	pytest.param(None, messageRaiseIfNoneDEFAULT, id='errorMessageNone'),
	pytest.param('', messageRaiseIfNoneDEFAULT, id='errorMessageEmpty'),
	pytest.param(messageHostMissing, messageHostMissing, id='messageHostMissing'),
)
