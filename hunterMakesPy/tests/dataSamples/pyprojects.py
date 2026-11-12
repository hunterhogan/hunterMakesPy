"""The text of `pyproject.toml` files, named by the state of `project.name`."""
from __future__ import annotations

from typing import TYPE_CHECKING
import pytest

if TYPE_CHECKING:
	from _pytest.mark.structures import ParameterSet

tomlProjectMalformed: str = "[project\nname = 'cobraPy'\n"
tomlProjectNameEmpty: str = "[project]\nname = ''\n"
tomlProjectNamed: str = "[project]\nname = 'cobraPy'\nversion = '2.3.5'\n"
tomlProjectNameless: str = "[project]\nversion = '13.21.34'\n"

boxOfPyprojects: tuple[ParameterSet, ...] = (
	pytest.param(None, id='pyprojectAbsent'),
	pytest.param(tomlProjectMalformed, id='tomlProjectMalformed'),
	pytest.param(tomlProjectNameEmpty, id='tomlProjectNameEmpty'),
	pytest.param(tomlProjectNamed, id='tomlProjectNamed'),
	pytest.param(tomlProjectNameless, id='tomlProjectNameless'),
)
"""Every `pyproject.toml` state of a working directory; `None` means the working directory has no `pyproject.toml`."""
