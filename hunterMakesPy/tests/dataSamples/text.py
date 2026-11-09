"""Text named by script and content.

No text contains a carriage return: `Path.write_text` translates newlines on Windows, so a carriage return would not survive
a write-and-read round trip through the platform's text mode.
"""
from __future__ import annotations

from typing import TYPE_CHECKING
import pytest

if TYPE_CHECKING:
	from _pytest.mark.structures import ParameterSet

textASCIIPrimes: str = '2 3 5 7 11 13 17'
textEastAsianCities: str = '北京\t東京\t서울'
textGreekCities: str = 'Αθήνα\nΣπάρτη\nΚόρινθος\n'  # ruff: ignore[ambiguous-unicode-character-string]

boxOfTexts: tuple[ParameterSet, ...] = (
	pytest.param(textASCIIPrimes, id='textASCIIPrimes'),
	pytest.param(textEastAsianCities, id='textEastAsianCities'),
	pytest.param(textGreekCities, id='textGreekCities'),
)
"""Every text: the full domain of a contract over text."""
