from humpy_toolz import functoolz

__version__ = '1.1.0'
from .dicttoolz import *
from .functoolz import *
from .itertoolz import *
from .recipes import *
from functools import partial, reduce

sorted = sorted
map = map
filter = filter
comp = compose
from . import curried, sandbox

functoolz._sigs.create_signature_registry()

def __getattr__(name):
    if name == '__version__':
        from importlib.metadata import version
        rv = version('humpy_toolz')
        globals()[name] = rv
        return rv
    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')
