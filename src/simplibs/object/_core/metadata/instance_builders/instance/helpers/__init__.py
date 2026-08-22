from .create_instance_class import create_instance_class
from .get_base_class import get_base_class


_DESIGN_NOTES = """
# Instance Helpers Sub-Package

## Purpose
Provides core sub-orchestrators and internal transformation tools used by `create_instance`.
Handles structural base class selection, mixin flattening/validation, dynamic namespace 
assembly (`class_dict`), slot layout checks, and metaprogramming class extension hooks.

## Internal Components Registry

| Component                     | Type     | Description                                                                 |
| :---------------------------- | :------- | :-------------------------------------------------------------------------- |
| `create_instance_class`       | Function | Synthesizes namespace, mixins, and base class into a dynamic type().        |
| `get_base_class`              | Function | Resolves structural base class (atom/composite × mutability).               |
| `_build_combined_init_mixins` | Function | Chains multiple `init_mixins` closures into a single sequential initializer.|
| `_build_instance_class_dict`  | Function | Aggregates mixin slots, methods, and attributes into target `class_dict`.   |
| `_extend_instance_class`      | Function | Executes static `__extend_instance_class__` metaprogramming hooks in-place. |
| `_resolve_flat_mixins`        | Function | Flattens, deduplicates, and validates the MRO mixin hierarchy tree.         |
| `_verify_mixin_compatibility` | Function | Validates mixin identity and checks context compatibility flags.            |

"""