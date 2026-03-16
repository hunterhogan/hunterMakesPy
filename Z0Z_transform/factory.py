"""Settings."""
from astToolkit import Be, dump, Grab, IfThis, Make, NodeChanger, NodeTourist, parsePathFilename2astModule, Then
from astToolkit.transformationTools import write_astModule
from functools import partial
from hunterMakesPy import PackageSettings, settingsPackage
from operator import eq as equalTo
from pathlib import Path
import ast

identifierPackage='humpy_toolz'

settingsTransformation: PackageSettings = PackageSettings(identifierPackage=identifierPackage
	, pathPackage=(settingsPackage.pathPackage / '..' / identifierPackage).resolve())

settingsTransformation.pathPackage.mkdir(parents=True, exist_ok=True)

path_toolz = Path('/clones/toolz/toolz')
package: str = 'toolz'

for pathRoot, listDirectories, listFilenames in path_toolz.walk():
	for directory in listDirectories:
		(settingsTransformation.pathPackage / directory).mkdir(parents=True, exist_ok=True)

	for filename in listFilenames:
		pathFilename: Path = pathRoot / filename
		astModule: ast.Module = parsePathFilename2astModule(pathFilename)

		for identifierModule in ('', '._signatures', '.curried', '.dicttoolz', '.functoolz', '.itertoolz', '.recipes', '.sandbox.core', '.sandbox.parallel', '.utils'):
			NodeChanger(Be.ImportFrom.moduleIs(partial(equalTo, package+identifierModule))
				, Grab.moduleAttribute(Then.replaceWith(settingsTransformation.identifierPackage+identifierModule))
			).visit(astModule)

			NodeChanger(Be.alias.nameIs(partial(equalTo, package+identifierModule))
				, Grab.nameAttribute(Then.replaceWith(settingsTransformation.identifierPackage+identifierModule))
			).visit(astModule)

			NodeChanger(Be.Subscript.sliceIs(IfThis.isConstant_value(package+identifierModule))
				, Grab.sliceAttribute(Then.replaceWith(Make.Constant(settingsTransformation.identifierPackage+identifierModule)))
			).visit(astModule)

		NodeChanger(IfThis.isNameIdentifier(package)
			, Grab.idAttribute(Then.replaceWith(settingsTransformation.identifierPackage))
		).visit(astModule)

		write_astModule(astModule, settingsTransformation.pathPackage / pathFilename.relative_to(path_toolz))

pathFilename = settingsTransformation.pathPackage / '__init__.py'
astModule: ast.Module = parsePathFilename2astModule(pathFilename)
identifierModule = 'functoolz'
astModule.body.insert(0, Make.ImportFrom(settingsTransformation.identifierPackage, [Make.alias(identifierModule)]))
write_astModule(astModule, pathFilename)
