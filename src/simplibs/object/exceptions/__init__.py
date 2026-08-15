from .base_exception import SimpleObjectError
from .SimpleInitializationError import SimpleInitializationError
from .SimpleDefinitionError import SimpleDefinitionError
from .SimpleLogicError import SimpleLogicError

__all__ = [
    "SimpleObjectError",
    "SimpleDefinitionError",
    "SimpleInitializationError",
    "SimpleLogicError",
]

_DESIGN_NOTES = """
# Simple Exceptions Sub-Package

## Purpose
Provides the complete set of public exception types used across the SimpleObject
library. These exceptions form a clear, symmetric 4-stage hierarchy built on top of
`SimpleObjectError`, allowing developers to precisely distinguish between errors occurring
during code definition, object instantiation, runtime execution, or test generation.

All exceptions exported by this package are part of the public API and may be safely
imported and caught by library users.

## Public Exception Registry

| Exception                   | Stage / Consumer                   | Description                                                                 |
| :-------------------------- | :--------------------------------- | :-------------------------------------------------------------------------- |
| `SimpleObjectError`         | Umbrella Base                      | Root exception for all Simple-related errors. Catch-all for the library.    |
| `SimpleDefinitionError`     | Definition-Time (Metadata)         | Raised when declarative class metadata or structural blueprints are invalid.|
| `SimpleInitializationError` | Instantiation-Time (Init/Mixins)   | Raised when instance setup, `__init__` arguments, or mixins fail.           |
| `SimpleLogicError`          | Execution-Time (User Data/State)   | Raised when runtime values fail validation, normalization, or state rules.  |

## Usage
Developers may catch all Simple-related errors using the umbrella exception:

```python
from simplibs.object.exceptions import SimpleObjectError

try:
    ...
except SimpleObjectError:
    # Handles any error originating from the SimpleObject library
    ...
```

Or target specific operational phases:

```python
from simplibs.object.exceptions import SimpleLogicError, SimpleDefinitionError

try:
    user_instance.value = raw_input
except SimpleLogicError:
    # Handles invalid runtime data or validation failures
    ...
except SimpleDefinitionError:
    # Handles invalid class blueprints (definition time)
    ...
```

"""
