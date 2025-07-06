from hunterMakesPy import makeDirsSafely, writeStringToHere
from tests.conftest import uniformTestFailureMessage
import io
import pathlib

def testMakeDirsSafelyCreatesParentDirectories(pathTmpTesting: pathlib.Path) -> None:
    nestedDirectory = pathTmpTesting / "sub1" / "sub2"
    filePath = nestedDirectory / "dummy.txt"
    makeDirsSafely(filePath)
    assert nestedDirectory.exists() and nestedDirectory.is_dir(), uniformTestFailureMessage(True, nestedDirectory.exists() and nestedDirectory.is_dir(), "testMakeDirsSafelyCreatesParentDirectories", filePath)

def testMakeDirsSafelyWithIOBaseDoesNotRaise() -> None:
    memoryStream = io.StringIO()
    makeDirsSafely(memoryStream)

def testWriteStringToHereCreatesFileAndWritesContent(pathTmpTesting: pathlib.Path) -> None:
    nestedDirectory = pathTmpTesting / "a" / "b"
    filePath = nestedDirectory / "test.txt"
    writeStringToHere("hello world", filePath)
    assert filePath.exists(), uniformTestFailureMessage(True, filePath.exists(), "testWriteStringToHereCreatesFileAndWritesContent", filePath)
    assert filePath.read_text() == "hello world", uniformTestFailureMessage("hello world", filePath.read_text(), "testWriteStringToHereCreatesFileAndWritesContent", filePath)
