"""Transform toolz."""
from astToolkit import Be, Grab, IfThis, Make, NodeChanger, parsePathFilename2astModule, Then
from astToolkit.transformationTools import write_astModule
from functools import partial
from humpy_toolz.functoolz import flip
from hunterMakesPy import identifierDotAttribute, PackageSettings, settingsPackage
from hunterMakesPy.filesystemToolkit import settings_autoflakeDEFAULT, settings_isortDEFAULT, writeStringToHere
from operator import contains, eq as equalTo, methodcaller
from pathlib import Path
from typing import Any
import ast

#======== Settings for the packages to be created ========

# TODO I don't know how to move this code block to a separate file in the same directory and import the symbols from the file. It
# seems pretty basic, and I feel pretty stupid. I would normally create "_theSSOT.py" for these settings and re-export the symbols
# through "__init__.py". More generally, I don't know how to divide this "sub-package", which is lateral to "hunterMakesPy", into
# a namespace with multiple modules.
Z0Z_notice: str = "Some of the work in this directory and its subdirectories may be protected by \nthe following copyright.\n___\n\n"

amIHavingFunYet: ast.Assign = Make.Assign([Make.Name('__version__', Make.Store())], Make.Constant('1.1.0'))

settings: dict[str, PackageSettings] = {}
allTransformeePackages: tuple[str, ...] = ('toolz', 'tlz')

getOtherName: dict[str, str] = {}
for identifierTransformee in allTransformeePackages:
	humpyPackage: str = f"humpy_{identifierTransformee}"
	getOtherName[identifierTransformee] = humpyPackage
	getOtherName[humpyPackage] = identifierTransformee

settingsWrite_astModule: dict[str, dict[str, Any]] = {'isort': settings_isortDEFAULT, 'autoflake': settings_autoflakeDEFAULT}
settingsWrite_astModule['autoflake']['remove_all_unused_imports'] = False
settingsWrite_astModule['autoflake']['ignore_init_module_imports'] = True

#======== Ingest and transform external packages and files ========

subModules: frozenset[identifierDotAttribute] = frozenset(('', '._signatures', '.compatibility', '.curried', '.curried.exceptions', '.curried.operator', '.dicttoolz', '.functoolz', '.itertoolz', '.recipes', '.sandbox', '.sandbox.core', '.sandbox.parallel', '.utils'))

transformAllHere: list[tuple[Path, str, str]] = []
for identifierTransformee in allTransformeePackages:
	transformAllHere.append((Path(f'/clones/toolz/{identifierTransformee}'), identifierTransformee, getOtherName[identifierTransformee]))  # noqa: PERF401

for pathTransformee, _identifierTransformee, humpyPackage in transformAllHere:
	settings[humpyPackage] = PackageSettings(identifierPackage=humpyPackage, pathPackage=(settingsPackage.pathPackage.parent / humpyPackage))
	settings[humpyPackage].pathPackage.mkdir(parents=True, exist_ok=True)
	writeStringToHere(Z0Z_notice + (pathTransformee.parent / 'LICENSE.txt').read_text(encoding='utf-8'), settings[humpyPackage].pathPackage / 'Notice_of_Copyright.txt')

for identifierTransformee in allTransformeePackages:
	for humpyPackage, settings_humpyPackage in settings.items():
		transformAllHere.append((settings_humpyPackage.pathPackage, identifierTransformee, humpyPackage))

for pathTransformee, identifierTransformee, humpyPackage in transformAllHere:
	for pathRoot, listDirectories, listFilenames in pathTransformee.walk():
		if '__pycache__' in listDirectories:
			listDirectories.remove('__pycache__')
		for directory in listDirectories:
			(settings[humpyPackage].pathPackage / directory).mkdir(parents=True, exist_ok=True)

		for filename in filter(lambda filename: filename.endswith(settings[humpyPackage].fileExtension), listFilenames):
			pathFilename: Path = pathRoot / filename
			astModule: ast.Module = parsePathFilename2astModule(pathFilename)

			for identifierModule in subModules:
				changeImportFrom = NodeChanger(Be.ImportFrom.moduleIs(partial(equalTo, identifierTransformee+identifierModule)), Grab.moduleAttribute(Then.replaceWith(getOtherName[identifierTransformee]+identifierModule)))
				changeImportFrom.visit(astModule)

				changeImport = NodeChanger(Be.alias.nameIs(partial(equalTo, identifierTransformee+identifierModule)), Grab.nameAttribute(Then.replaceWith(getOtherName[identifierTransformee]+identifierModule)))
				changeImport.visit(astModule)

				changeConstant = NodeChanger(IfThis.isConstant_value(identifierTransformee+identifierModule), Then.replaceWith(Make.Constant(getOtherName[identifierTransformee]+identifierModule)))
				changeConstant.visit(astModule)

			stringOld: identifierDotAttribute = f"`{identifierTransformee}`"
# FIXME Up to 6 errors on this line are due to lack of TYPE ANNOTATIONS for `humpy_toolz.flip`. Create code to add annotations, and the errors will instantly disappear!
			changeBacktickIdentifierInConstant=NodeChanger(IfThis.isAllOf(Be.Constant.valueIs(partial(flip(isinstance), str)), Be.Constant.valueIs(partial(flip(contains), stringOld))), Grab.valueAttribute(methodcaller('replace', stringOld, f"`{getOtherName[identifierTransformee]}`")))
			changeBacktickIdentifierInConstant.visit(astModule)

			changeName = NodeChanger(IfThis.isNameIdentifier(identifierTransformee), Grab.idAttribute(Then.replaceWith(getOtherName[identifierTransformee])))
			changeName.visit(astModule)

			write_astModule(astModule, settings[humpyPackage].pathPackage / pathFilename.relative_to(pathTransformee), settingsWrite_astModule)

#======== Post-transformation: acting on the new package ========

pathFilename = settings['humpy_toolz'].pathPackage / '__init__.py'
astModule: ast.Module = parsePathFilename2astModule(pathFilename)
identifierModule = 'functoolz'
astModule.body.insert(0, amIHavingFunYet)
astModule.body.insert(0, Make.ImportFrom(settings['humpy_toolz'].identifierPackage, [Make.alias(identifierModule)]))
write_astModule(astModule, pathFilename, settingsWrite_astModule)
