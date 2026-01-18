"""Tests for the coping mechanism module.

(AI generated docstring)

This module validates the behavior of package setting retrieval,
null-check utilities, and installation path resolution.

"""
from hunterMakesPy import PackageSettings, raiseIfNone
from hunterMakesPy.coping import getIdentifierPackagePACKAGING, getPathPackageINSTALLING
from hunterMakesPy.tests.conftest import uniformTestFailureMessage
from pathlib import Path
import pytest

@pytest.mark.parametrize(
	"returnTarget, expected",
	[
		(13, 13),
		(17, 17),
		("fibonacci", "fibonacci"),
		("prime", "prime"),
		([], []),
		({}, {}),
		(False, False),
		(0, 0),
	]
)
def testRaiseIfNoneReturnsNonNoneValues(returnTarget: object, expected: object) -> None:
	"""Verify that non-None values are returned exactly as provided.

	(AI generated docstring)

	Parameters
	----------
	returnTarget : object
		The value to pass to `raiseIfNone`.
	expected : object
		The expected return value (should be identical to `returnTarget`).

	"""
	actual: object = raiseIfNone(returnTarget)
	assert actual == expected, uniformTestFailureMessage(expected, actual, "testRaiseIfNoneReturnsNonNoneValues", returnTarget)
	assert actual is returnTarget, uniformTestFailureMessage(returnTarget, actual, "testRaiseIfNoneReturnsNonNoneValues identity check", returnTarget)

def testRaiseIfNoneRaisesValueErrorWhenGivenNone() -> None:
	"""Verify that ValueError is raised when input is None.

	(AI generated docstring)

	"""
	with pytest.raises(ValueError, match=r"A function unexpectedly returned `None`.*"):
		raiseIfNone(None)

@pytest.mark.parametrize(
	"customMessage",
	[
		"Configuration must include 'host' setting",
		"Database connection failed",
		"User input is required",
		"Network request returned empty response",
	]
)
def testRaiseIfNoneRaisesValueErrorWithCustomMessage(customMessage: str) -> None:
	"""Verify that custom error messages are used when provided.

	(AI generated docstring)

	Parameters
	----------
	customMessage : str
		The custom error message to expect.

	"""
	with pytest.raises(ValueError, match=customMessage):
		raiseIfNone(None, customMessage)

def testRaiseIfNoneWithEmptyStringMessage() -> None:
	"""Verify that empty custom message string triggers default message.

	(AI generated docstring)

	"""
	with pytest.raises(ValueError, match=r"A function unexpectedly returned `None`.*"):
		raiseIfNone(None, "")

def testRaiseIfNonePreservesTypeAnnotations() -> None:
	"""Verify that type info is preserved through the pass-through.

	(AI generated docstring)

	"""
	integerValue: int = raiseIfNone(23)
	assert isinstance(integerValue, int), uniformTestFailureMessage(int, type(integerValue), "testRaiseIfNonePreservesTypeAnnotations", integerValue)

	stringValue: str = raiseIfNone("cardinal")
	assert isinstance(stringValue, str), uniformTestFailureMessage(str, type(stringValue), "testRaiseIfNonePreservesTypeAnnotations", stringValue)

	listValue: list[int] = raiseIfNone([29, 31])
	assert isinstance(listValue, list), uniformTestFailureMessage(list, type(listValue), "testRaiseIfNonePreservesTypeAnnotations", listValue)

# Tests for PackageSettings dataclass
@pytest.mark.parametrize(
	"identifierPackageFALLBACK, expectedIdentifierPackage",
	[
		("astToolFactory", "hunterMakesPy"),  # Should read from pyproject.toml
		("nonExistentPackage", "hunterMakesPy"),  # Should read from pyproject.toml
		("customPackage", "hunterMakesPy"),  # Should read from pyproject.toml
	]
)
def testPackageSettingsWithFallbackUsesProjectToml(identifierPackageFALLBACK: str, expectedIdentifierPackage: str) -> None:
	"""Test that PackageSettings reads package name from pyproject.toml when using fallback.

	Parameters
	----------
	identifierPackageFALLBACK : str
		The fallback identifier to use if retrieval fails (or to trigger lookup).
	expectedIdentifierPackage : str
		The expected resolved package identifier.

	"""
	packageSettings: PackageSettings = PackageSettings(identifierPackageFALLBACK)
	assert packageSettings.identifierPackage == expectedIdentifierPackage, uniformTestFailureMessage(
		expectedIdentifierPackage, packageSettings.identifierPackage, "PackageSettings fallback", identifierPackageFALLBACK
	)

@pytest.mark.parametrize(
	"explicitIdentifierPackage, expectedIdentifierPackage",
	[
		("customPackageName", "customPackageName"),
		("fibonacci", "fibonacci"),
		("prime", "prime"),
		("astToolFactory", "astToolFactory"),
	]
)
def testPackageSettingsWithExplicitIdentifierPackage(explicitIdentifierPackage: str, expectedIdentifierPackage: str) -> None:
	"""Test that PackageSettings respects explicitly provided identifierPackage.

	Parameters
	----------
	explicitIdentifierPackage : str
		The explicitly provided package identifier.
	expectedIdentifierPackage : str
		The expected resolved package identifier.

	"""
	packageSettings: PackageSettings = PackageSettings(identifierPackage=explicitIdentifierPackage)
	assert packageSettings.identifierPackage == expectedIdentifierPackage, uniformTestFailureMessage(
		expectedIdentifierPackage, packageSettings.identifierPackage, "PackageSettings explicit identifierPackage", explicitIdentifierPackage
	)

@pytest.mark.parametrize(
	"explicitPathPackage, expectedPathPackage",
	[
		(Path("C:/fibonacci/path"), Path("C:/fibonacci/path")),
		(Path("C:/prime/directory"), Path("C:/prime/directory")),
		(Path("/usr/local/lib/package"), Path("/usr/local/lib/package")),
		(Path("relative/path"), Path("relative/path")),
	]
)
def testPackageSettingsWithExplicitPathPackage(explicitPathPackage: Path, expectedPathPackage: Path) -> None:
	"""Test that PackageSettings respects explicitly provided pathPackage.

	Parameters
	----------
	explicitPathPackage : Path
		The explicitly provided package path.
	expectedPathPackage : Path
		The expected resolved package path.

	"""
	packageSettings: PackageSettings = PackageSettings(pathPackage=explicitPathPackage)
	assert packageSettings.pathPackage == expectedPathPackage, uniformTestFailureMessage(
		expectedPathPackage, packageSettings.pathPackage, "PackageSettings explicit pathPackage", explicitPathPackage
	)

@pytest.mark.parametrize(
	"fileExtension, expectedFileExtension",
	[
		(".fibonacci", ".fibonacci"),
		(".prime", ".prime"),
		(".txt", ".txt"),
		(".md", ".md"),
		(".json", ".json"),
	]
)
def testPackageSettingsWithCustomFileExtension(fileExtension: str, expectedFileExtension: str) -> None:
	"""Test that PackageSettings respects custom file extensions.

	Parameters
	----------
	fileExtension : str
		The custom file extension to set.
	expectedFileExtension : str
		The expected file extension in the settings.

	"""
	packageSettings: PackageSettings = PackageSettings(fileExtension=fileExtension)
	assert packageSettings.fileExtension == expectedFileExtension, uniformTestFailureMessage(
		expectedFileExtension, packageSettings.fileExtension, "PackageSettings custom fileExtension", fileExtension
	)

def testPackageSettingsDefaultValues() -> None:
	"""Test that PackageSettings has correct default values when no arguments provided."""
	packageSettings: PackageSettings = PackageSettings()

	# Should have default file extension
	assert packageSettings.fileExtension == '.py', uniformTestFailureMessage(
		'.py', packageSettings.fileExtension, "PackageSettings default fileExtension"
	)

	# identifierPackage should be empty when no fallback provided
	assert packageSettings.identifierPackage == '', uniformTestFailureMessage(
		'', packageSettings.identifierPackage, "PackageSettings default identifierPackage"
	)

	expectedPath: Path = Path()
	assert packageSettings.pathPackage == expectedPath, uniformTestFailureMessage(
		expectedPath, packageSettings.pathPackage, "PackageSettings default pathPackage, pathPackage should remain as Path() when identifierPackage is empty"
	)

@pytest.mark.parametrize(
	"identifierPackageFALLBACK, identifierPackage, pathPackage, fileExtension",
	[
		("fallback", "custom", Path("C:/custom/path"), ".txt"),
		("fibonacci", "prime", Path("C:/fibonacci/lib"), ".md"),
		("defaultFallback", "overridePackage", Path("/usr/local/override"), ".json"),
	]
)
def testPackageSettingsAllParametersCombined(
	identifierPackageFALLBACK: str,
	identifierPackage: str,
	pathPackage: Path,
	fileExtension: str
) -> None:
	"""Test PackageSettings with all parameters provided.

	Parameters
	----------
	identifierPackageFALLBACK : str
		The fallback identifier.
	identifierPackage : str
		The explicit package identifier.
	pathPackage : Path
		The explicit package path.
	fileExtension : str
		The explicit file extension.

	"""
	packageSettings: PackageSettings = PackageSettings(
		identifierPackageFALLBACK
		, identifierPackage=identifierPackage
		, pathPackage=pathPackage
		, fileExtension=fileExtension
	)

	assert packageSettings.identifierPackage == identifierPackage, uniformTestFailureMessage(
		identifierPackage, packageSettings.identifierPackage, "PackageSettings combined identifierPackage"
	)
	assert packageSettings.pathPackage == pathPackage, uniformTestFailureMessage(
		pathPackage, packageSettings.pathPackage, "PackageSettings combined pathPackage"
	)
	assert packageSettings.fileExtension == fileExtension, uniformTestFailureMessage(
		fileExtension, packageSettings.fileExtension, "PackageSettings combined fileExtension"
	)

def testPackageSettingsFallbackIgnoredWhenExplicitIdentifierProvided() -> None:
	"""Test that fallback is ignored when explicit identifierPackage is provided."""
	packageSettings: PackageSettings = PackageSettings("shouldBeIgnored", identifierPackage="explicit")
	assert packageSettings.identifierPackage == "explicit", uniformTestFailureMessage(
		"explicit", packageSettings.identifierPackage, "PackageSettings fallback ignored"
	)

# Tests for helper functions
@pytest.mark.parametrize(
	"identifierPackageFALLBACK, expectedResult",
	[
		("fibonacci", "hunterMakesPy"),  # Should read from pyproject.toml
		("prime", "hunterMakesPy"),  # Should read from pyproject.toml
		("nonExistentPackage", "hunterMakesPy"),  # Should read from pyproject.toml
	]
)
def testGetIdentifierPackagePACKAGING(identifierPackageFALLBACK: str, expectedResult: str) -> None:
	"""Test that getIdentifierPackagePACKAGING reads from pyproject.toml correctly.

	Parameters
	----------
	identifierPackageFALLBACK : str
		The fallback identifier to provide.
	expectedResult : str
		The expected package identifier result.

	"""
	actual: str = getIdentifierPackagePACKAGING(identifierPackageFALLBACK)
	assert actual == expectedResult, uniformTestFailureMessage(
		expectedResult, actual, "getIdentifierPackagePACKAGING", identifierPackageFALLBACK
	)

@pytest.mark.parametrize(
	"identifierPackage",
	[
		"hunterMakesPy",  # This package exists
		"fibonacci",  # Non-existent package should fallback to cwd
		"prime",  # Non-existent package should fallback to cwd
	]
)
def testGetPathPackageINSTALLING(identifierPackage: str) -> None:
	"""Test that getPathPackageINSTALLING returns valid Path objects.

	Parameters
	----------
	identifierPackage : str
		The package identifier to look up.

	"""
	actual: Path = getPathPackageINSTALLING(identifierPackage)
	assert isinstance(actual, Path), uniformTestFailureMessage(
		Path, type(actual), "getPathPackageINSTALLING type", identifierPackage
	)
	assert actual.exists() or actual == Path.cwd(), uniformTestFailureMessage(
		"existing path or cwd", actual, "getPathPackageINSTALLING existence", identifierPackage
	)
