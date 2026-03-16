import humpy_toolz

def test_tlz():
    import humpy_tlz
    humpy_tlz.curry
    humpy_tlz.functoolz.curry
    assert humpy_tlz.__package__ == 'humpy_tlz'
    assert humpy_tlz.__name__ == 'humpy_tlz'
    import humpy_tlz.curried
    assert humpy_tlz.curried.__package__ == 'humpy_tlz.curried'
    assert humpy_tlz.curried.__name__ == 'humpy_tlz.curried'
    humpy_tlz.curried.curry
    import humpy_tlz.curried.operator
    assert humpy_tlz.curried.operator.__package__ in (None, 'humpy_tlz.curried')
    assert humpy_tlz.curried.operator.__name__ == 'humpy_tlz.curried.operator'
    assert humpy_tlz.functoolz.__name__ == 'humpy_tlz.functoolz'
    m1 = humpy_tlz.functoolz
    import humpy_tlz.functoolz as m2
    assert m1 is m2
    import tlz.sandbox
    try:
        import tlzthisisabadname.curried
        1 / 0
    except ImportError:
        pass
    try:
        import tlz.curry
        1 / 0
    except ImportError:
        pass
    try:
        import tlz.badsubmodulename
        1 / 0
    except ImportError:
        pass
    assert humpy_toolz.__package__ == 'humpy_toolz'
    assert humpy_toolz.curried.__package__ == 'humpy_toolz.curried'
    assert humpy_toolz.functoolz.__name__ == 'humpy_toolz.functoolz'
    try:
        import cytoolz
        assert cytoolz.__package__ == 'cytoolz'
        assert cytoolz.curried.__package__ == 'cytoolz.curried'
        assert cytoolz.functoolz.__name__ == 'cytoolz.functoolz'
    except ImportError:
        pass
    if hasattr(humpy_tlz, '__file__'):
        assert humpy_tlz.__file__ == humpy_toolz.__file__
    if hasattr(humpy_tlz.functoolz, '__file__'):
        assert humpy_tlz.functoolz.__file__ == humpy_toolz.functoolz.__file__
    assert humpy_tlz.pipe is humpy_toolz.pipe
    assert 'humpy_tlz' in humpy_tlz.__doc__
    assert humpy_tlz.curried.__doc__ is not None
