"""Provides parameter and input validation, integer parsing, and concurrency handling utilities."""
from collections.abc import Iterable, Sized
from dataclasses import dataclass
from typing import Any, TYPE_CHECKING
import charset_normalizer
import multiprocessing

if TYPE_CHECKING:
	from charset_normalizer.models import CharsetMatch

@dataclass
class ErrorMessageContext:
	"""Context information for constructing error messages.

	Parameters
	----------
	parameterValue : Any = None
		The value that caused the error.
	parameterValueType : str | None = None
		The name of the type of the parameter value.
	containerType : str | None = None
		The name of the type of the container holding the parameter.
	isElement : bool = False
		Whether the parameter is an element within a container.

	"""

	parameterValue: Any = None
	parameterValueType: str | None = None
	containerType: str | None = None
	isElement: bool = False

def _constructErrorMessage(context: ErrorMessageContext, parameterName: str, parameterType: type[Any] | None) -> str:
	"""Construct error message from available context using template.

	I received ["value" | a value | `None`] [of type `type` | `None`] [as an element in | `None`] [a `containerType` type |
	`None`] but `parameterName` must have integers [in type(s) `parameterType` | `None`].

	Hypothetically, this is a prototype that can be generalized to other functions. In this package and a few of my other
	packages, I have developed standardized error messages, but those are quite different from this. I will certainly continue to
	develop this kind of functionality, and this function will influence things.

	Parameters
	----------
	context : ErrorMessageContext
		The error context containing parameter value, type, and container information.
	parameterName : str
		The name of the parameter that caused the error.
	parameterType : type[Any] | None
		The expected type of the parameter, used in error messages.

	Returns
	-------
	errorMessage : str
		The constructed error message string.

	"""
	messageParts: list[str] = ["I received "]

	if context.parameterValue is not None and not isinstance(context.parameterValue, (bytes, bytearray, memoryview)):
		messageParts.append(f'"{context.parameterValue}"')
	else:
		messageParts.append("a value")

	if context.parameterValueType:
		messageParts.append(f" of type `{context.parameterValueType}`")

	if context.isElement:
		messageParts.append(" as an element in")

	if context.containerType:
		messageParts.append(f" a `{context.containerType}` type")

	messageParts.append(f" but {parameterName} must have integers")

	if parameterType:
		messageParts.append(f" in type(s) `{parameterType}`")

	return "".join(messageParts)

def defineConcurrencyLimit(*, limit: bool | float | int | None, cpuTotal: int = multiprocessing.cpu_count()) -> int:
	"""Determine the concurrency limit based on the provided parameter.

	Tests for this function can be run with:
	`from hunterMakesPy.tests.test_parseParameters import PytestFor_defineConcurrencyLimit`

	Parameters
	----------
	limit : bool | float | int | None
		Whether and how to limit CPU usage. See notes and examples for details how to describe the options to your users.
	cpuTotal : int = multiprocessing.cpu_count()
		The total number of CPUs available in the system. Default is `multiprocessing.cpu_count()`.

	Returns
	-------
	concurrencyLimit : int
		The calculated concurrency limit, ensuring it is at least 1.

	Notes
	-----
	Consider using `hunterMakesPy.oopsieKwargsie()` to handle malformed inputs. For example:

	```
	if not (CPUlimit is None or isinstance(CPUlimit, (bool, int, float))):
		CPUlimit = oopsieKwargsie(CPUlimit)
	```

	Example parameters
	------------------
	```python
	CPUlimit: bool | float | int | None
	CPUlimit: bool | float | int | None = None
	```

	Example docstring
	-----------------
	```python

	Arguments
	---------
	CPUlimit: bool | float | int | None
		Whether and how to limit the the number of available processors used by the function. See notes for details.

	Notes
	-----
	Limits on CPU usage, `CPUlimit`:
		- `False`, `None`, or `0`: No limits on processor usage; uses all available processors. All other values will potentially limit processor usage.
		- `True`: Yes, limit the processor usage; limits to 1 processor.
		- `int >= 1`: The maximum number of available processors to use.
		- `0 < float < 1`: The maximum number of processors to use expressed as a fraction of available processors.
		- `-1 < float < 0`: The number of processors to *not* use expressed as a fraction of available processors.
		- `int <= -1`: The number of available processors to *not* use.
		- If the value of `CPUlimit` is a `float` greater than 1 or less than -1, the function truncates the value to an `int` with the same sign as the `float`.
	```

	"""
	concurrencyLimit: int = cpuTotal

	if isinstance(limit, str):
		limitFromString: bool | None | str = oopsieKwargsie(limit)
		if isinstance(limitFromString, str):
			try:
				limit = float(limitFromString)
			except ValueError as ERRORmessage:
				message: str = f"I received '{limitFromString}', but it must be a number, `True`, `False`, or `None`."
				raise ValueError(message) from ERRORmessage
		else:
			limit = limitFromString
	if isinstance(limit, float) and abs(limit) >= 1:
		limit = round(limit)
	if limit is None or limit is False or limit == 0:
		pass
	elif limit is True:
		concurrencyLimit = 1
	elif limit >= 1:
		concurrencyLimit = int(limit)
	elif 0 < limit < 1:
		concurrencyLimit = round(limit * cpuTotal)
	elif -1 < limit < 0:
		concurrencyLimit = cpuTotal - abs(round(limit * cpuTotal))
	elif limit <= -1:
		concurrencyLimit = cpuTotal - abs(int(limit))

	return max(int(concurrencyLimit), 1)

# ruff: noqa: TRY301
def intInnit(listInt_Allegedly: Iterable[Any], parameterName: str | None = None, parameterType: type[Any] | None = None) -> list[int]:
	"""Validate and convert input values to a `list` of integers.

	Accepts various numeric types and attempts to convert them into integers while providing descriptive error messages. This
	package includes Pytest tests that can be imported and run: `from hunterMakesPy.tests.test_parseParameters import
	PytestFor_intInnit`.

	Parameters
	----------
	listInt_Allegedly : Iterable[Any]
		The input sequence that should contain integer-compatible values. Accepts integers, strings, floats, complex numbers, and
		binary data. Rejects boolean values and non-integer numeric values.
	parameterName : str | None = None
		Name of the parameter from your function for which this function is validating the input validated. If there is an error
		message, it provides context to your user. Defaults to 'the parameter'.
	parameterType : type[Any] | None = None
		Expected type(s) of the parameter, used in error messages.

	Returns
	-------
	listValidated : list[int]
		A `list` containing validated integers.

	Raises
	------
	ValueError
		When the input is empty or contains non-integer compatible values.
	TypeError
		When an element is a boolean or incompatible type.
	RuntimeError
		If the input sequence length changes during iteration.

	Notes
	-----
	The function performs strict validation and follows fail-early principles to catch potential issues before they become catastrophic.

	"""
	parameterName = parameterName or 'the parameter'
	parameterType = parameterType or list

	if not listInt_Allegedly:
		message: str = f"I did not receive a value for {parameterName}, but it is required."
		raise ValueError(message)

	# Be nice, and assume the input container is valid and every element is valid.
	# Nevertheless, this is a "fail-early" step, so reject ambiguity and try to induce errors now that could be catastrophic later.
	try:
		iter(listInt_Allegedly)
		lengthInitial: int | None = None
		if isinstance(listInt_Allegedly, Sized):
			lengthInitial = len(listInt_Allegedly)

		listValidated: list[int] = []

		for allegedInt in listInt_Allegedly:

			errorMessageContext: ErrorMessageContext = ErrorMessageContext(
				parameterValue = allegedInt,
				parameterValueType = type(allegedInt).__name__,
				isElement = True
			)

			# Always rejected as ambiguous
			if isinstance(allegedInt, bool):
				raise TypeError(errorMessageContext)

			# In this section, we know the Python type is not `int`, but maybe the value is clearly an integer.
			# Through a series of conversions, allow data to cascade down into either an `int` or a meaningful error message.

			if isinstance(allegedInt, (bytes, bytearray, memoryview)):
				errorMessageContext.parameterValue = None  # Don't expose potentially garbled binary data in error messages
				if isinstance(allegedInt, memoryview):
					allegedInt = allegedInt.tobytes()
				decodedString: CharsetMatch | None = charset_normalizer.from_bytes(allegedInt).best()
				if not decodedString:
					raise ValueError(errorMessageContext)
				allegedInt = errorMessageContext.parameterValue = str(decodedString)

			if isinstance(allegedInt, complex):
				if allegedInt.imag != 0:
					raise ValueError(errorMessageContext)
				allegedInt = float(allegedInt.real)
			elif isinstance(allegedInt, str):
				allegedInt = float(allegedInt.strip())

			if isinstance(allegedInt, float):
				if not float(allegedInt).is_integer():
					raise ValueError(errorMessageContext)
				allegedInt = int(allegedInt)
			else:
				allegedInt = int(allegedInt)

			listValidated.append(allegedInt)

			if lengthInitial is not None and isinstance(listInt_Allegedly, Sized) and len(listInt_Allegedly) != lengthInitial:
				raise RuntimeError((lengthInitial, len(listInt_Allegedly)))

	except (TypeError, ValueError) as ERRORmessage:
		if isinstance(ERRORmessage.args[0], ErrorMessageContext):
			context = ERRORmessage.args[0]
			if not context.containerType:
				context.containerType = type(listInt_Allegedly).__name__
			message = _constructErrorMessage(context, parameterName, parameterType)
			raise type(ERRORmessage)(message) from None
		# If it's not our Exception, don't molest it
		raise

	except RuntimeError as ERRORruntime:
		lengthInitial, lengthCurrent = ERRORruntime.args[0]
		ERRORmessage = (
			f"The input sequence {parameterName} was modified during iteration. "
			f"Initial length {lengthInitial}, current length {lengthCurrent}."
		)
		raise RuntimeError(
			ERRORmessage
		) from None

	else:
		return listValidated

def oopsieKwargsie(huh: Any) -> bool | None | str:
	"""Interpret a `str` as `True`, `False`, or `None` to avoid an `Exception`.

	If a calling function passes a `str` to a parameter that shouldn't receive a `str`, `oopsieKwargsie()` might help you avoid an
	`Exception`. It tries to interpret the string as `True`, `False`, or `None`.

	Tests for this function can be run with: `from hunterMakesPy.tests.test_parseParameters import PytestFor_oopsieKwargsie`.

	Parameters
	----------
	huh : Any
		(huh) The input string to be parsed.

	Returns
	-------
	interpretedValue : bool | None | str
		The reserved keyword `True`, `False`, or `None` or the original string, `huh`.

	"""
	if not isinstance(huh, str):
		try:
			huh = str(huh)
		except BaseException:  # noqa: BLE001
			return huh
	formatted: str = huh.strip().title()
	if formatted == str(True):
		return True
	if formatted == str(False):
		return False
	if formatted == str(None):
		return None
	return huh
