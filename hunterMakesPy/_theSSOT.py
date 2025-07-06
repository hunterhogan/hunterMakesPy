"""Primary: settings for this package.

Secondary: settings for manufacturing.
Tertiary: hardcoded values until I implement a dynamic solution.
"""
from importlib import import_module as importlib_import_module
from importlib.util import find_spec
from inspect import getfile as inspect_getfile
from pathlib import Path
from tomli import loads as tomli_loads
import dataclasses
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from importlib.machinery import ModuleSpec

try:
	identifierPackagePACKAGING: str = tomli_loads(Path("pyproject.toml").read_text())["project"]["name"]
except Exception:  # noqa: BLE001
	identifierPackagePACKAGING = "hunterMakesPy"

def getPathPackageINSTALLING() -> Path:
    """Return the root directory of the installed package."""
    try:
        moduleSpecification: ModuleSpec | None = find_spec(identifierPackagePACKAGING)
        if moduleSpecification and moduleSpecification.origin:
            pathFilename = Path(moduleSpecification.origin)
            return pathFilename.parent if pathFilename.is_file() else pathFilename
    except ModuleNotFoundError:
        pass
    return Path.cwd()

@dataclasses.dataclass
class PackageSettings:
	fileExtension: str = dataclasses.field(default='.py', metadata={'evaluateWhen': 'installing'})
	"""Default file extension for generated code files."""
	identifierPackage: str = dataclasses.field(default = identifierPackagePACKAGING, metadata={'evaluateWhen': 'packaging'})
	"""Name of this package, used for import paths and configuration."""
	pathPackage: Path = dataclasses.field(default_factory=getPathPackageINSTALLING, metadata={'evaluateWhen': 'installing'})
	"""Absolute path to the installed package directory."""

settingsPackage = PackageSettings()
