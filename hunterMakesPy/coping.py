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
			pathFilename: Path = Path(moduleSpecification.origin)
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

	Attributes
	----------
	identifierPackageFALLBACK : str = ''
		Fallback package identifier used only during initialization when automatic discovery fails.
	identifierPackage : str = ''
		Canonical name of the package. Automatically extracted from "pyproject.toml".
	pathPackage : Path = getPathPackageINSTALLING(identifierPackage)
		Absolute path to the installed package directory. Automatically resolved from `identifierPackage` if not provided.
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

def raiseIfNone(expression: TypeSansNone | None, errorMessage: str | None = None) -> TypeSansNone:
	"""Convert the `expression` return annotation from '`cerPytainty | None`' to '`cerPytainty`' because `expression` cannot be `None`; `raise` an `Exception` if you're wrong.

	The Python interpreter evaluates `expression` to a value: think of a function call or an attribute access. You can use
	`raiseIfNone` for fail early defensive programming. I use it, however, to cure type-checker-nihilism: that's when "or `None`"
	return types cause your type checker to repeatedly say, "You can't do that because the value might be `None`."

	Parameters
	----------
	expression : TypeSansNone | None
		Python code with a return type that is a `union` of `None` and `TypeSansNone`, which is a stand-in for one or more other types.
	errorMessage : str | None = 'A function unexpectedly returned `None`. Hint: look at the traceback immediately before `raiseIfNone`.'
		Custom error message for the `ValueError` `Exception` if `expression` is `None`.

	Returns
	-------
	contentment : TypeSansNone
		The value returned by `expression`, but guaranteed to not be `None`.

	Raises
	------
	ValueError
		If the value returned by `expression` is `None`.

	Examples
	--------
	Basic usage with attribute access:
	```python
	annotation = raiseIfNone(ast_arg.annotation)
	# Raises ValueError if ast_arg.annotation is None
	```

	Function return value validation:
	```python
	def findFirstMatch(listItems: list[str], pattern: str) -> str | None:
		for item in listItems:
			if pattern in item:
				return item
		return None

	listFiles = ['document.txt', 'image.png', 'data.csv']
	filename = raiseIfNone(findFirstMatch(listFiles, '.txt'))
	# Returns 'document.txt' when match exists
	```

	Dictionary value retrieval with custom message:
	```python
	configurationMapping = {'host': 'localhost', 'port': 8080}
	host = raiseIfNone(configurationMapping.get('host'),
					"Configuration must include 'host' setting")
	# Returns 'localhost' when key exists

	# This would raise ValueError with custom message:
	# database = raiseIfNone(configurationMapping.get('database'),
	#                      "Configuration must include 'database' setting")
	```

	Thanks
	------
	sobolevn, https://github.com/sobolevn, for the seed of this function. https://github.com/python/typing/discussions/1997#discussioncomment-13108399

	"""
	if expression is None:
		message: str = errorMessage or 'A function unexpectedly returned `None`. Hint: look at the traceback immediately before `raiseIfNone`.'
		raise ValueError(message)
	return expression
