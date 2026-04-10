"""Manipulate data structures with encoding, extraction, and merging utilities.

(AI generated docstring)

You can use this module to transform NumPy arrays [1] into compact run-length encoded
strings, extract strings from arbitrarily nested data structures, and merge multiple
dictionaries with list values. The module provides specialized utilities for working with
Cartesian mappings, heterogeneous nested data, and dictionary consolidation operations.

The run-length encoding function produces self-decoding string representations optimized for
large arrays with repetitive patterns. The string extraction function recursively traverses
nested structures to collect all convertible string values. The dictionary merging function
consolidates multiple dictionaries while offering optional deduplication and sorting.

Contents
--------
Functions
	autoDecodingRLE
		Transform a NumPy array into a compact, self-decoding run-length encoded string representation.
	stringItUp
		Convert every element in input data structures to strings.
	updateExtendPolishDictionaryLists
		Merge multiple dictionaries with list values into a single dictionary.

References
----------
[1] NumPy - Context7
	https://numpy.org/doc/stable/reference/index.html

"""
from charset_normalizer import CharsetMatch
from collections.abc import Mapping
from humpy_cytoolz.functoolz import identity
from humpy_cytoolz.recipes import partitionby
from hunterMakesPy import Ordinals
from more_itertools import consecutive_groups
from numpy import integer
from numpy.typing import NDArray
from typing import Any, cast
import charset_normalizer
import sys

# TODO refine autoDecodingRLE.
def autoDecodingRLE(arrayTarget: NDArray[integer[Any]], *, assumeAddSpaces: bool = False) -> str:
	"""Transform a NumPy array into a compact, self-decoding run-length encoded string representation.

	This function converts a NumPy array into a string that, when evaluated as Python code, recreates
	the original array structure. The function employs two compression strategies:
	1. Python's `range` syntax for consecutive integer sequences
	2. Multiplication syntax for repeated elements

	The resulting string representation is designed to be both human-readable and space-efficient,
	especially for large cartesian mappings with repetitive patterns. When this string is used as a
	data source, Python will automatically decode it into Python `list`, which if used as an argument
	to `numpy.array()`, will recreate the original array structure.

	Parameters
	----------
	arrayTarget : NDArray[integer[Any]]
		The NumPy array to be encoded.
	assumeAddSpaces : bool = False
		Affects internal length comparison during compression decisions. This parameter doesn't
		directly change output format but influences whether `range` or multiplication syntax is
		preferred in certain cases. The parameter exists because the Abstract Syntax Tree (AST)
		inserts spaces in its string representation.

	Returns
	-------
	encodedString : str
		A string representation of the array using run-length encoding that, when evaluated as Python
		code, reproduces the original array structure.

	Notes
	-----
	The "autoDecoding" feature means that the string representation evaluates directly to the desired
	data structure without explicit decompression steps.

	The encoded string uses only builtins — no imports are needed to decode it.
	"""
	def encodeByRecursion(arraySlice: NDArray[integer[Any]]) -> str:
		if arraySlice.ndim == 0:
			return str(int(arraySlice))
		if arraySlice.ndim == 1:
			return encodeListAsString(arraySlice.tolist())
		return '[' + ','.join(map(encodeByRecursion, arraySlice)) + ']'

	def encodeListAsString(listIntegers: list[int]) -> str:
		listTokens: list[str] = []

		for integersConsecutive in consecutive_groups(listIntegers):
			tupleIntegersConsecutive: tuple[int, ...] = tuple(integersConsecutive)
			integersConsecutiveLength: int = len(tupleIntegersConsecutive)

			if integersConsecutiveLength == 1:
				listTokens.append(str(tupleIntegersConsecutive[0]))
			else:
				start: int = tupleIntegersConsecutive[0]
				stop: int = start + integersConsecutiveLength
				if start == 0:
					startAs_str: str = ''
				else:
					startAs_str = f"{start},"
				stringRangeSyntax: str = f"*range({startAs_str}{stop})"

				stringCommaSeparated: str = ','.join(map(str, tupleIntegersConsecutive))

				if measureStringLength(stringRangeSyntax) < measureStringLength(stringCommaSeparated):
					listTokens.append(stringRangeSyntax)
				else:
					listTokens.append(stringCommaSeparated)

		listSegments: list[str] = []
		listBuffer: list[str] = []

		for tokensIdentical in partitionby(identity, listTokens):
			tokenAs_str: str = tokensIdentical[0]
			countRepetitions: int = len(tokensIdentical)

			if 1 < countRepetitions:
				stringMultiplicationSyntax: str = f"[{tokenAs_str}]*{countRepetitions}"
				stringListSyntax: str = "[" + ",".join([tokenAs_str] * countRepetitions) + "]"
				if measureStringLength(stringMultiplicationSyntax) < measureStringLength(stringListSyntax):
					if listBuffer:
						listSegments.append('[' + ','.join(listBuffer) + ']')
						listBuffer = []
					listSegments.append(stringMultiplicationSyntax)
					continue

			listBuffer.extend([tokenAs_str] * countRepetitions)

		if listBuffer:
			listSegments.append('[' + ','.join(listBuffer) + ']')

		return '+'.join(listSegments)

	def measureStringLength(string: str) -> int:
		"""`assumeAddSpaces` characters: `,` 1; `]*` 2."""
		return len(string) + assumeAddSpaces * (string.count(',') + string.count(']*') * 2)

	return encodeByRecursion(arrayTarget)

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
		elif isinstance(KitKat, memoryview):
			decodedString: CharsetMatch | None = charset_normalizer.from_bytes(KitKat.tobytes()).best()
			if decodedString:
				listStrungUp.append(str(decodedString))
		elif isinstance(KitKat, dict):
			DictDact: dict[Any, Any] = cast(dict[Any, Any], KitKat)
			for broken, piece in DictDact.items():
				drill(broken)
				drill(piece)
		elif isinstance(KitKat, (list, tuple, set, frozenset, range)):
			for kit in KitKat: # pyright: ignore[reportUnknownVariableType]
				drill(kit)
		elif hasattr(KitKat, '__iter__'):  # Unpack other iterables
			for kat in KitKat:
				drill(kat)
		else:
			try:
				sharingIsCaring: str = KitKat.__str__()
				listStrungUp.append(sharingIsCaring)
			except AttributeError:
				pass
			except TypeError:  # "The error traceback provided indicates that there is an issue when calling the __str__ method on an object that does not have this method properly defined, leading to a TypeError."
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

def updateExtendPolishDictionaryLists[小于: Ordinals](*dictionaryLists: Mapping[str, list[小于] | set[小于] | tuple[小于, ...]], destroyDuplicates: bool = False, reorderLists: bool = False, killErroneousDataTypes: bool = False) -> dict[str, list[小于]]:
	"""Merge multiple dictionaries with `list` values into a single dictionary with the `list` values merged.

	Plus options to destroy duplicates, sort `list` values, and handle erroneous data types.

	Parameters
	----------
	*dictionaryLists : Mapping[str, list[Any] | set[Any] | tuple[Any, ...]]
		Variable number of dictionaries to be merged. If only one dictionary is passed, it will be
		"polished".
	destroyDuplicates : bool = False
		If `True`, removes duplicate elements from the `list`. Defaults to `False`.
	reorderLists : bool = False
		If `True`, sorts each `list` value. Defaults to `False`. The elements must be comparable;
		otherwise, a `TypeError` will be raised.
	killErroneousDataTypes : bool = False
		If `True`, suppresses any `TypeError` `Exception` and omits the dictionary key or value that
		caused the `Exception`. Defaults to `False`.

	Returns
	-------
	ePluribusUnum : dict[str, list[Any]]
		A single dictionary with merged and optionally "polished" `list` values.

	Notes
	-----
	The returned value, `ePluribusUnum`, is a so-called primitive dictionary (`dict`). Furthermore,
	every dictionary key is a so-called primitive string (*cf.* `str()`) and every dictionary value
	is a so-called primitive `list` (`list`). If `dictionaryLists` has other data types, the data
	types will not be preserved. That could have unexpected consequences. Conversion from the
	original data type to a `list`, for example, may not preserve the order even if you want the
	order to be preserved.
	"""
	ePluribusUnum: dict[str, list[小于]] = {}

	for dictionaryListTarget in dictionaryLists:
		for keyName, keyValue in dictionaryListTarget.items():
			try:
				ImaStr = str(keyName)
				ImaList: list[小于] = list(keyValue)
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
