from __future__ import annotations

from importlib import import_module
from importlib.abc import Loader
from importlib.machinery import ModuleSpec
from types import ModuleType
from typing import TYPE_CHECKING
import contextlib
import humpy_toolz
import sys

if TYPE_CHECKING:
    from collections.abc import Sequence

class TlzLoader(Loader):
    """ Finds and loads ``humpy_tlz`` modules when added to sys.meta_path"""

    def __init__(self) -> None:
        self.always_from_toolz = {humpy_toolz.pipe}

    def _load_toolz(self, fullname: str) -> dict[str, ModuleType]:
        rv = {}
        _, dot, submodules = fullname.partition('.')
        try:
            module_name = ''.join(['humpy_cytoolz', dot, submodules])
            rv['humpy_cytoolz'] = import_module(module_name)
        except ImportError:
            pass
        try:
            module_name = ''.join(['humpy_toolz', dot, submodules])
            rv['humpy_toolz'] = import_module(module_name)
        except ImportError:
            pass
        if not rv:
            raise ImportError(fullname)
        return rv

    def find_module(self, fullname: str, path: Sequence[str] | None=None) -> TlzLoader | None:
        package, _, __ = fullname.partition('.')
        if package == 'humpy_tlz':
            return self
        return None

    def load_module(self, fullname: str) -> ModuleType:
        if fullname in sys.modules:
            return sys.modules[fullname]
        spec = ModuleSpec(fullname, self)
        module = self.create_module(spec)
        sys.modules[fullname] = module
        self.exec_module(module)
        return module

    def find_spec(self, fullname: str, path: Sequence[str] | None, target: ModuleType | None=None) -> ModuleSpec | None:
        package, _, __ = fullname.partition('.')
        if package == 'humpy_tlz':
            return ModuleSpec(fullname, self)
        return None

    def create_module(self, spec: ModuleSpec) -> ModuleType:
        return ModuleType(spec.name)

    def exec_module(self, module: ModuleType) -> None:
        toolz_mods = self._load_toolz(module.__name__)
        fast_mod = toolz_mods.get('humpy_cytoolz') or toolz_mods['humpy_toolz']
        slow_mod = toolz_mods.get('humpy_toolz') or toolz_mods['humpy_cytoolz']
        module.__dict__.update(humpy_toolz.merge(fast_mod.__dict__, module.__dict__))
        package = fast_mod.__package__
        if package is not None:
            package, dot, submodules = package.partition('.')
            module.__package__ = ''.join(['humpy_tlz', dot, submodules])
        if not module.__doc__:
            module.__doc__ = fast_mod.__doc__
        with contextlib.suppress(AttributeError):
            module.__file__ = slow_mod.__file__
        for k, v in fast_mod.__dict__.items():
            tv = slow_mod.__dict__.get(k)
            try:
                hash(tv)
            except TypeError:
                tv = None
            if tv in self.always_from_toolz:
                module.__dict__[k] = tv
            elif isinstance(v, ModuleType) and v.__package__ == fast_mod.__name__:
                package, dot, submodules = v.__name__.partition('.')
                module_name = ''.join(['humpy_tlz', dot, submodules])
                submodule = import_module(module_name)
                module.__dict__[k] = submodule
tlz_loader = TlzLoader()
sys.meta_path.append(tlz_loader)
tlz_loader.exec_module(sys.modules['humpy_tlz'])
