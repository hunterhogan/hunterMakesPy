# ruff: file-ignore[raise-within-try]
"""Validate integer inputs, calculate worker counts, and interpret string parameters.

(AI generated docstring)

You can use this module to convert integer-compatible inputs into lists of integers, calculate
worker counts from absolute or fractional limits, and interpret strings as `True`, `False`, or
`None`. Integer validation reports incompatible values with context about the caller's parameter.
Worker-count calculation uses the system CPU count from `multiprocessing` by default and also
accepts numeric strings. Binary integer inputs use `charset_normalizer` for text decoding.

Contents
--------
Functions
	defineConcurrencyLimit
		Calculate a worker count from an absolute, fractional, or reserved-CPU limit.
	intInnit
		Validate and convert input values to a `list` of integers.
	oopsieKwargsie
		Interpret text as `True`, `False`, or `None`.
"""
from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING
import charset_normalizer
import multiprocessing
import sys

if TYPE_CHECKING:
	from collections.abc import Collection
	from hunterMakesPy.theTypes import ConcurrencyLimit
	from typing import Any

def defineConcurrencyLimit(*, limit: ConcurrencyLimit, cpuTotal: int = multiprocessing.cpu_count()) -> int:
	"""Calculate a worker count from an absolute, fractional, or reserved-CPU limit.

	(AI generated docstring)

	You can select a worker count from `limit` and `cpuTotal` with an explicit count, a fraction
	of `cpuTotal`, a count of CPUs to reserve, or a boolean choice. You can also supply numeric
	strings and strings representing `True`, `False`, or `None`.

	Processor Counts
	----------------
	Floating-point counts whose absolute value is at least one round to the nearest integer before
	the count rules apply. All rounding uses Python `round`, including ties to the nearest even
	integer. The following rules determine the count before the minimum and maximum apply.

	- `None`, `False`, or zero select `cpuTotal`.
	- `True` selects one worker.
	- A positive count of at least one selects that count.
	- A positive fraction below one selects `round(limit * cpuTotal)` workers.
	- A negative fraction above negative one reserves `abs(round(limit * cpuTotal))` CPUs.
	- A negative count of at most negative one reserves `abs(int(limit))` CPUs.

	The result is at least one worker. On Windows, the result is at most 61 workers, matching
	the restriction for `concurrent.futures.ProcessPoolExecutor` [1].

	Parameters
	----------
	limit : bool | float | int | str | None
		The worker-count specification. `None`, `False`, or zero select `cpuTotal`; `True` selects
		one worker. Positive counts select workers to use, and negative counts select CPUs to reserve.
		Fractions between negative one and one select proportions to reserve or use, respectively.
		Strings representing `True`, `False`, or `None` ignore capitalization and surrounding
		whitespace. Other strings must represent numbers accepted by `float`.
	cpuTotal : int = multiprocessing.cpu_count()
		The CPU count used for fractional limits and reserved-CPU calculations. The default is the
		value of `multiprocessing.cpu_count` evaluated when this module is imported.

	Returns
	-------
	concurrencyLimit : int
		The calculated worker count, with a minimum of one and a Windows maximum of 61.
		An explicit positive count can exceed `cpuTotal`.

	Raises
	------
	ValueError
		If a string does not represent a number, `True`, `False`, or `None`.

	See Also
	--------
	`oopsieKwargsie`
		Interpret strings as `True`, `False`, or `None` without calculating a worker count.

	Examples
	--------
	The README selects three quarters of the default CPU count.

		```python
		from hunterMakesPy.parseParameters import defineConcurrencyLimit

		workers = defineConcurrencyLimit(limit=0.75)
		```

	References
	----------
	[1] Python documentation, "ProcessPoolExecutor", Windows worker-count restriction.
	https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ProcessPoolExecutor
	"""
	if isinstance(limit, str):
		limitFromString: bool | str | None = oopsieKwargsie(limit)
		if isinstance(limitFromString, str):
			try:
				limit = float(limitFromString)
			except ValueError as ERRORmessage:
				message: str = f"I received '{limitFromString}', but it must be a number, `True`, `False`, or `None`."
				raise ValueError(message) from ERRORmessage
		else:
			limit = limitFromString
	if isinstance(limit, float) and 1 <= abs(limit):
		limit = round(limit)

	concurrencyLimit: int = cpuTotal
	if (limit is None) or (limit is False) or (limit == 0):
		pass
	elif limit is True:
		concurrencyLimit = 1
	elif 1 <= limit:
		concurrencyLimit = int(limit)
	elif 0 < limit < 1:
		concurrencyLimit = round(limit * cpuTotal)
	elif -1 < limit < 0:
		concurrencyLimit = cpuTotal - abs(round(limit * cpuTotal))
	elif limit <= -1:
		concurrencyLimit = cpuTotal - abs(int(limit))

	#https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ProcessPoolExecutor
	if sys.platform == "win32":
		concurrencyLimit = min(concurrencyLimit, 61)
	return max(int(concurrencyLimit), 1)

def intInnit(listInt_Allegedly: Collection[Any], parameterName: str | None = None, parameterType: type[Any] | None = None) -> list[int]:
	"""Validate and convert input values to a `list` of integers.

	(AI generated docstring)

	You can validate a caller's collection before using its values as integers. Integers of any
	magnitude, including integers written as strings, keep every digit. Boolean values and numbers
	with fractional parts are rejected rather than rounded or truncated. Error messages identify
	the incompatible value and provide context about the caller's parameter.

	Parameters
	----------
	listInt_Allegedly : Collection[Any]
		Nonempty collection of integer-compatible values. Accepted elements include `int`, NumPy
		integers, `str`, `float`, `decimal.Decimal`, `fractions.Fraction`, and `complex` values
		with zero imaginary part. Text and decoded `bytes`, `bytearray`, or `memoryview` must
		represent integers. The collection must support `len` and iteration.
	parameterName : str = 'the parameter'
		Name of the caller's parameter for error messages. Omitted text, `None`, and empty text
		use `'the parameter'`.
	parameterType : type[Any] = list
		Type named in error messages. `None` uses `list`. This setting does not restrict the
		accepted collection or element types.

	Returns
	-------
	listValidated : list[int]
		A new `list` containing validated integers in the collection's iteration order.

	Raises
	------
	ValueError
		If the input is `None` or empty, or an element cannot represent an integer exactly.
		Rejected values include `13.5`, `'NW'`, infinity, and `13+1j`.
	TypeError
		If the input has no length or cannot be iterated, or an element is a boolean or an
		incompatible type, such as `None` or a `list`.
	RuntimeError
		If the input has a different length after conversion than before conversion.

	Examples
	--------
	The README validates port numbers supplied as text and integers.

		```python
		from hunterMakesPy.parseParameters import intInnit

		ports = intInnit(["8080", 443, "22"], "server_ports")
		```
	"""
	parameterName = parameterName or 'the parameter'
	parameterType = parameterType or list

	if listInt_Allegedly is None or len(listInt_Allegedly) == 0:  # pyright: ignore[reportUnnecessaryComparison]
		message: str = f"I did not receive a value for `{parameterName}`, but I must have it."
		raise ValueError(message)

	lengthInitial: int = len(listInt_Allegedly)
	listValidated: list[int] = []

	#=SIN= `for` statement: each element is a separate conversion whose failure needs a message about that element.
	for allegedInt in listInt_Allegedly:
		#ruff: ignore[too-many-statements-in-try-clause]
		try:
			#Always rejected as ambiguous
			if isinstance(allegedInt, bool):
				raise TypeError
			number: Any = allegedInt
			if isinstance(number, memoryview):
				number = number.tobytes()
			if isinstance(number, (bytes, bytearray)):
				number = str(charset_normalizer.from_bytes(number).best())
			if isinstance(number, complex):
				if number.imag != 0:
					raise ValueError
				number = number.real
			fraction: Fraction = Fraction(number)
			if fraction.denominator != 1:
				raise ValueError
		except (TypeError, ValueError, ArithmeticError) as ERROR:
			message = (f"I received `{allegedInt = }` of type `{type(allegedInt).__name__}` as an element in a "
				f"`{type(listInt_Allegedly).__name__}`, but `{parameterName}` must have integers in type(s) `{parameterType}`.")
			if isinstance(ERROR, TypeError):
				raise TypeError(message) from ERROR
			raise ValueError(message) from ERROR
		listValidated.append(int(fraction))

	if len(listInt_Allegedly) != lengthInitial:
		message = f"I observed the length of `{parameterName}` change from `{lengthInitial}` to `{len(listInt_Allegedly)}` while I iterated over it."
		raise RuntimeError(message)

	return listValidated

def oopsieKwargsie(huh: Any) -> bool | str | None:
	"""Interpret a `str` as `True`, `False`, or `None` to avoid an `Exception`.

	(AI generated docstring)

	If a calling function passes a `str` to a parameter that should not receive a `str`,
	`oopsieKwargsie` might help you avoid an `Exception`. Text representing `True`, `False`,
	or `None` ignores capitalization and surrounding whitespace. Other text retains its original
	capitalization and whitespace.

	Parameters
	----------
	huh : Any
		The value to interpret. A value other than a `str` is interpreted through its string
		representation. If that representation cannot be obtained, the original value is returned.

	Returns
	-------
	interpretedValue : Any
		`True`, `False`, or `None` for recognized text. Unrecognized text is returned unchanged.
		For an input other than a `str`, unrecognized text is its string representation. If obtaining
		that representation raised an exception, the result is the original `huh`.

	Examples
	--------
	The README interprets configuration values supplied as text.

		```python
		from hunterMakesPy.parseParameters import oopsieKwargsie

		oopsieKwargsie("True")   # Returns True.
		oopsieKwargsie("none")   # Returns None.
		oopsieKwargsie("hello")  # Returns "hello".
		```
	"""
	if not isinstance(huh, str):
		try:
			huh = str(huh)
		#ruff: ignore[blind-except]
		except BaseException:
			return huh
	formatted: str = huh.strip().title()
	if formatted == str(True):
		return True
	if formatted == str(False):
		return False
	if formatted == str(None):
		return None
	return huh
