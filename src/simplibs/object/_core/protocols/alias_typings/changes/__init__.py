from .ChangesDict import ChangesDict
from .ChangesTuple import ChangesTuple
from .ChangeTuple import ChangeTuple

_DESIGN_NOTES = """
# Changes Alias Typings Sub-Package

## Purpose
Provides type definitions for batch updates and individual change representations.

## Internal Components Registry

| Component      | Type      | Description                                                                  |
| :------------- | :-------- | :--------------------------------------------------------------------------- |
| `ChangesDict`  | TypeAlias | Key-value dictionary mapping element names to their new target values.       |
| `ChangesTuple` | TypeAlias | Tuple containing one or multiple change pairs for batch processing.          |
| `ChangeTuple`  | TypeAlias | Pair structure `(element_name, new_value)` representing a single update.    |
"""