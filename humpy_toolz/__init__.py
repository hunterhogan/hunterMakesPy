from .dicttoolz import *
from .functoolz import *
from .itertoolz import *
from .recipes import *
from functools import partial, reduce

__version__ = '1.1.0'
sorted = sorted
map = map
filter = filter
comp = compose
from . import curried, sandbox
from .functoolz import _sigs

_sigs.create_signature_registry()
from ._version import __version__

