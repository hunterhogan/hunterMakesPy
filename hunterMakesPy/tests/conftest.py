"""Fixtures that own temporary files, the working directory, and isolated copies of samples that a target mutates."""
from __future__ import annotations

from hunterMakesPy.tests.dataSamples.classes import ListGrowsWhenIterated
from typing import TYPE_CHECKING
import pytest

if TYPE_CHECKING:
	from collections.abc import Collection
	from pathlib import Path
	from typing import Any

@pytest.fixture
def listInt_Allegedly(request: pytest.FixtureRequest) -> Collection[Any] | int | None:
	"""`request.param`, or, for a `ListGrowsWhenIterated`, a copy that only one test grows."""
	if isinstance(request.param, ListGrowsWhenIterated):
		return request.param.copy()
	return request.param

@pytest.fixture
def pathFilename(request: pytest.FixtureRequest, tmp_path: Path) -> Path:
	"""Path, in a directory owned by one test, of a Python file containing `request.param`, or of no file if `request.param` is `None`."""
	pathFilename: Path = tmp_path / 'moduleSample.py'
	if request.param is not None:
		pathFilename.write_text(request.param, encoding='utf-8')
	return pathFilename

@pytest.fixture
def pathWorkingDirectory(request: pytest.FixtureRequest, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
	"""Working directory, owned by one test, whose `pyproject.toml` contains `request.param`, or which has no `pyproject.toml` if `request.param` is `None`."""
	if request.param is not None:
		(tmp_path / 'pyproject.toml').write_text(request.param, encoding='utf-8')
	monkeypatch.chdir(tmp_path)
	return tmp_path
