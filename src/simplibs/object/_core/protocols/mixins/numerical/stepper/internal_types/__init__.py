from .LimitAction import LimitAction
from .StepValue import StepValue

_DESIGN_NOTES = """
# Stepper Internal Types Sub-Package

## Purpose
Provides specialized type definitions for step value inputs and limit event callbacks.

## Internal Components Registry

| Component     | Type      | Description                                                                  |
| :------------ | :-------- | :--------------------------------------------------------------------------- |
| `LimitAction` | TypeAlias | Action or callback invoked when a numerical limit threshold is reached.     |
| `StepValue`   | TypeAlias | Value shift amount supporting explicit numbers or Ellipsis (`...`) default.  |
"""