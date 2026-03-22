from humpy_toolz import reduce
from humpy_toolz.sandbox.parallel import fold
from humpy_toolz.utils import no_default
from multiprocessing import Pool
from operator import add
from pickle import dumps, loads

no_default2 = loads(dumps(no_default))

def test_fold():
    assert fold(add, range(10), 0) == reduce(add, range(10), 0)
    assert fold(add, range(10), 0, map=Pool().map) == reduce(add, range(10), 0)
    assert fold(add, range(10), 0, chunksize=2) == reduce(add, range(10), 0)
    assert fold(add, range(10)) == fold(add, range(10), 0)

    def setadd(s, item):
        s = s.copy()
        s.add(item)
        return s
    assert fold(setadd, [1, 2, 3], set()) == {1, 2, 3}
    assert fold(setadd, [1, 2, 3], set(), chunksize=2, combine=set.union) == {1, 2, 3}
    assert fold(add, range(10), default=no_default2) == fold(add, range(10))
