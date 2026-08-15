from .raise_attribut_allready_set import raise_attribut_allready_set
from .raise_metadata_is_immutable import raise_metadata_is_immutable


_DESIGN_NOTES = """
# Metadata Validations Sub-Package

## Purpose
Provides structured error generators used during metadata assignment. Ensures
that blueprint and metadata fields follow strict write-once semantics.

## Internal Components Registry

| Component                       | Type     | Description                                               |
| :------------------------------ | :------- | :-------------------------------------------------------- |
| `raise_attribut_allready_set`   | Function | Raised when class-level blueprint attributes are overwritten. |
| `raise_metadata_is_immutable`   | Function | Raised when metadata fields are reassigned after initialization. |
"""
