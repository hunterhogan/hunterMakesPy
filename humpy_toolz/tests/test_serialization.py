from humpy_toolz import complement, compose, curry, juxt
from humpy_toolz.utils import raises
import humpy_toolz
import humpy_toolz.curried
import pickle

def test_compose():
    f = compose(str, sum)
    g = pickle.loads(pickle.dumps(f))
    assert f((1, 2)) == g((1, 2))

def test_curry():
    f = curry(map)(str)
    g = pickle.loads(pickle.dumps(f))
    assert list(f((1, 2, 3))) == list(g((1, 2, 3)))

def test_juxt():
    f = juxt(str, int, bool)
    g = pickle.loads(pickle.dumps(f))
    assert f(1) == g(1)
    assert f.funcs == g.funcs

def test_complement():
    f = complement(bool)
    assert f(True) is False
    assert f(False) is True
    g = pickle.loads(pickle.dumps(f))
    assert f(True) == g(True)
    assert f(False) == g(False)

def test_instanceproperty():
    p = humpy_toolz.functoolz.InstanceProperty(bool)
    assert p.__get__(None) is None
    assert p.__get__(0) is False
    assert p.__get__(1) is True
    p2 = pickle.loads(pickle.dumps(p))
    assert p2.__get__(None) is None
    assert p2.__get__(0) is False
    assert p2.__get__(1) is True

def f(x, y):
    return (x, y)

def test_flip():
    flip = pickle.loads(pickle.dumps(humpy_toolz.functoolz.flip))
    assert flip is humpy_toolz.functoolz.flip
    g1 = flip(f)
    g2 = pickle.loads(pickle.dumps(g1))
    assert g1(1, 2) == g2(1, 2) == f(2, 1)
    g1 = flip(f)(1)
    g2 = pickle.loads(pickle.dumps(g1))
    assert g1(2) == g2(2) == f(2, 1)

def test_curried_exceptions():
    merge = pickle.loads(pickle.dumps(humpy_toolz.curried.merge))
    assert merge is humpy_toolz.curried.merge

@humpy_toolz.curry
class GlobalCurried:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @humpy_toolz.curry
    def f1(self, a, b):
        return self.x + self.y + a + b

    def g1(self):
        pass

    def __reduce__(self):
        """Allow us to serialize instances of GlobalCurried"""
        return (GlobalCurried, (self.x, self.y))

    @humpy_toolz.curry
    class NestedCurried:

        def __init__(self, x, y):
            self.x = x
            self.y = y

        @humpy_toolz.curry
        def f2(self, a, b):
            return self.x + self.y + a + b

        def g2(self):
            pass

        def __reduce__(self):
            """Allow us to serialize instances of NestedCurried"""
            return (GlobalCurried.NestedCurried, (self.x, self.y))

    class Nested:

        def __init__(self, x, y):
            self.x = x
            self.y = y

        @humpy_toolz.curry
        def f3(self, a, b):
            return self.x + self.y + a + b

        def g3(self):
            pass

def test_curried_qualname():

    def preserves_identity(obj):
        return pickle.loads(pickle.dumps(obj)) is obj
    assert preserves_identity(GlobalCurried)
    assert preserves_identity(GlobalCurried.func.f1)
    assert preserves_identity(GlobalCurried.func.NestedCurried)
    assert preserves_identity(GlobalCurried.func.NestedCurried.func.f2)
    assert preserves_identity(GlobalCurried.func.Nested.f3)
    global_curried1 = GlobalCurried(1)
    global_curried2 = pickle.loads(pickle.dumps(global_curried1))
    assert global_curried1 is not global_curried2
    assert global_curried1(2).f1(3, 4) == global_curried2(2).f1(3, 4) == 10
    global_curried3 = global_curried1(2)
    global_curried4 = pickle.loads(pickle.dumps(global_curried3))
    assert global_curried3 is not global_curried4
    assert global_curried3.f1(3, 4) == global_curried4.f1(3, 4) == 10
    func1 = global_curried1(2).f1(3)
    func2 = pickle.loads(pickle.dumps(func1))
    assert func1 is not func2
    assert func1(4) == func2(4) == 10
    nested_curried1 = GlobalCurried.func.NestedCurried(1)
    nested_curried2 = pickle.loads(pickle.dumps(nested_curried1))
    assert nested_curried1 is not nested_curried2
    assert nested_curried1(2).f2(3, 4) == nested_curried2(2).f2(3, 4) == 10

def test_curried_bad_qualname():

    @humpy_toolz.curry
    class Bad:
        __qualname__ = 'toolz.functoolz.not.a.valid.path'
    assert raises(pickle.PicklingError, lambda: pickle.dumps(Bad))
