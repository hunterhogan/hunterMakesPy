"""#======== Post-transformation: act on the new packages. ========"""
from assimilate import regexChangeImports, settingsFor, settingsWrite_astModule
from astToolkit import Grab, IfThis, NodeChanger, NodeTourist, parsePathFilename2astModule, Then
from astToolkit.transformationTools import write_astModule
from hunterMakesPy import raiseIfNone
from hunterMakesPy.filesystemToolkit import writeStringToHere
from pathlib import Path
import ast

# NOTE Static version to replace the dynamic version so it passes the tests from the original packages.
astAssign__toolz_version__: ast.Assign = raiseIfNone(NodeTourist(IfThis.isAssignAndTargets0Is(IfThis.isNameIdentifier('__toolz_version__')), Then.extractIt).captureLastMatch(parsePathFilename2astModule(settingsFor['humpy_cytoolz'].pathPackage / '__init__.py')))
NodeChanger(IfThis.isNameIdentifier('__toolz_version__'), Grab.idAttribute(Then.replaceWith('__version__'))).visit(astAssign__toolz_version__)
for aPackage in ('humpy_cytoolz', 'humpy_toolz'):
	pathFilename__init__: Path = settingsFor[aPackage].pathPackage / '__init__.py'
	astModule: ast.Module = parsePathFilename2astModule(pathFilename__init__)
	astModule.body.insert(5, astAssign__toolz_version__)
	write_astModule(astModule, pathFilename__init__, settingsWrite_astModule)

# NOTE Find and replace a handful of textual references to the original packages.
	for pathFilename in pathFilename__init__.parent.rglob(f"*{settingsFor[aPackage].fileExtension}"):
		writeStringToHere(regexChangeImports(pathFilename.read_text()), pathFilename)

