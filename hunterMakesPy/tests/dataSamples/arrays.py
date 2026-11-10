"""Integer arrays named by structure: consecutive ranges, repeated values, and multidimensional patterns.

No consumer may mutate these arrays: every test in a session shares each object.
"""
from __future__ import annotations

from typing import TYPE_CHECKING
import numpy
import pytest

if TYPE_CHECKING:
	from _pytest.mark.structures import ParameterSet
	from numpy.typing import NDArray

#================== Zero dimensions and empty arrays =============================================================================

arrayEmpty: NDArray[numpy.int64] = numpy.array([], dtype=numpy.int64)
arrayScalarFibonacci: NDArray[numpy.int64] = numpy.array(233)

#================== One dimension ================================================================================================

arrayRange: NDArray[numpy.int64] = numpy.arange(50, 60)
arrayRangeNegative: NDArray[numpy.int64] = numpy.arange(-34, 35)
arrayRangeRange: NDArray[numpy.int64] = numpy.array([*range(461, 471), *range(479, 487)])
arrayRangeRepeat: NDArray[numpy.int64] = numpy.array([*range(251, 257), 271, 271, 271])
arrayRangeRun: NDArray[numpy.int64] = numpy.tile(numpy.arange(-5, 5), 3)
arrayRangeValue: NDArray[numpy.int64] = numpy.array([*range(91, 97), 101])
arrayRepeat: NDArray[numpy.int64] = numpy.array([191, 191, 191])
arrayRepeatRange: NDArray[numpy.int64] = numpy.array([373, 373, 373, *range(383, 389)])
arrayRepeatRangeValue: NDArray[numpy.int64] = numpy.array([*[401] * 7, *range(409, 415), 421])
arrayRepeatRepeatValue: NDArray[numpy.int64] = numpy.array([313, 313, 313, 331, 331, 349])
arrayRunsFibonacci: NDArray[numpy.int64] = numpy.array([3, 3, 3, 3, 8, 8, 13, 13, 13, 13, 13, 21])
arrayValueRange: NDArray[numpy.int64] = numpy.array([123, *range(71, 81)])
arrayValueRangeRepeat: NDArray[numpy.int64] = numpy.array([281, *range(291, 297), 307, 307])
arrayValueRangeRunValue: NDArray[numpy.int64] = numpy.array([97, *range(-5, 5), *range(-5, 5), *range(-5, 5), 97])
arrayValueRangeValue: NDArray[numpy.int64] = numpy.array([151, *range(163, 171), 181])
arrayValueRepeat: NDArray[numpy.int64] = numpy.array([211, 223, 223, 223])
arrayValueRepeatNegative: NDArray[numpy.int64] = numpy.array([5, -3, -3, -3])

#================== Multiple dimensions ==========================================================================================

array2x2x2Primes: NDArray[numpy.int64] = numpy.array([[[541, 547], [557, 563]], [[569, 571], [577, 587]]])
array2x3Primes: NDArray[numpy.int64] = numpy.array([[491, 499, 503], [509, 521, 523]])
array2x3x5Range: NDArray[numpy.int64] = numpy.arange(2 * 3 * 5).reshape(2, 3, 5)
array3x20RangeRun: NDArray[numpy.int64] = numpy.tile(numpy.arange(10), (3, 2))
array8x8Checkerboard: NDArray[numpy.int32] = (numpy.indices((8, 8)).sum(axis=0) % 2).astype(numpy.int32)
array10x12Stripes: NDArray[numpy.int64] = numpy.repeat(numpy.arange(10)[:, None] // 2, 12, axis=1)
array13x9Saddle: NDArray[numpy.int64] = (numpy.arange(13)[:, None] - 6) ** 2 - (numpy.arange(9)[None, :] - 4) ** 2
array100x100Modular: NDArray[numpy.int64] = ((numpy.arange(100)[:, None] * 13) % 7 + (numpy.arange(100)[None, :] * 17) % 11) % 10

# Bin edges of `librosa.filters.mel(sr=44100, n_fft=2048, n_mels=60)`: mel band 次Band is nonzero from edge 次Band to edge 次Band + 2.
edgesMelBands44100Hz: NDArray[numpy.int64] = numpy.array((
	1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 53, 56, 60, 65, 69, 74, 79, 84, 90, 97, 103, 110, 118, 126
	, 135, 145, 155, 165, 177, 189, 203, 217, 232, 248, 265, 284, 304, 325, 348, 372, 398, 426, 455, 487, 521, 558, 597, 638, 683
	, 731, 782, 836, 895, 958, 1025
))
array60x1025MelMask: NDArray[numpy.int32] = (
	(edgesMelBands44100Hz[:-2, None] <= numpy.arange(1025)) & (numpy.arange(1025) < edgesMelBands44100Hz[2:, None])
).astype(numpy.int32)

#================== Corpus =======================================================================================================

boxOfArraysInteger: tuple[ParameterSet, ...] = (
	pytest.param(array2x2x2Primes, id='array2x2x2Primes'),
	pytest.param(array2x3Primes, id='array2x3Primes'),
	pytest.param(array2x3x5Range, id='array2x3x5Range'),
	pytest.param(array3x20RangeRun, id='array3x20RangeRun'),
	pytest.param(array8x8Checkerboard, id='array8x8Checkerboard'),
	pytest.param(array10x12Stripes, id='array10x12Stripes'),
	pytest.param(array13x9Saddle, id='array13x9Saddle'),
	pytest.param(array60x1025MelMask, id='array60x1025MelMask'),
	pytest.param(array100x100Modular, id='array100x100Modular'),
	pytest.param(arrayEmpty, id='arrayEmpty'),
	pytest.param(arrayRange, id='arrayRange'),
	pytest.param(arrayRangeNegative, id='arrayRangeNegative'),
	pytest.param(arrayRangeRange, id='arrayRangeRange'),
	pytest.param(arrayRangeRepeat, id='arrayRangeRepeat'),
	pytest.param(arrayRangeRun, id='arrayRangeRun'),
	pytest.param(arrayRangeValue, id='arrayRangeValue'),
	pytest.param(arrayRepeat, id='arrayRepeat'),
	pytest.param(arrayRepeatRange, id='arrayRepeatRange'),
	pytest.param(arrayRepeatRangeValue, id='arrayRepeatRangeValue'),
	pytest.param(arrayRepeatRepeatValue, id='arrayRepeatRepeatValue'),
	pytest.param(arrayRunsFibonacci, id='arrayRunsFibonacci'),
	pytest.param(arrayScalarFibonacci, id='arrayScalarFibonacci'),
	pytest.param(arrayValueRange, id='arrayValueRange'),
	pytest.param(arrayValueRangeRepeat, id='arrayValueRangeRepeat'),
	pytest.param(arrayValueRangeRunValue, id='arrayValueRangeRunValue'),
	pytest.param(arrayValueRangeValue, id='arrayValueRangeValue'),
	pytest.param(arrayValueRepeat, id='arrayValueRepeat'),
	pytest.param(arrayValueRepeatNegative, id='arrayValueRepeatNegative'),
)
"""Every integer array: the full domain of a contract over integer arrays."""
