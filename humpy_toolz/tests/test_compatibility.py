import importlib
import pytest

def test_compat_warn():
    with pytest.warns(DeprecationWarning):
        import toolz.compatibility
        importlib.reload(humpy_toolz.compatibility)
