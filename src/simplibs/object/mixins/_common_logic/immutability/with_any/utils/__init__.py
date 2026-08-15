from .get_top_composite_paths import get_top_composite_paths
from .process_single_change import process_single_change
from .split_changes import split_changes
from .split_constants_paths import split_constants_paths

_DESIGN_NOTES = """
# Helpers for with_any Pipeline

## Purpose
Provides structural and routing utilities used by the mixed update pipeline
(`with_any`). These helpers classify updates, determine composite hierarchy,
and validate structural correctness.

## Internal Components Registry

| Component                 | Type     | Description                                         |
| :------------------------ | :------- | :-------------------------------------------------- |
| `get_top_composite_paths` | Function | Determines root vs child composite paths.           |
| `process_single_change`   | Function | Routes single update to correct pipeline.           |
| `split_changes`           | Function | Splits updates into constants and composites.       |
| `split_constants_paths`   | Function | Splits constants into contained vs unique groups.   |
"""
