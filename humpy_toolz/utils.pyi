from collections.abc import Callable

def raises(err: type[Exception], lamda: Callable[[], None]) -> bool: ...

no_default = "__no__default__"
