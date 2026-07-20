from .SimpleError import SimpleError


class SimpleMixinError(SimpleError):
    """Exception for invalid mixin definition."""


_DESIGN_NOTES = """
# SimpleMixinError

## Purpose
An exception designed for errors occurring within mixin logics that extend the final instance. It inherits from `SimpleError`, allowing it to be caught under the main library umbrella exception.

## Logic
This exception is typically raised during the evaluation and attachment of mixins to the generated class instance. It detects issues such as slot conflicts, incompatible mixin combinations, or unsupported value types.
"""