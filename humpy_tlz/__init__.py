"""``humpy_tlz`` mirrors the ``humpy_toolz`` API and uses ``cytoolz`` if possible.

The ``humpy_tlz`` package is installed when ``humpy_toolz`` is installed.  It provides
a convenient way to use functions from ``cytoolz``--a faster Cython
implementation of ``humpy_toolz``--if it is installed, otherwise it uses
functions from ``humpy_toolz``.
"""
from . import _build_tlz

