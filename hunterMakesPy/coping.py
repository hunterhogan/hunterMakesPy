"""Package configuration and defensive programming utilities for Python projects."""
from importlib.util import find_spec
from pathlib import Path
from tomllib import loads as tomllib_loads
from typing import TYPE_CHECKING, TypeVar
import dataclasses

if TYPE_CHECKING:
	from importlib.machinery import ModuleSpec

TypeSansNone = TypeVar('TypeSansNone')

def getIdentifierPackagePACKAGING(identifierPackageFALLBACK: str) -> str:
	"""Get package name from pyproject.toml or fallback to provided value."""
	try:
		return tomllib_loads(Path('pyproject.toml').read_text(encoding='utf-8'))['project']['name']
	except Exception:  # noqa: BLE001
		return identifierPackageFALLBACK

def getPathPackageINSTALLING(identifierPackage: str) -> Path:
	"""Return the root directory of the installed package."""
	try:
		moduleSpecification: ModuleSpec | None = find_spec(identifierPackage)
		if moduleSpecification and moduleSpecification.origin:
			pathFilename = Path(moduleSpecification.origin)
			return pathFilename.parent if pathFilename.is_file() else pathFilename
	except ModuleNotFoundError:
		pass
	return Path.cwd()

@dataclasses.dataclass
class PackageSettings:
	"""Configuration container for Python package metadata and runtime settings.

	This `class` provides a simple way to store and access basic information about a Python package, It will automatically resolve
	package identifiers and installation paths if they are not passed to the `class` constructor. Python `dataclasses` are easy to
	subtype and extend.

	Parameters
	----------
	identifierPackageFALLBACK : str = ''
		Fallback package identifier used only during initialization when automatic discovery fails.
	pathPackage : Path = Path()
		Absolute path to the installed package directory. Automatically resolved from `identifierPackage` if not provided.
	identifierPackage : str = ''
		Canonical name of the package. Automatically extracted from `pyproject.toml`.
	fileExtension : str = '.py'
		Default file extension.

	Examples
	--------
	Automatic package discovery from development environment:

	```python
	settings = PackageSettings(identifierPackageFALLBACK='cobraPy')
	# Automatically discovers package name from pyproject.toml
	# Resolves installation path from package identifier
	```

	Explicit configuration for specific deployment:

	```python
	settings = PackageSettings(
		identifierPackage='cobraPy',
		pathPackage=Path('/opt/tenEx/packages/cobraPy'),
		fileExtension='.pyx'
	)
	```

	"""

	identifierPackageFALLBACK: dataclasses.InitVar[str] = ''
	"""Fallback package identifier used during initialization only."""
	pathPackage: Path = dataclasses.field(default_factory=Path, metadata={'evaluateWhen': 'installing'})
	"""Absolute path to the installed package."""
	identifierPackage: str = dataclasses.field(default='', metadata={'evaluateWhen': 'packaging'})
	"""Name of this package."""
	fileExtension: str = dataclasses.field(default='.py', metadata={'evaluateWhen': 'installing'})
	"""Default file extension for files."""

	def __post_init__(self, identifierPackageFALLBACK: str) -> None:
		"""Initialize computed fields after dataclass initialization."""
		if not self.identifierPackage and identifierPackageFALLBACK:
			self.identifierPackage = getIdentifierPackagePACKAGING(identifierPackageFALLBACK)
		if self.pathPackage == Path() and self.identifierPackage:
			self.pathPackage = getPathPackageINSTALLING(self.identifierPackage)

def raiseIfNone(returnTarget: TypeSansNone | None, errorMessage: str | None = None) -> TypeSansNone:
	"""Raise a `ValueError` if the target value is `None`, otherwise return the value: tell the type checker that the return value is not `None`.

	(AI generated docstring)

	This is a defensive programming function that converts unexpected `None` values into explicit errors with context. It is useful for asserting that functions that might return `None` have actually returned a meaningful value.

	Parameters
	----------
	returnTarget : TypeSansNone | None
		The value to check for `None`. If not `None`, this value is returned unchanged.
	errorMessage : str | None = None
		Custom error message to include in the `ValueError`. If `None`, a default message with debugging hints is used.

	Returns
	-------
	returnTarget : TypeSansNone
		The original `returnTarget` value, guaranteed to not be `None`.

	Raises
	------
	ValueError
		If `returnTarget` is `None`.

	Examples
	--------
	Ensure a function result is not `None`:

	```python
	def findFirstMatch(listItems: list[str], pattern: str) -> str | None:
		for item in listItems:
			if pattern in item:
				return item
		return None

	listFiles = ['document.txt', 'image.png', 'data.csv']
	filename = raiseIfNone(findFirstMatch(listFiles, '.txt'))
	# Returns 'document.txt'
	```

	Handle dictionary lookups with custom error messages:

	```python
	configurationMapping = {'host': 'localhost', 'port': 8080}
	host = raiseIfNone(configurationMapping.get('host'),
					"Configuration must include 'host' setting")
	# Returns 'localhost'

	# This would raise ValueError with custom message:
	# database = raiseIfNone(configurationMapping.get('database'),
	#                       "Configuration must include 'database' setting")
	```

	Thanks
	------
	sobolevn, https://github.com/sobolevn, for the seed of the function. https://github.com/python/typing/discussions/1997#discussioncomment-13108399

	"""
	if returnTarget is None:
		message = errorMessage or 'A function unexpectedly returned `None`. Hint: look at the traceback immediately before `raiseIfNone`.'
		raise ValueError(message)
	return returnTarget
