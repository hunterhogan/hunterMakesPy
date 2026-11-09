"""Python source modules named by the state of their imports."""
from __future__ import annotations

sourceImportsUnsorted: str = (
	"import math\nimport collections\nfrom pathlib import PurePosixPath\n\n"
	"primes = collections.Counter([2, 3, 3, 5])\nnorth = PurePosixPath('north')\ntau = math.tau\n"
)
sourceImportsUnused: str = 'import sys\nimport os\nimport math\n\nfibonacci = 13\n'
sourceImportsUnusedThirdParty: str = 'import numpy\nimport math\n\nfibonacci = 21\n'
sourceImportsUsed: str = 'import math\n\nprimeGCD = math.gcd(221, 323)\n'
