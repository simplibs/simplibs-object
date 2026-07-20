from .ClassMethodExceptionInfoPayload import ClassMethodExceptionInfoPayload
from .exception_context_for_classmethod import exception_context_for_classmethod
from .exception_info_for_classmethod import exception_info_for_classmethod


_DESIGN_NOTES = """
# Exception Helpers Sub-Package

## Purpose
Provides structural exception payload definitions and contextual reflection extraction helpers tailored for diagnostic reporting inside method signature verifiers.

## Internal Components Registry

| Component                            | Type     | Description                                                                          |
| :----------------------------------- | :------- | :----------------------------------------------------------------------------------- |
| `ClassMethodExceptionInfoPayload`   | TypedDict| Explicit type definition mapping diagnostic metadata output fields.                  |
| `exception_context_for_classmethod` | Function | Low-level extraction utility mapping raw method attributes to basic error context.  |
| `exception_info_for_classmethod`    | Function | High-level diagnostic text and structural blueprint formatter for exception errors. |
"""