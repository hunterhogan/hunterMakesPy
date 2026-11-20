"""Text named by script and content.

No text contains a carriage return: `Path.write_text` translates newlines on Windows, so a carriage return would not survive
a write-and-read round trip through the platform's text mode.
"""
from __future__ import annotations

textASCIIPrimes: str = '2 3 5 7 11 13 17'
textEastAsianCities: str = '北京\t東京\t서울'
textGreekCities: str = 'Αθήνα\nΣπάρτη\nΚόρινθος\n'
