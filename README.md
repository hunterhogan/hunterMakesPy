# hunterMakesPy

Utilities for converting mixed input to integers, calculating CPU limits, handling None values, importing code dynamically, and manipulating nested data.

[![pip install hunterMakesPy](https://img.shields.io/badge/pip%20install-hunterMakesPy-gray.svg?colorB=3b434b)](https://pypi.org/project/hunterMakesPy/)

```bash
pip install hunterMakesPy
```

## What This Package Does

1. **Convert strings, floats, binary data to validated integers** — Accepts messy input like `["1", 2.0, b"3"]` and returns `[1, 2, 3]` or fails with descriptive errors.

2. **Calculate CPU/concurrency limits from flexible specifications** — Pass `0.75` for 75% of CPUs, `True` for 1 CPU, `4` for exactly 4 CPUs, or `-2` to reserve 2 CPUs.

3. **Eliminate type checker warnings about None** — Convert `Type | None` returns to `Type` by validating at runtime that values are not None.

4. **Import Python code from dot-notation paths or file paths** — Load functions or classes from `"scipy.signal.windows"` or `"path/to/file.py"` without manual module loading.

5. **Create nested directories without error handling** — Write to `"deep/nested/path/file.txt"` and parent directories are created automatically, existing directories are silently skipped.

6. **Format and write Python source code automatically** — Removes unused imports, sorts import statements, applies consistent formatting before writing files.

7. **Extract all strings from arbitrarily nested data** — Recursively traverse dictionaries, lists, tuples, sets and collect every string value into a flat list.

8. **Merge multiple dictionaries with list values** — Combine `{"a": [1, 2]}` and `{"a": [3], "b": [4]}` into `{"a": [1, 2, 3], "b": [4]}` with optional deduplication and sorting.

9. **Compress NumPy arrays to compact string representations** — Encode repetitive patterns and sequences using run-length encoding and Python range syntax that evaluates back to the original data.

10. **Replace ambiguous numeric literals with semantic names** — Use `decreasing` instead of `-1`, `inclusive` for boundary adjustments, `zeroIndexed` for index conversions, making intent explicit.

## Examples

```python
import hunterMakesPy as humpy

# Integer validation from mixed sources
ports = humpy.intInnit(["8080", 443, "22"], "server_ports")

# Flexible CPU limit calculation
workers = humpy.defineConcurrencyLimit(limit=0.75)  # 6 CPUs on 8-core machine

# None-checking without type errors
config = humpy.raiseIfNone(getConfig(), "Missing configuration")

# Dynamic imports
windowFunc = humpy.importLogicalPath2Identifier("scipy.signal.windows", "hann")

# Safe file writing
humpy.writeStringToHere("content", "nested/dirs/file.txt")  # Creates dirs

# String extraction from nested data
strings = humpy.stringItUp({"users": ["alice"], "config": {"host": "localhost"}})
# Returns: ["users", "alice", "config", "host", "localhost"]

# Dictionary merging
merged = humpy.updateExtendPolishDictionaryLists(
    {"servers": ["chicago"]},
    {"servers": ["tokyo", "chicago"]},
    destroyDuplicates=True
)
# Returns: {"servers": ["chicago", "tokyo"]}
```

## Testing Your Own Code

Import test suites to validate custom functions that match the expected signatures:

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
