# ruff: noqa D100, D103
from astToolkit import Be, Grab, NodeChanger, parsePathFilename2astModule
from astToolkit.transformationTools import write_astModule
from collections.abc import Callable, Iterable
from hunterMakesPy import PackageSettings, raiseIfNone
from hunterMakesPy.assimilate import settingsFor, settingsWrite_astModule
from pathlib import Path
from typing_extensions import TypeIs
import ast

def strStartsWith(identifierPackage: str) -> Callable[[str | None], TypeIs[str]]:
	def workhorse(node: str | None) -> TypeIs[str]:
		return isinstance(node, str) and (node.startswith(identifierPackage))
	return workhorse

def getPathFilenameInRelativeDirectory(settingsPackage: PackageSettings, relativePathTests: Path, filename: str) -> Path:
	pathFilename: Path = settingsPackage.pathPackage / relativePathTests / filename
	return pathFilename

def synchronizeFiles( settingsPackageSource: PackageSettings, settingsPackageDuplicate: PackageSettings, listFilenames: Iterable[str] = frozenset(), relativePathTests: Path = Path('tests'), ) -> None:
	for filename in listFilenames:
		astModule: ast.Module = parsePathFilename2astModule(getPathFilenameInRelativeDirectory(settingsPackageSource, relativePathTests, filename))

		NodeChanger(
			Be.ImportFrom.moduleIs(strStartsWith(settingsPackageSource.identifierPackage))
			, Grab.moduleAttribute(lambda node: raiseIfNone(node).replace(settingsPackageSource.identifierPackage, settingsPackageDuplicate.identifierPackage, 1))
		).visit(astModule)

		pathFilenameDuplicate: Path = getPathFilenameInRelativeDirectory(settingsPackageDuplicate, relativePathTests, filename)
		pathFilenameDuplicate.parent.mkdir(parents=True, exist_ok=True)
		write_astModule(astModule, pathFilenameDuplicate, settingsWrite_astModule)

if __name__ == '__main__':
	listFilenames: Iterable[str] = frozenset(('test_dicttoolz.py',))
	synchronizeFiles(settingsFor['humpy_toolz'], settingsFor['humpy_cytoolz'], listFilenames)
