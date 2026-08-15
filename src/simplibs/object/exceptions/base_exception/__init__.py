from .SimpleObjectError import SimpleObjectError


_DESIGN_NOTES = """
# Base Exception Sub-Package

## Purpose
Contains the core root exception `SimpleObjectError` for the entire SimpleObject ecosystem.
Isolating the root exception in its own sub-package prevents circular import issues
when other exception modules or internal library components inherit from it.

## Exports
- `SimpleObjectError`: The common ancestor for all library-specific exceptions.

| Exception              | Stage / Consumer                   | Description                                                                 |
| :--------------------- | :--------------------------------- | :-------------------------------------------------------------------------- |
| `SimpleObjectError`    | Umbrella Base                      | Root exception for all Simple-related errors. Catch-all for the library.    |

"""