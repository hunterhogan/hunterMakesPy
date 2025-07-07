# hunterMakesPy

A modular Python toolkit for defensive programming, parameter validation, file system utilities, and flexible data structure manipulation.

[![pip install hunterMakesPy](https://img.shields.io/badge/pip%20install-hunterMakesPy-gray.svg?colorB=3b434b)](https://pypi.org/project/hunterMakesPy/)

## Overview

hunterMakesPy provides utilities for safe error handling, flexible input validation, dynamic module and attribute importing, and merging or transforming complex data structures. The package emphasizes clear identifiers, robust type handling, and reusable components for building reliable Python applications.

## Installation

```bash
pip install hunterMakesPy
```

## Defensive Programming

Utilities for handling `None` values and defensive programming patterns.

```python
from hunterMakesPy import raiseIfNone

# Ensure a function result is not None
def findConfiguration(configName: str) -> dict[str, str] | None:
    # ... search logic ...
    return None

config = raiseIfNone(
    findConfiguration("database"),
    "Configuration 'database' is required but not found"
)
```

## Parameter Validation

Parameter validation, integer parsing, and concurrency handling.

```python
from hunterMakesPy import defineConcurrencyLimit, intInnit, oopsieKwargsie

# Smart concurrency limit calculation
cpuLimit = defineConcurrencyLimit(limit=0.75)  # Use 75% of available CPUs
cpuLimit = defineConcurrencyLimit(limit=True)  # Use exactly 1 CPU
cpuLimit = defineConcurrencyLimit(limit=4)     # Use exactly 4 CPUs

# Robust integer validation
validatedIntegers = intInnit([1, "2", 3.0, "4"], "port_numbers")

# String-to-boolean conversion for configuration
userInput = "True"
booleanValue = oopsieKwargsie(userInput)  # Returns True
```

## File System Utilities

Safe file operations and dynamic module importing.

```python
from hunterMakesPy import (
    importLogicalPath2Identifier,
    importPathFilename2Identifier,
    makeDirsSafely,
    writeStringToHere
)

# Dynamic imports
gcdFunction = importLogicalPath2Identifier("math", "gcd")
customFunction = importPathFilename2Identifier("path/to/module.py", "functionName")

# Safe file operations
pathFilename = Path("deep/nested/directory/file.txt")
writeStringToHere("content", pathFilename)  # Creates directories automatically
```

## Data Structure Manipulation

Utilities for string extraction, data flattening, and array compression.

```python
from hunterMakesPy import stringItUp, updateExtendPolishDictionaryLists, autoDecodingRLE
import numpy

# Extract all strings from nested data structures
nestedData = {"config": [1, "host", {"port": 8080}], "users": ["alice", "bob"]}
allStrings = stringItUp(nestedData)  # ['config', 'host', 'port', 'users', 'alice', 'bob']

# Merge dictionaries containing lists
dictionaryAlpha = {"servers": ["web1", "web2"], "databases": ["db1"]}
dictionaryBeta = {"servers": ["web3"], "databases": ["db2", "db3"]}
merged = updateExtendPolishDictionaryLists(dictionaryAlpha, dictionaryBeta, destroyDuplicates=True)

# Compress NumPy arrays with run-length encoding
arrayData = numpy.array([1, 2, 3, 4, 5, 5, 5, 6, 7, 8, 9])
compressed = autoDecodingRLE(arrayData)  # "[1,*range(2,6)]+[5]*2+[*range(6,10)]"
```

## Testing

The package includes comprehensive test suites that you can import and run:

```python
from hunterMakesPy.pytestForYourUse import (
    PytestFor_defineConcurrencyLimit,
    PytestFor_intInnit,
    PytestFor_oopsieKwargsie
)

# Run tests on the built-in functions
listOfTests = PytestFor_defineConcurrencyLimit()
for nameOfTest, callablePytest in listOfTests:
    callablePytest()

# Or test your own compatible functions
@pytest.mark.parametrize("nameOfTest,callablePytest",
                        PytestFor_intInnit(callableToTest=myFunction))
def test_myFunction(nameOfTest, callablePytest):
    callablePytest()
```

## My recovery

[![Static Badge](https://img.shields.io/badge/2011_August-Homeless_since-blue?style=flat)](https://HunterThinks.com/support)
[![YouTube Channel Subscribers](https://img.shields.io/youtube/channel/subscribers/UC3Gx7kz61009NbhpRtPP7tw)](https://www.youtube.com/@HunterHogan)

## How to code

Coding One Step at a Time:

0. WRITE CODE.
1. Don't write stupid code that's hard to revise.
2. Write good code.
3. When revising, write better code.

[![CC-BY-NC-4.0](https://github.com/hunterhogan/hunterMakesPy/blob/main/CC-BY-NC-4.0.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
