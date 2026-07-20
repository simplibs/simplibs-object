from .validate_method_has_exact_args_count import validate_method_has_exact_args_count
from .validate_method_not_use_param_placeholders import validate_method_not_use_param_placeholders
from .validate_method_param_match_expected import validate_method_param_match_expected


_DESIGN_NOTES = """
# Params Validation Sub-Package

## Purpose
Houses rigorous lexical name checking and positional constraint rules evaluating method parameter layouts.

## Internal Components Registry

| Component                                     | Type     | Description                                                                          |
| :-------------------------------------------- | :------- | :----------------------------------------------------------------------------------- |
| `validate_method_has_exact_args_count`        | Function | Ensures the total positional parameter capacity matches the internal schema exactly. |
| `validate_method_not_use_param_placeholders`  | Function | Rejects catch-all structural argument configurations like `*args` or `**kwargs`.      |
| `validate_method_param_match_expected`        | Function | Enforces naming alignment between signature elements and structural metadata specs. |
"""