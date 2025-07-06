from hunterMakesPy import raiseIfNone
from tests.conftest import uniformTestFailureMessage
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
    actual = raiseIfNone(returnTarget)
    assert actual == expected, uniformTestFailureMessage(expected, actual, "testRaiseIfNoneReturnsNonNoneValues", returnTarget)
    assert actual is returnTarget, uniformTestFailureMessage(returnTarget, actual, "testRaiseIfNoneReturnsNonNoneValues identity check", returnTarget)


def testRaiseIfNoneRaisesValueErrorWhenGivenNone() -> None:
    with pytest.raises(ValueError, match="A function unexpectedly returned `None`. Hint: look at the traceback immediately before `raiseIfNone`."):
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
    with pytest.raises(ValueError, match=customMessage):
        raiseIfNone(None, customMessage)


def testRaiseIfNoneWithEmptyStringMessage() -> None:
    with pytest.raises(ValueError, match="A function unexpectedly returned `None`. Hint: look at the traceback immediately before `raiseIfNone`."):
        raiseIfNone(None, "")


def testRaiseIfNonePreservesTypeAnnotations() -> None:
    integerValue: int = raiseIfNone(23)
    assert isinstance(integerValue, int), uniformTestFailureMessage(int, type(integerValue), "testRaiseIfNonePreservesTypeAnnotations", integerValue)

    stringValue: str = raiseIfNone("cardinal")
    assert isinstance(stringValue, str), uniformTestFailureMessage(str, type(stringValue), "testRaiseIfNonePreservesTypeAnnotations", stringValue)

    listValue: list[int] = raiseIfNone([29, 31])
    assert isinstance(listValue, list), uniformTestFailureMessage(list, type(listValue), "testRaiseIfNonePreservesTypeAnnotations", listValue)
