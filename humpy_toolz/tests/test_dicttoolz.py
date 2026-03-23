from collections import defaultdict as _defaultdict
from collections.abc import Callable, ItemsView, Iterator, KeysView, Mapping, ValuesView
from humpy_toolz.dicttoolz import (
	assoc, assoc_in, dissoc, itemfilter, itemmap, keyfilter, keymap, merge, merge_with, update_in, valfilter, valmap)
from humpy_toolz.functoolz import identity
from humpy_toolz.utils import raises
from typing import Any, ClassVar
import os

def inc(x: int) -> int:
    return x + 1

def iseven(i: int) -> bool:
    return i % 2 == 0

class TestDict:
    """Test typical usage: dict inputs, no factory keyword.

    Class attributes:
        D: callable that inputs a dict and creates or returns a MutableMapping
        kw: kwargs dict to specify "factory" keyword (if applicable)
    """
    D: ClassVar[Callable[..., Any]] = dict
    kw: ClassVar[dict[str, Any]] = {}

    def test_merge(self) -> None:
        D, kw = (self.D, self.kw)
        assert merge(D({1: 1, 2: 2}), D({3: 4}), **kw) == D({1: 1, 2: 2, 3: 4})

    def test_merge_iterable_arg(self) -> None:
        D, kw = (self.D, self.kw)
        assert merge([D({1: 1, 2: 2}), D({3: 4})], **kw) == D({1: 1, 2: 2, 3: 4})

    def test_merge_with(self) -> None:
        D, kw = (self.D, self.kw)
        dicts = (D({1: 1, 2: 2}), D({1: 10, 2: 20}))
        assert merge_with(sum, *dicts, **kw) == D({1: 11, 2: 22})
        assert merge_with(tuple, *dicts, **kw) == D({1: (1, 10), 2: (2, 20)})
        dicts = (D({1: 1, 2: 2, 3: 3}), D({1: 10, 2: 20}))
        assert merge_with(sum, *dicts, **kw) == D({1: 11, 2: 22, 3: 3})
        assert merge_with(tuple, *dicts, **kw) == D({1: (1, 10), 2: (2, 20), 3: (3,)})
        assert not merge_with(sum)

    def test_merge_with_iterable_arg(self) -> None:
        D, kw = (self.D, self.kw)
        dicts = (D({1: 1, 2: 2}), D({1: 10, 2: 20}))
        assert merge_with(sum, *dicts, **kw) == D({1: 11, 2: 22})
        assert merge_with(sum, dicts, **kw) == D({1: 11, 2: 22})
        assert merge_with(sum, iter(dicts), **kw) == D({1: 11, 2: 22})

    def test_valmap(self) -> None:
        D, kw = (self.D, self.kw)
        assert valmap(inc, D({1: 1, 2: 2}), **kw) == D({1: 2, 2: 3})

    def test_keymap(self) -> None:
        D, kw = (self.D, self.kw)
        assert keymap(inc, D({1: 1, 2: 2}), **kw) == D({2: 1, 3: 2})

    def test_itemmap(self) -> None:
        D, kw = (self.D, self.kw)
        assert itemmap(reversed, D({1: 2, 2: 4}), **kw) == D({2: 1, 4: 2})

    def test_valfilter(self) -> None:
        D, kw = (self.D, self.kw)
        assert valfilter(iseven, D({1: 2, 2: 3}), **kw) == D({1: 2})

    def test_keyfilter(self) -> None:
        D, kw = (self.D, self.kw)
        assert keyfilter(iseven, D({1: 2, 2: 3}), **kw) == D({2: 3})

    def test_itemfilter(self) -> None:
        D, kw = (self.D, self.kw)
        assert itemfilter(lambda item: iseven(item[0]), D({1: 2, 2: 3}), **kw) == D({2: 3})
        assert itemfilter(lambda item: iseven(item[1]), D({1: 2, 2: 3}), **kw) == D({1: 2})

    def test_assoc(self) -> None:
        D, kw = (self.D, self.kw)
        assert assoc(D({}), 'a', 1, **kw) == D({'a': 1})
        assert assoc(D({'a': 1}), 'a', 3, **kw) == D({'a': 3})
        assert assoc(D({'a': 1}), 'b', 3, **kw) == D({'a': 1, 'b': 3})
        d = D({'x': 1})
        oldd = d
        assoc(d, 'x', 2, **kw)
        assert d is oldd

    def test_dissoc(self) -> None:
        D, kw = (self.D, self.kw)
        assert dissoc(D({'a': 1}), 'a', **kw) == D({})
        assert dissoc(D({'a': 1, 'b': 2}), 'a', **kw) == D({'b': 2})
        assert dissoc(D({'a': 1, 'b': 2}), 'b', **kw) == D({'a': 1})
        assert dissoc(D({'a': 1, 'b': 2}), 'a', 'b', **kw) == D({})
        assert dissoc(D({'a': 1}), 'a', **kw) == dissoc(dissoc(D({'a': 1}), 'a', **kw), 'a', **kw)
        d = D({'x': 1})
        oldd = d
        d2 = dissoc(d, 'x', **kw)
        assert d is oldd
        assert d2 is not oldd

    def test_assoc_in(self) -> None:
        D, kw = (self.D, self.kw)
        assert assoc_in(D({'a': 1}), ['a'], 2, **kw) == D({'a': 2})
        assert assoc_in(D({'a': D({'b': 1})}), ['a', 'b'], 2, **kw) == D({'a': D({'b': 2})})
        assert assoc_in(D({}), ['a', 'b'], 1, **kw) == D({'a': D({'b': 1})})
        d = D({'x': 1})
        oldd = d
        d2 = assoc_in(d, ['x'], 2, **kw)
        assert d is oldd
        assert d2 is not oldd

    def test_update_in(self) -> None:
        D, kw = (self.D, self.kw)
        assert update_in(D({'a': 0}), ['a'], inc, **kw) == D({'a': 1})
        assert update_in(D({'a': 0, 'b': 1}), ['b'], str, **kw) == D({'a': 0, 'b': '1'})
        assert update_in(D({'t': 1, 'v': D({'a': 0})}), ['v', 'a'], inc, **kw) == D({'t': 1, 'v': D({'a': 1})})
        assert update_in(D({}), ['z'], str, None, **kw) == D({'z': 'None'})
        assert update_in(D({}), ['z'], inc, 0, **kw) == D({'z': 1})
        assert update_in(D({}), ['z'], lambda x: x + 'ar', default='b', **kw) == D({'z': 'bar'})
        assert update_in(D({}), [0, 1], inc, default=-1, **kw) == D({0: D({1: 0})})
        assert update_in(D({}), [0, 1], str, default=100, **kw) == D({0: D({1: '100'})})
        assert update_in(D({'foo': 'bar', 1: 50}), ['d', 1, 0], str, 20, **kw) == D({'foo': 'bar', 1: 50, 'd': D({1: D({0: '20'})})})
        d = D({'x': 1})
        oldd = d
        update_in(d, ['x'], inc, **kw)
        assert d is oldd

    def test_factory(self) -> None:
        D, kw = (self.D, self.kw)
        assert merge(defaultdict(int, D({1: 2})), D({2: 3})) == {1: 2, 2: 3}
        assert merge(defaultdict(int, D({1: 2})), D({2: 3}), factory=lambda: defaultdict(int)) == defaultdict(int, D({1: 2, 2: 3}))
        assert not merge(defaultdict(int, D({1: 2})), D({2: 3}), factory=lambda: defaultdict(int)) == {1: 2, 2: 3}
        assert raises(TypeError, lambda: merge(D({1: 2}), D({2: 3}), factoryy=dict))

class defaultdict(_defaultdict):

    def __eq__(self, other: object) -> bool:
        return super().__eq__(other) and isinstance(other, _defaultdict) and (self.default_factory == other.default_factory)

class TestDefaultDict(TestDict):
    """Test defaultdict as input and factory

    Class attributes:
        D: callable that inputs a dict and creates or returns a MutableMapping
        kw: kwargs dict to specify "factory" keyword (if applicable)
    """

    @staticmethod
    def D(dict_: dict[Any, Any]) -> defaultdict:
        return defaultdict(int, dict_)
    kw = {'factory': lambda: defaultdict(int)}

class CustomMapping:
    """Define methods of the MutableMapping protocol required by dicttoolz"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._d = dict(*args, **kwargs)

    def __getitem__(self, key: Any) -> Any:
        return self._d[key]

    def __setitem__(self, key: Any, val: Any) -> None:
        self._d[key] = val

    def __delitem__(self, key: Any) -> None:
        del self._d[key]

    def __iter__(self) -> Iterator[Any]:
        return iter(self._d)

    def __len__(self) -> int:
        return len(self._d)

    def __contains__(self, key: object) -> bool:
        return key in self._d

    def __eq__(self, other: object) -> bool:
        return isinstance(other, CustomMapping) and self._d == other._d

    def __ne__(self, other: object) -> bool:
        return not isinstance(other, CustomMapping) or self._d != other._d

    def keys(self) -> KeysView[Any]:
        return self._d.keys()

    def values(self) -> ValuesView[Any]:
        return self._d.values()

    def items(self) -> ItemsView[Any, Any]:
        return self._d.items()

    def update(self, *args: Any, **kwargs: Any) -> None:
        self._d.update(*args, **kwargs)

class TestCustomMapping(TestDict):
    """Test CustomMapping as input and factory

    Class attributes:
        D: callable that inputs a dict and creates or returns a MutableMapping
        kw: kwargs dict to specify "factory" keyword (if applicable)
    """
    D = CustomMapping
    kw = {'factory': lambda: CustomMapping()}

def test_environ() -> None:
    assert keymap(identity, os.environ) == os.environ
    assert valmap(identity, os.environ) == os.environ
    assert itemmap(identity, os.environ) == os.environ

def test_merge_with_non_dict_mappings() -> None:

    class Foo(Mapping):

        def __init__(self, d: dict[Any, Any]) -> None:
            self.d = d

        def __iter__(self) -> Iterator[Any]:
            return iter(self.d)

        def __getitem__(self, key: Any) -> Any:
            return self.d[key]

        def __len__(self) -> int:
            return len(self.d)
    d = Foo({1: 1})
    assert merge(d) is d or merge(d) == {1: 1}
    assert merge_with(sum, d) == {1: 1}
