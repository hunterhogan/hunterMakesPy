import importlib
import pytest

def test_compat_warn():
    with pytest.warns(DeprecationWarning):
        import humpy_cytoolz.compatibility
        importlib.reload(humpy_cytoolz.compatibility)
