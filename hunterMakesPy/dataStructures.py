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
		Collect string representations from nested values.
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
	"""Remove whitespace after commas and inside parentheses or square brackets.

	(AI generated docstring)

	Parameters
	----------
	string : str
		Text to compact. Whitespace inside quoted text is affected too, so use this operation
		only when that whitespace can be removed without changing the intended meaning.

	Returns
	-------
	stringCompacted : str
		Text without whitespace immediately after commas, opening parentheses, or opening
		square brackets, or immediately before closing parentheses or closing square brackets.
	"""
	commas: str = regex.sub(r',\s+', ',', string)
	bracketsOpening: str = regex.sub(r'([\[\(])\s+', r'\1', commas)
	return regex.sub(r'\s+([\]\)])', r'\1', bracketsOpening)

def autoDecodingRLE(arrayTarget: NDArray[integer[Any]], *, assumeAddSpaces: bool = False) -> str:
	"""Transform a NumPy integer array into a compact, self-decoding Python expression.

	(AI generated docstring)

	You can convert a NumPy integer array into text that, when evaluated as Python code, reproduces
	`arrayTarget.tolist()`. You can create a NumPy array, a PyTorch tensor, or another array-like
	object from the decoded value. The RLE (Run-Length Encoding) text does not need a decoder
	function; it is native Python syntax using unpacked `range` expressions for consecutive integers
	and list multiplication for repeated elements.

	The resulting text is minified Python code, so it is space-efficient and, hypothetically,
	human-readable.

	Parameters
	----------
	arrayTarget : NDArray[integer[Any]]
		The NumPy integer array to encode. A zero-dimensional array produces a scalar expression;
		all other arrays produce a list expression.
	assumeAddSpaces : bool = False
		Whether encoding choices should account for spaces that `ast.unparse` or a Python
		formatter may insert. `True` estimates one space per comma and two spaces around
		multiplication after `]`. The returned expression remains compact in either mode.

	Returns
	-------
	encodedString : str
		A Python expression representing `arrayTarget.tolist()`. The expression does not store
		NumPy dtype or shape metadata, including dimensions beyond an empty axis.
	"""
	def sliceNDArrayToNestedLists(arraySlice: NDArray[integer[Any]]) -> Any:
		def getLengthOption(optionAsStr: str) -> int:
			"""I use this estimate to compare encoding lengths with optional formatter spaces.

			(AI generated docstring)

			The estimate includes one extra space per comma and two extra spaces per `]*` when
			`assumeAddSpaces` is `True`.
			"""
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
		r"(?P<joinAhead>,)\((?P<malkovich>-?\d+|range\(-?\d+,-?\d+\)),(?P<multiply>\d+)\)(?P<bracketBehind>])|"
		#Pattern 2: Bracket or start ahead, comma behind
		r"(?P<bracketOrStartAhead>\[|^.)\((?P<malkovichMalkovich>-?\d+|range\(-?\d+,-?\d+\)),(?P<multiplyIDK>\d+)\)(?P<joinBehind>,)|"
		#Pattern 3: Bracket ahead, bracket behind
		r"(?P<bracketAhead>\[)\((?P<malkovichMalkovichMalkovich>-?\d+|range\(-?\d+,-?\d+\)),(?P<multiply_whatever>\d+)\)(?P<bracketBehindBracketBehind>])|"
		#Pattern 4: Comma ahead, comma behind
		r"(?P<joinAheadJoinAhead>,)\((?P<malkovichMalkovichMalkovichMalkovich>-?\d+|range\(-?\d+,-?\d+\)),(?P<multiplyOrSomething>\d+)\)(?P<joinBehindJoinBehind>,)"
		r")"
	)

	def replacementByContext(match: regex.Match[str]) -> str:
		"""I use this replacement to express a repeated value with Python list multiplication.

		(AI generated docstring)

		The replacement joins the repeated list with any surrounding list elements so that
		the resulting expression preserves the decoded values and their order.
		"""
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

	(AI generated docstring)

	You can collect text from nested inputs into a flat `list`. Dictionaries contribute both keys
	and values. Strings contribute their full text, and callables contribute their names.

	Parameters
	----------
	*scrapPile : Any
		(scrap2pile) Values or nested data structures to unpack and convert. No arguments produce
		an empty `list`. `bytes` and `bytearray` contribute their Python string representations.
		A `memoryview` contributes decoded text when text decoding succeeds. Other iterables
		contribute their elements and are consumed.

	Returns
	-------
	listStrungUp : list[str]
		(list2strung2up) A flat `list` of string representations. The result follows argument order
		and container iteration order. Unordered containers can make the result order unpredictable.

	Incomplete Conversion
	---------------------
	Other non-iterable values contribute their string representations. String conversion that
	returns `None` or raises `AttributeError` or `TypeError` omits those values. Other exceptions
	from that conversion produce a diagnostic on `sys.stderr` and propagate.

	If recursive input exceeds Python's recursion limit, the result retains text already collected
	and appends `repr` of the current top-level argument. Later arguments are not processed.

	Examples
	--------
	The README collects text from nested user and configuration data.

		```python
		from hunterMakesPy.dataStructures import stringItUp

		strings = stringItUp({"users": ["alice"], "config": {"host": "localhost"}})
		# Returns ["users", "alice", "config", "host", "localhost"].
		```
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
				sharingIsCaring: str | None = KitKat.__str__()
				if sharingIsCaring is not None:
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

	(AI generated docstring)

	You can use this function to combine values under matching keys across `dictionaryLists`.
	You receive a new dictionary with new lists and can remove duplicate elements, sort elements,
	or skip entries that raise `TypeError` during merging.

	Input Consumption
	-----------------
	The input mappings and reusable value containers remain unchanged. Iterable values such as
	generators are consumed. Each result list retains references to the original elements.

	Parameters
	----------
	*dictionaryLists : Mapping[文件, Iterable[文义]]
		The mappings to merge, with hashable keys and iterable values. A single mapping receives
		the same conversion and optional processing. Omitting all mappings produces an empty
		dictionary. Strings contribute individual characters. Mapping values contribute their keys.
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
		The merged dictionary, with a new list for every retained key. Mapping argument order and
		each value's iteration order determine element order unless `reorderLists` is `True`.
		Unordered inputs, such as sets, may produce unpredictable element order.

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
