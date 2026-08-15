from .create_value_property import create_value_property
from .create_instance_property import create_instance_property
from .create_properties_for_inner import create_properties_for_inner

_DESIGN_NOTES = """
# Property Builders Sub-Package

## Purpose
Provides unified generators for public-facing properties used across atomic and
composite runtime instances. These builders define the external API for reading
and mutating instance values, as well as accessing inner instance objects.

## Internal Components Registry

| Component                   | Type     | Description                                                                 |
| :-------------------------- | :------- | :-------------------------------------------------------------------------- |
| `create_value_property`     | Function | Builds the unified `value` property (getter + optional setter).             |
| `create_instance_property`  | Function | Builds read-only properties exposing inner instance objects.                |
| `create_properties_for_inner` | Function | Generates paired value/instance properties for composite inner elements.    |
"""
