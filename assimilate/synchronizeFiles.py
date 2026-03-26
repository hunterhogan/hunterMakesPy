# ruff: noqa D100, D103
from assimilate import settingsFor, settingsWrite_astModule
from astToolkit import Be, Grab, NodeChanger, parsePathFilename2astModule
from astToolkit.transformationTools import write_astModule
from hunterMakesPy import PackageSettings
from pathlib import Path

listFilenames = frozenset(('test_dicttoolz.py',))


def isImportedModuleWithinPackage(identifierImportedModule: str | None, identifierPackage: str) -> bool:
	isWithinPackage: bool = bool(identifierImportedModule) and (
		identifierImportedModule == identifierPackage
		or identifierImportedModule.startswith(f'{identifierPackage}.')
	)
	return isWithinPackage


def replaceImportedPackagePrefix(identifierImportedModule: str, identifierPackageSource: str, identifierPackageDuplicate: str) -> str:
	identifierPackageSourceWithSeparator: str = f'{identifierPackageSource}.'
	identifierImportedModuleRewritten: str = identifierImportedModule
	if identifierImportedModule == identifierPackageSource:
		identifierImportedModuleRewritten = identifierPackageDuplicate
	elif identifierImportedModule.startswith(identifierPackageSourceWithSeparator):
		identifierImportedModuleRewritten = (
			f'{identifierPackageDuplicate}.{identifierImportedModule.removeprefix(identifierPackageSourceWithSeparator)}'
		)
	return identifierImportedModuleRewritten


def changeImportedPackageIdentifier(astModule, settingsPackageSource: PackageSettings, settingsPackageDuplicate: PackageSettings) -> None:
	identifierPackageSource: str = settingsPackageSource.identifierPackage
	identifierPackageDuplicate: str = settingsPackageDuplicate.identifierPackage

	changeImportFrom = NodeChanger(
		Be.ImportFrom.moduleIs(lambda identifierImportedModule: isImportedModuleWithinPackage(identifierImportedModule, identifierPackageSource)),
		Grab.moduleAttribute(
			lambda identifierImportedModule: replaceImportedPackagePrefix(
				identifierImportedModule,
				identifierPackageSource,
				identifierPackageDuplicate,
			)
		),
	)
	changeImportFrom.visit(astModule)

	changeImport = NodeChanger(
		Be.alias.nameIs(lambda identifierImportedModule: isImportedModuleWithinPackage(identifierImportedModule, identifierPackageSource)),
		Grab.nameAttribute(
			lambda identifierImportedModule: replaceImportedPackagePrefix(
				identifierImportedModule,
				identifierPackageSource,
				identifierPackageDuplicate,
			)
		),
	)
	changeImport.visit(astModule)


def getPathFilenameInRelativeDirectory(settingsPackage: PackageSettings, pathRelativeDirectory: Path, filename: str) -> Path:
	pathFilename: Path = settingsPackage.pathPackage / pathRelativeDirectory / filename
	return pathFilename


def synchronizeFiles(
	settingsPackageSource: PackageSettings,
	settingsPackageDuplicate: PackageSettings,
	filenames: frozenset[str] = listFilenames,
	pathRelativeDirectory: Path = Path('tests'),
) -> None:
	for filename in filenames:
		pathFilenameSource: Path = getPathFilenameInRelativeDirectory(settingsPackageSource, pathRelativeDirectory, filename)
		pathFilenameDuplicate: Path = getPathFilenameInRelativeDirectory(settingsPackageDuplicate, pathRelativeDirectory, filename)
		pathFilenameDuplicate.parent.mkdir(parents=True, exist_ok=True)
		astModule = parsePathFilename2astModule(pathFilenameSource)
		changeImportedPackageIdentifier(astModule, settingsPackageSource, settingsPackageDuplicate)
		write_astModule(astModule, pathFilenameDuplicate, settingsWrite_astModule)


if __name__ == '__main__':
	synchronizeFiles(settingsFor['humpy_toolz'], settingsFor['humpy_cytoolz'])
