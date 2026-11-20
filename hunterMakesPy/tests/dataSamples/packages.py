"""Package identifiers named by whether the test environment has the package installed."""
from __future__ import annotations

boxOfIdentifiersPackageAbsent: tuple[str, ...] = ('astToolkit', 'mapFolding')

lookupIdentifiersPackageInstalled: dict[str, str] = {
	'fractions': 'fractions',
	'hunterMakesPy': 'hunterMakesPy',
	'hunterMakesPyTests': 'hunterMakesPy.tests',
	'json': 'json',
}
