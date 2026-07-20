from .SimpleError import SimpleError


class SimpleMetadataError(SimpleError):
    """Exception for errors in metadata definition and structure of SimpleObject classes."""


_DESIGN_NOTES = """
# SimpleMetadataError

## Purpose
A group exception for errors occurring during class declaration and validation. It inherits from `SimpleError`, allowing it to be caught under the main umbrella exception as well.

## Logic
This exception is typically raised within the metaclass and the metadata orchestrator. It indicates that the user has incorrectly defined their class (e.g., invalid name, type, or inner components).
"""