# Collections
from .collections import (
    CollectionBaseProtocol,
    CollectionProtocol,
    IterableProtocol,
    MappingProtocol,
)
# Comparison
from .comparison import (
    EqualityProtocol,
    OrderingProtocol,
)
# Generics
from .generics import (
    ClassGetItemProtocol,
)
# Interfaces
from .interfaces import (
    CallProtocol,
    ContextProtocol,
)
# Lifecycles
from .lifecycles import (
    CopyableProtocol,
    LifecycleProtocol,
    PickleReduceProtocol,
    PickleStateProtocol,
)
from .lifecycles.internal_types import (
    PicklePlan,
)
# Numeric
from .numeric import (
    ArithmeticProtocol,
    BitwiseProtocol,
    ConversionProtocol,
    InplaceProtocol,
    UnaryProtocol,
)
from .numeric.internal_types import (
    Operator,
    UnaryOperator,
)
# Representation
from .representation import (
    ValueDisplayProtocol,
    ValueFormattingProtocol,
)

__all__ = [
    # Collections
    "CollectionBaseProtocol",
    "CollectionProtocol",
    "IterableProtocol",
    "MappingProtocol",

    # Comparison
    "EqualityProtocol",
    "OrderingProtocol",

    # Generics
    "ClassGetItemProtocol",

    # Interfaces
    "CallProtocol",
    "ContextProtocol",

    # Lifecycles
    "CopyableProtocol",
    "LifecycleProtocol",
    "PickleReduceProtocol",
    "PickleStateProtocol",
    "PicklePlan",

    # Numeric
    "ArithmeticProtocol",
    "BitwiseProtocol",
    "ConversionProtocol",
    "InplaceProtocol",
    "UnaryProtocol",
    "Operator",
    "UnaryOperator",

    # Representation
    "ValueDisplayProtocol",
    "ValueFormattingProtocol",
]

_DESIGN_NOTES = """
# Dunders Mixin Protocols Main Package

## Purpose
Aggregates all low-level Python magic method (dunder) protocols into a single entry-point package.
Covers collections, comparisons, generic indexing, function invocation/context management, object lifecycles/serialization, numeric operators, and string representations.

## Internal Components Registry

| Component                             | Type      | Category       | Description                                                                  |
| :------------------------------------ | :-------- | :------------- | :--------------------------------------------------------------------------- |
| `CollectionBaseProtocol`              | Protocol  | Collections    | Structural anchor for collection mixins with size and containment support.   |
| `CollectionProtocol`                  | Protocol  | Collections    | Complete container interface combining sizing, containment, and iteration.  |
| `IterableProtocol`                    | Protocol  | Collections    | Interface guaranteeing element iteration capability via `__iter__`.          |
| `MappingProtocol`                     | Protocol  | Collections    | Key-value mapping interface with item retrieval, assignment, and deletion.   |
| `EqualityProtocol`                    | Protocol  | Comparison     | Interface for equality (`__eq__`, `__ne__`) and hashing (`__hash__`).        |
| `OrderingProtocol`                    | Protocol  | Comparison     | Interface for rich comparison operators (`<`, `<=`, `>`, `>=`).               |
| `ClassGetItemProtocol`                | Protocol  | Generics       | Interface guaranteeing class-level generic subscripting via `__class_getitem__`.|
| `CallProtocol`                        | Protocol  | Interfaces     | Interface enabling instance invocation as a function for state updates.      |
| `ContextProtocol`                     | Protocol  | Interfaces     | Interface for context manager protocol (`__enter__` and `__exit__`).         |
| `CopyableProtocol`                    | Protocol  | Lifecycles     | Interface for shallow (`__copy__`) and deep (`__deepcopy__`) copying.        |
| `LifecycleProtocol`                   | Protocol  | Lifecycles     | Master structural aggregator combining copying and pickle protocols.         |
| `PickleReduceProtocol`                | Protocol  | Lifecycles     | Low-level pickle protocol interface via factory reconstruction (`__reduce__`).|
| `PickleStateProtocol`                 | Protocol  | Lifecycles     | State persistence interface using `__getstate__` and `__setstate__`.         |
| `PicklePlan`                          | TypeAlias | Lifecycles     | Tuple structure defining class, empty arguments, and state dictionary for pickle.|
| `ArithmeticProtocol`                  | Protocol  | Numeric        | Standard and right-hand arithmetic operators (`+`, `-`, `*`, `/`, etc.).     |
| `BitwiseProtocol`                     | Protocol  | Numeric        | Bitwise logical operators (`&`, `|`, `^`, `<<`, `>>`, `~`).                 |
| `ConversionProtocol`                  | Protocol  | Numeric        | Native type conversion (`int`, `float`, `complex`) and rounding functions.   |
| `InplaceProtocol`                     | Protocol  | Numeric        | In-place arithmetic assignment operators (`+=`, `-=`, `*=`, etc.).           |
| `UnaryProtocol`                       | Protocol  | Numeric        | Unary mathematical sign and absolute value operators (`-x`, `+x`, `abs(x)`). |
| `Operator`                            | TypeAlias | Numeric        | Binary operator function accepting two arguments and returning a result.    |
| `UnaryOperator`                       | TypeAlias | Numeric        | Unary operator function accepting a single argument and returning a result.  |
| `ValueDisplayProtocol`                | Protocol  | Representation | Interface for string conversion (`__str__`) and developer repr (`__repr__`).  |
| `ValueFormattingProtocol`             | Protocol  | Representation | Interface for f-string formatting, byte conversion, and boolean evaluation.  |
"""