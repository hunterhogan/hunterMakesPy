"""The text of `pyproject.toml` files, named by the state of `project.name`."""
from __future__ import annotations

tomlProjectMalformed: str = "[project\nname = 'cobraPy'\n"
tomlProjectNameEmpty: str = "[project]\nname = ''\n"
tomlProjectNamed: str = "[project]\nname = 'cobraPy'\nversion = '2.3.5'\n"
tomlProjectNameless: str = "[project]\nversion = '13.21.34'\n"
