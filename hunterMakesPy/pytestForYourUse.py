"""Pytest tests you can use in your package to test some hunterMakesPy functions.

Each function in this module returns a list of test functions that can be used with `pytest.parametrize`.

Note: These test functions are now in `hunterMakesPy.tests` with all other tests.
"""

from hunterMakesPy.tests.test_parseParameters import (
	PytestFor_defineConcurrencyLimit as PytestFor_defineConcurrencyLimit, PytestFor_intInnit as PytestFor_intInnit,
	PytestFor_oopsieKwargsie as PytestFor_oopsieKwargsie)
