import importlib
import pytest

def test_compat_warn():
    with pytest.warns(DeprecationWarning):
        importlib.reload(humpy_toolz.compatibility)
