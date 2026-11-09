"""Test the hunterMakesPy package, and share its assertion helpers with other packages.

Other packages import the assertion helpers from here:

```python
from hunterMakesPy.tests import assert_array_equal, assertEqualTo
```

Test package organization (in hunterMakesPy/tests/):
- conftest.py: Fixtures: working directories with a given `pyproject.toml` and Python files written from source
- conftestAnnex.py: Assertion helpers, re-exported here, with assertion rewriting registered before import
- dataSamples/: Static samples, expected results with their basis, and pytest-ready parameter rows
- test_coping.py: Package identity and location, and `raiseIfNone`
- test_dataStructures.py: Run-length encoding, whitespace removal, string extraction, and merging mappings of lists
- test_kitFilesystem.py: Writing and appending text, writing Python source, creating directories, and importing identifiers
- test_parseParameters.py: Worker counts, integer validation, and interpreting strings as `True`, `False`, or `None`
- test_theTypes.py: Runtime behavior of `CallableFunction`
"""
from __future__ import annotations

import pytest

# Register assertion rewriting before importing `conftestAnnex`, so its plain `assert` statements report their operands.
# ruff: ignore[non-empty-init-module]
pytest.register_assert_rewrite('hunterMakesPy.tests.conftestAnnex')

# isort: split
# ruff: ignore[module-import-not-at-top-of-file]
from hunterMakesPy.tests.conftestAnnex import (
	assert_allclose as assert_allclose, assert_approx as assert_approx, assert_array_equal as assert_array_equal,
	assertEqualTo as assertEqualTo, messageTestFailure as messageTestFailure, messageTestFailure_ndarray as messageTestFailure_ndarray)
