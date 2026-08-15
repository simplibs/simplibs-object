from .create_composite_init import create_composite_init
from .create_properties_for_inners import create_properties_for_inners
from .create_recalculate_inners import create_recalculate_inners
from .create_recalculate_self import create_recalculate_self

_DESIGN_NOTES = """
# Composite Class Builders Helpers Sub-Package

## Purpose
Aggregates dynamic low-level building blocks and calculation hooks required to assemble multi-property reactive composite structures.

## Internal Components Registry

| Component                      | Type     | Description                                                                          |
| :----------------------------- | :------- | :----------------------------------------------------------------------------------- |
| `create_composite_init`        | Function | Compiles the comprehensive tree-aware initialization method closure for containers.  |
| `create_properties_for_inners` | Function | Synthesizes field descriptor mappings allowing safe direct child access.             |
| `create_recalculate_inners`    | Function | Injects downward reactive propagation hooks updating dependent child states.        |
| `create_recalculate_self`      | Function | Injects upward reactive transformation hooks re-evaluating the parent container state.|
"""