"""Provides utilities for string extraction from nested data structures and merges multiple dictionaries containing lists into one dictionary."""

from collections.abc import Mapping
from numpy import integer
from numpy.typing import NDArray
from typing import Any, Protocol, TYPE_CHECKING, TypeVar
import more_itertools
import re as regex

if TYPE_CHECKING:
	from collections.abc import Iterator

def removeExtraWhitespace(text: str) -> str:
	"""Remove extra whitespace from string representation of Python data structures."""
	# Remove spaces after commas
	text = regex.sub(r',\s+', ',', text)
	# Remove spaces after opening brackets/parens
	text = regex.sub(r'([\[\(])\s+', r'\1', text)
	# Remove spaces before closing brackets/parens
	return regex.sub(r'\s+([\]\)])', r'\1', text)

def autoDecodingRLE(arrayTarget: NDArray[integer[Any]], *, assumeAddSpaces: bool = False) -> str:
	"""Transform a NumPy array into a compact, self-decoding run-length encoded string representation.

	This function converts a NumPy array into a string that, when evaluated as Python code,
	recreates the original array structure. The function employs two compression strategies:
	1. Python's `range` syntax for consecutive integer sequences
	2. Multiplication syntax for repeated elements

	The resulting string representation is designed to be both human-readable and space-efficient,
	especially for large cartesian mappings with repetitive patterns. When this string is used
	as a data source, Python will automatically decode it into Python `list`, which if used as an
	argument to `numpy.array()`, will recreate the original array structure.

	Parameters
	----------
	arrayTarget : NDArray[integer[Any]]
		(array2target) The NumPy array to be encoded.
	assumeAddSpaces : bool = False
		(assume2add2spaces) Affects internal length comparison during compression decisions.
		This parameter doesn't directly change output format but influences whether
		`range` or multiplication syntax is preferred in certain cases. The parameter
		exists because the Abstract Syntax Tree (AST) inserts spaces in its string
		representation.

	Returns
	-------
	rleString : str
		(rle2string) A string representation of the array using run-length encoding that,
		when evaluated as Python code, reproduces the original array structure.

	Notes
	-----
	The "autoDecoding" feature means that the string representation evaluates directly
	to the desired data structure without explicit decompression steps.

	"""
	def sliceNDArrayToNestedLists(arraySlice: NDArray[integer[Any]]) -> Any:
		def getLengthOption(optionAsStr: str) -> int:
			"""`assumeAddSpaces` characters: `,` 1; `]*` 2."""
			return assumeAddSpaces * (optionAsStr.count(',') + optionAsStr.count(']*') * 2) + len(optionAsStr)

		if arraySlice.ndim > 1:
			axisOfOperation = 0
			return [sliceNDArrayToNestedLists(arraySlice[index]) for index in range(arraySlice.shape[axisOfOperation])]
		if arraySlice.ndim == 1:
			arraySliceAsList: list[int | range] = []
			cache_consecutiveGroup_addMe: dict[Iterator[Any], list[int] | list[range]] = {}
			for consecutiveGroup in more_itertools.consecutive_groups(arraySlice.tolist()):
				if consecutiveGroup in cache_consecutiveGroup_addMe:
					addMe = cache_consecutiveGroup_addMe[consecutiveGroup]
				else:
					ImaSerious: list[int] = list(consecutiveGroup)
					ImaRange = [range(ImaSerious[0], ImaSerious[-1] + 1)]
					ImaRangeAsStr = removeExtraWhitespace(str(ImaRange)).replace('range(0,', 'range(').replace('range', '*range')

					option1 = ImaRange
					option1AsStr = ImaRangeAsStr
					option2 = ImaSerious
					option2AsStr = None

					# alpha, potential function
					option1AsStr = option1AsStr or removeExtraWhitespace(str(option1))
					lengthOption1 = getLengthOption(option1AsStr)

					option2AsStr = option2AsStr or removeExtraWhitespace(str(option2))
					lengthOption2 = getLengthOption(option2AsStr)

					if lengthOption1 < lengthOption2:
						addMe = option1
					else:
						addMe = option2

					cache_consecutiveGroup_addMe[consecutiveGroup] = addMe

				arraySliceAsList += addMe

			listRangeAndTuple: list[int | range | tuple[int | range, int]] = []
			cache_malkovichGrouped_addMe: dict[tuple[int | range, int], list[tuple[int | range, int]] | list[int | range]] = {}
			for malkovichGrouped in more_itertools.run_length.encode(arraySliceAsList):
				if malkovichGrouped in cache_malkovichGrouped_addMe:
					addMe = cache_malkovichGrouped_addMe[malkovichGrouped]
				else:
					lengthMalkovich = malkovichGrouped[-1]
					malkovichAsList = list(more_itertools.run_length.decode([malkovichGrouped]))
					malkovichMalkovich = f"[{malkovichGrouped[0]}]*{lengthMalkovich}"

					option1 = [malkovichGrouped]
					option1AsStr = malkovichMalkovich
					option2 = malkovichAsList
					option2AsStr = None

					# beta, potential function
					option1AsStr = option1AsStr or removeExtraWhitespace(str(option1))
					lengthOption1 = getLengthOption(option1AsStr)

					option2AsStr = option2AsStr or removeExtraWhitespace(str(option2))
					lengthOption2 = getLengthOption(option2AsStr)

					if lengthOption1 < lengthOption2:
						addMe = option1
					else:
						addMe = option2

					cache_malkovichGrouped_addMe[malkovichGrouped] = addMe

				listRangeAndTuple += addMe

			return listRangeAndTuple
		return arraySlice

	arrayAsNestedLists = sliceNDArrayToNestedLists(arrayTarget)

	arrayAsStr = removeExtraWhitespace(str(arrayAsNestedLists))

	patternRegex = regex.compile(
		"(?<!rang)(?:"
		# Pattern 1: Comma ahead, bracket behind  # noqa: ERA001
		"(?P<joinAhead>,)\\((?P<malkovich>\\d+),(?P<multiply>\\d+)\\)(?P<bracketBehind>])|"
		# Pattern 2: Bracket or start ahead, comma behind  # noqa: ERA001
		"(?P<bracketOrStartAhead>\\[|^.)\\((?P<malkovichMalkovich>\\d+),(?P<multiplyIDK>\\d+)\\)(?P<joinBehind>,)|"
		# Pattern 3: Bracket ahead, bracket behind  # noqa: ERA001
		"(?P<bracketAhead>\\[)\\((?P<malkovichMalkovichMalkovich>\\d+),(?P<multiply_whatever>\\d+)\\)(?P<bracketBehindBracketBehind>])|"
		# Pattern 4: Comma ahead, comma behind  # noqa: ERA001
		"(?P<joinAheadJoinAhead>,)\\((?P<malkovichMalkovichMalkovichMalkovich>\\d+),(?P<multiplyOrSomething>\\d+)\\)(?P<joinBehindJoinBehind>,)"
		")"
	)

	def replacementByContext(match: regex.Match[str]) -> str:
		"""Generate replacement string based on context patterns."""
		elephino = match.groupdict()
		joinAhead = elephino.get('joinAhead') or elephino.get('joinAheadJoinAhead')
		malkovich = elephino.get('malkovich') or elephino.get('malkovichMalkovich') or elephino.get('malkovichMalkovichMalkovich') or elephino.get('malkovichMalkovichMalkovichMalkovich')
		multiply = elephino.get('multiply') or elephino.get('multiplyIDK') or elephino.get('multiply_whatever') or elephino.get('multiplyOrSomething')
		joinBehind = elephino.get('joinBehind') or elephino.get('joinBehindJoinBehind')

		replaceAhead = "]+[" if joinAhead == "," else "["

		replaceBehind = "+[" if joinBehind == "," else ""

		return f"{replaceAhead}{malkovich}]*{multiply}{replaceBehind}"

	arrayAsStr = patternRegex.sub(replacementByContext, arrayAsStr)
	arrayAsStr = patternRegex.sub(replacementByContext, arrayAsStr)

	# Replace `range(0,stop)` syntax with `range(stop)` syntax.  # noqa: ERA001
	# Add unpack operator `*` for automatic decoding when evaluated.
	return arrayAsStr.replace('range(0,', 'range(').replace('range', '*range')

def stringItUp(*scrapPile: Any) -> list[str]:
	"""Convert, if possible, every element in the input data structure to a string.

	Order is not preserved or readily predictable.

	Parameters
	----------
	*scrapPile : Any
		(scrap2pile) One or more data structures to unpack and convert to strings.

	Returns
	-------
	listStrungUp : list[str]
		(list2strung2up) A `list` of string versions of all convertible elements.

	"""
	scrap = None
	listStrungUp: list[str] = []

	def drill(KitKat: Any) -> None:
		match KitKat:
			case str():
				listStrungUp.append(KitKat)
			case bool() | bytearray() | bytes() | complex() | float() | int() | memoryview() | None:
				listStrungUp.append(str(KitKat))
			case dict():
				for broken, piece in KitKat.items():
					drill(broken)
					drill(piece)
			case list() | tuple() | set() | frozenset() | range():
				for kit in KitKat:
					drill(kit)
			case _:
				if hasattr(KitKat, '__iter__'):  # Unpack other iterables
					for kat in KitKat:
						drill(kat)
				else:
					try:
						sharingIsCaring = KitKat.__str__()
						listStrungUp.append(sharingIsCaring)
					except AttributeError:
						pass
					except TypeError:  # "The error traceback provided indicates that there is an issue when calling the __str__ method on an object that does not have this method properly defined, leading to a TypeError."
						pass
					except:
						print(f"\nWoah! I received '{repr(KitKat)}'.\nTheir report card says, 'Plays well with others: Needs improvement.'\n")  # noqa: T201
						raise
	try:
		for scrap in scrapPile:
			drill(scrap)
	except RecursionError:
		listStrungUp.append(repr(scrap))
	return listStrungUp

class Ordinals(Protocol):
	"""Protocol for types that support ordering comparisons."""

	def __le__(self, other: "Ordinals", /) -> bool:
		"""Less than or equal to comparison."""
		...
	def __ge__(self, other: "Ordinals", /) -> bool:
		"""Greater than or equal to comparison."""
		...

小于 = TypeVar('小于', bound=Ordinals)

def updateExtendPolishDictionaryLists(*dictionaryLists: Mapping[str, list[小于] | set[小于] | tuple[小于, ...]], destroyDuplicates: bool = False, reorderLists: bool = False, killErroneousDataTypes: bool = False) -> dict[str, list[小于]]:
	"""Merge multiple dictionaries with `list` values into a single dictionary with the `list` values merged.

	Plus options to destroy duplicates, sort `list` values, and handle erroneous data types.

	Parameters
	----------
	*dictionaryLists : Mapping[str, list[Any] | set[Any] | tuple[Any, ...]]
		Variable number of dictionaries to be merged. If only one dictionary is passed, it will be "polished".
	destroyDuplicates : bool = False
		If `True`, removes duplicate elements from the `list`. Defaults to `False`.
	reorderLists : bool = False
		If `True`, sorts each `list` value. Defaults to `False`. The elements must be comparable; otherwise, a `TypeError` will be raised.
	killErroneousDataTypes : bool = False
		If `True`, suppresses any `TypeError` `Exception` and omits the dictionary key or value that caused the `Exception`.
		Defaults to `False`.

	Returns
	-------
	ePluribusUnum : dict[str, list[Any]]
		A single dictionary with merged and optionally "polished" `list` values.

	Notes
	-----
	The returned value, `ePluribusUnum`, is a so-called primitive dictionary (`dict`). Furthermore, every dictionary key is a
	so-called primitive string (*cf.* `str()`) and every dictionary value is a so-called primitive `list` (`list`). If
	`dictionaryLists` has other data types, the data types will not be preserved. That could have unexpected consequences.
	Conversion from the original data type to a `list`, for example, may not preserve the order even if you want the order to be
	preserved.

	"""
	ePluribusUnum: dict[str, list[小于]] = {}

	for dictionaryListTarget in dictionaryLists:
		for keyName, keyValue in dictionaryListTarget.items():
			try:
				ImaStr = str(keyName)
				ImaList = list(keyValue)
				ePluribusUnum.setdefault(ImaStr, []).extend(ImaList)
			except TypeError:
				if killErroneousDataTypes:
					continue
				else:
					raise

	if destroyDuplicates:
		for ImaStr, ImaList in ePluribusUnum.items():
			ePluribusUnum[ImaStr] = list(dict.fromkeys(ImaList))
	if reorderLists:
		for ImaStr, ImaRichComparisonSupporter in ePluribusUnum.items():
			ePluribusUnum[ImaStr] = sorted(ImaRichComparisonSupporter)

	return ePluribusUnum
