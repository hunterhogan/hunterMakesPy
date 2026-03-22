from __future__ import annotations

from collections.abc import Callable
from enum import Enum
from typing import Any

def raises(err: type[Exception], lamda: Callable[[], Any]) -> bool:
    try:
        lamda()
        return False
    except err:
        return True

class NoDefaultType(Enum):
    no_default = '__no_default__'
no_default = NoDefaultType.no_default

class NoPadType(Enum):
    no_pad = '__no_pad__'
no_pad = NoPadType.no_pad
