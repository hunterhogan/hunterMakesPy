from functools import partial
from hunterMakesPy import identifierDotAttribute, PackageSettings, settingsPackage
from hunterMakesPy.filesystemToolkit import settings_autoflakeDEFAULT, settings_isortDEFAULT, writeStringToHere
from pathlib import Path
from typing import Any
import re as regex

"""# DEVELOPMENT
Potentially dynamic sources go through the chop shop.
https://github.com/pytoolz/toolz/
https://github.com/pytoolz/cytoolz/
https://github.com/mgrinshpon/toolz-stubs

Static sources should be ingested once, assimilated, and stored.
"""
#============ Eliminate hardcoding. ===============

subModulesHARDCODED: frozenset[identifierDotAttribute] = frozenset(('', '._signatures', '.compatibility', '.curried', '.curried.exceptions'
	, '.curried.operator', '.dicttoolz', '.functoolz', '.itertoolz', '.recipes', '.sandbox', '.sandbox.core', '.sandbox.parallel', '.utils'))

#============ Containers of settings. ============

settingsWrite_astModule: dict[str, dict[str, Any]] = {'isort': settings_isortDEFAULT, 'autoflake': settings_autoflakeDEFAULT}
allTransformeePackages: tuple[str, ...] = ('toolz', 'tlz', 'cytoolz')
getOtherName: dict[str, str] = {}
transformALLdot_pyHere: list[tuple[Path, str, str]] = []
settingsFor: dict[str, PackageSettings] = {}

#============ Settings without containers. ============

cythonDirectives: str = """# cython: embedsignature=True
# cython: freethreading_compatible=True
# cython: language_level=3
"""
noticeCopyrightHeader: str = "Some of the works in this directory and its subdirectories may be protected by \nthe following copyright.\n___\n\n"
pathRoot_tools_stubs = Path("/clones/toolz-stubs/src/toolz-stubs")
regexChangeImports: partial[str] = partial(regex.sub, "(from |import )(.?.?toolz)", "\\1humpy_\\2")  # ty:ignore[invalid-assignment] https://github.com/astral-sh/ty/issues/2799
subModules: frozenset[identifierDotAttribute] = subModulesHARDCODED

#============ Put settings in the containers. ============

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



