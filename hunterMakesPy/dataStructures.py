"""Manipulate data structures with encoding, extraction, and merging utilities.

You can use this module to encode integer arrays as compact Python expressions, extract strings
from nested data, normalize whitespace in representations of Python data, and merge mappings of
iterable values into dictionaries of lists.

Contents
--------
Functions
	autoDecodingRLE
		Encode an integer array as a compact Python expression.
	removeExtraWhitespace
		Remove whitespace after commas and inside parentheses or square brackets.
	stringItUp
		Convert every element in input data structures to strings.
	updateExtendPolishDictionaryLists
		Merge iterable values into lists with optional deduplication and sorting.
"""
from __future__ import annotations

from charset_normalizer import CharsetMatch
from humpy_cytoolz.dicttoolz import valmap as mapValues
from humpy_cytoolz.functoolz import compose
from types import FunctionType
from typing import cast, overload, TYPE_CHECKING
import charset_normalizer
import more_itertools
import re as regex
import sys

if TYPE_CHECKING:
	from collections.abc import Callable, Iterable, Iterator, Mapping
	from hunterMakesPy import 小于, 文义, 文件
	from numpy import integer
	from numpy.typing import NDArray
	from typing import Any, Literal

def removeExtraWhitespace(string: str) -> str:
	#ruff: ignore[docstring-missing-returns]
	"""Remove extra whitespace from string representation of Python data structures."""
	commas: str = regex.sub(r',\s+', ',', string)
	bracketsOpening: str = regex.sub(r'([\[\(])\s+', r'\1', commas)
	return regex.sub(r'\s+([\]\)])', r'\1', bracketsOpening)

def autoDecodingRLE(arrayTarget: NDArray[integer[Any]], *, assumeAddSpaces: bool = False) -> str:
	"""Transform a NumPy array into a compact, self-decoding run-length encoded string representation.

	Use this function to convert a NumPy array into a string that, when evaluated as Python code,
	creates a list or nested lists representing the original array structure. You can create a NumPy
	array, torch Tensor, or other array-like object with the auto-decoded list of lists. The RLE
	(Run-Length Encoding) string does _not_ need a decoder function: it is native Python syntax. The
	function employs two encoding strategies: 1. Python `range` syntax for consecutive integer
	sequences. 2. Multiplication syntax for repeated elements.

	The resulting string representation is merely minified Python code, so it is space-efficient and,
	hypothetically, human-readable.

	Parameters
	----------
	arrayTarget : NDArray[integer[Any]]
		The NumPy array to be encoded.
	assumeAddSpaces : bool = False
		Affects internal length comparison during compression decisions. This parameter doesn't
		directly change the output: instead, use it to assume that something else will add spaces,
		such as `ast.unparse()` (Abstract Syntax Tree) or a Python formatter.

	Returns
	-------
	encodedString : str
		A string representation of the array using run-length encoding that, when evaluated as Python
		code, reproduces the original array structure.
	"""
	def sliceNDArrayToNestedLists(arraySlice: NDArray[integer[Any]]) -> Any:
		def getLengthOption(optionAsStr: str) -> int:
			#ruff: ignore[docstring-missing-returns]
			"""`assumeAddSpaces` characters: `,` 1 space; `]*` 2 spaces."""
			return assumeAddSpaces * (optionAsStr.count(',') + optionAsStr.count(']*') * 2) + len(optionAsStr)

		if 1 < arraySlice.ndim:
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
					ImaRange: list[range] = [range(ImaSerious[0], ImaSerious[-1] + 1)]
					ImaRangeAsStr: str = removeExtraWhitespace(str(ImaRange)).replace('range(0,', 'range(').replace('range', '*range')

					option1 = ImaRange
					option1AsStr = ImaRangeAsStr
					option2 = ImaSerious
					option2AsStr: str | None = None

					option1AsStr: str = option1AsStr or removeExtraWhitespace(str(option1))
					lengthOption1: int = getLengthOption(option1AsStr)

					option2AsStr = option2AsStr or removeExtraWhitespace(str(option2))
					lengthOption2: int = getLengthOption(option2AsStr)

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
					lengthMalkovich: int = malkovichGrouped[-1]
					malkovichAsList: list[int | range] = list(more_itertools.run_length.decode([malkovichGrouped]))
					malkovichMalkovich: str = f"[{malkovichGrouped[0]}]*{lengthMalkovich}"

					option1 = [malkovichGrouped]
					option1AsStr = malkovichMalkovich
					option2 = malkovichAsList
					option2AsStr = None

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

	arrayAsStr: str = removeExtraWhitespace(str(arrayAsNestedLists))

	patternRegex: regex.Pattern[str] = regex.compile(
		r"(?<!rang)(?:"
		#Pattern 1: Comma ahead, bracket behind
		r"(?P<joinAhead>,)\((?P<malkovich>\d+),(?P<multiply>\d+)\)(?P<bracketBehind>])|"
		#Pattern 2: Bracket or start ahead, comma behind
		r"(?P<bracketOrStartAhead>\[|^.)\((?P<malkovichMalkovich>\d+),(?P<multiplyIDK>\d+)\)(?P<joinBehind>,)|"
		#Pattern 3: Bracket ahead, bracket behind
		r"(?P<bracketAhead>\[)\((?P<malkovichMalkovichMalkovich>\d+),(?P<multiply_whatever>\d+)\)(?P<bracketBehindBracketBehind>])|"
		#Pattern 4: Comma ahead, comma behind
		r"(?P<joinAheadJoinAhead>,)\((?P<malkovichMalkovichMalkovichMalkovich>\d+),(?P<multiplyOrSomething>\d+)\)(?P<joinBehindJoinBehind>,)"
		r")"
	)

	def replacementByContext(match: regex.Match[str]) -> str:
		#ruff: ignore[docstring-missing-returns]
		"""Generate replacement string based on context patterns."""
		elephino: dict[str, str | None] = match.groupdict()
		joinAhead: str | None = elephino.get('joinAhead') or elephino.get('joinAheadJoinAhead')
		malkovich: str | None = elephino.get('malkovich') or elephino.get('malkovichMalkovich') or elephino.get('malkovichMalkovichMalkovich') or elephino.get('malkovichMalkovichMalkovichMalkovich')
		multiply: str | None = elephino.get('multiply') or elephino.get('multiplyIDK') or elephino.get('multiply_whatever') or elephino.get('multiplyOrSomething')
		joinBehind: str | None = elephino.get('joinBehind') or elephino.get('joinBehindJoinBehind')

		replaceAhead: str = "]+[" if joinAhead == "," else "["

		replaceBehind: str = "+[" if joinBehind == "," else ""

		return f"{replaceAhead}{malkovich}]*{multiply}{replaceBehind}"

	arrayAsStr = patternRegex.sub(replacementByContext, arrayAsStr)
	arrayAsStr = patternRegex.sub(replacementByContext, arrayAsStr)

	#.replace `range(0,stop)` syntax with `range(stop)` syntax.
	#Add unpack operator `*` for automatic decoding when evaluated.
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
	scrap: Any = None
	listStrungUp: list[str] = []

	def drill(KitKat: Any) -> None:
		if isinstance(KitKat, str):
			listStrungUp.append(KitKat)
		elif (KitKat is None) or (isinstance(KitKat, (bool, bytearray, bytes, complex, float, int))):
			listStrungUp.append(str(KitKat))
		elif callable(KitKat):
			if isinstance(KitKat, FunctionType):
				listStrungUp.append(KitKat.__name__)
			else:
				listStrungUp.append(getattr(KitKat, '__name__', type(KitKat).__name__))
		elif isinstance(KitKat, memoryview):
			decodedString: CharsetMatch | None = charset_normalizer.from_bytes(KitKat.tobytes()).best()
			if decodedString:
				listStrungUp.append(str(decodedString))
		elif isinstance(KitKat, dict):
			DictDact: dict[Any, Any] = cast('dict[Any, Any]', KitKat)
			for broken, piece in DictDact.items():
				drill(broken)
				drill(piece)
		elif isinstance(KitKat, (list, tuple, set, frozenset, range)):
			for kit in KitKat:  # pyright: ignore[reportUnknownVariableType]
				drill(kit)
		elif hasattr(KitKat, '__iter__'):
			for kat in KitKat:
				drill(kat)
		else:
			try:
				#ruff: ignore[unnecessary-dunder-call]
				sharingIsCaring: str = KitKat.__str__()
				listStrungUp.append(sharingIsCaring)
			except AttributeError:
				pass
			except TypeError:
				#"The error traceback provided indicates that there is an issue when calling the __str__ method on an object that does not have this method properly defined, leading to a TypeError."
				pass
			except:
				message: str = (f"\nWoah! I received '{repr(KitKat)}'.\nTheir report card says, 'Plays well with others: Needs improvement.'\n")
				sys.stderr.write(message)
				raise
	try:
		for scrap in scrapPile:
			drill(scrap)
	except RecursionError:
		listStrungUp.append(repr(scrap))
	return listStrungUp

@overload
def updateExtendPolishDictionaryLists(*dictionaryLists: Mapping[文件, Iterable[文义]], destroyDuplicates: bool = False, reorderLists: Literal[False] = False, killErroneousDataTypes: bool = False) -> dict[文件, list[文义]]: ...

@overload
def updateExtendPolishDictionaryLists(*dictionaryLists: Mapping[文件, Iterable[小于]], destroyDuplicates: bool = False, reorderLists: Literal[True], killErroneousDataTypes: bool = False) -> dict[文件, list[小于]]: ...

@overload
def updateExtendPolishDictionaryLists(*dictionaryLists: Mapping[文件, Iterable[小于]], destroyDuplicates: bool = False, reorderLists: bool, killErroneousDataTypes: bool = False) -> dict[文件, list[小于]]: ...

def updateExtendPolishDictionaryLists(*dictionaryLists: Mapping[文件, Iterable[文义]], destroyDuplicates: bool = False, reorderLists: bool = False, killErroneousDataTypes: bool = False) -> dict[文件, list[文义]]:
	"""Merge mappings of iterable values into a dictionary of lists.

	You can use this function to combine values under matching keys across `dictionaryLists`.
	This function returns a new dictionary with new lists and can remove duplicate elements,
	sort elements, or skip entries that raise `TypeError` during merging.

	Iteration and Ordering
	----------------------
	This function consumes each value's iterable in mapping argument order. Within each value,
	the list follows the iterable's order, which may be unpredictable for sets. Strings contribute
	individual characters, and mapping values contribute their keys.

	Deduplication uses `dict.fromkeys` [1] to preserve first occurrences. Sorting uses `sorted` [2]
	and runs after deduplication. Every retained value becomes a list regardless of the input type.

	Parameters
	----------
	*dictionaryLists : Mapping[文件, Iterable[文义]]
		The mappings to merge, with hashable keys and iterable values. A single mapping receives
		the same conversion and optional processing. No mappings produce an empty dictionary.
	destroyDuplicates : bool = False
		If `True`, remove duplicate elements from each merged list, preserving the first occurrence.
		Elements must be hashable when this option is enabled.
	reorderLists : bool = False
		If `True`, sort each merged list in ascending order after optional deduplication.
		Elements within each list must be mutually comparable.
	killErroneousDataTypes : bool = False
		If `True`, skip an entry when converting the entry's value to a list or merging the entry
		raises `TypeError`. Successfully merged values for the same key remain in the result.
		This option does not suppress `TypeError` from deduplication or sorting.

	Returns
	-------
	ePluribusUnum : dict[文件, list[文义]]
		The merged dictionary, with a list for every retained key. This function does not modify
		the input mappings or their containers, but the lists retain references to the original elements.

	Raises
	------
	TypeError
		If a value cannot be iterated or an entry cannot be merged and `killErroneousDataTypes`
		is `False`. Also raised for unhashable elements during deduplication or incomparable
		elements during sorting, regardless of `killErroneousDataTypes`.

	Examples
	--------
	The README merges server lists while preserving the first occurrence of each server name.

		```python
		from hunterMakesPy.dataStructures import updateExtendPolishDictionaryLists

		merged = updateExtendPolishDictionaryLists(
			{"servers": ["chicago"]},
			{"servers": ["tokyo", "chicago"]},
			destroyDuplicates=True,
		)
		# Returns {"servers": ["chicago", "tokyo"]}.
		```

	References
	----------
	[1] Python dictionaries and `dict.fromkeys`.
		https://docs.python.org/3/library/stdtypes.html#dict.fromkeys
	[2] Python `sorted`.
		https://docs.python.org/3/library/functions.html#sorted
	"""
	ePluribusUnum: dict[文件, list[文义]] = {}

	for dictionaryListTarget in dictionaryLists:
		for keyName, keyValue in dictionaryListTarget.items():
			try:
				ImaList: list[文义] = list(keyValue)
				ePluribusUnum.setdefault(keyName, []).extend(ImaList)
			except TypeError as error:
				if killErroneousDataTypes:
					continue
				raise TypeError from error

	if destroyDuplicates:
		ePluribusUnum = mapValues(compose(list, dict.fromkeys), ePluribusUnum)
	if reorderLists:
		#=SIN= `sorted` is broken.
		ePluribusUnum = mapValues(cast('Callable[[list[文义]], list[文义]]', sorted), ePluribusUnum)

	return ePluribusUnum
