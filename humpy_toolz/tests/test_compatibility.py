import importlib
import pytest

def test_compat_warn():
    with pytest.warns(DeprecationWarning):
        import humpy_toolz.compatibility
        importlib.reload(humpy_toolz.compatibility)
