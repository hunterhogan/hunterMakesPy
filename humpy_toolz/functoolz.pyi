import collections.abc
import functools
import inspect
import typing

__all__ = (
    "apply",
    "complement",
    "compose",
    "compose_left",
    "curry",
    "do",
    "excepts",
    "flip",
    "identity",
    "juxt",
    "memoize",
    "pipe",
    "thread_first",
    "thread_last",
)
PYPY = bool

### Internal type stubs
_T = typing.TypeVar("_T")
_Instance = typing.TypeVar("_Instance")
type _Getter[_Instance, _T] = typing.Callable[[_Instance], _T]
type _Setter[_Instance, _T] = typing.Callable[[_Instance, _T], None]
type _Deleter[_Instance] = typing.Callable[[_Instance], None]
type _InstancePropertyState[_Instance, _T] = tuple[
    _Getter[_Instance, _T] | None,
    _Setter[_Instance, _T] | None,
    _Deleter[_Instance] | None,
    str | None,
    _T | None,
]

### Toolz

def identity[T](x: T) -> T:
    """Identity function. Return x

    >>> identity(3)
    3
    """

def apply[**P, T](func: typing.Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
    """Applies a function and returns the results

    >>> def double(x): return 2*x
    >>> def inc(x):    return x + 1
    >>> apply(double, 5)
    10

    >>> tuple(map(apply, [double, inc, double], [10, 500, 8000]))
    (20, 501, 16000)
    """

def thread_first[T, R](
    val: T, *forms: typing.Callable[[T], R] | tuple[typing.Callable[..., R], typing.Any]
) -> R:
    """Thread value through a sequence of functions/forms

    >>> def double(x): return 2*x
    >>> def inc(x):    return x + 1
    >>> thread_first(1, inc, double)
    4

    If the function expects more than one input you can specify those inputs
    in a tuple.  The value is used as the first input.

    >>> def add(x, y): return x + y
    >>> def pow(x, y): return x**y
    >>> thread_first(1, (add, 4), (pow, 2))  # pow(add(1, 4), 2)
    25

    So in general
        thread_first(x, f, (g, y, z))
    expands to
        g(f(x), y, z)

    See Also
    --------
        thread_last
    """

def thread_last[T, U](
    val: T, *forms: typing.Callable[[T], U] | tuple[typing.Callable[..., U]]
) -> U:
    """Thread value through a sequence of functions/forms

    >>> def double(x): return 2*x
    >>> def inc(x):    return x + 1
    >>> thread_last(1, inc, double)
    4

    If the function expects more than one input you can specify those inputs
    in a tuple.  The value is used as the last input.

    >>> def add(x, y): return x + y
    >>> def pow(x, y): return x**y
    >>> thread_last(1, (add, 4), (pow, 2))  # pow(2, add(4, 1))
    32

    So in general
        thread_last(x, f, (g, y, z))
    expands to
        g(y, z, f(x))

    >>> def iseven(x):
    ...     return x % 2 == 0
    >>> list(thread_last([1, 2, 3], (map, inc), (filter, iseven)))
    [2, 4]

    See Also
    --------
        thread_first
    """

class InstanceProperty[Instance, T](property):
    """Like @property, but returns ``classval`` when used as a class attribute

    Should not be used directly.  Use ``instanceproperty`` instead.
    """
    def __init__(
        self,
        fget: _Getter[_Instance, _T] | None = None,
        fset: _Setter[_Instance, _T] | None = None,
        fdel: _Deleter[_Instance] | None = None,
        doc: str | None = None,
        classval: _T | None = None,
    ) -> None: ...
    @typing.overload
    def __get__(self, obj: None, type: type | None = ...) -> _T | None: ...
    @typing.overload
    def __get__(self, obj: _Instance, type: type | None = ...) -> _T: ...
    @typing.override
    def __get__(self, obj: _Instance | None, type: type | None = None) -> _T | None: ...
    @typing.override
    def __reduce__(
        self,
    ) -> tuple[type[InstanceProperty], _InstancePropertyState]:  # pyright: ignore[reportMissingTypeArgument]
        # TODO figure out how to type this correctly
        ...

@typing.overload
def instanceproperty(
    fget: _Getter[_Instance, _T],
    fset: _Setter[_Instance, _T] | None = ...,
    fdel: _Deleter[_Instance] | None = ...,
    doc: str | None = ...,
    classval: _T | None = ...,
) -> InstanceProperty[_Instance, _T]: ...
@typing.overload
def instanceproperty(
    fget: typing.Literal[None] | None = None,
    fset: _Setter[_Instance, _T] | None = ...,  # pyright: ignore[reportInvalidTypeVarUse]
    fdel: _Deleter[_Instance] | None = ...,
    doc: str | None = ...,
    classval: _T | None = ...,
) -> typing.Callable[[_Getter[_Instance, _T]], InstanceProperty[_Instance, _T]]: ...
def instanceproperty(
    fget: _Getter[_Instance, _T] | None = None,
    fset: _Setter[_Instance, _T] | None = None,
    fdel: _Deleter[_Instance] | None = None,
    doc: str | None = None,
    classval: _T | None = None,
) -> (
    InstanceProperty[_Instance, _T]
    | typing.Callable[[_Getter[_Instance, _T]], InstanceProperty[_Instance, _T]]
):
    """Like @property, but returns ``classval`` when used as a class attribute

    >>> class MyClass(object):
    ...     '''The class docstring'''
    ...     @instanceproperty(classval=__doc__)
    ...     def __doc__(self):
    ...         return 'An object docstring'
    ...     @instanceproperty
    ...     def val(self):
    ...         return 42
    ...
    >>> MyClass.__doc__
    'The class docstring'
    >>> MyClass.val is None
    True
    >>> obj = MyClass()
    >>> obj.__doc__
    'An object docstring'
    >>> obj.val
    42
    """

_CurryState = tuple

class curry[**P, T]:
    """Curry a callable function

    Enables partial application of arguments through calling a function with an
    incomplete set of arguments.

    >>> def mul(x, y):
    ...     return x * y
    >>> mul = curry(mul)

    >>> double = mul(2)
    >>> double(10)
    20

    Also supports keyword arguments

    >>> @curry                  # Can use curry as a decorator
    ... def f(x, y, a=10):
    ...     return a * (x + y)

    >>> add = f(a=1)
    >>> add(2, 3)
    5

    See Also
    --------
        toolz.curried - namespace of curried functions
                        https://toolz.readthedocs.io/en/latest/curry.html
    """
    def __init__(
        self,
        func: curry[P, T] | functools.partial[T] | typing.Callable[P, T],
        /,  # Must be positional-only
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> None: ...
    @instanceproperty
    def func(self) -> typing.Callable[P, T]: ...
    @instanceproperty
    def __signature__(self) -> inspect.Signature: ...
    @instanceproperty
    def args(self) -> tuple[typing.Any, ...]: ...
    @instanceproperty
    def keywords(self) -> dict[str, typing.Any]: ...
    @instanceproperty
    def func_name(self) -> str: ...
    @typing.override
    def __hash__(self) -> int: ...
    @typing.override
    def __eq__(self, other: object) -> bool: ...
    @typing.override
    def __ne__(self, other: object) -> bool: ...
    @typing.overload
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T: ...
    @typing.overload
    def __call__(
        self, *args: typing.Any, **kwargs: typing.Any
    ) -> functools.partial[T]: ...
    def bind(self, *args: typing.Any, **kwargs: typing.Any) -> curry[P, T]: ...
    def call(self, *args: typing.Any, **kwargs: typing.Any) -> T: ...
    def __get__(self, instance: object, owner: type) -> curry[P, T]: ...
    @typing.override
    def __reduce__(
        self,
    ) -> tuple[typing.Callable[..., T], _CurryState]: ...

@curry
def memoize[T](
    func: typing.Callable[..., T],
    cache: dict[typing.Any, T] | None = None,
    key: typing.Callable[
        [tuple[typing.Any, ...], collections.abc.Mapping[str, typing.Any]], typing.Any
    ]
    | None = None,
) -> typing.Callable[..., T]:
    """Cache a function's result for speedy future evaluation

    Considerations:
        Trades memory for speed.
        Only use on pure functions.

    >>> def add(x, y):  return x + y
    >>> add = memoize(add)

    Or use as a decorator

    >>> @memoize
    ... def add(x, y):
    ...     return x + y

    Use the ``cache`` keyword to provide a dict-like object as an initial cache

    >>> @memoize(cache={(1, 2): 3})
    ... def add(x, y):
    ...     return x + y

    Note that the above works as a decorator because ``memoize`` is curried.

    It is also possible to provide a ``key(args, kwargs)`` function that
    calculates keys used for the cache, which receives an ``args`` tuple and
    ``kwargs`` dict as input, and must return a hashable value.  However,
    the default key function should be sufficient most of the time.

    >>> # Use key function that ignores extraneous keyword arguments
    >>> @memoize(key=lambda args, kwargs: args)
    ... def add(x, y, verbose=False):
    ...     if verbose:
    ...         print('Calculating %s + %s' % (x, y))
    ...     return x + y
    """

@typing.overload
def compose[**P, T](fn_0: typing.Callable[P, T]) -> typing.Callable[P, T]: ...
@typing.overload
def compose[**P, T0, T1](
    fn_0: typing.Callable[[T0], T1], fn_1: typing.Callable[P, T0]
) -> typing.Callable[P, T1]: ...
@typing.overload
def compose[**P, T0, T1, T2](
    fn_0: typing.Callable[[T1], T2],
    fn_1: typing.Callable[[T0], T1],
    fn_2: typing.Callable[P, T0],
) -> typing.Callable[P, T2]: ...
@typing.overload
def compose[**P, T0, T1, T2, T3](
    fn_0: typing.Callable[[T2], T3],
    fn_1: typing.Callable[[T1], T2],
    fn_2: typing.Callable[[T0], T1],
    fn_3: typing.Callable[P, T0],
) -> typing.Callable[P, T3]: ...
@typing.overload
def compose[**P, T0, T1, T2, T3, T4](
    fn_0: typing.Callable[[T3], T4],
    fn_1: typing.Callable[[T2], T3],
    fn_2: typing.Callable[[T1], T2],
    fn_3: typing.Callable[[T0], T1],
    fn_4: typing.Callable[P, T0],
) -> typing.Callable[P, T4]: ...
@typing.overload
def compose[**P, T0, T1, T2, T3, T4, T5](
    fn_0: typing.Callable[[T4], T5],
    fn_1: typing.Callable[[T3], T4],
    fn_2: typing.Callable[[T2], T3],
    fn_3: typing.Callable[[T1], T2],
    fn_4: typing.Callable[[T0], T1],
    fn_5: typing.Callable[P, T0],
) -> typing.Callable[P, T5]: ...
@typing.overload
def compose(
    *funcs: typing.Callable[..., typing.Any],
) -> typing.Callable[..., typing.Any]: ...
def compose(
    *funcs: typing.Callable[..., typing.Any],
) -> typing.Callable[..., typing.Any]:
    """Compose functions to operate in series.

    Returns a function that applies other functions in sequence.

    Functions are applied from right to left so that
    ``compose(f, g, h)(x, y)`` is the same as ``f(g(h(x, y)))``.

    If no arguments are provided, the identity function (f(x) = x) is returned.

    >>> inc = lambda i: i + 1
    >>> compose(str, inc)(3)
    '4'

    See Also
    --------
        compose_left
        pipe
    """

@typing.overload
def compose_left[**P, T](fn_0: typing.Callable[P, T]) -> typing.Callable[P, T]: ...
@typing.overload
def compose_left[**P, T0, T1](
    fn_0: typing.Callable[P, T0], fn_1: typing.Callable[[T0], T1]
) -> typing.Callable[P, T1]: ...
@typing.overload
def compose_left[**P, T0, T1, T2](
    fn_0: typing.Callable[P, T0],
    fn_1: typing.Callable[[T0], T1],
    fn_2: typing.Callable[[T1], T2],
) -> typing.Callable[P, T2]: ...
@typing.overload
def compose_left[**P, T0, T1, T2, T3](
    fn_0: typing.Callable[P, T0],
    fn_1: typing.Callable[[T0], T1],
    fn_2: typing.Callable[[T1], T2],
    fn_3: typing.Callable[[T2], T3],
) -> typing.Callable[P, T3]: ...
@typing.overload
def compose_left[**P, T0, T1, T2, T3, T4](
    fn_0: typing.Callable[P, T0],
    fn_1: typing.Callable[[T0], T1],
    fn_2: typing.Callable[[T1], T2],
    fn_3: typing.Callable[[T2], T3],
    fn_4: typing.Callable[[T3], T4],
) -> typing.Callable[P, T4]: ...
@typing.overload
def compose_left[**P, T0, T1, T2, T3, T4, T5](
    fn_0: typing.Callable[P, T0],
    fn_1: typing.Callable[[T0], T1],
    fn_2: typing.Callable[[T1], T2],
    fn_3: typing.Callable[[T2], T3],
    fn_4: typing.Callable[[T3], T4],
    fn_5: typing.Callable[[T4], T5],
) -> typing.Callable[P, T5]: ...
@typing.overload
def compose_left(
    *funcs: typing.Callable[..., typing.Any],
) -> typing.Callable[..., typing.Any]: ...
def compose_left(
    *funcs: typing.Callable[..., typing.Any],
) -> typing.Callable[..., typing.Any]:
    """Compose functions to operate in series.

    Returns a function that applies other functions in sequence.

    Functions are applied from left to right so that
    ``compose_left(f, g, h)(x, y)`` is the same as ``h(g(f(x, y)))``.

    If no arguments are provided, the identity function (f(x) = x) is returned.

    >>> inc = lambda i: i + 1
    >>> compose_left(inc, str)(3)
    '4'

    See Also
    --------
        compose
        pipe
    """

@typing.overload
def pipe[T0, T1](
    data: T0,
    fn_0: typing.Callable[[T0], T1],
) -> T1: ...
@typing.overload
def pipe[T0, T1, T2](
    data: T0,
    fn_0: typing.Callable[[T0], T1],
    fn_1: typing.Callable[[T1], T2],
) -> T2: ...
@typing.overload
def pipe[T0, T1, T2, T3](
    data: T0,
    fn_0: typing.Callable[[T0], T1],
    fn_1: typing.Callable[[T1], T2],
    fn_2: typing.Callable[[T2], T3],
) -> T3: ...
@typing.overload
def pipe[T0, T1, T2, T3, T4](
    data: T0,
    fn_0: typing.Callable[[T0], T1],
    fn_1: typing.Callable[[T1], T2],
    fn_2: typing.Callable[[T2], T3],
    fn_3: typing.Callable[[T3], T4],
) -> T4: ...
@typing.overload
def pipe[T0, T1, T2, T3, T4, T5](
    data: T0,
    fn_0: typing.Callable[[T0], T1],
    fn_1: typing.Callable[[T1], T2],
    fn_2: typing.Callable[[T2], T3],
    fn_3: typing.Callable[[T3], T4],
    fn_4: typing.Callable[[T4], T5],
) -> T5: ...
@typing.overload
def pipe[T0, T1, T2, T3, T4, T5, T6](
    data: T0,
    fn_0: typing.Callable[[T0], T1],
    fn_1: typing.Callable[[T1], T2],
    fn_2: typing.Callable[[T2], T3],
    fn_3: typing.Callable[[T3], T4],
    fn_4: typing.Callable[[T4], T5],
    fn_5: typing.Callable[[T5], T6],
) -> T6: ...
@typing.overload
def pipe(data: typing.Any, *funcs: typing.Callable[..., typing.Any]) -> typing.Any: ...
def pipe(data: typing.Any, *funcs: typing.Callable[..., typing.Any]) -> typing.Any:
    """Pipe a value through a sequence of functions

    I.e. ``pipe(data, f, g, h)`` is equivalent to ``h(g(f(data)))``

    We think of the value as progressing through a pipe of several
    transformations, much like pipes in UNIX

    ``$ cat data | f | g | h``

    >>> double = lambda i: 2 * i
    >>> pipe(3, double, str)
    '6'

    See Also
    --------
        compose
        compose_left
        thread_first
        thread_last
    """

def complement[**P](func: typing.Callable[P, bool]) -> typing.Callable[P, bool]:
    """Convert a predicate function to its logical complement.

    In other words, return a function that, for inputs that normally
    yield True, yields False, and vice-versa.

    >>> def iseven(n): return n % 2 == 0
    >>> isodd = complement(iseven)
    >>> iseven(2)
    True
    >>> isodd(2)
    False
    """

@typing.overload
def juxt() -> typing.Callable[..., tuple[()]]: ...
@typing.overload
def juxt[**P, T0](
    fn_0: typing.Callable[P, T0],
) -> typing.Callable[P, tuple[T0]]: ...
@typing.overload
def juxt[**P, T0, T1](
    fn_0: typing.Callable[P, T0],
    fn_1: typing.Callable[P, T1],
) -> typing.Callable[P, tuple[T0, T1]]: ...
@typing.overload
def juxt[**P, T0, T1, T2](
    fn_0: typing.Callable[P, T0],
    fn_1: typing.Callable[P, T1],
    fn_2: typing.Callable[P, T2],
) -> typing.Callable[P, tuple[T0, T1, T2]]: ...
@typing.overload
def juxt[**P, T0, T1, T2, T3](
    fn_0: typing.Callable[P, T0],
    fn_1: typing.Callable[P, T1],
    fn_2: typing.Callable[P, T2],
    fn_3: typing.Callable[P, T3],
) -> typing.Callable[P, tuple[T0, T1, T2, T3]]: ...
@typing.overload
def juxt[**P, T0, T1, T2, T3, T4](
    fn_0: typing.Callable[P, T0],
    fn_1: typing.Callable[P, T1],
    fn_2: typing.Callable[P, T2],
    fn_3: typing.Callable[P, T3],
    fn_4: typing.Callable[P, T4],
) -> typing.Callable[P, tuple[T0, T1, T2, T3, T4]]: ...
@typing.overload
def juxt[**P, T0, T1, T2, T3, T4, T5](
    fn_0: typing.Callable[P, T0],
    fn_1: typing.Callable[P, T1],
    fn_2: typing.Callable[P, T2],
    fn_3: typing.Callable[P, T3],
    fn_4: typing.Callable[P, T4],
    fn_5: typing.Callable[P, T5],
) -> typing.Callable[P, tuple[T0, T1, T2, T3, T4, T5]]: ...
@typing.overload
def juxt[**P, T](
    funcs: collections.abc.Iterable[typing.Callable[P, T]],
) -> typing.Callable[P, tuple[T, ...]]: ...
@typing.overload
def juxt[**P, T](
    *funcs: typing.Callable[P, T],
) -> typing.Callable[P, tuple[T, ...]]: ...
def juxt[**P, T](
    *funcs: typing.Callable[P, T] | collections.abc.Iterable[typing.Callable[P, T]],
) -> typing.Callable[P, tuple[T, ...]]:
    """Creates a function that calls several functions with the same arguments

    Takes several functions and returns a function that applies its arguments
    to each of those functions then returns a tuple of the results.

    Name comes from juxtaposition: the fact of two things being seen or placed
    close together with contrasting effect.

    >>> inc = lambda x: x + 1
    >>> double = lambda x: x * 2
    >>> juxt(inc, double)(10)
    (11, 20)
    >>> juxt([inc, double])(10)
    (11, 20)
    """

def do[T](func: typing.Callable[[T], typing.Any], x: T) -> T:
    """Runs ``func`` on ``x``, returns ``x``

    Because the results of ``func`` are not returned, only the side
    effects of ``func`` are relevant.

    Logging functions can be made by composing ``do`` with a storage function
    like ``list.append`` or ``file.write``

    >>> from toolz import compose
    >>> from toolz.curried import do

    >>> log = []
    >>> inc = lambda x: x + 1
    >>> inc = compose(inc, do(log.append))
    >>> inc(1)
    2
    >>> inc(11)
    12
    >>> log
    [1, 11]
    """

@curry
def flip[T, U, R](func: typing.Callable[[T, U], R], a: U, b: T) -> R:
    """Call the function call with the arguments flipped

    This function is curried.

    >>> def div(a, b):
    ...     return a // b
    ...
    >>> flip(div, 2, 6)
    3
    >>> div_by_two = flip(div, 2)
    >>> div_by_two(4)
    2

    This is particularly useful for built in functions and functions defined
    in C extensions that accept positional only arguments. For example:
    isinstance, issubclass.

    >>> data = [1, 'a', 'b', 2, 1.5, object(), 3]
    >>> only_ints = list(filter(flip(isinstance, int), data))
    >>> only_ints
    [1, 2, 3]
    """

class excepts[T, **P]:
    """A wrapper around a function to catch exceptions and
    dispatch to a handler.

    This is like a functional try/except block, in the same way that
    ifexprs are functional if/else blocks.

    Examples
    --------
    >>> excepting = excepts(
    ...     ValueError,
    ...     lambda a: [1, 2].index(a),
    ...     lambda _: -1,
    ... )
    >>> excepting(1)
    0
    >>> excepting(3)
    -1

    Multiple exceptions and default except clause.

    >>> excepting = excepts((IndexError, KeyError), lambda a: a[0])
    >>> excepting([])
    >>> excepting([1])
    1
    >>> excepting({})
    >>> excepting({0: 1})
    1
    """
    def __init__(
        self,
        exc: type[Exception] | tuple[type[Exception], ...],
        func: typing.Callable[P, T],
        handler: typing.Callable[[Exception], T] | None = None,
    ) -> None: ...
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T: ...
    @property
    def __name__(self) -> str: ...
