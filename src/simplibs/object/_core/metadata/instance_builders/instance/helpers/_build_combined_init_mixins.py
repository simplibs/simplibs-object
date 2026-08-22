def _build_combined_init_mixins(
    init_mixins_hooks: list
):
    """Creates a unified function that sequentially invokes all collected mixin initialization closures."""

    # 1. Define combined mixin initialization closure
    def combined_init_mixins(self):

        # 1.1 Traverse through collected initialization hooks
        for init_mixin in init_mixins_hooks:

            # 1.2 Execute initialization logic from hook
            init_mixin(self)

    # 2. Return preconfigured composite initialization function
    return combined_init_mixins


_DESIGN_NOTES = """
# _build_combined_init_mixins

## Purpose
Synthesizes multiple `init_mixins` methods collected from independent mixins into a single, 
chained closure `combined_init_mixins`.

## Pipeline & Logic
1. **Closure Binding**
   Captures `init_hooks` inside a lightweight function closure.

2. **Sequential Execution**
   When invoked on an instance (`self`), `combined_init_mixins` iterates linearly through 
   all collected initialization hooks and executes them in sequence.

## Architectural Notes
- **Eliminating `super()` Chains**: Because mixins are flattened and injected directly into 
  `class_dict` rather than added to MRO, standard `super().init_mixins()` calls are avoided. 
  This explicit chain provides deterministic execution order without MRO traversal overhead.
- **Decoupled Function Factory**: Keeping this factory in a dedicated helper maintains 
  `_build_instance_class_dict` as a pure dict builder without inline closure pollution.
"""