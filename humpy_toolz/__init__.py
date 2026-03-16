from .dicttoolz import *
from .functoolz import *
from .itertoolz import *
from .recipes import *
from functools import partial, reduce
from humpy_toolz import functoolz

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
