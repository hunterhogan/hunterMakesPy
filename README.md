# hunterMakesPy

Utilities for converting mixed input to integers, calculating CPU limits, handling None values, importing code dynamically, and manipulating nested data. Also includes `humpy_toolz`, `humpy_cytoolz`, and `humpy_tlz`: typed forks of `toolz` and `cytoolz` with curried namespaces and a sandbox.

[![pip install hunterMakesPy](https://img.shields.io/badge/pip%20install-hunterMakesPy-gray.svg?colorB=3b434b)](https://pypi.org/project/hunterMakesPy/)

## Validate, Convert, and Parse Inputs

### Convert Mixed Input to Validated Integers

Accepts strings, floats, complex numbers, and binary data and returns a list of validated integers. Ambiguous or incompatible values produce descriptive errors.

```python
from hunterMakesPy.parseParameters import intInnit

ports = intInnit(["8080", 443, "22"], "server_ports")
# Returns: [8080, 443, 22]
```

### Calculate Concurrency Limits from Flexible Specifications

Pass `0.75` for 75% of CPUs, `True` for 1 CPU, `4` for exactly 4 CPUs, or `-2` to reserve 2 CPUs.

```python
from hunterMakesPy.parseParameters import defineConcurrencyLimit

workers = defineConcurrencyLimit(limit=0.75)  # 6 on an 8-core machine
```

### Interpret Strings as Boolean or None

Parse string values such as `"true"`, `"false"`, or `"none"` into their Python equivalents without raising exceptions on mismatch.

```python
from hunterMakesPy.parseParameters import oopsieKwargsie

oopsieKwargsie("True")   # Returns: True
oopsieKwargsie("none")   # Returns: None
oopsieKwargsie("hello")  # Returns: "hello"
```

## Eliminate None with Runtime Validation

Convert `Type | None` return annotations to `Type` by raising at runtime if the value is `None`. Removes `None`-checking noise from downstream code and satisfies type checkers.

```python
from hunterMakesPy import raiseIfNone

config = raiseIfNone(getConfig(), "Missing configuration")
```

## Replace Ambiguous Numeric Literals with Semantic Names

Use `decreasing` instead of `-1`, `inclusive` for boundary adjustments, and `zeroIndexed` for index conversions. Intent becomes explicit and the code reads as prose.

```python
from hunterMakesPy import decreasing, inclusive, zeroIndexed

rangeEnd = lengthSequence + inclusive
indexLast = lengthSequence - zeroIndexed
step = decreasing
```

## Import Modules by Dot-Notation Path or File Path

Load functions or classes from `"scipy.signal.windows"` or `"path/to/file.py"` without manual module-loading boilerplate.

```python
from hunterMakesPy.filesystemToolkit import importLogicalPath2Identifier

windowFunction = importLogicalPath2Identifier("scipy.signal.windows", "hann")
```

## Create Directories Safely and Write Files with Formatting

Write to `"deep/nested/path/file.txt"` and parent directories are created automatically. `writePython` removes unused imports and sorts import statements before writing.

```python
from hunterMakesPy.filesystemToolkit import writeStringToHere, writePython

writeStringToHere("content", "nested/dirs/file.txt")  # Creates dirs
writePython(sourceCode, "output/module.py")            # Formats, then writes
```

## Extract Strings from Arbitrarily Nested Data

Recursively traverse dictionaries, lists, tuples, and sets and collect every string value into a flat list.

```python
from hunterMakesPy.dataStructures import stringItUp

strings = stringItUp({"users": ["alice"], "config": {"host": "localhost"}})
# Returns: ["users", "alice", "config", "host", "localhost"]
```

## Merge Dictionaries with List Values

Combine `{"a": [1, 2]}` and `{"a": [3], "b": [4]}` into `{"a": [1, 2, 3], "b": [4]}` with optional deduplication and sorting.

```python
from hunterMakesPy.dataStructures import updateExtendPolishDictionaryLists

merged = updateExtendPolishDictionaryLists(
    {"servers": ["chicago"]},
    {"servers": ["tokyo", "chicago"]},
    destroyDuplicates=True,
)
# Returns: {"servers": ["chicago", "tokyo"]}
```

## Compress NumPy Arrays to Self-Decoding Strings

Encode repetitive patterns and consecutive sequences using run-length encoding and Python `range` syntax. The resulting string evaluates back to the original data.

```python
from hunterMakesPy.dataStructures import autoDecodingRLE

encoded = autoDecodingRLE(arrayTarget)
```

## Configure Package Metadata at Runtime

`PackageSettings` reads `pyproject.toml` automatically to resolve the package name and installation path.

```python
from hunterMakesPy import PackageSettings

settings = PackageSettings(identifierPackageFALLBACK="myPackage")
```

## Reuse Test Suites for Custom Implementations

Import parameterized test generators to validate custom functions that match the expected signatures.

```python
from hunterMakesPy.tests.test_parseParameters import PytestFor_intInnit

@pytest.mark.parametrize("test_name,test_func", PytestFor_intInnit(myFunction))
def test_my_integer_validator(test_name, test_func):
    test_func()
```

---

## `humpy_toolz`: Typed Pure-Python Functional Utilities

`humpy_toolz` is a typed fork of [`toolz`](https://github.com/pytoolz/toolz). It provides composable functions for iterators, dictionaries, and function composition with full type stubs and docstrings.

### Dictionary Transformations without Mutation

Create new mappings by associating, dissociating, filtering, and mapping over keys or values. Nested access is supported through key-path sequences.

```python
from humpy_toolz import merge, valmap, keyfilter, assoc

merged = merge({"a": 1}, {"b": 2})             # {"a": 1, "b": 2}
doubled = valmap(lambda x: x * 2, {"a": 1})    # {"a": 2}
evens = keyfilter(lambda k: k > 1, {1: "a", 2: "b"})  # {2: "b"}
updated = assoc({"x": 10}, "y", 20)            # {"x": 10, "y": 20}
```

### Compose, Curry, and Thread Functions

Build transformation sequences from left or right, partially apply arguments with `curry`, and thread a value through a series of functions.

```python
from humpy_toolz import compose_left, curry, pipe

increment = lambda x: x + 1
double = lambda x: x * 2
transform = compose_left(increment, double)
transform(3)  # 8

pipe(3, increment, double)  # 8
```

### Slice, Group, and Deduplicate Iterators

Lazy operations over iterables: `take`, `drop`, `partition`, `sliding_window`, `unique`, `interleave`, `groupby`, `frequencies`, and more.

```python
from humpy_toolz import take, frequencies, groupby, unique

list(take(3, range(100)))              # [0, 1, 2]
frequencies(["a", "b", "a", "c"])      # {"a": 2, "b": 1, "c": 1}
groupby(len, ["cat", "mouse", "dog"])  # {3: ["cat", "dog"], 5: ["mouse"]}
list(unique([1, 2, 1, 3]))            # [1, 2, 3]
```

### Curried Namespace for Partial Application

Every function in `humpy_toolz.curried` accepts partial arguments and returns a new callable waiting for the rest.

```python
from humpy_toolz.curried import map, filter, get

list(map(str.upper, ["hello", "world"]))  # ["HELLO", "WORLD"]
list(filter(lambda x: x > 2, [1, 2, 3, 4]))  # [3, 4]
list(map(get(0), [(1, 2), (3, 4)]))       # [1, 3]
```

### Sandbox: Parallel Fold and Equality-Based Hashing

`humpy_toolz.sandbox` provides `fold` for unordered parallel reductions and `EqualityHashKey` for hashing otherwise-unhashable types.

```python
from humpy_toolz.sandbox import fold, EqualityHashKey
from operator import add

fold(add, range(100), default=0)  # 4950
```

---

## `humpy_cytoolz`: Cython-Accelerated Functional Utilities

`humpy_cytoolz` is a typed fork of [`cytoolz`](https://github.com/pytoolz/cytoolz). It exposes the same API as `humpy_toolz` but the core modules (`dicttoolz`, `functoolz`, `itertoolz`, `recipes`, `utils`) are compiled as Cython extension modules for lower overhead on hot paths.

```python
from humpy_cytoolz import groupby, curry, merge
```

Install with the `cython` build dependency to compile the extensions. If compilation is unavailable, use `humpy_toolz` directly.

---

## `humpy_tlz`: Automatic Cython-or-Pure Dispatch

`humpy_tlz` mirrors the `humpy_toolz` API and imports from `humpy_cytoolz` when available, falling back to `humpy_toolz` otherwise. Use `humpy_tlz` in library code so callers benefit from Cython acceleration without requiring it.

```python
from humpy_tlz import pipe, curry, groupby
```

---

## My recovery

[![Static Badge](https://img.shields.io/badge/2011_August-Homeless_since-blue?style=flat)](https://HunterThinks.com/support)
[![YouTube Channel Subscribers](https://img.shields.io/youtube/channel/subscribers/UC3Gx7kz61009NbhpRtPP7tw)](https://www.youtube.com/@HunterHogan)

[![CC-BY-NC-4.0](https://raw.githubusercontent.com/hunterhogan/hunterMakesPy/refs/heads/main/.github/CC-BY-NC-4.0.png)](https://creativecommons.org/licenses/by-nc/4.0/)
