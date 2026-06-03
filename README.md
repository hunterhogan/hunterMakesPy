# hunterMakesPy

Utilities for converting mixed input to integers, calculating CPU limits, handling None values, importing code dynamically, and manipulating nested data.

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
writePython(sourceCode, "output/module.py")           # Formats, then writes
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

## My recovery

[![Static Badge](https://img.shields.io/badge/2011_August-Homeless_since-blue?style=flat)](https://HunterThinks.com/support)
[![YouTube Channel Subscribers](https://img.shields.io/youtube/channel/subscribers/UC3Gx7kz61009NbhpRtPP7tw)](https://www.youtube.com/@HunterHogan)

[![CC-BY-NC-4.0](https://raw.githubusercontent.com/hunterhogan/hunterMakesPy/refs/heads/main/.github/CC-BY-NC-4.0.png)](https://creativecommons.org/licenses/by-nc/4.0/)
