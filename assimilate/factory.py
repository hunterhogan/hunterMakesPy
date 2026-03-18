"""Transform toolz."""
from shutil import copytree
from astToolkit import Be, Grab, IfThis, Make, NodeChanger, NodeTourist, parsePathFilename2astModule, Then
from astToolkit.transformationTools import write_astModule
from functools import partial
from hunterMakesPy import identifierDotAttribute, PackageSettings, raiseIfNone, settingsPackage
from hunterMakesPy.filesystemToolkit import settings_autoflakeDEFAULT, settings_isortDEFAULT, writeStringToHere
from itertools import product as CartesianProduct
from operator import contains, eq as equalTo
from pathlib import Path
from typing import Any, cast
import ast
import re as regex

#======== Settings for the packages to be created. ========

# TODO I don't know how to move this code block to a separate file in the same directory and import the symbols from the file. It
# seems pretty basic, and I feel pretty stupid. I would normally create "_theSSOT.py" for these settings and re-export the symbols
# through "__init__.py". More generally, I don't know how to divide this "sub-package", which is lateral to "hunterMakesPy", into
# a namespace with multiple modules.
#-------- Eliminate hardcoding. -----------

subModulesHARDCODED: frozenset[identifierDotAttribute] = frozenset(('', '._signatures', '.compatibility', '.curried', '.curried.exceptions'
	, '.curried.operator', '.dicttoolz', '.functoolz', '.itertoolz', '.recipes', '.sandbox', '.sandbox.core', '.sandbox.parallel', '.utils'))

#-------- Containers of settings: try to consolidate these. --------

settingsWrite_astModule: dict[str, dict[str, Any]] = {'isort': settings_isortDEFAULT, 'autoflake': settings_autoflakeDEFAULT}
allTransformeePackages: tuple[str, ...] = ('toolz', 'tlz', 'cytoolz')
getOtherName: dict[str, str] = {}
transformALLdot_pyHere: list[tuple[Path, str, str]] = []
settingsFor: dict[str, PackageSettings] = {}

#-------- Put settings in the containers. --------

noticeCopyrightHeader: str = "Some of the work in this directory and its subdirectories may be protected by \nthe following copyright.\n___\n\n"

settingsWrite_astModule['autoflake']['remove_all_unused_imports'] = False
settingsWrite_astModule['autoflake']['expand_star_imports'] = False
settingsWrite_astModule['autoflake']['ignore_init_module_imports'] = True

for identifierTransformee in allTransformeePackages:
	humpyPackage: str = f"humpy_{identifierTransformee}"
	getOtherName[identifierTransformee] = humpyPackage
	getOtherName[humpyPackage] = identifierTransformee

	pathTransformee: Path = Path(f'/clones/{identifierTransformee}/{identifierTransformee}')

	settingsFor[humpyPackage] = PackageSettings(identifierPackage=humpyPackage, pathPackage=(settingsPackage.pathPackage.parent / humpyPackage))
	settingsFor[humpyPackage].pathPackage.mkdir(parents=True, exist_ok=True)

	if identifierTransformee == 'tlz':
		pathTransformee = Path(f'/clones/toolz/{identifierTransformee}')
	else:
		writeStringToHere(noticeCopyrightHeader + (pathTransformee.parent / 'LICENSE.txt').read_text(encoding='utf-8'), settingsFor[humpyPackage].pathPackage / 'Notice_of_Copyright.txt')

	transformALLdot_pyHere.append((pathTransformee, identifierTransformee, getOtherName[identifierTransformee]))

regexChangeImports: partial[str] = partial(regex.sub, "(from |import )(.?.?toolz)", "\\1humpy_\\2")  # ty:ignore[invalid-assignment] https://github.com/astral-sh/ty/issues/2799

subModules: frozenset[identifierDotAttribute] = subModulesHARDCODED
#======== Ingest and transform external packages and files ========

for pathTransformee, identifierTransformee, humpyPackage in transformALLdot_pyHere:
	for pathRoot, listDirectories, listFilenames in pathTransformee.walk():
		if '__pycache__' in listDirectories:
			listDirectories.remove('__pycache__')
		for directory in listDirectories:
			(settingsFor[humpyPackage].pathPackage / directory).mkdir(parents=True, exist_ok=True)

		for filename in filter(lambda filename: filename.endswith(settingsFor[humpyPackage].fileExtension), listFilenames):
			astModule: ast.Module = parsePathFilename2astModule(pathRoot / filename)

			for packageTransformee, identifierModule in CartesianProduct(allTransformeePackages, subModules):
				changeImportFrom = NodeChanger(Be.ImportFrom.moduleIs(partial(equalTo, packageTransformee+identifierModule)), Grab.moduleAttribute(Then.replaceWith(getOtherName[packageTransformee]+identifierModule)))
				changeImportFrom.visit(astModule)

				changeImport = NodeChanger(Be.alias.nameIs(partial(equalTo, packageTransformee+identifierModule)), Grab.nameAttribute(Then.replaceWith(getOtherName[packageTransformee]+identifierModule)))
				changeImport.visit(astModule)

				changeConstant = NodeChanger(IfThis.isConstant_value(packageTransformee+identifierModule), Then.replaceWith(Make.Constant(getOtherName[packageTransformee]+identifierModule)))
				changeConstant.visit(astModule)

				if identifierModule != '':
					stringOld: identifierDotAttribute = f" {packageTransformee}{identifierModule}"
					changeIdentifierInConstant = NodeChanger(IfThis.isAllOf(Be.Constant.valueIs(lambda nodeDOTvalue: isinstance(nodeDOTvalue, str)), Be.Constant.valueIs(lambda nodeDOTvalue, stringOld=stringOld: contains(nodeDOTvalue, stringOld))), lambda node, stringOld=stringOld, packageTransformee=packageTransformee, identifierModule=identifierModule: Make.Constant(cast(str, node.value).replace(stringOld, f" {getOtherName[packageTransformee]}{identifierModule}")))
					changeIdentifierInConstant.visit(astModule)

			for packageTransformee in allTransformeePackages:
				stringOld: str = f"`{packageTransformee}`"
				changeBacktickIdentifierInConstant = NodeChanger(IfThis.isAllOf(Be.Constant.valueIs(lambda nodeDOTvalue: isinstance(nodeDOTvalue, str)), Be.Constant.valueIs(lambda nodeDOTvalue, stringOld=stringOld: contains(nodeDOTvalue, stringOld))), lambda node, stringOld=stringOld, packageTransformee=packageTransformee: Make.Constant(cast(str, node.value).replace(stringOld, f"`{getOtherName[packageTransformee]}`")))
				changeBacktickIdentifierInConstant.visit(astModule)

				changeName = NodeChanger(IfThis.isNameIdentifier(packageTransformee), Grab.idAttribute(Then.replaceWith(getOtherName[packageTransformee])))
				changeName.visit(astModule)

			write_astModule(astModule, settingsFor[humpyPackage].pathPackage / pathRoot.relative_to(pathTransformee) / filename, settingsWrite_astModule)

	if identifierTransformee == 'cytoolz':
		for pathFilename in pathTransformee.glob('*.pxd'):
			writeStringToHere(regexChangeImports(pathFilename.read_text()), settingsFor[humpyPackage].pathPackage / pathFilename.relative_to(pathTransformee))
		for pathFilename in pathTransformee.glob('*.pyx'):
			writeStringToHere(regexChangeImports(pathFilename.read_text().replace(identifierTransformee, getOtherName[identifierTransformee])), settingsFor[humpyPackage].pathPackage / pathFilename.relative_to(pathTransformee))

		filename_setupDOTpy: str ='setup.py'
		astModule: ast.Module = parsePathFilename2astModule(pathTransformee.parent / filename_setupDOTpy)
		changeIdentifierInConstant = NodeChanger(IfThis.isAllOf(Be.Constant.valueIs(lambda nodeDOTvalue: isinstance(nodeDOTvalue, str)), Be.Constant.valueIs(lambda nodeDOTvalue, identifierTransformee=identifierTransformee: contains(nodeDOTvalue, identifierTransformee))), lambda node, identifierTransformee=identifierTransformee: Make.Constant(cast(str, node.value).replace(identifierTransformee, getOtherName[identifierTransformee])))
		changeIdentifierInConstant.visit(astModule)
		write_astModule(astModule, settingsFor[humpyPackage].pathPackage.parent / filename_setupDOTpy, settingsWrite_astModule)

#======== Post-transformation: acting on the new packages ========

astAssign__toolz_version__: ast.Assign = raiseIfNone(NodeTourist(IfThis.isAssignAndTargets0Is(IfThis.isNameIdentifier('__toolz_version__')), Then.extractIt).captureLastMatch(parsePathFilename2astModule(settingsFor['humpy_cytoolz'].pathPackage / '__init__.py')))
NodeChanger(IfThis.isNameIdentifier('__toolz_version__'), Grab.idAttribute(Then.replaceWith('__version__'))).visit(astAssign__toolz_version__)

for aPackage in ('humpy_cytoolz', 'humpy_toolz'):
	pathFilename__init__: Path = settingsFor[aPackage].pathPackage / '__init__.py'
	astModule: ast.Module = parsePathFilename2astModule(pathFilename__init__)
	astModule.body.insert(5, astAssign__toolz_version__)
	write_astModule(astModule, pathFilename__init__, settingsWrite_astModule)

	for pathFilename in pathFilename__init__.parent.rglob(f"*{settingsFor[aPackage].fileExtension}"):
		writeStringToHere(regexChangeImports(pathFilename.read_text()), pathFilename)

#======== Copy stub files. ===========

pathRoot_tools_stubs = Path("/clones/toolz-stubs/src/toolz-stubs")
copytree(pathRoot_tools_stubs, settingsFor['humpy_toolz'].pathPackage, dirs_exist_ok=True)
