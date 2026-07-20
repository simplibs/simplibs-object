from typing import Any, TYPE_CHECKING
from types import UnionType
from simplibs.sentinels import UNSET
# Inners
from .validations import (
    validate_default_matches_annotation,
    validate_default_is_defined,
)
# Annotations
if TYPE_CHECKING:
    from ......protocols.classes import SimpleClassLike


def process_default_for_constant(
    default_type: type | UnionType,
    owner_class: "SimpleClassLike",
) -> Any:
    """
    Validates and extracts the mandatory default value definition for a constant leaf structure.

    Ensures that the default value is explicitly provided and strictly conforms to the compiled
    type restrictions previously established by the type processor.
    """

    # 1. Fetch the raw default attribute value from the class blueprint
    raw_default = getattr(owner_class, "_default", UNSET)

    # 2. Trigger validation pipeline if the value is missing or breaks type bounds
    if (raw_default is UNSET or
        not isinstance(raw_default, default_type)):
        validate_default_is_defined(raw_default, owner_class)
        validate_default_matches_annotation(raw_default, default_type, owner_class)

    # 3. Return the fully validated constant default value payload
    return raw_default


_DESIGN_NOTES = """
# process_default_for_constant

## Purpose
Acts as the dedicated initialization processor for the `_default` attribute within the `SimpleConstantMetadata` engine. It guarantees that terminal leaf elements contain a non-ambiguous, fully predictable fallback payload that completely aligns with their type definitions.

## Scope & Separation of Concerns
This processor is exclusively designated for **Constant Leaf Objects**. It is completely omitted from the `SimpleObjectMetadata` composition pipeline. 
- In compound objects (`SimpleObject`), an explicit default is structurally illegal because their state is calculated dynamically via `_logic`.
- Constant nodes require an explicit baseline state; hence, this function enforces a strict presence-and-type validation layer.

## Short-Circuit Execution Vector
The conditional check is optimized for maximum execution efficiency:
```python
if (raw_default is UNSET or not isinstance(raw_default, default_type)):

```

* **Happy Path Efficiency**: If the developer provided a valid, type-compliant default value, the condition evaluates to `False` instantly. The runtime short-circuits past the entire error factory block, incurring no extra allocation overhead.
* **Fail-Safe Orchestration**: If the condition matches, the control flow delegates analysis down to the validation sub-package. `validate_default_is_defined` intercepts absolute absence (`UNSET`) first, while `validate_default_matches_annotation` handles type-hint violations.

## Upstream Dependencies

This processor relies directly on the output of `process_type`. The `default_type` parameter must be fully flattened and compiled into an atomic `type` or native `UnionType` beforehand, ensuring that Python's native `isinstance()` check can execute reliably without throwing internal parsing errors.
"""