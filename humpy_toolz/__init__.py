from .dicttoolz import *
from .functoolz import *
from .itertoolz import *
from .recipes import *
from functools import partial, reduce
from . import curried, sandbox
from .functoolz import _sigs

__version__ = '1.1.0'
sorted = sorted
map = map
filter = filter
comp = compose

_sigs.create_signature_registry()

