"""Built-in containers named by their structure and by the kind of their values.

No consumer may mutate these containers: every test in a session shares each object.
"""
from __future__ import annotations

from typing import Any

listContainsItself: list[Any] = []
listContainsItself.append(listContainsItself)

lookupPrimesFewer: dict[str, list[int]] = {'NE': [11, 13], 'SW': [17]}
lookupPrimesMore: dict[str, list[int]] = {'NE': [19, 23, 13, 29, 11], 'SW': [31, 17, 37]}

boxOfLookupsIntText: tuple[dict[str, list[int | str]], ...] = ({'NE': [11, 'NE']},)
boxOfLookupsIntValues: tuple[dict[str, list[int]] | dict[str, int], ...] = (lookupPrimesFewer, {'NE': 23, 'NW': 29})
boxOfLookupsNested: tuple[dict[str, list[list[int]]], ...] = ({'NE': [[11], [13]]},)
boxOfLookupsPrimes: tuple[dict[str, list[int]], ...] = (lookupPrimesFewer, lookupPrimesMore)
boxOfLookupsServers: tuple[dict[str, list[str]], ...] = ({'servers': ['chicago']}, {'servers': ['tokyo', 'chicago']})
boxOfLookupsSets: tuple[dict[str, set[int]], ...] = ({'NE': {13, 11}}, {'NE': {17, 11}})
boxOfLookupsText: tuple[dict[str, str], dict[str, dict[str, int]]] = ({'NE': 'NE'}, {'NE': {'SW': 37}})
boxOfLookupsTupleRange: tuple[dict[str, tuple[int, ...]], dict[str, range]] = ({'NE': (11, 13)}, {'NE': range(17, 20)})
